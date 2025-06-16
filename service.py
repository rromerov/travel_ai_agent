import bentoml
from fastapi import FastAPI, Depends, HTTPException
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai.chat_models import AzureChatOpenAI
from src.react_agent_graph import TravelAgent
from src.dependencies import rate_limiter, token_limiter
from src.rate_limiter import TokenBucket

app = FastAPI()

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
@bentoml.asgi_app(app=app, path="/v1", name="TravelAgentService")
class Generate:
    @bentoml.on_startup
    def start_model(self):
        # You can replace the model with your desired chat model
        llm  = TravelAgent(
            model_provider = AzureChatOpenAI(
                model = "gpt-4o",
                azure_deployment = "gpt-4o",
                temperature = 0.1,
                api_version = "2024-10-21"
            )
        )
        self.agent = llm.build_and_compile_agent()
    
    @app.get("/generate/recommendation")
    def recommender_system(
        self,
        prompt: str,
        _: None = Depends(rate_limiter),
        token_bucket: TokenBucket = Depends(token_limiter)
    ) -> str:
        estimated_cost = 2500  # Estimated tokens per response

        if not token_bucket.allow_request(cost=estimated_cost):
            raise HTTPException(
                status_code=429,
                detail="Token limit exceeded. Please wait before sending another request."
            )
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

        # Build the agent graph
        response = self.agent.invoke(
            input
            )
        output = response["messages"][-1].content
        return output