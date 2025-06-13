from src.travel_agent_tools import get_weather_data_us, retrieve_customer_location, retrieve_available_locations
from langgraph.graph import START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_openai.chat_models import AzureChatOpenAI
from typing import Annotated, TypedDict
from langchain_community.callbacks.openai_info import OpenAICallbackHandler

# Provide the list of tools to be used in the agent
tools = [retrieve_customer_location, get_weather_data_us, retrieve_available_locations]

# Callback Handler to get the total amount of tokens consumed by the OpenAI model.
callback_handler = OpenAICallbackHandler()

# Initialize the Azure OpenAI model with the tools
model = AzureChatOpenAI(
    model = "gpt-4o",
    azure_deployment= "gpt-4o",
    api_version="2024-02-01",
    temperature=0.1
).bind_tools(tools)

# Define the state of the graph
class State(TypedDict):
    messages: Annotated[list, add_messages]

# Define the node that will invoke the model with the messages
def model_node(state: State) -> State:
    res = model.invoke(state["messages"])
    return {"messages": res}

# Create the state graph and add nodes and edges
builder = StateGraph(State)
builder.add_node("model", model_node)
builder.add_node("tools", ToolNode(tools))
builder.add_edge(START, "model")
builder.add_conditional_edges("model", tools_condition)
builder.add_edge("tools","model")

# Compile the graph to create the final agent graph
AGENT = builder.compile()