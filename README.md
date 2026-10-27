# Open API Web Services — Assignment 6

Arts and Advanced Big Data | Week 6

Two interactive Streamlit web apps powered by public Open APIs.

## Service 1: Explore Artworks
- **File:** `met_app.py`
- **API:** The Metropolitan Museum of Art Collection API
- Search by keyword, adjust the result count, and view artwork images, titles, artists, dates, and museum links.
- Uses one-hour caching and handles unavailable API responses.

## Service 2: Interactive Weather Dashboard
- **File:** `weather_map.py`
- **API:** Open-Meteo Forecast API
- Click a location on a map to view a 48-hour temperature chart and summary metrics.
- Uses ten-minute caching and handles unavailable API responses.

## Run locally

```bash
pip install -r requirements.txt
streamlit run met_app.py
```

For the weather dashboard:

```bash
streamlit run weather_map.py
```

## Deploy on Streamlit Community Cloud
Deploy two apps from the same GitHub repository, selecting `met_app.py` and `weather_map.py` as the respective main file paths.

## Live apps
- Explore Artworks: (add your Streamlit URL after deployment)
- Interactive Weather Dashboard: (add your Streamlit URL after deployment)

## Credits
- Artwork metadata and images: The Metropolitan Museum of Art Open Access Collection API (CC0)
- Weather forecast: Open-Meteo (non-commercial use)
