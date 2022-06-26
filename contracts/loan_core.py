# SmartPy Code
import smartpy as sp

LibAdmin = sp.io.import_script_from_url("file:contracts/lib/admin.py")


class LoanCore(LibAdmin.Admin):
    def __init__(self, owner):
        LibAdmin.Admin.__init__(self, owner)


sp.add_compilation_target("LoanCore", LoanCore(
    sp.address("tz1Ke2h7sDdakHJQh8WX4Z372du1KChsksyU")))
