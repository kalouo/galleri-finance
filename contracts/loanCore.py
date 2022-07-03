# SmartPy Code
import smartpy as sp

CommonLib = sp.io.import_script_from_url("file:contracts/lib/commonLib.py")
Constants = sp.io.import_script_from_url("file:contracts/lib/constants.py")


class LoanCore(CommonLib.Ownable):
    def __init__(self, owner, lendingNoteContract=None):
        self.init(**self.get_initial_storage(lendingNoteContract))

        # Libraries
        CommonLib.Ownable.__init__(self, owner)

    @sp.entry_point
    def startLoan(self):
        # Checks that the caller is the origination controller
        # Needs loan core admin lib
        # Transfers the collateral token to the collateral vault
        # Needs test FA2 NFT
        # Transfers the loan token to itself
        # Needs FA1.2 fungible
        # Needs FA2 fungible
        # Writes loan details to contract storage
        # Emits a lender's note to the lender
        # Transfers the principal to the borrower minus platform fees.
        # Needs a fee controller contract
        # Emits an event
        None

    @sp.entry_point
    def repay(self):
        None

    @sp.entry_point
    def claim(self):
        None

    # Admin Functions:
    @sp.entry_point
    def setLendingNoteContract(self, contractAddress):
        sp.set_type(contractAddress, sp.TAddress)
        self._onlyOwner()

        self.data.lendingNoteContract = contractAddress

    def get_initial_storage(self, lendingNoteContract):
        storage = {}

        if lendingNoteContract is None:
            storage['lendingNoteContract'] = Constants.NULL_ADDRESS
        else:
            storage['lendingNoteContract'] = lendingNoteContract

        return storage


sp.add_compilation_target("LoanCore", LoanCore(
    owner=sp.address("tz1Rn1TTJo3RwLfDN2XyjQgQ2nf8hcdvqrsy")
))
