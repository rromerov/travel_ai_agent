import bentoml
import fastapi
from langchain_community.callbacks.openai_info import OpenAICallbackHandler
from langchain_core.messages import HumanMessage, SystemMessage
from src.react_agent_graph import AGENT

app = fastapi.FastAPI()

# Callback Handler to get the total amount of tokens consumed
callback_handler = OpenAICallbackHandler()

# Leverage BentoML to create a service
@bentoml.service(
    resources = {
        "cpu": 2
    },
    traffic = {
        "timeout": 120
    },
    http = {
        "port": 8000
    },
    workers = 2
)

# Mount the FastAPI app to BentoML
@bentoml.asgi_app(app = app, path = "/v1")
class Generate:
    @app.get("/generate/recommendation")
    def recommender_system(self, prompt: str) -> str:
        input = {
            "messages": [
                SystemMessage(
                    content = """
                    You are an expert travel agent specializing in planning weather-aware activities across cities in the United States. Your task is to:
                    1. Validate the city input by the user.
                    2. If the city is not found or is outside the US, notify the user immediately.
                    3. Retrieve the weather forecast for the upcoming days.
                    4. Based on the forecast, suggest suitable activities from the knowledge base.
                    Only suggest activities if reliable location and weather data are available.

                    For example:
                    - Recommend indoor activities if it's rainy or stormy.
                    - Suggest outdoor activities for sunny or clear days.
                    - Prioritize safety and comfort.

                    Include weather forecast in your response using this format: June 17 will be mostly clear.
                    Always be clear and friendly in your responses.
                    """
                ), 
                HumanMessage(content = prompt)
            ]
        }

        response = AGENT.invoke(input,
                                config={
                                    "callbacks": [callback_handler]
                                })
        output = response["messages"][-1].content
        return output