from state import State
from llm import llm
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from vector_store import retriever

def performance(state: State) -> State:
    raw_code = state['raw_code']
    language = state.get('language', '')
    detected_issues = state.get("detected_issues", [])

    prior_types = [issue.get('type', 'unknown') for issue in detected_issues[:2]]
    query = f"performance optimizations for {language} code: Big-O analysis, efficient data structures for {', '.join(prior_types)}"
    rag_docs = retriever.get_relevant_documents(query)
    rag_context = "\n".join([doc.page_content for doc in rag_docs])

    performance_prompt = ChatPromptTemplate.from_template(
        """You are a Performance Agent optimizing code efficiency.
        Code: {code}
        Language: {language}
        Prior issues: {prior_issues}
        RAG context (Big-O guides): {rag_context}

        1. Estimate Big-O (time/space).
        2. Flag bottlenecks: nested loops, inefficient data structures.
        3. Suggest refactors (e.g., use dict instead of list search) referencing RAG examples.

        Respond ONLY in JSON: {{"issues": [{{"type": "str e.g. O(n^2)", "description": "str", "severity": "low/med/high", "suggestion": "str with optimized example", "complexity": "O(n)"}}], "perf_score": 0-10}}
        """
    )
    chain = performance_prompt | llm | JsonOutputParser()
    prior_str = [f"{issue.get('type', 'unknown')}: {issue.get('description', 'N/A')}" for issue in detected_issues]
    response = chain.invoke({
        "code": raw_code,
        "language": language,
        "prior_issues": prior_str,
        "rag_context": rag_context
    })
    agent_feedback = state.get("agent_feedback", {})
    agent_feedback["performance"] = response
    state["agent_feedback"] = agent_feedback

    detected_issues = state.get("detected_issues", [])
    if "issues" in response:
        for issue in response["issues"]:
            if "type" not in issue:
                issue["type"] = "perf_risk" 
        detected_issues.extend(response["issues"])
    state["detected_issues"] = detected_issues

    return state