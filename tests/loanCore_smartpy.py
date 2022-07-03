import smartpy as sp

LoanCore = sp.io.import_script_from_url("file:contracts/loanCore.py")
LendingNote = sp.io.import_script_from_url("file:contracts/lendingNote.py")
Constants = sp.io.import_script_from_url("file:contracts/lib/constants.py")
FA2Lib = sp.io.import_script_from_url("file:contracts/lib/FA2Lib.py")

SAMPLE_METADATA = sp.utils.metadata_of_url("http://example.com")


@sp.add_test(name="A Test")
def test():
    scenario = sp.test_scenario()

    # Initialize addresses.
    _admin = sp.test_account("_admin")
    _alice = sp.test_account("_alice")
    _bob = sp.test_account("_bob")

    # Initialize contracts
    nonFungibleToken = FA2Lib.OwnableFA2NFT(_admin.address, SAMPLE_METADATA)
    fungibleToken = FA2Lib.OwnableFA2Fungible(_admin.address, SAMPLE_METADATA)
    loanCore = LoanCore.LoanCore(_admin.address)
    lendingNote = LendingNote.LendingNote(loanCore.address, SAMPLE_METADATA)

    # Add contracts to scenarios
    scenario += nonFungibleToken
    scenario += fungibleToken
    scenario += loanCore
    scenario += lendingNote

    TOKEN_0 = FA2Lib.make_metadata(
        name="Example FA2",
        decimals=0,
        symbol="EFA2")

    # Mint fungible tokens to Alice and Bob.
    scenario += fungibleToken.mint([sp.record(
        to_=_alice.address,
        amount=100_000_000_000,
        token=sp.variant("new", TOKEN_0)
    ), sp.record(
        to_=_bob.address,
        amount=100_000_000_000,
        token=sp.variant("existing", 0)
    )]).run(sender=_admin)

    # Verify that fungible tokens have been minted.
    scenario.verify(fungibleToken.data.ledger[sp.pair(
        _alice.address, 0)] == sp.nat(100_000_000_000))

    scenario.verify(fungibleToken.data.ledger[sp.pair(
        _bob.address, 0)] == sp.nat(100_000_000_000))

    # Mint NFT to Bob.
    NFT1 = FA2Lib.make_metadata(
        name="Example FA2",
        decimals=0,
        symbol="EFA2-2")

    scenario += nonFungibleToken.mint([
        sp.record(
            to_=_bob.address,
            metadata=NFT1)
    ]).run(sender=_admin)

    # Verify that NFT was minted to Bob.
    # Reflects NFT ledger type.
    # See https://gitlab.com/tezos/tzip/-/blob/master/proposals/tzip-12/tzip-12.md#nft-asset-contract 
    scenario.verify(nonFungibleToken.data.ledger[0] == _bob.address)

    # `lendingNote` is deployed with the correct administrator
    scenario.verify(lendingNote.data.administrator == loanCore.address)

    # `setLendingNoteContract` cannot be called by a non-owner
    scenario += loanCore.setLendingNoteContract(
        lendingNote.address).run(sender=_alice.address, valid=False)

    # `setLendingNoteContract` cannot be called by the contract owner
    scenario += loanCore.setLendingNoteContract(
        lendingNote.address).run(sender=_admin.address, valid=True)

    scenario.verify(loanCore.data.lendingNoteContract == lendingNote.address)
