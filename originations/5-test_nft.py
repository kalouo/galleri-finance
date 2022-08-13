from chinstrap.originations import getContract


def deploy(chinstrapState, network, accounts):
    contract = getContract("test_nft")
    initial_storage = contract.storage.encode(
        {
            "administrator": accounts[0].key.public_key_hash(),
            "last_token_id": 0,
            "ledger": {},
            "metadata": {'': '0x687474703a2f2f6578616d706c652e636f6d'},
            "operators": {},
            "supply": {},
            "token_metadata": {},
        }
    )
    return initial_storage, contract
