# SmartPy Code
import smartpy as sp

Constants = sp.io.import_script_from_url("file:contracts/lib/constants.py")
LendingNoteLib = sp.io.import_script_from_url("file:contracts/LendingNote.py")
FA2Lib = sp.io.import_script_from_url("file:contracts/lib/FA2Lib.py")
CollateralVault = sp.io.import_script_from_url(
    "file:contracts/CollateralVault.py")


class LoanCore(LendingNoteLib.LendingNote):
    def __init__(self, admin, metadata):
        LendingNoteLib.LendingNote.__init__(self, admin, metadata)

        self.update_initial_storage(**self.get_initial_storage())

    @sp.entry_point
    def start_loan(
        self,
        lender,
        borrower,
        loan_denomination_contract,
        loan_denomination_id,
        loan_principal_amount,
        collateral_contract,
        collateral_token_id,
        # _loan_duration,
    ):
        # Type checks.
        sp.set_type(lender, sp.TAddress)
        sp.set_type(borrower, sp.TAddress)
        sp.set_type(loan_denomination_contract, sp.TAddress)
        sp.set_type(loan_principal_amount, sp.TNat)
        sp.set_type(loan_denomination_id, sp.TNat)

        # Verify that the call is coming from the origination controller.

        # Verify that the currency is permitted
        self.verify_permitted_currency(loan_denomination_contract)

        # Write loan to contract storage.

        # Transfer collateral to the collateral vault.

        collateral_vault = sp.contract(CollateralVault.Deposit.get_type(),
                                       self.data.collateral_vault_address,
                                       entry_point='deposit').open_some()

        # payload = sp.record(asset_contract_address=asset_contract_address,
        #                     asset_token_id=asset_token_id, recipient=sp.sender)

        payload = sp.record(depositor=borrower, collateral_contract=collateral_contract,
                            collateral_token_id=collateral_token_id, amount=1, deposit_id=1)

        sp.transfer(payload, sp.mutez(0), collateral_vault)

        # Transfer loan amount to the contract
        self.transfer_funds(lender,
                            sp.self_address,
                            loan_denomination_contract,
                            loan_denomination_id,
                            loan_principal_amount
                            )

        # Calculate the processing fee.
        processing_fee = self.compute_processing_fee(
            loan_principal_amount,
            self.data.currency_precision[loan_denomination_contract]
        )

        # Calculate loan amount net of processing fee
        net_loan_amount = sp.as_nat(loan_principal_amount - processing_fee)

        # Transfer net loan amount to the borrower.
        self.transfer_funds(sp.self_address,
                            borrower,
                            loan_denomination_contract,
                            loan_denomination_id,
                            net_loan_amount
                            )

        # Issue a transferable lending note to the lender.
        self.issue_lending_note(lender)

        # Emits an event

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
        self.data.permitted_currencies[currency] = True
        self.data.currency_precision[currency] = precision

    @sp.entry_point
    def set_collateral_vault(self, collateral_vault_address):
        sp.set_type(collateral_vault_address, sp.TAddress)
        sp.verify(self.is_administrator(sp.sender), "NOT_ADMIN")
        self.data.collateral_vault_address = collateral_vault_address

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

    def verify_permitted_currency(self, currency):
        sp.verify(self.data.permitted_currencies.contains(
            currency) == True, "CURRENCY_NOT_AUTHORIZED")

    def compute_processing_fee(self, loan_amount, currency_precision):
        sp.set_type(loan_amount, sp.TNat)
        sp.set_type(currency_precision, sp.TNat)

        return self.apply_percentage(loan_amount, self.data.processing_fee, currency_precision)

    def apply_percentage(self, base_amount, basis_points, precision):
        sp.set_type(base_amount, sp.TNat)
        sp.set_type(basis_points, sp.TNat)
        sp.set_type(precision, sp.TNat)

        multiplier = (basis_points * precision) / Constants.BASIS_POINT_DIVISOR
        return ((base_amount * multiplier) // precision)

    def get_initial_storage(self):
        storage = {}
        storage['processing_fee'] = sp.nat(0)

        storage["collateral_vault_address"] = Constants.NULL_ADDRESS

        storage['permitted_currencies'] = sp.big_map(
            tkey=sp.TAddress, tvalue=sp.TBool)
        storage['currency_precision'] = sp.big_map(
            tkey=sp.TAddress, tvalue=sp.TNat)

        return storage


sp.add_compilation_target(
    "LoanCore",
    LoanCore(
        admin=sp.address("tz1YtuZ4vhzzn7ssCt93Put8U9UJDdvCXci4"),
        metadata=sp.utils.metadata_of_url("http://example.com")
    )
)
