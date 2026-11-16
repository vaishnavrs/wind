import json
import requests
from datetime import datetime,timedelta,timezone
import math
from django.core.cache import cache

def fetch_actual_data():

    url = "https://data.elexon.co.uk/bmrs/api/v1/datasets/FUELHH/stream"


    params = {
        "settlementDateFrom": "2026-01-01",
        "settlementDateTo": "2026-01-31",
        "fuelType": "WIND",
    }

    response = requests.get(url, params=params,timeout=60)

    response.raise_for_status()  

    return response.json()  


def fetch_forecast_data():

    url = "https://data.elexon.co.uk/bmrs/api/v1/datasets/WINDFOR/stream"

    params = {
        "publishDateTimeFrom": "2026-01-01T00:00:00Z",
        "publishDateTimeTo": "2026-01-31T23:59:59Z"
    }

    response = requests.get(url, params=params,timeout=60)

    response.raise_for_status() 

    return response.json()  


def build_actual_lookup(actual_data):

    actual_lookup = {}

    for record in actual_data:

        delivery_time = record.get("startTime")
        generation = record.get("generation")

        
        if delivery_time is None or generation is None:
            continue

      
        try:
            generation = float(generation)
        except (ValueError, TypeError):
            continue

      
        actual_lookup[delivery_time] = generation

    return actual_lookup




def build_forecast_lookup(forecast_data):

    forecast_lookup = {}

    for record in forecast_data:

        delivery_time = record.get("startTime")
        publish_time = record.get("publishTime")
        generation = record.get("generation")

        # Check for missing values
        if not delivery_time or not publish_time or generation is None:
            continue

        # Validate generation
        try:
            generation = float(generation)
        except (ValueError, TypeError):
            continue

        # Store valid forecast record
        if delivery_time not in forecast_lookup:
            forecast_lookup[delivery_time] = []

        # Keep the original record structure
        forecast_lookup[delivery_time].append({
            **record,
            "generation": generation
        })

    return forecast_lookup



def select_forecast(forecasts,decision_cuttoff):

    eligible_forcasts = []

    for forecast in forecasts:
        publish_time = datetime.fromisoformat(
            forecast['publishTime'].replace("Z","+00:00")
        )

        if publish_time <= decision_cuttoff:
            eligible_forcasts.append(forecast)
    eligible_forcasts.sort(key=lambda x:x["publishTime"])

    if eligible_forcasts:
        return eligible_forcasts[-1]
    return None

def match_actuals_with_forecasts(actual_lookup,forecast_lookup):

    matched_data = []

    for delivery_time in actual_lookup:
        delivery_datetime = datetime.fromisoformat(
            delivery_time.replace("Z","+00:00")
        )

        if  delivery_datetime.minute !=0:
            continue

        decision_cutoff = delivery_datetime.replace(
            hour= 10,
            minute= 0,
            second= 0,
            microsecond= 0
        )- timedelta(days=1)

        next_datetime = delivery_datetime + timedelta(minutes=30)

        next_time = next_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")

        first_actual = actual_lookup.get(delivery_time)
        second_actual = actual_lookup.get(next_time)

        if first_actual is None or second_actual is None:
            continue

        # Calculate hourly average actual generation
        actual_generation = (first_actual + second_actual) / 2

        # Get forecast versions for this delivery period
        forecasts = forecast_lookup.get(delivery_time, [])

        # Select the latest eligible forecast
        selected_forecast = select_forecast(
            forecasts,
            decision_cutoff
        )

        if selected_forecast is None:
            continue

        forecast_generation = selected_forecast["generation"]

        matched_data.append({
            "delivery_time": delivery_time,
            "actual_generation": actual_generation,
            "forecast_generation": forecast_generation,
            "forecast_publish_time": selected_forecast["publishTime"]
        })

    matched_data.sort(key=lambda record: record["delivery_time"])

    return matched_data


def calculate_errors(matched_data):
    for record in matched_data:
        forecast = record["forecast_generation"]
        actual = record["actual_generation"]

        record["error"] = forecast - actual
        record["absolute_error"] = abs(record["error"])

    return matched_data





