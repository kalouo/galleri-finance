# SmartPy Code
import smartpy as sp


def import_sp(file_path):
    return sp.io.import_script_from_url("file:" + file_path)


Constants = import_sp("contracts/lib/constants.py")

LibFA2 = import_sp("contracts/lib/FA2_lib.py")
LibCommon = import_sp("contracts/lib/common_lib.py")
LibLoanNote = import_sp("contracts/loan_note.py")
LibCollateralVault = import_sp("contracts/collateral_vault.py")


class LoanCore(LibCommon.Ownable):
    def __init__(self, owner):
        LibCommon.Ownable.__init__(self, owner)

        self.update_initial_storage(**self._get_initial_storage())

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
        loan_duration,
    ):
        # Type checks.
        sp.set_type(lender, sp.TAddress)
        sp.set_type(borrower, sp.TAddress)
        sp.set_type(loan_denomination_contract, sp.TAddress)
        sp.set_type(loan_principal_amount, sp.TNat)
        sp.set_type(loan_denomination_id, sp.TNat)
        sp.set_type(collateral_contract, sp.TAddress)
        sp.set_type(collateral_token_id, sp.TNat)
        sp.set_type(loan_duration, sp.TInt)

        # Verify that the call is coming from the origination controller.

        # Verify that the currency is permitted
        self._verify_permitted_currency(loan_denomination_contract)

        # Write loan to contract storage.
        self.data.loans_by_id[self.data.loan_id] = sp.record(
            lender=lender,
            borrower=borrower,
            loan_denomination_contract=loan_denomination_contract,
            loan_denomination_id=loan_denomination_id,
            loan_principal_amount=loan_principal_amount,
            collateral_contract=collateral_contract,
            collateral_token_id=collateral_token_id,
            loan_origination_timestamp=sp.now,
            loan_duration=loan_duration
        )

        # Transfer collateral to the collateral vault.
        self._transfer_collateral_to_vault(
            borrower,
            collateral_contract,
            collateral_token_id,
            self.data.loan_id
        )

        # Transfer loan amount to the contract
        self._transfer_funds(lender,
                             sp.self_address,
                             loan_denomination_contract,
                             loan_denomination_id,
                             loan_principal_amount
                             )

        # Calculate the processing fee.
        processing_fee = self._compute_processing_fee(
            loan_principal_amount,
            self.data.currency_precision[loan_denomination_contract]
        )

        # Calculate loan amount net of processing fee
        net_loan_amount = sp.as_nat(loan_principal_amount - processing_fee)

        # Transfer net loan amount to the borrower.
        self._transfer_funds(sp.self_address,
                             borrower,
                             loan_denomination_contract,
                             loan_denomination_id,
                             net_loan_amount
                             )

        # Issue borrower and lender notes.
        self._issue_borrower_note(borrower, self.data.loan_id)
        self._issue_lender_note(lender, self.data.loan_id)

        self._increment_loan_id()

        # Emits an event

    @sp.entry_point
    def repay(self, loan_id):
        sp.set_type(loan_id, sp.TNat)

        sp.verify(self.data.loans_by_id.contains(
            loan_id), "NON-EXISTENT LOAN")

        loan = self.data.loans_by_id[loan_id]
        sp.verify(sp.sender == loan.borrower, "UNAUTHORIZED CALLER")

        sp.verify(sp.now <= loan.loan_origination_timestamp.add_seconds(
            loan.loan_duration), "EXPIRED")

        self._transfer_funds(loan.borrower,
                             loan.lender,
                             loan.loan_denomination_contract,
                             loan.loan_denomination_id,
                             loan.loan_principal_amount
                             )
        self._withdraw_collateral_from_vault(loan_id, loan.borrower)

        del self.data.loans_by_id[loan_id]

    @sp.entry_point
    def claim(self, loan_id):
        sp.set_type(loan_id, sp.TNat)
        sp.verify(self.data.loans_by_id.contains(loan_id), "NON-EXISTENT LOAN")

        loan = self.data.loans_by_id[loan_id]
        sp.verify(sp.sender == loan.lender, "UNAUTHORIZED CALLER")

        sp.verify(sp.now > loan.loan_origination_timestamp.add_seconds(
            loan.loan_duration), "NOT_EXPIRED")

        self._withdraw_collateral_from_vault(loan_id, loan.lender)

        del self.data.loans_by_id[loan_id]

    @sp.entry_point
    def set_processing_fee(self, new_processing_fee):
        sp.set_type(new_processing_fee, sp.TNat)
        self._only_owner()
        sp.verify(new_processing_fee < 250, "INVALID_FEE")

        self.data.processing_fee = new_processing_fee

    @sp.entry_point
    def whitelist_currency(self, currency, precision):
        sp.set_type(currency, sp.TAddress)
        sp.set_type(precision, sp.TNat)

        self._only_owner()
        self.data.permitted_currencies[currency] = True
        self.data.currency_precision[currency] = precision

    @sp.entry_point
    def set_collateral_vault(self, collateral_vault_address):
        sp.set_type(collateral_vault_address, sp.TAddress)
        self._only_owner()
        self.data.collateral_vault_address = collateral_vault_address

    @sp.entry_point
    def set_loan_note_contracts(self, borrower_note_address, lender_note_address):
        sp.set_type(lender_note_address, sp.TAddress)
        sp.set_type(borrower_note_address, sp.TAddress)

        self._only_owner()

        # A sequence of further verifications are required here.

        self.data.lender_note_address = lender_note_address
        self.data.borrower_note_address = borrower_note_address

    @sp.onchain_view()
    def get_loan_by_id(self, loan_id):
        sp.set_type(loan_id, sp.TNat)
        sp.result(self.data.loans_by_id[loan_id])

    def _issue_borrower_note(self, borrower, loan_id):
        sp.set_type(borrower, sp.TAddress)
        LibLoanNote.Mint.execute(
            self.data.borrower_note_address, loan_id, borrower)

    def _issue_lender_note(self, lender, loan_id):
        sp.set_type(lender, sp.TAddress)
        LibLoanNote.Mint.execute(
            self.data.lender_note_address, loan_id, lender)

    def _transfer_funds(self, _from, _to, _currency, _tokenId, _amount):
        sp.set_type(_from, sp.TAddress)
        sp.set_type(_to, sp.TAddress)
        sp.set_type(_currency, sp.TAddress)
        sp.set_type(_amount, sp.TNat)
        sp.set_type(_tokenId, sp.TNat)

        LibFA2.Transfer.execute(_currency, _from, _to, _tokenId, _amount)

    def _verify_permitted_currency(self, currency):
        sp.verify(self.data.permitted_currencies.contains(
            currency) == True, "CURRENCY_NOT_AUTHORIZED")

    def _compute_processing_fee(self, loan_amount, currency_precision):
        sp.set_type(loan_amount, sp.TNat)
        sp.set_type(currency_precision, sp.TNat)

        return self._apply_percentage(loan_amount, self.data.processing_fee, currency_precision)

    def _apply_percentage(self, base_amount, basis_points, precision):
        sp.set_type(base_amount, sp.TNat)
        sp.set_type(basis_points, sp.TNat)
        sp.set_type(precision, sp.TNat)

        multiplier = (basis_points * precision) / Constants.BASIS_POINT_DIVISOR
        return ((base_amount * multiplier) // precision)

    def _transfer_collateral_to_vault(self, borrower, collateral_contract, collateral_id, loan_id):
        collateral_vault = sp.contract(LibCollateralVault.Deposit.get_type(),
                                       self.data.collateral_vault_address,
                                       entry_point='deposit').open_some()

        payload = sp.record(depositor=borrower, collateral_contract=collateral_contract,
                            collateral_token_id=collateral_id, amount=1, deposit_id=loan_id)

        sp.transfer(payload, sp.mutez(0), collateral_vault)

    def _withdraw_collateral_from_vault(self, deposit_id, recipient):
        collateral_vault = sp.contract(LibCollateralVault.Withdraw.get_type(),
                                       self.data.collateral_vault_address,
                                       entry_point='withdraw').open_some()

        payload = sp.record(deposit_id=deposit_id, recipient=recipient)

        sp.transfer(payload, sp.mutez(0), collateral_vault)

    def _increment_loan_id(self):
        self.data.loan_id += 1

    def _get_initial_storage(self):
        storage = {}
        storage["loan_id"] = sp.nat(0)
        storage['processing_fee'] = sp.nat(0)

        t_loan = sp.TRecord(
            lender=sp.TAddress,
            borrower=sp.TAddress,
            loan_denomination_contract=sp.TAddress,
            loan_denomination_id=sp.TNat,
            loan_principal_amount=sp.TNat,
            collateral_contract=sp.TAddress,
            collateral_token_id=sp.TNat,
            loan_origination_timestamp=sp.TTimestamp,
            loan_duration=sp.TInt
        )

        storage["loans_by_id"] = sp.big_map(tkey=sp.TNat, tvalue=t_loan)

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
