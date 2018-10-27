
Meteo service
=================
[![Coverage Status](https://coveralls.io/repos/github/Ranc58/meteo_service/badge.svg?branch=develop)](https://coveralls.io/github/Ranc58/meteo_service?branch=develop)
[![Build Status](https://travis-ci.org/Ranc58/meteo_service.svg?branch=master)](https://travis-ci.org/Ranc58/meteo_service)


Meteo API. Based on DRF. Written for fun.

# How to install

1) With docker:
    - If it need - setup postgres in `env/.env` file. By default, this file is configured for use with Docker.
    - `docker-compose up --build`.
    - For create forecasts from 1 november 2016 `docker-compose exec app python3 manage.py make_forecasts`.  Run with flag `--week` for crate forecasts until next 7 days.
    - For run tests `docker-compose exec app python3 manage.py test`. \
    Postgres data will be saved in `postgres/pgdata`
    
2) Without docker:
    - Recomended use venv or virtualenv for better isolation.\
      Venv setup example: \
      `python3 -m venv myenv`\
      `source myenv/bin/activate`
    - `cp env/.env src/;  cd src/`.
    - Setup postgres in `.env` file.
    - `pip3 install -r requirements.txt`
    - Run django `./run_server.sh`.
    - For run tests (from `src`) `python3 manage.py test`.
    - For create forecasts from 1 november 2016 (from `src`) `python3 manage.py make_forecasts`. Run with flag `--week` for crate forecasts until next 7 days.
    
# How to use
Full SWAGGER doc you can find here: `http://127.0.0.1:8000/a/v1/doc` 

1) Make `GET` request to `http://127.0.0.1:8000/a/v1/temperature/forecasts/<DATA>`. 
    You can use additional query params:
    
    - `type`: Temperature type. May have values `c`(celsius), `f`(fahrenheit), `k`(kelvin). By default used celsius.
    - `days`: Forecast days count. Should be int values. By default - 3 days.  
    - `hour`: For getting by current hour.
    
    Example request: `http://127.0.0.1:8000/a/v1/temperature/forecasts/2018-10-26` will return
    
    ```
        {
          "type": "c",
          "forecasts": [
            {
              "forecast_temperature": 7,
              "forecast_datetime": "2018-10-26 00:00"
            },
            {
              "forecast_temperature": -5,
              "forecast_datetime": "2018-10-26 01:00"
            },
            {
              "forecast_temperature": 11,
              "forecast_datetime": "2018-10-26 02:00"
            },
            {
              "forecast_temperature": 25,
              "forecast_datetime": "2018-10-26 03:00"
            },
         ..........For every day and every hour until 2018-10-29
    ``` 

2) Make `GET` request to `http://127.0.0.1:8000/a/v1/temperature/<DATE>` for get forecasts for current day. `DATE` format must be `YEAR-m-d`.
    You can use additional query params:
    
    - `type`: Temperature type. May have values `c`(celsius), `f`(fahrenheit), `k`(kelvin). By default used celsius.
    - `hour`: For getting by current hour.
        
    Example request `http://127.0.0.1:8000/a/v1/temperature/2018-10-23?type=k&hour=12` will return:
    
    ```
        {
          "type": "k",
          "temperature_data": [
            {
              "forecast_temperature": -3550.95,
              "forecast_datetime": "2018-10-23 12:00"
            }
          ]
        }
    ``` 
 