# AI Travel Agent

This AI travel agent is designed to help suggest places to visit in the United States. It provides personalized recommendations for destinations and activities within the US, taking into account the current weather and user preferences. The system leverages advanced language models and integrates with weather and geocoding APIs to ensure relevant and timely suggestions for your travel plans.

> [!TIP]
> This project was built using Python 3.12. For a better experience, you can install Python 3.12 using this command:
> ```
> uv python install 3.12
>```
> Not using `uv`? You can install Python 3.12 using the following command:
> ```bash
> curl -LsSf https://astral.sh/uv/install.sh | sh
> ```
> Another installation methods are available in the [uv documentation](https://docs.astral.sh/uv/getting-started/installation/#installation-methods). Here you can find installation steps and other guides to help you get started with `uv`.

> [!NOTE]
> The LLM used in this project is `gpt-4o`, in particular the one available in Azure AI Fondry. You can change the model in the [`service.py`](service.py) file, particularly [here you can edit the model](service.py#L32). As you will need to install the LLM provider, you can use the following command to install it:
>
> ```bash
> uv add langchain-{llm_provider} # Replace {llm_provider} with the actual provider name, e.g., deepseek
> ```
> or 
> ```bash
> pip install langchain-{llm_provider}
> ``` 
> This also applies to the `embedding model` used in the project, which is set to `text-embedding-3-large`. You can change it in the following [file](src/travel_agent_tools.py#L101).

To initialize this model, set the following environments variables (if you are using Azure OpenAI):

```bash
export AZURE_OPENAI_API_KEY="YOUR_API_KEY"
export AZURE_OPENAI_ENDPOINT="YOUR_ENDPOINT"
```

Additionally, you will need the Google Maps Geocoding API, which requires an API key. You can set it using the following environment variable:

```bash
export GOOGLE_MAPS_API_KEY="YOUR_GOOGLE_MAPS_API_KEY"
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

>[!NOTE]
> If you are using `uv`, you can skip the virtual environment setup as `uv` will handle it for you.

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

## Run the API
To run the API, you can use the following command (if you are using a virtual environment):
```bash
bentoml serve
```

or if you are using uv, you can run:
```bash
uv run bentoml serve
```
This will start the API server, and you can access it at `http://localhost:8000`. 
The `default` section allows you to access the API using the `/generate/recommendation` route.  

## Example Usage
You can use `CURL` to test the API. For example, you can run the following command to get a recommendation for a trip to Chicago:
```bash
curl -X 'GET' \
  'http://localhost:8000/v1/generate/recommendation?prompt=Recommend%20me%20places%20in%20chicago' \
  -H 'accept: application/json' \
  -H 'x-api-key: ${API_KEY}'
```
This will return a response like:
```bash
"Here’s the weather forecast for Chicago in the upcoming days:\n\n- June 12: Mostly Cloudy\n- June 13: Chance of Rain Showers\n- June 14: Partly Cloudy\n- June 15: Mostly Cloudy\n- June 16-19: Chance of Showers and Thunderstorms\n\nBased on this forecast, here are some recommendations:\n\n### Indoor Activities (Ideal for rainy or cloudy days):\n- **Shedd Aquarium**: Explore marine life from around the globe in this world-class indoor aquarium.\n\n### Outdoor Activities (Best for partly cloudy days like June 14):\n- **Millennium Park**: Enjoy the iconic Cloud Gate sculpture and beautiful outdoor spaces.\n- **Chicago Riverwalk**: Stroll along the scenic riverwalk with views of the city skyline.\n\nFor safety and comfort, prioritize indoor activities during rainy or stormy days. Let me know if you'd like more tailored suggestions!"
```

## Example using cities outside the US
You can also try with cities outside the US, like: Monclova, Coahuila, Mexico:
```bash
curl -X 'GET' \
  'http://localhost:8000/v1/generate/recommendation?prompt=Recommend%20me%20places%20in%20monclova%2C%20coahuila' \
  -H 'accept: application/json' \
  -H 'x-api-key: ${API_KEY}'
```

And you will get a response like:
```bash
"It seems that Monclova, Coahuila is located in Mexico, not the United States. My expertise is focused on planning weather-aware activities in cities within the United States. Unfortunately, I cannot assist with recommendations for cities outside the U.S.\n\nIf you have a U.S. city in mind, feel free to share it, and I’ll be happy to help!"
```

## Example of rate limiting by API Key
You can also test the rate limiting by using the API key multiple times. For example, you can run the following command multiple times:

### Successful request
```bash
curl -X 'GET' \
  'http://localhost:8000/v1/generate/recommendation?prompt=Recommend%20me%20places%20in%20chicago' \
  -H 'accept: application/json' \
  -H 'x-api-key: ${API_KEY}'
```

Response:
```bash
"Based on the weather forecast for Chicago, here are some recommendations:\n\n### Weather Forecast:\n- **June 12:** Mostly Cloudy\n- **June 13:** Chance Rain Showers\n- **June 14:** Partly Cloudy\n- **June 15:** Mostly Cloudy\n- **June 16-19:** Chance Showers and Thunderstorms\n\n### Suggested Activities:\n1. **Shedd Aquarium**: Explore marine life from around the globe in this indoor aquarium. Perfect for cloudy or rainy days.\n2. **Art Institute of Chicago**: Dive into art and architecture in this indoor space, ideal for staying dry during rain showers.\n\nLet me know if you'd like more specific recommendations or details!"
```

### Rate limit exceeded
```bash
curl -X 'GET' \
  'http://localhost:8000/v1/generate/recommendation?prompt=Recommend%20me%20places%20in%20chicago' \
  -H 'accept: application/json' \
  -H 'x-api-key: ${API_KEY}'
```

Response:
```JSON
{
  "detail": "Request rate limit exceeded."
}
```

## Unit Tests
To run the unit tests, you can use the following command if you are using a virtual environment:
```bash
python -m unittest discover
``` 

or if you are using `uv`, you can run:
```bash
uv run unittests -m discover
```


