import enum
import uuid

from src.econsim.banking.bank import BankAccount


class ActorEntity:
    name: str
    id_uuid: uuid.UUID
    account: 'BankAccount'  # Forward reference to avoid circular import issues
    
    def __init__(self, name: str):
        self.name = name
        self.id_uuid = uuid.uuid4()


class RciType(enum.Enum):
    RESIDENTIAL = 0
    COMMERCIAL = 1
    INDUSTRIAL = 2