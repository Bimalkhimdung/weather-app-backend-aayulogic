import os
import time

from datetime import datetime
from django.db.models import Avg

from weather_api.models import Weather, WeatherStats

def feed_data_to_model():
    start_time = time.time()
    # path to the directory
    directory = 'wx_data'
    total_files = os.listdir(directory)
    total_files_length = len(total_files)

    # iterate over files in given directory
    for index, filename in enumerate(total_files):
        f = os.path.join(directory, filename)
        station_id = os.path.splitext(filename)[0]
        print(f"Ingestion for station {station_id} started")
        # checking if it is a file
        if os.path.isfile(f):

            weather_instances = []
            with open (f, 'r') as weather_data:
                weather_datum = weather_data.readlines()
                for data in weather_datum:
                    converted_data_in_list = data.split("\t")
                    # remove unnecessary new lines and whitespaces
                    clean_data = list(map(lambda x: x.strip(), converted_data_in_list))
                    date = str(clean_data[0])
                    maxmimum_temperature = clean_data[1]
                    minimum_temperature = clean_data[2]
                    amount_of_precipitation = clean_data[3]
                    # convert date into datetime format
                    converted_date = datetime.strptime(date, '%Y%m%d').date()
                    if Weather.objects.filter(
                        station_id=station_id, date=converted_date
                    ).exists():
                        # if data already exists, skip
                        continue

                    weather_instances.append(
                        Weather(
                            station_id=station_id,
                            date=converted_date,
                            maximum_temperature=maxmimum_temperature,
                            minimum_temperature=minimum_temperature,
                            amount_of_precipitation=amount_of_precipitation
                        )
                    )
            Weather.objects.bulk_create(weather_instances, ignore_conflicts=True)
            print(f"Ingestion for station {station_id} started.")
            print(f"Completed ingestion {index+1} out of {total_files_length} station.")


    end_time = time.time()
    print(f"Total time taken to feed to model: {end_time-start_time} seconds")


def data_analysis_of_weather():
    start_time = time.time()
    print("Starting data analysis of weather.")
    unique_station_ids = set(Weather.objects.values_list('station_id', flat=True))
    for index, station_id in enumerate(unique_station_ids):
        unique_station_yearly_data = set(Weather.objects.filter(station_id=station_id).values_list('date__year', flat=True))
        weather_stats = []
        for unique_year in unique_station_yearly_data:
            stats = Weather.objects.filter(
                station_id=station_id, date__year=unique_year
            ).exclude(
                maximum_temperature=-9999,
                minimum_temperature=-9999,
                amount_of_precipitation=-9999
            ).aggregate(
                average_maximum_temperature=Avg('maximum_temperature'),
                average_minimum_temperature=Avg('minimum_temperature'),
                average_amount_of_precipitation=Avg('amount_of_precipitation')
            )
            weather_stats.append(
                WeatherStats(
                    station_id=station_id,
                    year=unique_year,
                    average_maximum_temperature=round(stats['average_maximum_temperature'], 2),
                    average_minimum_temperature=round(stats['average_minimum_temperature'], 2),
                    average_amount_of_precipitation=round(stats['average_amount_of_precipitation']/10, 2) # since amount_of_precipitation is in mm
                )
            )

        WeatherStats.objects.bulk_create(weather_stats)
        print(f"Completed data analysis {index+1} out of {len(unique_station_ids)} station.")
        end_time = time.time()
        print(f"Total time taken to feed to model: {end_time-start_time} seconds")


def main():
    feed_data_to_model()
    data_analysis_of_weather()
