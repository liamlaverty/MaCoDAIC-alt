from src.econsim.entities.actor_entity import ActorEntity, RciType


class WholesalerEntity(ActorEntity):
    def __init__(self, id: int):
        super().__init__(name=f"WholesalerEntity_{id}")
        self.id = id
        self.rci_type: RciType = RciType.INDUSTRIAL

        self.stock = 1_000_000_000
        self.stock_capacity = 1_000_000_000
        self.stock_price_per_unit = 0.25