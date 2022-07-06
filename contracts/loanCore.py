# SmartPy Code
import smartpy as sp

Constants = sp.io.import_script_from_url("file:contracts/lib/constants.py")
LendingNoteLib = sp.io.import_script_from_url("file:contracts/LendingNote.py")
FA2Lib = sp.io.import_script_from_url("file:contracts/lib/FA2Lib.py")


class LoanCore(LendingNoteLib.LendingNote):
    def __init__(self, admin, metadata):
        LendingNoteLib.LendingNote.__init__(self, admin, metadata)

        self.update_initial_storage(**self.get_initial_storage())

    @sp.entry_point
    def start_loan(self, lender, borrower, loanCurrency, tokenId, amount):
        # Type checks.
        sp.set_type(lender, sp.TAddress)
        sp.set_type(borrower, sp.TAddress)
        sp.set_type(loanCurrency, sp.TAddress)
        sp.set_type(amount, sp.TNat)
        sp.set_type(tokenId, sp.TNat)

        # Verify that the call is coming from the origination controller.

        # Verify that the currency is whitelisted
        self.verify_whitelisted_currency(loanCurrency)
        # Write loan to contract storage.

        # Transfer collateral to the collateral vault.

        # Transfer loan amount to the contract
        self.transfer_funds(lender, sp.self_address,
                            loanCurrency, tokenId, amount)

        # Deduct fees and commissions
        # processing_fee = sp.ediv(token at precision x percentage at precision, precision)

        # Transfer loan amount to the borrower
        self.transfer_funds(sp.self_address, borrower,
                            loanCurrency, tokenId, amount)

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

    @sp.entry_point
    def whitelist_currency(self, currency, precision):
        sp.set_type(currency, sp.TAddress)
        sp.set_type(precision, sp.TNat)

        sp.verify(self.is_administrator(sp.sender), "NOT_ADMIN")
        self.data.whitelisted_currencies[currency] = precision

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

    def verify_whitelisted_currency(self, currency):
        sp.verify(self.data.whitelisted_currencies.contains(
            currency) == True, "CURRENCY_NOT_AUTHORIZED")

    def get_initial_storage(self):
        storage = {}
        storage['whitelisted_currencies'] = sp.big_map(
            tkey=sp.TAddress, tvalue=sp.TNat)

        return storage


sp.add_compilation_target(
    "LoanCore",
    LoanCore(
        admin=sp.address("tz1YtuZ4vhzzn7ssCt93Put8U9UJDdvCXci4"),
        metadata=sp.utils.metadata_of_url("http://example.com")
    )
)
