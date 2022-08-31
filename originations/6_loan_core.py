from chinstrap.originations import getContract


def deploy(chinstrapState, network, accounts):
    contract = getContract("loan_core")
    initial_storage = contract.storage.encode(
        {
            "borrower_note_address": "tz1Ke2h7sDdakHJQh8WX4Z372du1KChsksyU",
            "collateral_vault_address": "tz1Ke2h7sDdakHJQh8WX4Z372du1KChsksyU",
            "lender_note_address": "tz1Ke2h7sDdakHJQh8WX4Z372du1KChsksyU",
            "interest_fee": 5,
            "processing_fee": 1,
            "loan_id": 0,
            "currency_precision": {},
            "loans_by_id": {},
            "permitted_currencies": {},
            "origination_controllers": {},
            "owner": accounts[0].key.public_key_hash()
        }
    )
    return initial_storage, contract