def calculate_metrics(matched_data):

    total_periods = len(matched_data)

    # Handle empty matched data
    if total_periods == 0:
        return {
            "total_matched_periods": 0,
            "mae": 0,
            "rmse": 0,
            "bias": 0
        }

    total_absolute_error = sum(
        record["absolute_error"] for record in matched_data
    )

    total_squared_error = sum(
        record["error"] ** 2 for record in matched_data
    )

    total_error = sum(
        record["error"] for record in matched_data
    )

    mae = total_absolute_error / total_periods

    rmse = math.sqrt(total_squared_error / total_periods)

    bias = total_error / total_periods

    return {
        "total_matched_periods": total_periods,
        "mae": round(mae, 2),
        "rmse": round(rmse, 2),
        "bias": round(bias, 2)
    }




def calculate_coverage(matched_data, actual_lookup):

    expected_periods = sum(
        1 for time in actual_lookup
        if time[14:16] == "00"
    )

    matched_periods = len(matched_data)

    missing_periods = max(
        expected_periods - matched_periods,
        0
    )

    # Handle empty actual data
    if expected_periods == 0:
        coverage = 0
    else:
        coverage = (matched_periods / expected_periods) * 100

    return {
        "expected_periods": expected_periods,
        "matched_periods": matched_periods,
        "missing_periods": missing_periods,
        "coverage_percentage": round(coverage, 2)
    }



def get_dashboard_data():

    # Fetch data from Elexon
    actual_data = fetch_actual_data()
    forecast_data = fetch_forecast_data()

    # Create lookup dictionaries
    actual_lookup = build_actual_lookup(actual_data)
    forecast_lookup = build_forecast_lookup(forecast_data)

    # Match actuals with forecasts
    matched_data = match_actuals_with_forecasts(
        actual_lookup,
        forecast_lookup
    )

    # Calculate errors
    matched_data = calculate_errors(matched_data)

    #Calculate metrics
    metrics = calculate_metrics(matched_data)

    # Calculate coverage
    coverage = calculate_coverage(
        matched_data,
        actual_lookup
    )

    # Return dashboard data
    return {
        "month": "January 2026",
        "total_actual_records": len(actual_data),
        "total_forecast_records": len(forecast_data),
        "mae": metrics["mae"],
        "rmse": metrics["rmse"],
        "bias": metrics["bias"],
        **coverage
    }


def calculate_daily_metrics(matched_data):

    daily_data = {}

    for record in matched_data:

        delivery_time = record["delivery_time"]

        
        delivery_date = delivery_time[:10]

        if delivery_date not in daily_data:
            daily_data[delivery_date] = []

        daily_data[delivery_date].append(record)

    daily_metrics = []

    for date, records in daily_data.items():

        total_periods = len(records)

        total_absolute_error = sum(
            record["absolute_error"] for record in records
        )

        total_error = sum(
            record["error"] for record in records
        )

        daily_mae = total_absolute_error / total_periods

        daily_bias = total_error / total_periods

        daily_metrics.append({
            "date": date,
            "total_periods": total_periods,
            "mae": round(daily_mae, 2),
            "bias": round(daily_bias, 2)
        })

    return daily_metrics



def get_processed_data():

    cached_data = cache.get("windsight_processed_data")

    if cached_data is not None:
        print("Returning data from cache")
        return cached_data

    print("Fetching fresh data from Elexon")

    try:
        # Fetch actual and forecast data
        actual_data = fetch_actual_data()
        forecast_data = fetch_forecast_data()

        # Check whether API returned data
        if not actual_data or not forecast_data:
            raise ValueError("Elexon returned empty datasets")

      
        actual_lookup = build_actual_lookup(actual_data)
        forecast_lookup = build_forecast_lookup(forecast_data)

        # Match actuals and forecasts
        matched_data = match_actuals_with_forecasts(
            actual_lookup,
            forecast_lookup
        )

        if not matched_data:
            raise ValueError("No matching forecast and actual records found")

        # Calculate errors
        matched_data = calculate_errors(matched_data)

        # Calculate metrics
        metrics = calculate_metrics(matched_data)

        # Calculate coverage
        coverage = calculate_coverage(
            matched_data,
            actual_lookup
        )

        # Calculate daily accuracy
        daily_metrics = calculate_daily_metrics(matched_data)

        # Combine results
        processed_data = {
            "dashboard": {
                "month": "January 2026",
                "total_actual_records": len(actual_data),
                "total_forecast_records": len(forecast_data),
                **metrics,
                **coverage
            },
            "forecasts": matched_data,
            "daily_accuracy": daily_metrics
        }

        
        cache.set(
            "windsight_processed_data",
            processed_data,
            timeout=3600
        )

        return processed_data

    except requests.exceptions.RequestException as error:
        print(f"Elexon API error: {error}")
        raise

    except ValueError as error:
        print(f"Data processing error: {error}")
        raise
