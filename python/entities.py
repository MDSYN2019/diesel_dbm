from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen = True)
class SegmentId:
    """
    build a value object to represent the unique identifier for a segment 
    """
    value: int
    def __post_init__(self) -> None:
        if self.value <= 0:
            raise ValueError("SegmentId must be positive")
        
@dataclass(frozen = True)
class Segment:
    """
     This entity does not know about SQL rows, cursors, psycopg, Diesel, FastAPI, or
    anything external
    """    
    id: SegmentId
    name: str
    description: str
    created_at: datetime
    updated_at: datetime

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("Segment name cannot be empty")
        if not self.description.strip():
            raise ValueError("Segment description cannot be empty")

    def is_stale(self, cutoff: datetime) -> bool:
        return self.updated_at < cutoff

    
        
            
    
        
    
