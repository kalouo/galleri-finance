# SmartPy Code
from lib2to3.pgen2 import token
import smartpy as sp

Constants = sp.io.import_script_from_url("file:contracts/lib/constants.py")
LendingNoteLib = sp.io.import_script_from_url("file:contracts/LendingNote.py")
FA2Lib = sp.io.import_script_from_url("file:contracts/lib/FA2Lib.py")


class LoanCore(LendingNoteLib.LendingNote):
    def __init__(self, admin, metadata):
        LendingNoteLib.LendingNote.__init__(self, admin, metadata)

        self.update_initial_storage(**self.get_initial_storage())

    @sp.entry_point
    def startLoan(self, lender, borrower, loanCurrency, tokenId, amount):
        # Type checks.
        sp.set_type(lender, sp.TAddress)
        sp.set_type(borrower, sp.TAddress)
        sp.set_type(loanCurrency, sp.TAddress)
        sp.set_type(amount, sp.TNat)
        sp.set_type(tokenId, sp.TNat)

        # Verify that the call is coming from the origination controller.

        # Write loan to contract storage.

        # Transfer collateral to the collateral vault.

        # Transfer loan amount to the borrower (net of fees)
        self.transfer_funds(lender, borrower, loanCurrency, tokenId, amount)

        # Issue a transferable lending note to the lender.
        self.issue_lending_note(lender)

        # Transfer loan to borrower

        # Emits an event
        None

    @sp.entry_point
    def repay(self):
        None

    @sp.entry_point
    def claim(self):
        None

    def issue_lending_note(self, lender):
        sp.set_type(lender, sp.TAddress)
        self.mint([LendingNoteLib.MintArg.make(lender)])

    def transfer_funds(self, _from, _to, _currency, _tokenId, _amount):
        sp.set_type(_from, sp.TAddress)
        sp.set_type(_to, sp.TAddress)
        sp.set_type(_currency, sp.TAddress)
        sp.set_type(_amount, sp.TNat)
        sp.set_type(_tokenId, sp.TNat)

        FA2Lib.Transfer.execute(_currency, _from, _to, _tokenId, _amount)

    def get_initial_storage(self):
        storage = {}

        return storage


sp.add_compilation_target(
    "LoanCore",
    LoanCore(
        admin=sp.address("tz1YtuZ4vhzzn7ssCt93Put8U9UJDdvCXci4"),
        metadata=sp.utils.metadata_of_url("http://example.com")
    )
)
