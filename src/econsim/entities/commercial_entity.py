from decimal import Decimal

from src.econsim.entities.actor_entity import ActorEntity, RciType


class CommercialEntity(ActorEntity):
    def __init__(self, id: int, lot_address: int, monthly_wage: float):
        super().__init__(name=f"CommercialEntity_{id}")
        self.id = id
        self.rci_type: RciType = RciType.COMMERCIAL
        self.jobs = 10

        self.lot_address: int = lot_address
        self.stock = 1000
        self.stock_capacity = 1000
        self.stock_price_per_unit = 1.0
        self.employee_wage = monthly_wage / 28
        self.tax_owed = Decimal('0')