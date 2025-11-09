from state import State 
from llm import llm 
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from state import RouteDecision 

def router(state: State) -> State:
    code_snippet = state['raw_code']
    language = state.get("language", "") 
    context = state.get("context", "") 

    router_prompt = ChatPromptTemplate.from_template(
        """You are a code router. Given code: {code}
        Language (if known): {language}
        Context: {context}

        1. Detect language if unknown (python/js/etc.).
        2. Flag quick issues: syntax errors, obvious security (e.g., eval()), perf risks (e.g., nested loops).
        Respond ONLY in JSON: {{"language": "str", "detected_issues": [{{"type": "str", "severity": "low/med/high"}}], "route": "full_review|syntax_only|security_first|skip"}}
        """
    )

    chain = router_prompt | llm | JsonOutputParser()
    response = chain.invoke({
        "code": code_snippet,
        "language": language,
        "context": context
    })

    print(response["language"])
    print(response["detected_issues"])

    try:
        route_value = response["route"]
        state["route_decision"] = RouteDecision(route_value)
        print(state["route_decision"])
    except ValueError:
        state["route_decision"] = RouteDecision.SKIP
        print("Fallback route: SKIP")

    if "error" in state["raw_code"][:100].lower():
        state["route_decision"] = RouteDecision.SYNTAX_ONLY

    state["language"] = response["language"]
    state["detected_issues"] = response["detected_issues"]

    return state