# SmartPy Code
import smartpy as sp

Constants = sp.io.import_script_from_url("file:contracts/lib/constants.py")
CommonLib = sp.io.import_script_from_url("file:contracts/lib/CommonLib.py")
LoanNoteLib = sp.io.import_script_from_url("file:contracts/loan_note.py")
FA2Lib = sp.io.import_script_from_url("file:contracts/lib/FA2Lib.py")
CollateralVaultLib = sp.io.import_script_from_url(
    "file:contracts/collateral_vault.py")


class LoanCore(CommonLib.Ownable):
    def __init__(self, owner):
        CommonLib.Ownable.__init__(self, owner)

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

        collateral_vault = sp.contract(CollateralVaultLib.Deposit.get_type(),
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

        # Issue borrower and lender notes.
        self.issue_borrower_note(borrower, self.data.loan_id)
        self.issue_lender_note(lender, self.data.loan_id)
        
        self._increment_loan_id()

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
        self._onlyOwner()
        sp.verify(new_processing_fee < 250, "INVALID_FEE")

        self.data.processing_fee = new_processing_fee

    @sp.entry_point
    def whitelist_currency(self, currency, precision):
        sp.set_type(currency, sp.TAddress)
        sp.set_type(precision, sp.TNat)

        self._onlyOwner()
        self.data.permitted_currencies[currency] = True
        self.data.currency_precision[currency] = precision

    @sp.entry_point
    def set_collateral_vault(self, collateral_vault_address):
        sp.set_type(collateral_vault_address, sp.TAddress)
        self._onlyOwner()
        self.data.collateral_vault_address = collateral_vault_address

    @sp.entry_point
    def set_loan_note_contracts(self, borrower_note_address, lender_note_address):
        sp.set_type(lender_note_address, sp.TAddress)
        sp.set_type(borrower_note_address, sp.TAddress)

        self._onlyOwner()

        # A sequence of further verifications are required here.

        self.data.lender_note_address = lender_note_address
        self.data.borrower_note_address = borrower_note_address

    def issue_borrower_note(self, borrower, loan_id):
        sp.set_type(borrower, sp.TAddress)
        LoanNoteLib.Mint.execute(
            self.data.borrower_note_address, loan_id, borrower)

    def issue_lender_note(self, lender, loan_id):
        sp.set_type(lender, sp.TAddress)
        LoanNoteLib.Mint.execute(
            self.data.lender_note_address, loan_id, lender)

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

    def _increment_loan_id(self):
        self.data.loan_id += 1

    def get_initial_storage(self):
        storage = {}
        storage["loan_id"] = sp.nat(0)
        storage['processing_fee'] = sp.nat(0)

        storage["collateral_vault_address"] = Constants.NULL_ADDRESS
        storage["borrower_note_address"] = Constants.NULL_ADDRESS
        storage["lender_note_address"] = Constants.NULL_ADDRESS

        storage['permitted_currencies'] = sp.big_map(
            tkey=sp.TAddress, tvalue=sp.TBool)
        storage['currency_precision'] = sp.big_map(
            tkey=sp.TAddress, tvalue=sp.TNat)

        return storage


sp.add_compilation_target(
    "loan_core",
    LoanCore(owner=Constants.NULL_ADDRESS)
)
