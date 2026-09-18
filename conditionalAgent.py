from typing import TypedDict, List
from langgraph.graph import StateGraph, START,END

# Defining State Schema
class AgentState(TypedDict):
    number1: int
    operation: str
    number2: int
    finalNumber: int

def adder(state:AgentState) -> AgentState:
    """This node adds the 2 numbers

    Args:
        state (AgentState): _description_

    Returns:
        AgentState: _description_
    """
    state["finalNumber"] = state["number1"] + state["number2"]
    return state

def subtractor(state:AgentState) -> AgentState:
    """This node subtracts the 2 numbers

    Args:
        state (AgentState): _description_

    Returns:
        AgentState: _description_
    """
    state["finalNumber"] = state["number1"] - state["number2"]
    return state

def decideNextNode(state:AgentState) -> AgentState:
    """This node will select the next node of the graph"""
    if state["operation"] == "+":
        return "additional_operation"
    
    if state["operation"] == "-":
        return "subtraction_operation"
 
 
# Graph Build
graph = StateGraph(AgentState)
graph.add_node("add_node", adder)
graph.add_node("subtract_node", subtractor)

# passthrough function
graph.add_node("router", lambda state:state) 
graph.add_edge(START, "router")
graph.add_conditional_edges(
    "router",decideNextNode,
    {
        "additional_operation":"add_node",
        "subtraction_operation":"subtract_node"
    } 
)

graph.add_edge("add_node", END)
graph.add_edge("subtract_node", END)
app = graph.compile()

initial_state_1 = AgentState(number1=10, operation='-', number2=5)

result = app.invoke(initial_state_1)
print(result)       