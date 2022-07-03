# SmartPy Code
import smartpy as sp


class Ownable(sp.Contract):
    def __init__(self, owner: sp.TAddress) -> None:
        self.update_initial_storage(owner=owner)

    def _onlyOwner(self):
        sp.verify(self.data.owner == sp.sender,
                  "Ownable: caller is not the owner")

    def _setOwner(self, address: sp.TAddress):
        """
                        Set a new owner!
        """
        self._onlyOwner()
        self.data.owner = address

    def _renounceOwnership(self):
        """
                        Current owner can renounce his ownership!
                        WARNING - cannot undo this
        """
        self._setOwner(sp.address("tz1Ke2h7sDdakHJQh8WX4Z372du1KChsksyU"))
