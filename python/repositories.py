from typing import Protocol
from entities import Segment, SegmentId


class SegmentRepository(Protocol):
    """
    Applying the dependency inversion principle, we define a repository interface that abstracts the data layer 
    """
    def get_by_id(self, segment_id: SegmentId) -> Segment | None:
        ...
    def list_segments(self, limit: int = 100) -> list[Segment]:
        ...
    def save(self, segment: Segment) -> None:
        ...
    
    
        
