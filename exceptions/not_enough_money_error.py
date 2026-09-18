class NotEnoughMoneyError(Exception):
    """Raised when an operation is attempted but there is not enough money in the account."""
    pass