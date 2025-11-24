from datetime import datetime
from typing import List, Optional, Dict, Any

from pydantic import BaseModel


class StatsResponse(BaseModel):
    endpoint: str
    parameters: Dict[str, Any]
    total_calls: int
    last_called: Optional[datetime]
