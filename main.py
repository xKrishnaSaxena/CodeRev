from fastapi import FastAPI
from pydantic import BaseModel
from langgraph.graph import StateGraph,END
from state import State,RouteDecision
from agents.router import router
from fastapi.responses import HTMLResponse
class Code(BaseModel):
    code_snippet:str
    language:str
    context:str

app = FastAPI()

graph=StateGraph(State)
graph.add_node("router",router)
graph.set_entry_point("router")
graph.add_edge("router",END)

main_graph=graph.compile()

@app.get("/health")
def health_checker():
    return {"Hello world"}

@app.post("/review")
async def code_review(code:Code):
    initialState:State={
        "raw_code":code.code_snippet,
        "language":code.language,
        "context":code.context,
        "issues_list":[],
        "agent_feedback":{},
        "route_decision":RouteDecision.SKIP
    }
    res=await main_graph.ainvoke(initialState)

    return res


@app.get("/graph", response_class=HTMLResponse)
def get_graph_diagram():
    mermaid_source = main_graph.get_graph().draw_mermaid()

    html_content = f"""
    <html>
    <head>
      <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    </head>
    <body>
      <div class="mermaid">
      {mermaid_source}
      </div>
      <script>
        mermaid.initialize({{ startOnLoad: true }});
      </script>
    </body>
    </html>
    """

    return html_content