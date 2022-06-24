# SmartPy Code
import smartpy as sp


class StoreValue(sp.Contract):
    def __init__(self, value):
        self.init(storedValue=value)

    @sp.entry_point
    def replace(self, value):
        self.data.storedValue = value

    @sp.entry_point
    def double(self):
        self.data.storedValue *= 2


sp.add_compilation_target("StoreValue", StoreValue(0))
