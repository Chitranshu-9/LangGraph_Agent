from typing import TypedDict, List
import random
from langgraph.graph import StateGraph, START,END

# Defining State Schema
class AgentState(TypedDict):
    name: str
    number: List[int]
    counter: int
    
    
def greeting_node(state: AgentState) -> AgentState:
    """This function says hi to the user"""
    state["result"] = f"Hi there {state["name"]}"
    state["counter"] = 0
    # print(state)
    return state

    
def random_node(state: AgentState) -> AgentState:
    """Generates random number between 0 and 10"""
    state["number"].append(random.randint(0,10))
    state["counter"] += 1
    # print(state)
    return state

def should_continue(state: AgentState) -> AgentState:
    """decides what to do next"""
    if state["counter"] < 5:
        print("ENTERING LOOP ", state["counter"])
        return "loop"
    else:
        return "exit"
    
graph = StateGraph(AgentState)
graph.add_node("greeting", greeting_node)
graph.add_node("random", random_node)

graph.add_edge("greeting", "random")

graph.add_conditional_edges(
    "random", # Source node
    should_continue, # Source function
    {
        "loop":"random",
        "exit":END
    } 
)

graph.set_entry_point("greeting")
app = graph.compile()

result = app.invoke({"name":"Chitranshu", "number":[], "counter":-2})
print(result)       