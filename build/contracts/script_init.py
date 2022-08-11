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

    @sp.entry_point
    def mint(self, batch):
        """Tokens can only be minted through internal calls"""
        sp.set_type(batch, Mint.get_batch_type())
        sp.verify(self.is_administrator(sp.sender), "FA2_NOT_ADMIN")

        with sp.for_("action", batch) as action:
            metadata = sp.record(
                token_id=action.token_id, token_info=action.metadata)
            self.data.token_metadata[action.token_id] = metadata
            self.data.ledger[action.token_id] = action.to
            self.data.last_token_id += 1

    @sp.entry_point
    def burn(self, token_id):
        """Users can burn tokens if they have the transfer policy permission.

        Burning an nft destroys its metadata.
        """
        sp.set_type(token_id, sp.TNat)
        sp.verify(self.is_administrator(sp.sender), "FA2_NOT_ADMIN")

        del self.data.ledger[token_id]
        del self.data.token_metadata[token_id]

    @sp.onchain_view()
    def owner_of(self, token_id):
        sp.set_type(token_id, sp.TNat)
        sp.result(self.data.ledger[token_id])


class Burn:
    def execute(token_address, token_id):
        """Executes FA2 burn transaction
        Args:
            token_address (sp.address): FA2 token contract address
            to (sp.address): recipient
            token_id (sp.nat): token ID
        """
        burn_token_contract = sp.contract(
            sp.TNat, token_address,
            entry_point='burn').open_some()
        sp.transfer(token_id, sp.mutez(0), burn_token_contract)


class Mint:
    def execute(token_address, token_id, to):
        """Executes FA2 mint transaction
        Args:
            token_address (sp.address): FA2 token contract address
            to (sp.address): recipient
            token_id (sp.nat): token ID
        """
        mint_token_contract = sp.contract(Mint.get_batch_type(
        ), token_address, entry_point='mint').open_some()
        mint_payload = [Mint.make(token_id, to)]
        sp.transfer(mint_payload, sp.mutez(0), mint_token_contract)

    """Helper type used for the `mint` function
    """
    def get_type():
        """Get the token amount type
        Returns:
            sp.TRecord: [description]
        """
        return sp.TRecord(
            token_id=sp.TNat,
            to=sp.TAddress,
            metadata=sp.TMap(sp.TString, sp.TBytes),
        ).layout(("token_id", ("to", "metadata")))

    def get_batch_type():
        """Get a list of the token amount type
        Returns:
            sp.TList: the token amount list type
        """
        return sp.TList(Mint.get_type())

    def make_metadata(symbol, name, decimals):
        return FA2Lib.make_metadata(symbol, name, decimals)

    def make(token_id, to):
        """Creates a typed token amount
        Args:
            _to (sp.address): recipient
        Returns:
            sp.record: arguments for `mint` function
        """

        return sp.set_type_expr(sp.record(to=to, token_id=token_id, metadata=Mint.make_metadata("LN", "Lending LoanNote", 0)), Mint.get_type())


if __name__ == "__main__":

    sp.add_compilation_target(
        "loan_note",
        LoanNote(
            admin=sp.address("tz1YtuZ4vhzzn7ssCt93Put8U9UJDdvCXci4"),
            metadata=sp.utils.metadata_of_url("http://example.com")
        )
    )
