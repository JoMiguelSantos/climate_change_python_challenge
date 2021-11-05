from django.contrib import admin
from django.urls import path
from .views import CityView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/city", CityView.as_view()),
]
