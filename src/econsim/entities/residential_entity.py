from decimal import Decimal

from src.econsim.entities.actor_entity import ActorEntity, RciType


class ResidentialEntity(ActorEntity):
    def __init__(self, id: int, lot_address: int):
        super().__init__(name=f"ResidentialEntity_{id}")
        self.id = id
        self.rci_type: RciType = RciType.RESIDENTIAL

        self.employed = False
        self.employed_at: int | None = None
        self.employed_type: RciType | None = None

        self.lot_address: int = lot_address

        # Per period consumption and utility tracking vars
        self.lifetime_utility = Decimal(0)
        self.basket_count = 0
        self.period_utility = Decimal(0)
        self.subsistence_q_met = False

        # Base utility is the utility of the initial unit of consumption before decay is applied.
        self.base_utility = Decimal(30.0)

        # utility_decay is a geometric decay factor for marginal utility of consumption
        self.utility_decay = Decimal(0.8)

    def marginal_utility(self, units_held: int) -> Decimal:
        """
        Calcualte utility of the next good consumed, based on geometric
        decay from base_utility

        Args:
            - units_held: The number of units already held by the resident.
        Returns:
            - The marginal utility of the next unit of consumption.
        """
        return self.base_utility * (self.utility_decay ** units_held)

    def willing_to_buy(self, price: Decimal) -> bool:
        """
        Determine if the resident is willing to buy a good at the given price.

        This follows a quasi-linear utility function, where the resident will
        consume if the next unit's MarginalUtility is greater than or equal to
        the price of the good.

        Args:
            - price: The price of the good to be purchased.
        Returns:
            - True if the resident is willing to buy, False otherwise.
        """
        return self.marginal_utility(self.basket_count) >= price