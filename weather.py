import requests
import json
from datetime import datetime, timedelta, date
import csv
from sys import argv
from os.path import exists
from pathlib import Path


url = "https://weather2020-weather-v1.p.rapidapi.com/zip/e8ecee8ff60c478f8a36280fea0524fe/02482"

headers = {
    "x-rapidapi-key": argv[1],
    "x-rapidapi-host": "weather2020-weather-v1.p.rapidapi.com",
}

response = requests.get(url, headers=headers).text
a = json.loads(response)
today = date.today().strftime("%Y-%m-%d")


class WeatherCachedFile:
    def __init__(self, filepath="out.txt"):
        self.path = filepath
        if not exists(self.path):
            Path(self.path).touch()

    def checkInputData(self):
        if len(argv) == 3:
            return datetime.strptime(argv[2], "%Y-%m-%d")
        else:
            return datetime.strptime(today, "%Y-%m-%d")

    def getWeatherData(self):
        with open(
            self.path, "w", newline="", encoding="utf-8"
        ) as new_data_file:
            csv_writer = csv.writer(new_data_file)

            for data in a:
                weekDay = 0
                while weekDay < 7:
                    timestampStart = datetime.fromtimestamp(
                        data["startDate"]
                    ) + timedelta(days=weekDay)
                    csv_writer.writerow(
                        [
                            timestampStart.strftime("%Y-%m-%d"),
                            data["conditions"][0]["tag"],
                        ]
                    )
                    weekDay += 1

    def checkWeatherData(self):
        with open(self.path, "r") as data_file:
            savedData = []
            weatherDates = csv.reader(data_file)
            for line in weatherDates:
                savedData.append(line)
            if savedData:
                if datetime.strptime(today, "%Y-%m-%d") > datetime.strptime(
                    savedData[0][0], "%Y-%m-%d"
                ):
                    self.getWeatherData()
            else:
                self.getWeatherData()


class WeatherForecast:
    def __init__(self, APIkey, filepath="out.txt"):
        self.APIkey = APIkey
        self.path = filepath
        self.fp = open(filepath)
        self.csv_fp = csv.reader(self.fp)
        self.cache = {line[0]: line[1] for line in self.csv_fp}

    def __del__(self):
        self.fp.close()

    def __getitem__(self, key):
        if key not in self.cache:
            return "Nie wiem"
        elif "rain" in self.cache[key]:
            return "Będzie padać"
        else:
            return "Nie będzie padać"

    def items(self):
        temp = self.cache.items()
        for element in temp:
            yield (element)

    def __iter__(self):
        return iter(self.cache)


# Check if saved data is correct and update
weatherFilePath = WeatherCachedFile("out.txt")
weatherFilePath.checkWeatherData()
inputDate = weatherFilePath.checkInputData()
# Get forecast
wf = WeatherForecast(argv[1])

# print(wf["2020-12-25"])
# for element in wf.items():
#     print(element)

# for element in wf:
#     print(element)
