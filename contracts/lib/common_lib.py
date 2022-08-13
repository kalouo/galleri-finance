

import smartpy as sp


class Ownable(sp.Contract):
    def __init__(self, owner: sp.TAddress) -> None:
        self.init(owner=owner)

    def _only_owner(self):
        sp.verify(self.data.owner == sp.sender,
                  "Ownable: caller is not the owner")

    def _set_owner(self, address: sp.TAddress):
        """
                        Set a new owner!
        """
        self._only_owner()
        self.data.owner = address

    def _renounceOwnership(self):
        """
                        Current owner can renounce his ownership!
                        WARNING - cannot undo this
        """
        self._set_owner(sp.address("tz1Ke2h7sDdakHJQh8WX4Z372du1KChsksyU"))
