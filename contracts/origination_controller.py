import smartpy as sp


def import_sp(file_path):
    return sp.io.import_script_from_url("file:" + file_path)


Constants = import_sp("contracts/lib/constants.py")
LibCommon = import_sp("contracts/lib/common_lib.py")
LibLoanCore = import_sp("contracts/loan_core.py")


class OriginationController(LibCommon.Ownable):
    def __init__(self, owner, loan_manager):
        LibCommon.Ownable.__init__(self, owner)

        self.update_initial_storage(**self._get_initial_storage(loan_manager))

    @sp.entry_point
    def create_request(self,
                       collateral_contract,
                       collateral_token_id,
                       loan_denomination_contract,
                       loan_denomination_token_id,
                       loan_duration,
                       loan_principal_amount,
                       interest_amount,
                       time_adjustable_interest):

        # Type checks.

        sp.set_type(collateral_contract, sp.TAddress)
        sp.set_type(collateral_token_id, sp.TNat)
        sp.set_type(interest_amount, sp.TNat)
        sp.set_type(loan_denomination_contract, sp.TAddress)
        sp.set_type(loan_denomination_token_id, sp.TNat)
        sp.set_type(loan_duration, sp.TInt)
        sp.set_type(loan_principal_amount, sp.TNat)
        sp.set_type(time_adjustable_interest, sp.TBool)

        request = sp.record(
            creator=sp.sender,
            collateral_contract=collateral_contract,
            collateral_token_id=collateral_token_id,
            loan_denomination_contract=loan_denomination_contract,
            loan_denomination_token_id=loan_denomination_token_id,
            loan_duration=loan_duration,
            loan_principal_amount=loan_principal_amount,
            interest_amount=interest_amount,
            time_adjustable_interest=time_adjustable_interest
        )

        self.data.requests_by_id[self.data.request_id] = request

        self._increment_request_id()

    @sp.entry_point
    def cancel_request(self, request_id):
        sp.verify(sp.sender == self.data.requests_by_id[request_id].creator)
        del self.data.requests_by_id[request_id]

    @sp.entry_point
    def originate_loan(self, request_id):
        sp.set_type(request_id, sp.TNat)

        request = self.data.requests_by_id[request_id]

        payload = sp.record(
            lender=sp.sender,
            borrower=request.creator,
            loan_denomination_contract=request.loan_denomination_contract,
            loan_denomination_token_id=request.loan_denomination_token_id,
            loan_principal_amount=request.loan_principal_amount,
            interest_amount=request.interest_amount,
            collateral_contract=request.collateral_contract,
            collateral_token_id=request.collateral_token_id,
            loan_duration=request.loan_duration,
            time_adjustable_interest=request.time_adjustable_interest
        )

        loan_manager = sp.contract(LibLoanCore.StartLoan.get_type(),
                                   self.data.loan_manager,
                                   entry_point='start_loan').open_some()

        sp.transfer(payload, sp.mutez(0), loan_manager)

    @sp.entry_point
    def set_loan_manager(self, loan_manager_address):
        sp.set_type(loan_manager_address, sp.TAddress)
        self.data.loan_manager = loan_manager_address

    @sp.entry_point
    def set_owner(self, new_owner):
        sp.set_type(new_owner, sp.TAddress)
        self._set_owner(new_owner)

    @sp.onchain_view()
    def get_request_by_id(self, request_id):
        sp.set_type(request_id, sp.TNat)
        sp.result(self.data.requests_by_id[request_id])

    def _increment_request_id(self):
        self.data.request_id += 1

    def _get_initial_storage(self, loan_manager):
        t_request = sp.TRecord(
            creator=sp.TAddress,
            collateral_contract=sp.TAddress,
            collateral_token_id=sp.TNat,
            loan_denomination_contract=sp.TAddress,
            loan_denomination_token_id=sp.TNat,
            loan_duration=sp.TInt,
            loan_principal_amount=sp.TNat,
            interest_amount=sp.TNat,
            time_adjustable_interest=sp.TBool
        )

        storage = {}
        storage["request_id"] = 0
        storage["loan_manager"] = loan_manager
        storage["requests_by_id"] = sp.big_map(tkey=sp.TNat, tvalue=t_request)

        return storage



if __name__ == "__main__":

    sp.add_compilation_target(
        "origination_controller",
        OriginationController(
            owner=Constants.NULL_ADDRESS,
            loan_manager=Constants.NULL_ADDRESS
        )
    )
