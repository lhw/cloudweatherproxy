from aiocloudweather.station import (
    WeatherStation,
    WundergroundRawSensor,
    WeathercloudRawSensor,
)


def test_weather_station_from_wunderground():
    raw_sensor_data = WundergroundRawSensor(
        station_id="12345",
        station_key="12345",
        barometer=29.92,
        temperature=72.5,
        humidity=44,
        dewpoint=49.2,
        rain=0,
        dailyrain=0,
        winddirection=249,
        windspeed=2.0,
        windgustspeed=2.7,
        uv=2,
        solarradiation=289.2,
    )
    weather_station = WeatherStation.from_wunderground(raw_sensor_data)

    assert weather_station.station_id == "12345"
    assert weather_station.station_key == "12345"
    assert round(weather_station.barometer.value, 2) == 1013.21
    assert weather_station.barometer.unit == "hPa"
    assert weather_station.temperature.value == 22.5
    assert weather_station.temperature.unit == "°C"
    assert weather_station.humidity.value == 44
    assert weather_station.humidity.unit == "%"
    assert weather_station.solarradiation.value == 289200.0
    assert weather_station.solarradiation.unit == "lx"
    assert weather_station.winddirection.value == 249


def test_weather_station_from_wunderground_2():
    raw_sensor_data = WundergroundRawSensor(
        station_id="12345",
        station_key="12345",
        barometer=29.92,
        temperature=72.5,
        humidity=44,
        dewpoint=49.2,
        rain=0,
        dailyrain=0,
        winddirection=249,
        windspeed=2.0,
        windgustspeed=2.7,
        uv=2,
        solarradiation_new=9.57,
    )
    weather_station = WeatherStation.from_wunderground(raw_sensor_data)

    assert weather_station.station_id == "12345"
    assert weather_station.station_key == "12345"
    assert weather_station.solarradiation.value == 9.57
    assert weather_station.solarradiation.unit == "W/m²"


def test_weather_station_from_weathercloud():
    raw_sensor_data = WeathercloudRawSensor(
        station_id="12345",
        station_key="12345",
        barometer=10130,
        temperature=160,
        humidity=80,
        dewpoint=129,
        rain=109,
        dailyrain=25,
        winddirection=288,
        windspeed=0,
        windgustspeed=0,
        uv=0,
        solarradiation=470,
    )
    weather_station = WeatherStation.from_weathercloud(raw_sensor_data)

    assert weather_station.station_id == "12345"
    assert weather_station.station_key == "12345"
    assert weather_station.barometer.value == 1013
    assert weather_station.barometer.unit == "hPa"
    assert weather_station.temperature.value == 16
    assert weather_station.temperature.unit == "°C"
    assert weather_station.humidity.value == 80
    assert weather_station.humidity.unit == "%"
    assert weather_station.rain.value == 10.9
    assert weather_station.rain.unit == "mm/h"
    assert weather_station.dailyrain.value == 2.5
    assert weather_station.dailyrain.unit == "mm"
    assert weather_station.winddirection.value == 288
