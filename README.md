# WindSight UK — Wind Generation Forecast Analysis

## Project Overview

WindSight UK is a full-stack analytics application that evaluates the accuracy of wind generation forecasts in Great Britain.

The application retrieves actual wind generation data and forecast data from the Elexon BMRS API, matches forecasts with actual generation, and presents forecast performance through an interactive dashboard.

It helps users understand how closely forecasted wind generation aligns with actual generation and identify periods of forecast error.

## Features

- Retrieves actual wind generation data from Elexon.
- Retrieves wind generation forecasts from Elexon.
- Matches forecasts with actual generation periods.
- Selects the latest eligible forecast before the defined decision cutoff.
- Calculates forecast accuracy metrics:
  - Mean Absolute Error (MAE)
  - Root Mean Squared Error (RMSE)
  - Bias
- Displays forecast and actual generation comparisons.
- Shows daily forecast accuracy.
- Reports data matching coverage and missing periods.
- Provides an interactive React dashboard.
- Runs through Docker Compose.

## Technology Stack

**Frontend**
- React
- Vite
- Axios
- Recharts
- CSS

**Backend**
- Python
- Django
- Django REST Framework
- Requests

**Deployment and Containerization**
- Docker
- Docker Compose
- Nginx
- Gunicorn

## Data Sources

The application uses the following Elexon BMRS datasets:

| Dataset | Purpose |
|---|---|
| FUELHH | Actual half-hourly generation data |
| WINDFOR | Wind generation forecast data |

API base URL:

https://data.elexon.co.uk/bmrs/api/v1/

Analysis period: January 2026.

## Forecast Matching Methodology

### 1. Actual generation

Actual wind generation is retrieved from the FUELHH dataset using the wind fuel type.

The actual generation data is available at half-hourly resolution.

### 2. Forecast generation

Forecast data is retrieved from the WINDFOR dataset.

Each forecast record contains:
- Delivery time (`startTime`)
- Publication time (`publishTime`)
- Forecast generation (`generation`)

### 3. Forecast selection

For each hourly delivery period, the application selects the latest forecast published on or before the defined decision cutoff.

The current analysis uses the following assumption:

**Decision cutoff:** 10:00 UTC on the previous calendar day.

This is an analytical assumption used for this project, not a claim about an official market deadline.

### 4. Hourly actual generation

The actual generation data is available every 30 minutes, whereas the comparison is performed hourly.

The application calculates hourly actual generation by averaging the two corresponding half-hourly readings.

This aggregation is a documented analytical assumption.

### 5. Error calculation

Forecast error is calculated as:

`Forecast Generation - Actual Generation`

A positive error indicates that the forecast was higher than actual generation. A negative error indicates that the forecast was lower than actual generation.

## Forecast Accuracy Metrics

| Metric | Description |
|---|---|
| MAE | Average absolute difference between forecast and actual generation |
| RMSE | Square root of the average squared forecast error |
| Bias | Average signed forecast error |

All generation values and error metrics are expressed in MW.

## API Endpoints

| Endpoint | Description |
|---|---|
| `/api/dashboard/` | Dashboard summary and accuracy metrics |
| `/api/forecasts/` | Matched forecast and actual generation records |
| `/api/daily-accuracy/` | Daily forecast accuracy metrics |

## Project Structure

```text
wind/
├── backend/
│   ├── analytics/
│   │   ├── services.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── config/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── manage.py
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── services/
│   │   └── styles/
│   ├── Dockerfile
│   └── nginx.conf
│
├── docker-compose.yml
└── README.md
```

## Running the Application Locally

### Prerequisites

- Docker Desktop
- Docker Compose

### Start the application

Clone the repository:

```bash
git clone https://github.com/vaishnavrs/wind.git
cd wind
```

Build and start the services:

```bash
docker compose up --build
```

Open the application:

**Frontend:** http://localhost:3000

**Backend API:** http://localhost:8000/api/dashboard/

Stop the services:

```bash
docker compose down
```

## Important Limitations

- This analysis focuses only on wind generation.
- It does not include electricity demand, wholesale market prices, or other generation sources.
- Therefore, the dashboard does not calculate the total electricity procurement requirement.
- The forecast cutoff and hourly averaging approach are analytical assumptions.
- Results depend on the availability and completeness of the source API data.

## Deployment

Deployment URL: To be added.

## Video Demonstration

Unlisted YouTube demonstration: To be added.

## Acknowledgement of AI Assistance

AI tools were used for learning support, debugging assistance, code explanations, and documentation guidance during development. The implementation and analysis were reviewed and tested as part of the project development process.