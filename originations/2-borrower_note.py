from chinstrap.originations import getContract


def deploy(chinstrapState, network, accounts):
    contract = getContract("borrower_note")
    initial_storage = contract.storage.encode(
        {
            "ledger": {},
            "operators": {},
            "token_metadata": {},
            "last_token_id": 0,
            "metadata": {'': '0x687474703a2f2f6578616d706c652e636f6d'},
            "administrator": accounts[0].key.public_key_hash()
        }
    )
    return initial_storage, contract
