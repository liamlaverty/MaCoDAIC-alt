

from decimal import Decimal

from models.enums import CompetitionModel


class WholesalerConfig:
    name: str = 'Orange Wholesaler'
    price: Decimal = Decimal('10.0')
    initial_stock: int = 100


class RetailerConfig:
    num_retailers: int = 10
    starting_money: Decimal = Decimal('200.0')
    competition_model: CompetitionModel
    

class ConsumerConfig:
    num_consumers: int = 100
    earns_per_iteration: Decimal = Decimal('100.0')
