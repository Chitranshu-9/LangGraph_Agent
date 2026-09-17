from typing import TypedDict, List
from langgraph.graph import StateGraph

# Defining State Schema
class AgentState(TypedDict):
    values :List[int]
    name:str
    result:str

def processValues(state: AgentState) -> AgentState:
    """This function handles multiple different Inputs"""
    state["result"] = f"Hi there {state["name"]}, Your sum = {sum(state["values"])}"
    
    # print(state)
    return state

graph = StateGraph(AgentState)

graph.add_node("processor", processValues)
graph.set_entry_point("processor")
graph.set_finish_point("processor")

# Always store compiled graph in a variable
app = graph.compile()

from IPython.display import Image, display
display(Image(app.get_graph().draw_mermaid_png()))

answers = app.invoke({"values":[1,2,3,4], "name":"Chitranshu"})

print(answers)