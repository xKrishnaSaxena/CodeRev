from state import State
from llm import llm
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate

def synthesis(state: State) -> State:
    raw_code = state['raw_code']
    language = state.get('language', '')
    detected_issues = state.get("detected_issues", [])
    agent_feedback = state.get("agent_feedback", {})
    syntax_out = agent_feedback.get("syntax", {})
    security_out = agent_feedback.get("security", {})
    perf_out = agent_feedback.get("performance", {})

    synthesis_prompt = ChatPromptTemplate.from_template(
        """You are a Synthesis Agent compiling a code review report.
        Raw code: {code}
        Language: {language}
        All agent outputs:
        Syntax: {syntax_out}
        Security: {security_out}
        Performance: {perf_out}
        Prior issues: {all_issues}

        1. Merge/dedupe issues (group by type/line).
        2. Compute overall_score (0-100): Weight security (40%), perf (30%), syntax (30%).
        3. Generate concise report with top 5 issues and fixes.
        4. Optional: Provide full improved_code if fixes are simple.

        Respond ONLY in JSON: {{"overall_score": int, "top_issues": [{{"type": "str", "severity": "str", "description": "str", "suggestion": "str"}}], "report_summary": "str <200 words", "improved_code": "optional full snippet"}}
        """
    )
    chain = synthesis_prompt | llm | JsonOutputParser()
    all_issues_str = [f"{issue.get('type', 'unknown')}: {issue.get('description', 'N/A')}" for issue in detected_issues]
    response = chain.invoke({
        "code": raw_code,
        "language": language,
        "syntax_out": syntax_out,
        "security_out": security_out,
        "perf_out": perf_out,
        "all_issues": all_issues_str, 
    })
    state["final_report"] = response

    return state