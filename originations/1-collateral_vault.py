from chinstrap.originations import getContract


def deploy(chinstrapState, network, accounts):
    contract = getContract("collateral_vault")
    initial_storage = contract.storage.encode(
        {"deposits": {}, "owner": accounts[0].key.public_key_hash()}
    )
    return initial_storage, contract
