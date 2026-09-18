from decimal import Decimal

from src.econsim.entities.actor_entity import ActorEntity, RciType


class IndustrialEntity(ActorEntity):
    def __init__(self, id: int, lot_address: int, monthly_wage: float):
        super().__init__(name=f"IndustrialEntity_{id}")
        self.id = id
        self.rci_type: RciType = RciType.INDUSTRIAL
        self.jobs = 100
        self.employee_wage = monthly_wage / 28
        self.lot_address: int = lot_address

        self.stock = 1000
        self.stock_capacity = 1000
        self.stock_price_per_unit = 0.5
        self.stock_regeneration_rate = 0.1 # 10% of stock capacity per day
        self.tax_owed = Decimal('0')