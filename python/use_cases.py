from datetime import datetime

from entities import Segment, SegmentId
from exceptions import SegmentNotFoundError
from repositories import SegmentRepository


class ListSegments:
    def __init__(self, repository: SegmentRepository):
        self.repository = repository

    def execute(self, limit: int = 100) -> list[Segment]:
        return self.repository.list_segments(limit = limit)

class GetSegment:
    def __init__(self, repository: SegmentRepository):
        self.repository = repository


    def execute(self, segment_id: int) -> Segment:
        segment = self.repository.get_by_id(SegmentId(segment_id))

        if segment is None:
            raise SegmentNotFoundError(f"Segment {segment_id} not found")

        return segment


class FindStaleSegments:
    def __init__(self, repository: SegmentRepository):
        self.repository = repository

    def execute
