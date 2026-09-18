from src.econsim.banking.bank import Bank
from decimal import Decimal


def assert_money_conserved(bank: Bank, expected_total: Decimal, day: int) -> None:
    """
    Assert that the money in the central bank exactly matches the expected total.

    Args:
        - bank (Bank): The central bank whose total money is to be checked.
        - expected_total (Decimal): The expected total amount of money in the bank.
        - day (int): The current simulation day.
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


def assert_account_count_match_entity_count(bank: Bank, fixed_entities: list, entity_lists: list[list], day: int) -> None:
    """
    Assert that the number of accounts in the bank matches the number of unique entities.

    Args:
        - bank (Bank): The central bank whose accounts are to be checked.
        - fixed_entities (list): A list of entities that should always have accounts.
        - entity_lists (list[list]): A list of lists of entities that should have accounts.
        - day (int): The current simulation day.
    Raises:
        - AssertionError: If there is a mismatch between accounts and entities.
    """
    expected = {e.id_uuid for e in fixed_entities}
    total_listed = len(fixed_entities)
    for entities in entity_lists:
        expected.update(e.id_uuid for e in entities)
        total_listed += len(entities)
    if len(expected) != total_listed:
        raise AssertionError(f'Day {day}: an entity is in the entity lists more than once.')
    actual = set(bank.accounts_by_owner)
    if actual != expected:
        raise AssertionError(f'Day {day}: {len(actual - expected)} accounts have no entity, '
                             f'{len(expected - actual)} entities have no account.')