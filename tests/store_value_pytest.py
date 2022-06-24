from unittest import TestCase
from pytezos import MichelsonRuntimeError
from chinstrap.tests import getContractInterface


class StoreValueTests(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract = getContractInterface("StoreValue")

    def test_should_pass_if_the_return_value_is_5(self):
        value = 5
        storage = 0
        result = self.contract.replace(value).interpret(storage=storage)
        assert result.storage == 5
