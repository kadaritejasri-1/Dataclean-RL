from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Literal


class Observation(BaseModel):
    preview_rows: List[Dict[str, Any]]
    issues_summary: Dict[str, int]
    budget_remaining: int
    last_action_result: str


class Action(BaseModel):
    action_type: Literal[
        "fix_missing",
        "remove_duplicates",
        "convert_type",
        "normalize_text",
        "drop_row",
        "fill_default",
        "rename_column"
    ]
    row_id: Optional[int] = None
    column: Optional[str] = None
    value: Optional[Any] = None


class Reward(BaseModel):
    value: float
    reason: str