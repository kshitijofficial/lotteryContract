import pytest
from collections.abc import Generator

from smart_contracts.lottery.contract import Lottery
from algopy_testing import AlgopyTestContext, algopy_testing_context
import algopy
from algopy import (
    UInt64,
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
    contract = Lottery()
    ledger = context.ledger
    entry_fee = UInt64(100_00_000)
    app_id = context.ledger.get_app(contract)
    # Create accounts for creator and participants
    creator_account = context.default_sender
    participant_account_1 = context.any.account()
    participant_account_2 = context.any.account()

    ledger.update_account(creator_account, min_balance=10_00_000,balance=1_00_000)
    ledger.update_account(participant_account_2, min_balance=10_00_000,balance=1_00_000)
    ledger.update_account(participant_account_1, min_balance=10_00_000,balance=10_00_000)
    
    print(f"Balance for account 1 after commit:", participant_account_1.balance)
    print(f"Balance for account 2 after commit:", participant_account_2.balance)

    assert participant_account_1.balance == participant_account_2.balance
   
    #assert participant_account_1.balance == participant_account_2.balance
    with context.txn.create_group(
        gtxns=[
            context.any.txn.application_call(
                sender=creator_account,
                app_id=app_id,
                app_args=[algopy.Bytes(b"create_application"), entry_fee],
            ),
            context.any.txn.payment(
                sender=participant_account_1,
                receiver=app_id.address,
                amount=entry_fee,
            ),
            context.any.txn.payment(
                sender=participant_account_2,
                receiver=app_id.address,
                amount=entry_fee,
            )
        ],
        active_txn_index=0,
    ):contract.create_application(entry_fee)

    # Participants enter the lottery
    contract.enter_lottery(payment_txn=context.any.txn.payment(
        sender=participant_account_1,
        receiver=app_id.address,
        amount=entry_fee,
    ))
    contract.enter_lottery(payment_txn=context.any.txn.payment(
        sender=participant_account_2,
        receiver=app_id.address,
        amount=entry_fee,
    ))
  
   

    # # Act: Pick a winner
    # with context.txn.create_group(
    #     gtxns=[
    #         context.any.txn.application_call(
    #             sender=creator_account,
    #             app_id=app_id,
    #             app_args=[algopy.Bytes(b"pick_winner")],
    #         )
    #     ]
    # ):contract.pick_winner()

    # Assert that one of the participants received 1 ALGO (less fees), while the application keeps 1 ALGO


def test_delete_application():
    pass
