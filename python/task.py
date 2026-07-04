from enum import Enum
from datetime import datetime, timedelta 

from dataclasses import dataclass, field
from uuid import UUID, uuid4
from typing import Optional
from entity import Entity

class TaskStatus(Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"


class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

# frozen = True makes this immutable as it should be for a value object
@dataclass(frozen = True)
                    
@dataclass
class Task(Entity):
    """
    Let's implement our core domain entity. This entity will encapsulate
    the fundamental concepts and rules related to tasks in our task
    management system
    """
    title: str  # A concise name for the task 
    
    description: str # A detailed explanation of the task, providing context and information for the user 
    due_date: Optional[Deadline] = None 
    priority: Priority = Priority.MEDIUM
    status: TaskStatus = field(default = TaskStatus.PENDING, init = False)
    
