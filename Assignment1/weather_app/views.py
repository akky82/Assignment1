from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from datetime import datetime
from .forms import FeedbackForm, WeatherForm
import os
import json
import requests
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

api_key = "6a0c0dd6f5fe299a55e79d388afb256f"
lat, lon = "", ""
url = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s" \
      "&exclude=current,minute,hourly,alerts&units=metric&appid=%s" % (lat, lon, api_key)


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def future(request):
    return render(request, 'future.html')


class FeedbackView(View):
    def get(self, request):
        file_path = 'weather_app/feedback.json'

        # Check if the feedback file is not empty, then print the comments
        if os.path.getsize(file_path) > 0:
            with open(file_path, 'r') as f:
                feedback = json.load(f)
                for x in feedback['feedback']:
                    print(x)
                    print(feedback['feedback'][0]['firstName'] + " "
                          + feedback['feedback'][0]['lastName'][0] + " - "
                          + feedback['feedback'][0]['time'])
                    print(feedback['feedback'][0]['feedback'])
            print(feedback)
        form = FeedbackForm()
        return render(request, 'feedback.html', {'form': form})

    def post(self, request):
        file_path = 'weather_app/feedback.json'
        # Get the form data and format to json then dict
        data = json.dumps(request.POST, indent=4)
        json_data = json.loads(data)
        # Get current time/date and append to the dict
        curr_time = datetime.now()
        format_time = {'time': curr_time.strftime("%d/%m/%Y %H:%M:%S")}
        json_data.update(format_time)

        # Write the json to the comments file
        with open(file_path, 'r+') as f:
            # if the file is empty for some reason, add the
            if os.path.getsize(file_path) == 0:
                json_init = "{\"feedback\": []}"
                file_data = json.loads(json_init)
            else:
                # read the file and append the new feedback, format to json and write to file
                file_data = json.load(f)

            file_data["feedback"].append(json_data)
            new_data = json.dumps(file_data, indent=4)
            f.seek(0)
            f.write(new_data)

            ''' I realise after writing this that I could've just have the json file start
            with [] to have the whole file as an array, and not had the feedback element 
            with an array in it at all, however left is this way for reference and practice'''

        form = FeedbackForm()
        return render(request, 'feedback.html', {'form': form})


class WeatherView(View):
    def get(self, request):
        form = WeatherForm();
        return render(request, 'weather.html', {'form': form})

    def post(self, request):
        form = WeatherForm()
        return render(request, 'weather.html', {'form': form})
