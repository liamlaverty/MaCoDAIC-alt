
"""
Bank and account structures for the RCI economy simulation (for use in `economy-rci-jun.ipynb`)
 
Performance notes:
    - transfer() takes BankAccount objects. Keep a reference on each entity
      (entity.account) so that the hot path does no dictionary lookups.
    - Each transfer updates an aggregated flow matrix, keyed by
      (sender_type, receiver_type, purpose). This replaces one log object per
      transfer. The flow matrix is also the data for a MONIAC-style display.
    - Totals for each owner type are kept up to date on each transfer, so
      sum_all_accounts() is O(number of owner types), not O(number of accounts).
    - The full per-transfer log is optional (keep_transaction_log=True). It
      stores plain tuples with the simulation day, not objects with uuid4()
      and datetime.now().
"""
import uuid
from collections import defaultdict
from decimal import Decimal
 
from exceptions.not_enough_money_error import NotEnoughMoneyError
 
 
class BankAccount:
    __slots__ = ('balance', 'owner_id', 'owner_type')
 
    def __init__(self, owner_id: uuid.UUID, owner_type: str, initial_balance: Decimal = Decimal(0)):
        self.balance = initial_balance
        self.owner_id = owner_id
        self.owner_type = owner_type
 
 
class Bank:
    def __init__(self, keep_transaction_log: bool = False):
        self.accounts_by_owner: dict[uuid.UUID, BankAccount] = {}
        self.totals_by_type: dict[str, Decimal] = defaultdict(Decimal)
        # (sender_type, receiver_type, purpose) -> [total_amount, transfer_count]
        self.flows: dict[tuple[str, str, str], list] = {}
        self.keep_transaction_log = keep_transaction_log
        # (day, sender_id, receiver_id, purpose, amount)
        self.transaction_log: list[tuple] = []
        self.day = 0
 
    # ---- accounts -----------------------------------------------------------
 
    def create_account(self, owner, initial_balance: Decimal = Decimal(0)) -> BankAccount:
        """
        Create an account for owner, and attach it to the owner as owner.account.
        """
        if owner.id_uuid in self.accounts_by_owner:
            raise ValueError(f'Account already exists for owner {owner.name} (UUID: {owner.id_uuid})')
        account = BankAccount(owner.id_uuid, type(owner).__name__, initial_balance)
        self.accounts_by_owner[owner.id_uuid] = account
        self.totals_by_type[account.owner_type] += initial_balance
        owner.account = account
        return account
 
    def get_account_by_owner(self, owner: uuid.UUID) -> BankAccount:
        account = self.accounts_by_owner.get(owner)
        if account is None:
            raise ValueError(f'No account found for owner {owner}')
        return account
 
    def get_balance(self, owner: uuid.UUID) -> Decimal:
        """Compatibility wrapper. In hot loops, read entity.account.balance."""
        return self.get_account_by_owner(owner).balance
 
    def sum_all_accounts(self, entity_type: str | None = None) -> Decimal:
        if entity_type is None:
            return sum(self.totals_by_type.values(), Decimal(0))
        return self.totals_by_type.get(entity_type, Decimal(0))
 
    # ---- transfers ----------------------------------------------------------
 
    def transfer(self, sender: BankAccount, receiver: BankAccount,
                 amount: Decimal, for_good_service: str) -> None:
        """
        Move amount from sender to receiver. This is the hot path.
 
        Raises:
            - ValueError: If amount is negative.
            - NotEnoughMoneyError: If the sender does not have enough money.
        """
        if amount < 0:
            raise ValueError(f'Transfer amount must not be negative: {amount}')
        if sender.balance < amount:
            raise NotEnoughMoneyError(
                f'Sender {sender.owner_id} does not have enough money to transfer {amount}. '
                f'Current balance: {sender.balance}')
 
        sender.balance -= amount
        receiver.balance += amount
 
        s_type = sender.owner_type
        r_type = receiver.owner_type
        if s_type != r_type:
            totals = self.totals_by_type
            totals[s_type] -= amount
            totals[r_type] += amount
 
        key = (s_type, r_type, for_good_service)
        flow = self.flows.get(key)
        if flow is None:
            self.flows[key] = [amount, 1]
        else:
            flow[0] += amount
            flow[1] += 1
 
        if self.keep_transaction_log:
            self.transaction_log.append(
                (self.day, sender.owner_id, receiver.owner_id, for_good_service, amount))
 
    def transfer_money(self, sender: uuid.UUID, receiver: uuid.UUID,
                       amount: Decimal, for_good_service: str) -> None:
        """Compatibility wrapper for the old UUID-based call sites."""
        self.transfer(self.get_account_by_owner(sender),
                      self.get_account_by_owner(receiver),
                      amount, for_good_service)
 
    # ---- reporting ----------------------------------------------------------
 
    def take_flows(self) -> dict[tuple[str, str, str], list]:
        """
        Return the flow matrix for the period, and start a new one.
        Call this at the end of each month (or day) and store the result in history.
        """
        flows, self.flows = self.flows, {}
        return flows
 
    def check_totals(self) -> None:
        """
        Debug check: recalculate the totals from all accounts and compare them
        with the running totals. Do not call this in the hot path.
        """
        actual = defaultdict(Decimal)
        for account in self.accounts_by_owner.values():
            actual[account.owner_type] += account.balance
        for owner_type, total in actual.items():
            if self.totals_by_type[owner_type] != total:
                raise AssertionError(
                    f'Running total for {owner_type} is {self.totals_by_type[owner_type]}, actual is {total}')
 

