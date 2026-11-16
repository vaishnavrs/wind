from django.urls import path
from .views import  DashBoardView,ForecastDataView,DailyAccuracyView


urlpatterns = [
    path('dashboard/', DashBoardView.as_view(), name='dashboard'),
    path('forecasts/', ForecastDataView.as_view(), name='forecast-data'),
    path('daily-accuracy/',DailyAccuracyView.as_view(),name='daily-accuracy')
]