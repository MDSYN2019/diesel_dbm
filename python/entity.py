from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class Entity:
    """
    This Entity base class provides a foundation for all our entities,
    ensuring that they have a unique identifier and appopriate equality
    and hashing behaviour

    This provides a template behaviour for all entities in our system
    
    """
    id: UUID = field(default_factory = uuid4)
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented

        return self.id == other.id
        
    def __hash__(self) -> int:
        return hash(self.id)

    

