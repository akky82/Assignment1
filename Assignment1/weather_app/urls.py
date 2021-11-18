from django.urls import path
from . import views
from weather_app.views import FeedbackView, WeatherView


app_name = "weather_app"

urlpatterns = [
    path('', views.home),
    path('about/', views.about),
    path('future/', views.future),
    path('disclaimer/', views.disclaimer),
    path('privacy/', views.privacy),
    path('feedback/', FeedbackView.as_view(), name="feedback"),
    path('weather/', WeatherView.as_view(), name="weather"),
]
