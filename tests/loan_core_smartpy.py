import smartpy as sp

LoanCore = sp.io.import_script_from_url("file:contracts/loan_core.py")
LoanNote = sp.io.import_script_from_url("file:contracts/loan_note.py")
Constants = sp.io.import_script_from_url("file:contracts/lib/constants.py")
FA2Lib = sp.io.import_script_from_url("file:contracts/lib/FA2_lib.py")
CollateralVault = sp.io.import_script_from_url(
    "file:contracts/collateral_vault.py")

SAMPLE_METADATA = sp.utils.metadata_of_url("http://example.com")


@sp.add_test(name="Loan Core Test")
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
    collateralVault = CollateralVault.CollateralVault(loanCore.address)
    borrowerNote = LoanNote.LoanNote(loanCore.address, SAMPLE_METADATA)
    lenderNote = LoanNote.LoanNote(loanCore.address, SAMPLE_METADATA)
    # Add contracts to scenarios
    scenario += nonFungibleToken
    scenario += fungibleToken

    scenario += loanCore
    scenario += collateralVault
    scenario += borrowerNote
    scenario += lenderNote

    # Whitelist the contract
    PRECISION = sp.nat(1000000000000000000)

    scenario += loanCore.whitelist_currency(
        currency=fungibleToken.address, precision=PRECISION).run(sender=_admin)

    scenario.verify(
        loanCore.data.permitted_currencies[fungibleToken.address] == True)

    scenario.verify(
        loanCore.data.currency_precision[fungibleToken.address] == PRECISION)
    # Set processing fee of 1%
    scenario += loanCore.set_processing_fee(100).run(sender=_admin)
    scenario.verify(loanCore.data.processing_fee == sp.nat(100))

    scenario += loanCore.set_collateral_vault(
        collateralVault.address).run(sender=_admin)

    scenario.verify(loanCore.data.collateral_vault_address ==
                    collateralVault.address)

    scenario += loanCore.set_loan_note_contracts(
        borrower_note_address=borrowerNote.address,
        lender_note_address=lenderNote.address
    ).run(sender=_admin)

    scenario.verify(loanCore.data.borrower_note_address ==
                    borrowerNote.address)
    scenario.verify(loanCore.data.lender_note_address == lenderNote.address)

    TOKEN_0 = FA2Lib.Utils.make_metadata(
        name="Example FA2",
        decimals=0,
        symbol="EFA2")

    # Mint fungible tokens to Alice and Bob.
    scenario += fungibleToken.mint([sp.record(
        to_=_alice.address,
        amount=sp.nat(1000) * PRECISION,
        token=sp.variant("new", TOKEN_0)
    ), sp.record(
        to_=_bob.address,
        amount=sp.nat(1000) * PRECISION,
        token=sp.variant("existing", 0)
    )]).run(sender=_admin)

    # Verify that fungible tokens have been minted.
    scenario.verify(fungibleToken.data.ledger[sp.pair(
        _alice.address, 0)] == sp.nat(1000) * PRECISION)

    scenario.verify(fungibleToken.data.ledger[sp.pair(
        _bob.address, 0)] == sp.nat(1000) * PRECISION)

    # Mint NFT to Bob.
    NFT1 = FA2Lib.Utils.make_metadata(
        name="Example FA2",
        decimals=0,
        symbol="EFA2-2")

    scenario += nonFungibleToken.mint([
        sp.record(
            to_=_alice.address,
            metadata=NFT1)
    ]).run(sender=_admin)

    # Verify that NFT was minted to Bob.
    # Reflects NFT ledger type.
    # See https://gitlab.com/tezos/tzip/-/blob/master/proposals/tzip-12/tzip-12.md#nft-asset-contract
    scenario.verify(nonFungibleToken.data.ledger[0] == _alice.address)

    # Alice approves the loan contract to spend her funds.
    scenario += fungibleToken.update_operators([sp.variant("add_operator", sp.record(
        owner=_bob.address,
        operator=loanCore.address,
        token_id=0
    ))]).run(sender=_bob)

    # Verify that permissions have been given.
    scenario.verify(fungibleToken.data.operators.contains(
        sp.record(owner=_bob.address, operator=loanCore.address, token_id=0)
    )),

    scenario += nonFungibleToken.update_operators([sp.variant("add_operator", sp.record(
        owner=_alice.address,
        operator=collateralVault.address,
        token_id=0
    ))]).run(sender=_alice)

    # Verify that permissions have been given.
    scenario.verify(nonFungibleToken.data.operators.contains(
        sp.record(owner=_alice.address,
                  operator=collateralVault.address, token_id=0)
    )),

    loanAmount = sp.nat(100) * PRECISION
    scenario += loanCore.start_loan(lender=_bob.address,
                                    borrower=_alice.address,
                                    loan_denomination_contract=fungibleToken.address,
                                    loan_denomination_id=0,
                                    loan_principal_amount=loanAmount,
                                    collateral_contract=nonFungibleToken.address,
                                    collateral_token_id=0,
                                    loan_duration=0
                                    )

    scenario.verify(loanCore.get_loan_by_id(0) == sp.record(
                    lender=_bob.address,
                    borrower=_alice.address,
                    loan_denomination_contract=fungibleToken.address,
                    loan_denomination_id=0,
                    loan_principal_amount=loanAmount,
                    collateral_contract=nonFungibleToken.address,
                    collateral_token_id=0,
                    loan_duration=0))

    # # Verify that Bob owns the lender note.
    scenario.verify(lenderNote.data.ledger[0] == _bob.address)

    # Verify that Bob owns the borrower note.
    scenario.verify(borrowerNote.data.ledger[0] == _alice.address)

    scenario.verify(loanCore.data.loan_id == 1)

    # Verify the NFT is locked in the collateral vaut.
    scenario.verify(nonFungibleToken.data.ledger[0] == collateralVault.address)

    scenario.verify(fungibleToken.data.ledger[sp.pair(
        _bob.address, 0)] == sp.nat(900) * PRECISION)

    scenario.verify(fungibleToken.data.ledger[sp.pair(
        _alice.address, 0)] == sp.nat(1099) * PRECISION)
