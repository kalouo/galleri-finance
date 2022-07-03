import smartpy as sp

FA2Lib = sp.io.import_script_from_url("file:contracts/lib/FA2Lib.py")


class LendingNote(FA2Lib.OwnableFA2NFT):
    def __init__(self, admin, metadata):
        FA2Lib.OwnableFA2NFT.__init__(self, admin, metadata)


sp.add_compilation_target(
    "LendingNote",
    LendingNote(
        admin=sp.address("tz1YtuZ4vhzzn7ssCt93Put8U9UJDdvCXci4"),
        metadata=sp.utils.metadata_of_url("http://example.com")
    )
)
