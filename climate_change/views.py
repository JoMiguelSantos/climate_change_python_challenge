from django.http import HttpResponse, JsonResponse, Http404
from .models import City
from django.views import View
from django.db.models import Max, Value
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

import json


@method_decorator(csrf_exempt, name="dispatch")
class CityView(View):
    def get(self, request):
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")
        highest_average_temperature = (
            City.objects.filter(date__range=[start_date, end_date])
            .annotate(common=Value(1))
            .values("common")
            .annotate(highest_average_temperature=Max("average_temperature"))
            .values("highest_average_temperature")[0]["highest_average_temperature"]
        )
        highest_average_temperature_cities = serializers.serialize(
            "json",
            City.objects.filter(
                date__range=[start_date, end_date],
                average_temperature=highest_average_temperature,
            ),
        )
        return JsonResponse(
            {"highest_average_temperature_cities": highest_average_temperature_cities},
            status=200,
        )

    def post(self, request):
        parsed_body = json.loads(request.body)
        date = parsed_body["date"]
        average_temperature = parsed_body["average_temperature"]
        average_temperature_uncertainty = parsed_body["average_temperature_uncertainty"]
        city = parsed_body["city"]
        country = parsed_body["country"]
        latitude = parsed_body["latitude"]
        longitude = parsed_body["longitude"]
        _, created = City.objects.get_or_create(
            date=date,
            city=city,
            country=country,
            defaults={
                "average_temperature": average_temperature,
                "average_temperature_uncertainty": average_temperature_uncertainty,
                "latitude": latitude,
                "longitude": longitude,
            },
        )
        return HttpResponse(status=201) if created else HttpResponse(status=409)

    def put(self, request):
        parsed_body = json.loads(request.body)
        date = parsed_body["date"]
        average_temperature = parsed_body.get("average_temperature")
        average_temperature_uncertainty = parsed_body.get(
            "average_temperature_uncertainty"
        )
        city = parsed_body["city"]
        updated_fields = {
            field_update[0]: field_update[1]
            for field_update in [
                ("average_temperature", average_temperature),
                ("average_temperature_uncertainty", average_temperature_uncertainty),
            ]
            if field_update[1] is not None
        }
        try:
            City.objects.filter(date=date, city=city).update(**updated_fields)
        except City.DoesNotExist:
            return Http404
        return HttpResponse(status=204)
