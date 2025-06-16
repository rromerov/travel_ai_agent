from src.travel_agent_tools import get_weather_data_us, retrieve_customer_location, retrieve_available_locations
from langgraph.graph import START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_openai.chat_models import AzureChatOpenAI
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.tools import BaseTool
from typing import Annotated, TypedDict, Optional

class TravelAgent:
    """
    Agent class to build and compile a LangGraph-based conversational agent.

    This agent integrates a language model (e.g., AzureChatOpenAI) with a set of tools 
    to support multi-step reasoning and tool-augmented responses. It uses LangGraph to 
    define the flow between the model and tool execution nodes.

    Attributes:
        model_provider (BaseChatMOdel): A chat model instance to handle natural language interactions.
        tools (list[BaseTool]): A list of LangChain tools to be bound to the model.

    Example:
        agent = Agent()
        runnable_agent = agent.build_and_compile_agent()
        output = runnable_agent.invoke({"messages": [HumanMessage(content="What's the weather in NYC?")]})

    Returns:
    - A compiled LangGraph Runnable that processes message state using the model and tools.
    """

    def __init__(self,
                 model_provider: Optional[BaseChatModel] = None,
                 tools: Optional[list[BaseTool]] = None):
        self.model_provider = model_provider or AzureChatOpenAI(
            model = "gpt-4o",
            azure_deployment= "gpt-4o",
            temperature= 0.1,
            api_version="2024-10-21"
        )
        self.tools = tools or [
            retrieve_customer_location,
            get_weather_data_us,
            retrieve_available_locations
        ]
    
    # Define the state of the graph
    class State(TypedDict):
        messages: Annotated[list, add_messages]

    # Define model node used inside the LangGraph
    def __model_node(self, state: State):
        res = self.model.invoke(state["messages"])
        return {"messages": res}

    def build_and_compile_agent(self):
        llm = self.model_provider
        # Bind the model to the selected tools
        self.model = llm.bind_tools(self.tools)
        # Build the stateful graph
        builder = StateGraph(self.State)
        builder.add_node("model", self.__model_node)         # LLM inference
        builder.add_node("tools", ToolNode(self.tools))    # Tool execution node
        builder.add_edge(START, "model")              # Start → Model
        builder.add_conditional_edges("model", tools_condition)  # If tools are needed → use tools
        builder.add_edge("tools", "model")            # After tools → back to model

        # Compile and return the runnable agent
        return builder.compile()