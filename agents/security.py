from state import State
from llm import llm
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
import vector_store

def security(state: State) -> State:
    raw_code = state['raw_code']
    language = state.get('language', '')
    detected_issues = state.get("detected_issues", [])

    prior_types = [issue.get('type', 'unknown') for issue in detected_issues[:2]]
    query = f"secure coding patterns for {language} to prevent {', '.join(prior_types)} (OWASP Top 10)"
    rag_docs = vector_store.retriever.invoke(query)
    rag_context = "\n".join([doc.page_content for doc in rag_docs])
    security_prompt = ChatPromptTemplate.from_template(
        """You are a Security Agent scanning for vulnerabilities.
        Code: {code}
        Language: {language}
        Prior issues: {prior_issues}
        RAG context (OWASP best practices): {rag_context}

        1. Detect risks: SQL/JS injection, hard-coded secrets, unsafe deserialization.
        2. Prioritize OWASP Top 10 and reference RAG examples in suggestions.

        Respond ONLY in JSON: {{"issues": [{{"type": "str e.g. injection", "line": int, "description": "str", "severity": "low/med/high", "suggestion": "str with fix example"}}], "risk_score": 0-10}}
        """
    )
    chain = security_prompt | llm | JsonOutputParser()
    prior_str = [f"{issue.get('type', 'unknown')}: {issue.get('description', 'N/A')}" for issue in detected_issues]
    response = chain.invoke({
        "code": raw_code,
        "language": language,
        "prior_issues": prior_str,
        "rag_context": rag_context
    })
    agent_feedback = state.get("agent_feedback", {})
    agent_feedback["security"] = response
    state["agent_feedback"] = agent_feedback

    detected_issues = state.get("detected_issues", [])
    if "issues" in response:
        for issue in response["issues"]:
            if "type" not in issue:
                issue["type"] = "security_vuln"
        detected_issues.extend(response["issues"])
    state["detected_issues"] = detected_issues

    return state