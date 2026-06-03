

from decimal import Decimal

from models.enums import CompetitionModel


class WholesalerConfig:
    name: str = 'Orange Wholesaler'
    price: Decimal = Decimal('10.0')
    initial_stock: int = 100


class RetailerConfig:
    def __init__(self,
                 num_retailers: int = 5,
                 starting_money: Decimal = Decimal('200.0'),
                 competition_model: CompetitionModel = CompetitionModel.BERTRAND):
        self.num_retailers = num_retailers
        self.starting_money = starting_money
        self.competition_model = competition_model
    

class ConsumerConfig:
    num_consumers: int = 100
    earns_per_iteration: Decimal = Decimal('100.0')
