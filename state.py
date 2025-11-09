from typing import  TypedDict,List,Dict,Any
from enum import Enum
class RouteDecision(str,Enum):
    FULL_REVIEW="full_review"
    SYNTAX_ONLY="syntax_only"
    SECURITY_FIRST="security_first"
    SKIP="skip"

class State(TypedDict):
    raw_code:str
    issues_list = List[Dict[str, Any]]
    agent_feedback=Dict[str, Any]
    route_decision=RouteDecision
    language:str
    context:str