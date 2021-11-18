from django.shortcuts import render
from django.views import View
from django.contrib import messages
from .forms import FeedbackForm, WeatherForm
import json
from . import functions
from django.views.decorators.csrf import csrf_exempt


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def future(request):
    return render(request, 'future.html')


def disclaimer(request):
    return render(request, 'disclaimer.html')


def privacy(request):
    return render(request, 'privacy.html')


class FeedbackView(View):
    @csrf_exempt
    def get(self, request):
        feedback = functions.get_feedback()

        form = FeedbackForm()
        # Pass the feedback comments to the template
        return render(request, 'feedback.html', {'form': form, 'feedback': feedback})

    @csrf_exempt
    def post(self, request):
        feedback = ""
        # Get the form data and format to json then dict
        form_data = FeedbackForm(request.POST)
        if form_data.is_valid():
            data = json.dumps(request.POST, indent=4)
            json_data = json.loads(data)

            # Save new feedback and return appended feedback to be rendered
            feedback = functions.save_feedback(json_data)

            messages.success(request, "Thank you for your feedback, a team member"
                                      " will be in contact with you if necessary.")

        form = FeedbackForm()
        # Pass the feedback comments, including the new one, to the template
        return render(request, 'feedback.html', {'form': form, 'feedback': feedback})


class WeatherView(View):
    def get(self, request):
        form = WeatherForm()
        return render(request, 'weather.html', {'form': form})

    def post(self, request):
        form = WeatherForm()
        form_data = WeatherForm(request.POST)
        if form_data.is_valid():
            lat = request.POST['latitude']
            lon = request.POST['longitude']

            # Pass the lon/lat to a function that makes the API call and returns the info we want as a dict
            weather_data = functions.call_weather(lat, lon)

            # If the co-ords weren't valid, the function returns false and we get send an error
            if not weather_data:
                err_message = "Latitude \"%s\" and/or longitude \"%s\" invalid. Please note" \
                              " latitude ranges from <b>-90.0&deg S</b> to <b>90.0&deg N</b> and " \
                              "longitude ranges from <b>-180.0&deg W</b> to <b>180.0&deg E</b>." % (lat, lon)
                messages.error(request, err_message)
                return render(request, 'weather.html', {'form': form})
            else:
                # Otherwise, render the weather page, passing the dict of weather data to the template
                return render(request, 'weather.html', {'form': form, 'weather': weather_data})
