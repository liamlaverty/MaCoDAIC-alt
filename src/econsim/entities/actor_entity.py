import enum
import uuid


class ActorEntity:
    name: str
    id_uuid: uuid.UUID
    
    def __init__(self, name: str):
        self.name = name
        self.id_uuid = uuid.uuid4()


class RciType(enum.Enum):
    RESIDENTIAL = 0
    COMMERCIAL = 1
    INDUSTRIAL = 2