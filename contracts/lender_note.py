import smartpy as sp

LibLoanNote = sp.io.import_script_from_url("file:""contracts/lib/loan_note.py")
LibFA2 = sp.io.import_script_from_url("file:""contracts/lib/FA2_lib.py")
Constants = sp.io.import_script_from_url("file:contracts/lib/constants.py")


class LenderNote(LibLoanNote.LoanNote):

    def __init__(self, admin, metadata, token_metadata={}, ledger={}, policy=None, metadata_base=None):
        LibLoanNote.LoanNote.__init__(
            self, admin, metadata, token_metadata=token_metadata, ledger=ledger, policy=policy, metadata_base=metadata_base)


if __name__ == "__main__":

    sp.add_compilation_target(
        "lender_note",
        LenderNote(
            admin=sp.address("tz1YtuZ4vhzzn7ssCt93Put8U9UJDdvCXci4"),
            metadata=sp.utils.metadata_of_url("http://example.com"),
        )
    )
