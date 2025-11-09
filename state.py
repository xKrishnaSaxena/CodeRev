from typing import  TypedDict,List,Dict,Any
from enum import Enum
class RouteDecision(str,Enum):
    FULL_REVIEW="full_review"
    SYNTAX_ONLY="syntax_only"
    SECURITY_FIRST="security_first"
    SKIP="skip"

class State(TypedDict):
    raw_code: str
    language: str
    context: str
    detected_issues: List[Dict[str, Any]] 
    agent_feedback: Dict[str, Any]         
    route_decision: RouteDecision          
    final_report: Dict[str, Any]