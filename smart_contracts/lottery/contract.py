# pyright: reportMissingModuleSource=false
from algopy import (
    Global,
    Txn,
    UInt64,
    arc4,
    gtxn,
    itxn,
    Account,
    ARC4Contract,
)

# We want the methods in our contract to follow the ARC4 standard
class Lottery(ARC4Contract):
    # The minimum entry fee to join the lottery
    entry_fee: UInt64
    
    # To keep track of the total number of participants
    total_entries: UInt64
    
    # Creator's address for managing the lottery
    creator_address: Account

    @arc4.abimethod(
        allow_actions=["NoOp"],
        create="require",
    )
    def create_application(
        self,
        entry_fee: UInt64,  # The entry fee required to participate in the lottery
    ) -> None:
        """
        Initialize the lottery contract with an entry fee.
        """
        # Initialize the entry fee and creator address in the contract's state
        self.entry_fee = entry_fee
        self.creator_address = Global.creator_address
        self.total_entries = UInt64(0)  # Initialize the total number of entries to 0

    @arc4.abimethod
    def enter_lottery(self, payment_txn: gtxn.PaymentTransaction) -> None:
        """
        Allow users to enter the lottery by sending the entry fee.
        """
        # Ensure that the payment is sent to the application address
        assert payment_txn.receiver == Global.current_application_address
        
        # # Ensure that the payment amount(microalgo) is equal to the entry fee
        assert payment_txn.amount == self.entry_fee
        
        self.total_entries += UInt64(1)
        
    @arc4.abimethod
    def pick_winner(self) ->None:
        """
        Allows the contract creator to randomly pick a winner.
        """
        # # Ensure that only the creator can call this function
        assert Txn.sender == self.creator_address

        # Ensure there is at least one participant
        assert self.total_entries > UInt64(0)

        # Simple pseudo-random number generator using round and index
        round_number = Global.round
        group_size = Global.group_size

        # Calculate pseudo-random index based on round number and group size
        random_number = round_number % self.total_entries

        # Get the winner's address from the transaction at the calculated index
        winner_index = random_number % group_size
        winner_address = gtxn.Transaction(winner_index).sender

        # itxn.fee(UInt64(1000))
        # Transfer all ALGOs collected to the winner
        itxn.Payment(
            amount=Global.current_application_address.balance - UInt64(100_00_00),
            receiver=winner_address,
            fee=1000
        ).submit()

    @arc4.abimethod(
        allow_actions=["DeleteApplication"]
    )
    def delete_application(self) -> None:
        """
        Allows the creator to delete the application.
        """
        # Only allow the creator to delete the application
        assert Txn.sender == self.creator_address

        # Send the remaining balance to the creator
        itxn.Payment(
            receiver=self.creator_address,
            amount=0,
            close_remainder_to=self.creator_address,
            fee=1000
        ).submit()

