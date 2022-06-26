# SmartPy Code
import smartpy as sp


class Admin(sp.Contract):
    def __init__(self, owner):
        self.init_type(sp.TRecord(owner=sp.TAddress))
        self.init(**self.get_initial_storage(owner))

    def get_initial_storage(self, owner):
        storage = {}
        storage["owner"] = owner
        return storage
