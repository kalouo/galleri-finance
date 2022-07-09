import smartpy as sp

FA2Lib = sp.io.import_script_from_url(
    "https://smartpy.io/templates/fa2_lib.py")


class OwnableFA2NFT(FA2Lib.Admin,
                    FA2Lib.ChangeMetadata,
                    FA2Lib.WithdrawMutez,
                    FA2Lib.MintNft,
                    FA2Lib.BurnNft,
                    FA2Lib.OnchainviewBalanceOf,
                    FA2Lib.Fa2Nft
                    ):

    def __init__(self, admin, metadata, token_metadata={}, ledger={}, policy=None, metadata_base=None):
        FA2Lib.Fa2Nft.__init__(self, metadata, token_metadata=token_metadata,
                               ledger=ledger, policy=policy, metadata_base=metadata_base)
        FA2Lib.Admin.__init__(self, admin)


class OwnableFA2Fungible(FA2Lib.Admin,
                         FA2Lib.ChangeMetadata,
                         FA2Lib.WithdrawMutez,
                         FA2Lib.OnchainviewBalanceOf,
                         FA2Lib.Fa2Fungible,
                         FA2Lib.MintFungible
                         ):

    def __init__(self, admin, metadata, token_metadata={}, ledger={}, policy=None, metadata_base=None):
        FA2Lib.Fa2Fungible.__init__(self, metadata, token_metadata=token_metadata,
                                    ledger=ledger, policy=policy, metadata_base=metadata_base)
        FA2Lib.Admin.__init__(self, admin)


# Helpers


class Transfer:
    """Class to facilitate FA2 operations."""
    def get_type():
        """Returns a single transfer type, layouted
        Returns:
            sp.TRecord: single transfer type, layouted
        """
        tx_type = sp.TRecord(to_=sp.TAddress,
                             token_id=sp.TNat,
                             amount=sp.TNat).layout(
            ("to_", ("token_id", "amount"))
        )
        transfer_type = sp.TRecord(from_=sp.TAddress,
                                   txs=sp.TList(tx_type)).layout(
                                       ("from_", "txs"))
        return transfer_type

    def get_batch_type():
        """Returns a list type containing transfer types
        Returns:
            sp.TList: list type containing transfer types
        """
        return sp.TList(Transfer.get_type())

    def item(from_, txs):
        """ Creates a typed transfer item as per FA2 specification
        Args:
            from_ (sp.address): address of the sender
            txs (dict): dictionary containing the keys "to_" (the recipient), "token_id" (id to transfer), and "amount" (amount of token to transfer)
        Returns:
            Transfer: transfer sp.record typed
        """
        return sp.set_type_expr(sp.record(from_=from_, txs=txs), Transfer.get_type())

    def execute(token_address, from_, to_, token_id, amount):
        """Executes FA2 token transfer
        Args:
            token_address (sp.address): FA2 token contract address
            from_ (sp.address): sender
            to_ (sp.address): recipient
            token_id (sp.nat): token ID
            amount (sp.nat): token amount to transfer
        """
        transfer_token_contract = sp.contract(Transfer.get_batch_type(
        ), token_address, entry_point="transfer").open_some()
        transfer_payload = [Transfer.item(from_, [sp.record(
            to_=to_, token_id=token_id, amount=amount)])]
        sp.transfer(transfer_payload, sp.mutez(0), transfer_token_contract)


class Utils:

    def make_metadata(symbol, name, decimals):
        return FA2Lib.make_metadata(symbol, name, decimals)
