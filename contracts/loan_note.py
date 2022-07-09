import smartpy as sp

FA2Lib = sp.io.import_script_from_url(
    "https://smartpy.io/templates/fa2_lib.py")


class LoanNote(FA2Lib.Admin,
           FA2Lib.Fa2Nft,
           FA2Lib.OnchainviewBalanceOf,
           ):

    def __init__(self, admin, metadata, token_metadata={}, ledger={}, policy=None, metadata_base=None):
        FA2Lib.Fa2Nft.__init__(self, metadata, token_metadata=token_metadata,
                               ledger=ledger, policy=policy, metadata_base=metadata_base)
        FA2Lib.Admin.__init__(self, admin)

    def mint(self, batch):
        """Tokens can only be minted through internal calls"""
        sp.set_type(batch, MintArg.get_batch_type())
        with sp.for_("action", batch) as action:
            token_id = sp.compute(self.data.last_token_id)
            metadata = sp.record(
                token_id=token_id, token_info=action.metadata)
            self.data.token_metadata[token_id] = metadata
            self.data.ledger[token_id] = action.to_
            self.data.last_token_id += 1


class MintArg:
    """Helper type used for the `mint` function
    """
    def get_type():
        """Get the token amount type
        Returns:
            sp.TRecord: [description]
        """
        return sp.TRecord(
            to_=sp.TAddress,
            metadata=sp.TMap(sp.TString, sp.TBytes),
        ).layout(("to_", "metadata"))

    def get_batch_type():
        """Get a list of the token amount type
        Returns:
            sp.TList: the token amount list type
        """
        return sp.TList(MintArg.get_type())

    def make_metadata(symbol, name, decimals):
        return FA2Lib.make_metadata(symbol, name, decimals)

    def make(to):
        """Creates a typed token amount
        Args:
            _to (sp.address): recipient
        Returns:
            sp.record: arguments for `mint` function
        """

        return sp.set_type_expr(sp.record(to_=to, metadata=MintArg.make_metadata("LN", "Lending LoanNote", 0)), MintArg.get_type())


sp.add_compilation_target(
    "loan_note",
    LoanNote(
        admin=sp.address("tz1YtuZ4vhzzn7ssCt93Put8U9UJDdvCXci4"),
        metadata=sp.utils.metadata_of_url("http://example.com")
    )
)
