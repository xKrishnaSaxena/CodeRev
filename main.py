from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langgraph.graph import StateGraph, END
from state import State, RouteDecision
from agents.router import router
from agents.performance import performance
from agents.security import security
from agents.syntax import syntax
from agents.final_synthesis import synthesis
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager
from vector_store import init_rag

class Code(BaseModel):
    code_snippet: str
    language: str
    context: str

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_rag() 
    yield

app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server (adjust port if different)
        "http://127.0.0.1:5173",
        "http://localhost:3000",  # Common React dev port, if needed
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Allows GET, POST, OPTIONS, etc.
    allow_headers=["*"],  # Allows all headers (e.g., Content-Type)
)

graph = StateGraph(State)

graph.add_node("router", router)
graph.add_node("syntax", syntax)
graph.add_node("security", security)
graph.add_node("performance", performance)
graph.add_node("synthesis", synthesis)

graph.set_entry_point("router")

def route_cond(state: State) -> str:
    decision = state.get("route_decision", RouteDecision.SKIP)
    if decision == RouteDecision.SKIP:
        return "synthesis"
    elif decision == RouteDecision.SYNTAX_ONLY:
        return "syntax"
    elif decision == RouteDecision.SECURITY_FIRST:
        return "security"
    else:
        return "syntax"

graph.add_conditional_edges(
    "router",
    route_cond,
    {
        "syntax": "syntax",
        "security": "security",
        "synthesis": "synthesis"
    }
)

graph.add_conditional_edges(
    "syntax",
    lambda state: "performance" if any(issue.get("type", "") == "perf_risk" for issue in state.get("detected_issues", [])) else "synthesis",
    {"performance": "performance", "synthesis": "synthesis"}
)

graph.add_edge("security", "synthesis")
graph.add_edge("performance", "synthesis")
graph.add_edge("synthesis", END)

main_graph = graph.compile()

@app.get("/health")
def health_checker():
    return {"Hello world"}

@app.post("/review")
async def code_review(code: Code):
    initial_state: State = {
        "raw_code": code.code_snippet,
        "language": code.language,
        "context": code.context,
        "detected_issues": [],
        "agent_feedback": {},
        "route_decision": RouteDecision.SKIP
    }
    print(initial_state)
    res = await main_graph.ainvoke(initial_state)
    print("RESPONNNNNSEEE")
    print(res)
    return {"report": res.get("final_report", {}), "issues": res.get("detected_issues", [])}

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