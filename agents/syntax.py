from state import State
from llm import llm
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
import vector_store

def syntax(state: State) -> State:
    raw_code = state['raw_code']
    language = state.get('language', '')
    detected_issues = state.get("detected_issues", [])

    prior_types = [issue.get('type', 'unknown') for issue in detected_issues[:2]]
    query = f"style guidelines for {language} code (e.g., PEP8 indentation, naming conventions)"
    rag_docs = vector_store.retriever.invoke(query)
    rag_context = "\n".join([doc.page_content for doc in rag_docs])

    syntax_prompt = ChatPromptTemplate.from_template(
        """You are a Syntax Agent reviewing code for errors and style.
        Code: {code}
        Language: {language}
        Prior issues: {prior_issues}
        RAG context (PEP8 guidelines): {rag_context}

        1. Check for syntax errors (e.g., unmatched braces, invalid imports).
        2. Flag style violations (e.g., indentation, naming conventions).
        3. Reference RAG for language-specific rules in suggestions.

        Respond ONLY in JSON: {{"issues": [{{"type": "syntax_error", "line": int, "description": "str", "severity": "low/med/high", "suggestion": "str"}}], "is_valid": true/false, "cleaned_code": "optional fixed snippet"}}
        """
    )
    chain = syntax_prompt | llm | JsonOutputParser()
    prior_str = [f"{issue.get('type', 'unknown')}: {issue.get('description', 'N/A')}" for issue in detected_issues]
    response = chain.invoke({
        "code": raw_code,
        "language": language,
        "prior_issues": prior_str,
        "rag_context": rag_context
    })
    agent_feedback = state.get("agent_feedback", {})
    agent_feedback["syntax"] = response
    state["agent_feedback"] = agent_feedback

    detected_issues = state.get("detected_issues", [])
    if "issues" in response:
        for issue in response["issues"]:
            if "type" not in issue:
                issue["type"] = "syntax_error"
        detected_issues.extend(response["issues"])
    state["detected_issues"] = detected_issues

    return state