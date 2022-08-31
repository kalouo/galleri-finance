from chinstrap.originations import getContract


def deploy(chinstrapState, network, accounts):
    contract = getContract("origination_controller")
    initial_storage = contract.storage.encode(
        {
            "loan_manager": "tz1Ke2h7sDdakHJQh8WX4Z372du1KChsksyU",
            "request_id": 0,
            "requests_by_id": {},
            "owner": accounts[0].key.public_key_hash()
        }
    )
    return initial_storage, contract
