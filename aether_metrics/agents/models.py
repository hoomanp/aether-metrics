from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime

class AIUsageMetrics(BaseModel):
    user_id: str
    tool_name: str
    token_count: int
    task_category: str  # e.g., "code_gen", "test_gen", "refactor"
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class VelocityMetrics(BaseModel):
    team_id: str
    cycle_time_delta: float  # -10.5 means 10.5% improvement
    story_points_delivered: float
    ai_augmented_ratio: float  # Percentage of tasks involving AI tools

class CoverageMetrics(BaseModel):
    repository: str
    microservice: Optional[str] = None
    feature_name: str
    test_case_count: int
    line_coverage_pct: float
    uncovered_lines: List[int] = []

class A2AMessage(BaseModel):
    sender_id: str
    recipient_id: str
    request_type: str  # e.g., "GET_METRICS", "TRIGGER_TEST_GEN", "REPORT_DIP"
    payload: Dict
    priority: int = 1
