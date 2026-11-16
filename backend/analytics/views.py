from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .services import get_processed_data
from rest_framework import status




class DashBoardView(APIView):

    def get(self, request):
        try:
            data = get_processed_data()

            return Response(data["dashboard"])

        except Exception as error:
            print(f"Dashboard API error: {error}")

            return Response(
                {
                    "status": "error",
                    "message": "Unable to retrieve dashboard data. Please try again later."
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )


class ForecastDataView(APIView):

    def get(self, request):
        try:
            data = get_processed_data()

            return Response(data["forecasts"])

        except Exception as error:
            print(f"Forecast API error: {error}")

            return Response(
                {
                    "status": "error",
                    "message": "Unable to retrieve forecast data. Please try again later."
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )


class DailyAccuracyView(APIView):

    def get(self, request):
        try:
            data = get_processed_data()

            return Response(data["daily_accuracy"])

        except Exception as error:
            print(f"Daily Accuracy API error: {error}")

            return Response(
                {
                    "status": "error",
                    "message": "Unable to retrieve daily accuracy data. Please try again later."
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
