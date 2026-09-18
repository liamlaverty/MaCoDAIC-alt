from src.econsim.banking.bank import Bank
from decimal import Decimal


def assert_money_conserved(bank: Bank, expected_total: Decimal, day: int) -> None:
    """
    Assert that the money in the central bank exactly matches the expected total.

    Args:
        - bank: The central bank whose total money is to be checked.
        - expected_total: The expected total amount of money in the bank.
        - day: The current simulation day.
    Raises:
        - AssertionError: If the total money in the bank does not match the expected total.
    """
    actual_total = bank.total_money()
    running_total = bank.sum_all_accounts()
    if running_total != actual_total:
        bank.debug_check_totals()
        raise AssertionError(
            f'Money conservation check failed on day {day}: '
            f'actual total {actual_total}, running total {running_total}, expected total {expected_total}')
    if actual_total != expected_total:
        raise AssertionError(
            f'Money conservation check failed on day {day}: '
            f'actual total {actual_total}, running total {running_total}, expected total {expected_total}')