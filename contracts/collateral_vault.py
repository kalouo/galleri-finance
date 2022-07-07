import smartpy as sp

Constants = sp.io.import_script_from_url("file:contracts/lib/constants.py")
CommonLib = sp.io.import_script_from_url("file:contracts/lib/CommonLib.py")
FA2Lib = sp.io.import_script_from_url("file:contracts/lib/FA2Lib.py")


# class ErrorMessage:
#     NOT_ADMIN = "{}NOT_ADMIN"


class Deposit:
    def get_type():
        return sp.TRecord(
            depositor=sp.TAddress,
            collateral_contract=sp.TAddress,
            collateral_token_id=sp.TNat,
            amount=sp.TNat,
            deposit_id=sp.TNat
        )


class CollateralVault(CommonLib.Ownable):
    def __init__(self, owner):
        CommonLib.Ownable.__init__(self, owner)
        self.update_initial_storage(**self.get_initial_storage())

    def get_initial_storage(self):
        storage = {}

        t_deposit = sp.TRecord(
            collateral_contract=sp.TAddress,
            collateral_token_id=sp.TNat,
            deposit_amount=sp.TNat,
        )

        storage['deposits'] = sp.big_map(tkey=sp.TNat, tvalue=t_deposit)

        return storage

    @sp.entry_point
    def deposit(self, depositor, collateral_contract, collateral_token_id, amount, deposit_id):
        sp.set_type(collateral_contract, sp.TAddress)
        sp.set_type(collateral_token_id, sp.TNat)
        sp.set_type(deposit_id, sp.TNat)

        self._onlyOwner()

        self._transfer_collateral(
            depositor,
            sp.self_address,
            collateral_contract,
            collateral_token_id,
            amount
        )

        self.data.deposits[deposit_id] = sp.record(
            collateral_contract=collateral_contract,
            collateral_token_id=collateral_token_id,
            deposit_amount=amount
        )

    def _transfer_collateral(self, _from, _to, _currency, _tokenId, _amount):
        sp.set_type(_from, sp.TAddress)
        sp.set_type(_to, sp.TAddress)
        sp.set_type(_currency, sp.TAddress)
        sp.set_type(_amount, sp.TNat)
        sp.set_type(_tokenId, sp.TNat)

        FA2Lib.Transfer.execute(_currency, _from, _to, _tokenId, _amount)


# sp.add_compilation_target(
#     "collateral_vault",
#     CollateralVault(
#         owner=Constants.NULL_ADDRESS,
#     )
# )
