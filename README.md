# climate_change_python_challenge

## Introduction

This project establishes a Django REST API which is easily deployable with Docker Compose, including a Postgres database instance.
There's a set of operations possible which you can find further ahead on this file on the API section and some examples further down on the Examples section.

## Instructions

To be able to run this example you'll need the following:

-   Docker and Docker Compose installed in your computer (you can follow the instructions [here](https://docs.docker.com/get-docker/))
-   A [Kaggle account](https://www.kaggle.com/) and a [API Token](https://github.com/Kaggle/kaggle-api#api-credentials)

After you get Docker and have an Kaggle account, download the `kaggle.json` and copy it into the root folder of the project. This will enable us to download the dataset via the Kaggle API.

Once the previous steps are completed, run `docker-compose up --build` on your command line interface (on Windows the best solution would be to use [WSL](https://docs.microsoft.com/en-us/windows/wsl/install) to avoid compatibility issues).

This will deploy a container containing the Database and and Web Server, initialize the Django migrations and attempt to download the dataset and load into the database.
Because the dataset is quite big, this step will take around 10 min to complete the loading so go grab a coffee while you wait.
Once this step is done the server will be turned up and you're ready to make requests.
You can find more detailed steps in the `init.sh` file.

## API

_PATH_

`/api/city`

_GET Request_:
You can query the City for the cities with the highest average temperatures within a time range by passing `city`,`start_date` and `end_date` as query params.

_POST Request_:
You can create a new entry for a city by passing all the parameters in the request body as JSON.

_PUT Request_:
You can update an existing entry's `average_temperature` or/and `average_temperature_uncertainty` for a city by passing these values as well as `city` and `date` as parameters in the request body as JSON.

You can find examples in the `Examples` further down this README.

## Examples

### Find the entry whose city has the highest AverageTemperature since the year 2000.

_Request_:
`curl --location --request GET 'http://localhost:8000/api/city?city=Berlin&start_date=2000-01-01&end_date=2022-01-01'`

_Response_:

```
{
    "highest_average_temperature_cities": "[{\"model\": \"climate_change.city\", \"pk\": 858495, \"fields\": {\"date\": \"2006-07-01\", \"average_temperature\": 23.795, \"average_temperature_uncertainty\": 0.316, \"city\": \"Berlin\", \"country\": \"Germany\", \"latitude\": \"52.24N\", \"longitude\": \"13.14E\"}}]"
}
```

### Following above: assume the temperature observation of the city last month breaks the record. It is 0.1 degree higher with the same uncertainty. Create this entry.

_Request_:

```
curl --location --request POST 'http://localhost:8000/api/city' \
--header 'X-API-KEY: cc5fdc57-c2ed-4a61-8d17-1444950cf87f' \
--header 'Content-Type: application/json' \
--data-raw '{
    "date": "2021-10-01",
    "city": "Berlin",
    "country": "Germany",
    "average_temperature": 23.895,
    "average_temperature_uncertainty": 0.316,
    "latitude": "52.24N",
    "longitude": "13.14E"
}'
```

_Response_:

If created successfully, you'll get the Status Code 204 or else if the entry already exists you'll get the Status Code 403

### Following question 1: assume the returned entry has been found erroneous. The actual average temperature of this entry is 2.5 degrees lower. Update this entry.

_Request_:

```
curl --location --request PUT 'http://localhost:8000/api/city' \
--header 'Content-Type: application/json' \
--data-raw '{
    "city": "Berlin",
    "date": "2006-07-01",
    "average_temperature": 21.295
}'
```

_Response_:

If updated successfully, you'll get the Status Code 204 or else if the entry does not exist you'll get the Status Code 404

## Observations

This exercise took me around 4 hours of continuous work to complete.
Even though the general idea of how to structure of the API was clear and the steps were as expected, my little acquaintance with Django (did most of my Python development with Flask) had me take a bit longer than expected but my goal was also to learn more about Django's inner workings so this was a good exercise for that.
Loading such a big file into a DB also had its own challenges and I had to explore the most efficient/fastest way to loading the data so it wouldn't take forever.
