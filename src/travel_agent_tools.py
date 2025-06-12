from langchain_core.tools import tool, ToolException
from langchain.tools.retriever import create_retriever_tool
from typing import List, Annotated
import requests
import os
from src.chroma_db_vectorstore import retriever
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

@tool
def retrieve_customer_location(
    location: Annotated[str, "US City"]) ->  dict:
    """
    Function to generate coordinates of a desired location based of customer's query.
    """
    params = {
        "address": f"{location}",
        "region": "us",
        "key": os.environ["GOOGLE_MAPS_API_KEY"]
    }

    url = "https://maps.googleapis.com/maps/api/geocode/json"

    try:
        response = requests.get(url=url, params=params)
        response.raise_for_status()  # raises HTTPError if not 2xx
    except requests.exceptions.HTTPError as error:
        raise ToolException(f"Unexpected response encountered: {error}")
    # turn response to json format, in order to access the content
    raw_data = response.json()
    data = raw_data["results"][0]["geometry"]["location"]
    return {
        "latitude": data["lat"],
        "longitude": data["lng"]
    }

from langchain_core.tools import ToolException
import requests
from typing import Annotated

@tool
def get_weather_data_us(
    latitude: Annotated[float, "Latitude of customer's place of interest"],
    longitude: Annotated[float, "Longitude of customer's place of interest"]
) -> dict:
    """Function to get the weather of USA cities"""
    
    # Retrieve data from the weather.gov API endpoint based on coordinates
    url = f"https://api.weather.gov/points/{latitude},{longitude}"
    headers = {
        "User-Agent": "MyLocalWeatherTest/0.1"
    }

    # Call weather.gov to get the forecast URL for the location
    try:
        response = requests.get(url=url, headers=headers)
        # If the coordinates are outside the US or invalid
        if response.status_code == 404:
            raise ToolException(f"Coordinates {latitude}, {longitude} are outside the US or invalid.")
        response.raise_for_status()  # raises HTTPError if not 2xx
    except requests.exceptions.RequestException as e:
        raise ToolException(f"Error retrieving point data: {str(e)}")

    # Extract the forecast URL from the response
    try:
        forecast_url = response.json()["properties"]["forecast"]
        weather_response = requests.get(url=forecast_url, headers=headers)
        weather_response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise ToolException(f"Error retrieving weather data: {str(e)}")
    except KeyError:
        raise ToolException("Forecast data not available for this location.")

    # Parse the forecast response and extract daily weather summaries
    try:
        weather_data = weather_response.json()
        periods = weather_data["properties"]["periods"]
        count_of_days = len(periods)
        # Return the date and short weather summary for each forecasted period
        return {
            periods[i]["startTime"][:10]: periods[i]["shortForecast"]
            for i in range(count_of_days)
        }
    except Exception:
        raise ToolException("Failed to parse weather data.")


retrieve_available_locations = create_retriever_tool(
    retriever,
    "retrieve_available_activities",
    "Search and return ideal activities to do in the city considering weather forecast",
)