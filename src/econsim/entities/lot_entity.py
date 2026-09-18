from src.econsim.entities.actor_entity import RciType


class LotEntity:
    def __init__(self, id: int, lot_type: RciType):
        self.id = id
        self.rci_type: RciType = lot_type
        self.occupied = False
        self.occupied_by: int | None = None