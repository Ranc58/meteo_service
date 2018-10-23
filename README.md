Meteo service
=================
# How to install

1) With docker:
    - If it need - setup postgres in `env/.env` file. By default, this file is configured for use with Docker.
    - `docker-compose up --build`.
    - For run tests `docker-compose exec app python3 manage.py test`. \
    Postgres data will be saved in `postgres/pgdata`
    
2) Without docker:
    - Recomended use venv or virtualenv for better isolation.\
      Venv setup example: \
      `python3 -m venv myenv`\
      `source myenv/bin/activate`
    - `cp env/.env src/;  cd src/`.
    - Setup postgres and redis in `.env` file.
    - `pip3 install -r requirements.txt`
    - Run django and celery `./run_server.sh`.
    - For run tests (from `src`) `python3 manage.py test`.
    
# How to use
Full SWAGGER doc you can find here: `http://127.0.0.1:8000/a/v1/doc` 

1) Make `GET` request to `http://127.0.0.1:8000/a/v1/forecasts`. It will return something like 
```python
{
  "type": "c",
  "forecasts": [
    {
      "forecast_temperature": 13,
      "forecast_datetime": "2018-23-10 06:06"
    },
    {
      "forecast_temperature": 11,
      "forecast_datetime": "2018-23-10 00:27"
    },
    {
      "forecast_temperature": 15.8,
      "forecast_datetime": "2018-23-10 12:27"
    },
    {
      "forecast_temperature": 12.8,
      "forecast_datetime": "2018-23-10 18:27"
    }
  ]
}
```
You can use additional query params:
    - `type`: Temperature type. May have values `c`(celsius), `f`(fahrenheit), `k`(kelvin). By default used celsius.
    - `days`: Forecast days count. Should be int values. By default - 3 days. 
2) Make `GET` request to `http://127.0.0.1:8000/a/v1/forecasts/<DATE>` for get forecasts for current day. `DATE` format must be `YEAR-m-d`. It will return something like
```python
{
  "type": "c",
  "day_forecasts": [
    {
      "forecast_temperature": -1,
      "forecast_datetime": "2018-10-23 06:06"
    },
    {
      "forecast_temperature": -13,
      "forecast_datetime": "2018-10-23 00:27"
    },
    {
      "forecast_temperature": -15.8,
      "forecast_datetime": "2018-10-23 12:27"
    },
    {
      "forecast_temperature": -8,
      "forecast_datetime": "2018-10-23 18:27"
    }
  ]
}    
``` 
You can use additional query params:
    - `type`: Temperature type. May have values `c`(celsius), `f`(fahrenheit), `k`(kelvin). By default used celsius.
    - `hour`: For getting by current hour.
