import pytest
from collections.abc import Generator

from smart_contracts.lottery.contract import Lottery
from algopy_testing import AlgopyTestContext, algopy_testing_context
import algopy
from _algopy_testing.context_helpers.txn_context import TransactionContext, DeferredAppCall
from algopy.gtxn import PaymentTransaction
from algopy import (
    UInt64,
    Account,
    gtxn,
    Global
)

@pytest.fixture()
def context() -> Generator[AlgopyTestContext, None, None]:
    with algopy_testing_context() as ctx:
        yield ctx

def test_create_application(
    context: AlgopyTestContext,
) -> None:
    contract = Lottery()
    entery_fee = context.any.uint64()
    default_account = context.default_sender
    contract.create_application(entery_fee)
    
    assert contract.creator_address == default_account
    assert contract.entry_fee == entery_fee
    assert contract.total_entries == UInt64(0)

def test_enter_lottery(
    context: AlgopyTestContext,
) -> None:
    contract = Lottery()
    
    # Create the lottery application first
    entry_fee = UInt64(100_00_00)
    contract.create_application(entry_fee)
    
    # Now retrieve the app from the ledger
    test_app = context.ledger.get_app(contract)
   
    payment_txn=context.any.txn.payment(receiver=test_app.address, amount=entry_fee)

    # Call the enter_lottery method with the payment transaction
    contract.enter_lottery(payment_txn=payment_txn)
    
    assert contract.total_entries == UInt64(1)
    assert payment_txn.receiver == test_app.address
    assert payment_txn.amount == entry_fee

def test_pick_winner(context: AlgopyTestContext)->None:

    # Initialize the transaction context
    contract = Lottery()
    ledger = context.ledger
    entry_fee = UInt64(1_000_000)
    app_id = context.ledger.get_app(contract)
    # Create accounts for creator and participants
    creator_account = context.default_sender
    participant_account_1 = context.any.account()
    participant_account_2 = context.any.account()

    ledger.update_account(creator_account, min_balance=1_000_000,balance=100_000_000)
    ledger.update_account(participant_account_2, min_balance=1_000_000,balance=100_000_000)
    ledger.update_account(participant_account_1, min_balance=1_000_000,balance=100_000_000)
    
    contract.create_application(entry_fee)
    print(f"Entery after commit:", contract.entry_fee)

    payment_txn=context.any.txn.payment(receiver=app_id.address, amount=UInt64(1_000_00))

    # Call the enter_lottery method with the payment transaction
    contract.enter_lottery(payment_txn=payment_txn)
    
    print(f"Balance for contract after commit:", app_id.address.balance)
    print(f"Balance for account 1 after commit:", participant_account_1.balance)
    
    

# def test_delete_application():
#     pass
