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
    def start_loan(self, lender, borrower, currency, tokenId, amount):
        # Type checks.
        sp.set_type(lender, sp.TAddress)
        sp.set_type(borrower, sp.TAddress)
        sp.set_type(currency, sp.TAddress)
        sp.set_type(amount, sp.TNat)
        sp.set_type(tokenId, sp.TNat)

        # Verify that the call is coming from the origination controller.

        # Verify that the currency is whitelisted
        self.verify_whitelisted_currency(currency)

        # Write loan to contract storage.

        # Transfer collateral to the collateral vault.

        # Transfer loan amount to the contract
        self.transfer_funds(lender, sp.self_address, currency, tokenId, amount)

        # Calculate loan amount net of processing fee.
        precision = self.data.whitelisted_currencies[currency]
        processing_fee = self.compute_processing_fee(amount, precision)
        net_amount = sp.as_nat(amount - processing_fee)

        # Transfer net loan amount to the borrower.
        self.transfer_funds(sp.self_address, borrower,
                            currency, tokenId, net_amount)

        # Issue a transferable lending note to the lender.
        self.issue_lending_note(lender)

        # Emits an event
        None

    @sp.entry_point
    def repay(self):
        None

    @sp.entry_point
    def claim(self):
        None

    @sp.entry_point
    def set_processing_fee(self, new_processing_fee):
        sp.set_type(new_processing_fee, sp.TNat)
        sp.verify(self.is_administrator(sp.sender), "NOT_ADMIN")
        sp.verify(new_processing_fee < 250, "INVALID_FEE")

        self.data.processing_fee = new_processing_fee

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

    def compute_processing_fee(self, loan_amount, currency_precision):
        sp.set_type(loan_amount, sp.TNat)
        sp.set_type(currency_precision, sp.TNat)

        return self.split_tokens(loan_amount, self.data.processing_fee, currency_precision)

    def split_tokens(self, base_amount, basis_points, precision):
        sp.set_type(base_amount, sp.TNat)
        sp.set_type(basis_points, sp.TNat)
        sp.set_type(precision, sp.TNat)

        multiplier = (basis_points * precision) / Constants.BASIS_POINT_DIVISOR
        return ((base_amount * multiplier) // precision)

    def get_initial_storage(self):
        storage = {}
        storage['processing_fee'] = sp.nat(0)
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
