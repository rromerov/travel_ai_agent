# AI Travel Agent

> [!TIP] This project was built using Python 3.12. For a better experience, you can install Python 3.12 using this command:

```
uv python install 3.12
```

To install all necessary dependencies you can either can use a `virtual environment` or `uv`. 

## Using Virtual Environment
Create a virtual environment in the current directory:
```bash
python3 -m venv .venv
```

Then activate the virtual environment:
```bash
source .venv/bin/activate
```

Once activated, you can install the dependencies:
```bash
pip install -r requirements.txt
```
## Using uv
If you have `uv` installed, you can install the dependencies with:
```bash
uv add -r requirements.txt
```

>[!NOTE] If you are using `uv`, you can skip the virtual environment setup as `uv` will handle it for you.

## Load API keys
To use the API, you need a API KEY, these are generated using the following script:

Using the virtual environment, run the following command:
```bash
python src/utils/api_keys.py 
```

or using `uv`
```bash
uv run src/utils/api_keys.py 
```

Use one of this API keys to access the API:

> [!NOTE] 
> This will populate a json file inside the data folder. Once generated you can access them at the [following link](data/api_keys.json).

## APIs used

- [Google Maps Geocoding](https://developers.google.com/maps/documentation/geocoding/requests-geocoding#geocoding-lookup) for converting addresses into geographic coordinates. It offers a free tier with a limited number of requests per month.

You can see the response from this API [here](results/geocode.json)

- [National Weather Service API](https://www.weather.gov/documentation/services-web-api) for retrieving weather data by providing coordinates within US. It provides a free API with no authentication required.

> [!NOTE]  
> Two responses are generated using this API:  
> 1. The first request requires coordinates and returns a response like [this](results/points.json).  
> 2. The response from the first call includes a second endpoint, which returns the [forecast data seen here](results/forecast.json).



