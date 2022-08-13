import smartpy as sp

LibFA2 = sp.io.import_script_from_url("file:""contracts/lib/FA2_lib.py")
Constants = sp.io.import_script_from_url("file:contracts/lib/constants.py")

class TestCurrency(LibFA2.OwnableFA2Fungible):

    def __init__(self, admin, metadata, token_metadata={}, ledger={}, policy=None, metadata_base=None):
        LibFA2.OwnableFA2NFT.__init__(
            self, admin, metadata, token_metadata, ledger, policy, metadata_base)


sp.add_compilation_target(
    "test_nft",
    TestCurrency(
        admin=Constants.NULL_ADDRESS,
        metadata=sp.utils.metadata_of_url("http://example.com")
    )
)
