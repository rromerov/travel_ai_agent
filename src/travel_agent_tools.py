from langchain_core.tools import tool, ToolException
from langchain.tools.retriever import create_retriever_tool
from langchain_openai.embeddings import AzureOpenAIEmbeddings
from typing import Annotated
import requests
import os
from src.vectorstore import ChromaDBVectorStore

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

    headers = {
         "Connection": "close"
    }

    url = "https://maps.googleapis.com/maps/api/geocode/json"

    try:
            with requests.Session() as session:
                # Make the API call to Google's geocoding service
                response = session.get(url=url, params=params, headers=headers)
                response.raise_for_status()  # Raise error for HTTP issues

                # Parse JSON response within context manager
                results = response.json().get("results", [])
                if not results:
                    raise ToolException(f"No coordinates found for: {location}")

                geometry = results[0]["geometry"]["location"]
                return {
                    "latitude": geometry["lat"],
                    "longitude": geometry["lng"]
                }

    except requests.exceptions.RequestException as e:
        raise ToolException(f"Failed to retrieve location data: {str(e)}")
    except KeyError:
       raise ToolException("Malformed response from location service.")

@tool
def get_weather_data_us(
    latitude: Annotated[float, "Latitude of customer's place of interest"],
    longitude: Annotated[float, "Longitude of customer's place of interest"]
) -> dict:
    """Function to get the weather of USA cities"""
    # Retrieve data from the weather.gov API endpoint based on coordinates
    url = f"https://api.weather.gov/points/{latitude},{longitude}"
    headers = {
        "User-Agent": "MyLocalWeatherTest/0.1",
        "Connection": "close"
    }
    try:
            with requests.Session() as session:
                # Step 1: Call weather.gov to get the forecast URL for the given coordinates
                response = session.get(url=url, headers=headers)
                
                if response.status_code == 404:
                    raise ToolException(f"Coordinates {latitude}, {longitude} are outside the US or invalid.")

                response.raise_for_status()  # Raise for other non-2xx status codes

                # Parse forecast URL from JSON response
                forecast_url = response.json()["properties"]["forecast"]

                # Step 2: Fetch weather data from forecast URL
                weather_response = session.get(url=forecast_url, headers=headers)
                weather_response.raise_for_status()

                # Parse the weather data
                weather_data = weather_response.json()
                periods = weather_data["properties"]["periods"]
                # Format and return weather summary by date
                return {
                    period["startTime"][:10]: period["shortForecast"]
                    for period in periods
                }

    except requests.exceptions.RequestException as e:
        raise ToolException(f"Network error during weather data retrieval: {str(e)}")

    except KeyError:
        raise ToolException("Missing expected fields in weather data.")

    except (TypeError, ValueError):
        raise ToolException("Failed to parse weather data correctly.")

# You can replace the embedding model with your desired embedding model
vectorstore = ChromaDBVectorStore(
        collection_name="travel_collection",
        namespace="chroma",
        persist_directory="./data",
        embedding_model=AzureOpenAIEmbeddings(
                model="text-embedding-3-large",
                api_version="2024-02-01"
                )
                )

retriever = vectorstore.add_index()

retrieve_available_locations = create_retriever_tool(
    retriever,
    "retrieve_available_activities",
    "Search and return ideal activities to do in the city considering weather forecast",
)