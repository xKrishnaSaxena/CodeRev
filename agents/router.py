from state import State
from llm import llm

def router(state:State):
    code_snippet=state['raw_code']
    language=state['language']
    context=state['context']
    prompt = f"""You are a code router. Given code: {code_snippet}
    Language (if known): {language}
    Context: {context}

    1. Detect language if unknown (python/js/etc.).
    2. Flag quick issues: syntax errors, obvious security (e.g., eval()), perf risks (e.g., nested loops).
    Respond ONLY in JSON: "language": "str", "detected_issues": ["type": "str", "severity": "low/med/high"], "route": "full_review|syntax_only|security_first|skip"""

    response=llm.invoke(prompt)
    print(response)
    return response