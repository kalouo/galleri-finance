import smartpy as sp

FA2Lib = sp.io.import_script_from_url("file:contracts/lib/FA2Lib.py")


class LendingNote(FA2Lib.OwnableFA2NFT):
    def __init__(self, admin, metadata):
        FA2Lib.OwnableFA2NFT.__init__(self, admin, metadata)
