import smartpy as sp

LoanCore = sp.io.import_script_from_url("file:contracts/loanCore.py")
LendingNote = sp.io.import_script_from_url("file:contracts/lendingNote.py")
Constants = sp.io.import_script_from_url("file:contracts/lib/constants.py")


@sp.add_test(name="A Test")
def test():
    scenario = sp.test_scenario()

    # Initialize addresses.
    _admin = sp.test_account("_admin")
    _alice = sp.test_account("_alice")

    # Initialize contracts
    loanCore = LoanCore.LoanCore(_admin.address)
    lendingNote = LendingNote.LendingNote(
        loanCore.address, Constants.SAMPLE_METADATA)

    scenario += loanCore
    scenario += lendingNote


    # `lendingNote` is deployed with the correct administrator
    scenario.verify(lendingNote.data.administrator == loanCore.address)

    # `setLendingNoteContract` cannot be called by a non-owner
    scenario += loanCore.setLendingNoteContract(
        lendingNote.address).run(sender=_alice.address, valid=False)

    # `setLendingNoteContract` cannot be called by the contract owner
    scenario += loanCore.setLendingNoteContract(
        lendingNote.address).run(sender=_admin.address, valid=True)

    scenario.verify(loanCore.data.lendingNoteContract == lendingNote.address)
