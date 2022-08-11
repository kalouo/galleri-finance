import smartpy as sp

class Contract(sp.Contract):
  def __init__(self):
    self.init_type(sp.TRecord(deposits = sp.TBigMap(sp.TNat, sp.TRecord(collateral_contract = sp.TAddress, collateral_token_id = sp.TNat, deposit_amount = sp.TNat).layout(("collateral_contract", ("collateral_token_id", "deposit_amount")))), owner = sp.TAddress).layout(("deposits", "owner")))
    self.init(deposits = {},
              owner = sp.address('tz1Ke2h7sDdakHJQh8WX4Z372du1KChsksyU'))

  @sp.entry_point
  def deposit(self, params):
    sp.set_type(params.collateral_contract, sp.TAddress)
    sp.set_type(params.collateral_token_id, sp.TNat)
    sp.set_type(params.deposit_id, sp.TNat)
    sp.verify(self.data.owner == sp.sender, 'Ownable: caller is not the owner')
    sp.set_type(params.depositor, sp.TAddress)
    sp.set_type(sp.self_address, sp.TAddress)
    sp.set_type(params.collateral_contract, sp.TAddress)
    sp.set_type(params.amount, sp.TNat)
    sp.set_type(params.collateral_token_id, sp.TNat)
    sp.transfer(sp.list([sp.set_type_expr(sp.record(from_ = params.depositor, txs = sp.list([sp.record(to_ = sp.self_address, token_id = params.collateral_token_id, amount = params.amount)])), sp.TRecord(from_ = sp.TAddress, txs = sp.TList(sp.TRecord(amount = sp.TNat, to_ = sp.TAddress, token_id = sp.TNat).layout(("to_", ("token_id", "amount"))))).layout(("from_", "txs")))]), sp.tez(0), sp.contract(sp.TList(sp.TRecord(from_ = sp.TAddress, txs = sp.TList(sp.TRecord(amount = sp.TNat, to_ = sp.TAddress, token_id = sp.TNat).layout(("to_", ("token_id", "amount"))))).layout(("from_", "txs"))), params.collateral_contract, entry_point='transfer').open_some())
    self.data.deposits[params.deposit_id] = sp.record(collateral_contract = params.collateral_contract, collateral_token_id = params.collateral_token_id, deposit_amount = params.amount)

  @sp.entry_point
  def withdraw(self, params):
    sp.set_type(params.recipient, sp.TAddress)
    sp.set_type(params.deposit_id, sp.TNat)
    sp.verify(self.data.owner == sp.sender, 'Ownable: caller is not the owner')
    sp.verify(self.data.deposits.contains(params.deposit_id))
    sp.set_type(sp.self_address, sp.TAddress)
    sp.set_type(params.recipient, sp.TAddress)
    sp.set_type(self.data.deposits[params.deposit_id].collateral_contract, sp.TAddress)
    sp.set_type(self.data.deposits[params.deposit_id].deposit_amount, sp.TNat)
    sp.set_type(self.data.deposits[params.deposit_id].collateral_token_id, sp.TNat)
    sp.transfer(sp.list([sp.set_type_expr(sp.record(from_ = sp.self_address, txs = sp.list([sp.record(to_ = params.recipient, token_id = self.data.deposits[params.deposit_id].collateral_token_id, amount = self.data.deposits[params.deposit_id].deposit_amount)])), sp.TRecord(from_ = sp.TAddress, txs = sp.TList(sp.TRecord(amount = sp.TNat, to_ = sp.TAddress, token_id = sp.TNat).layout(("to_", ("token_id", "amount"))))).layout(("from_", "txs")))]), sp.tez(0), sp.contract(sp.TList(sp.TRecord(from_ = sp.TAddress, txs = sp.TList(sp.TRecord(amount = sp.TNat, to_ = sp.TAddress, token_id = sp.TNat).layout(("to_", ("token_id", "amount"))))).layout(("from_", "txs"))), self.data.deposits[params.deposit_id].collateral_contract, entry_point='transfer').open_some())
    del self.data.deposits[params.deposit_id]

sp.add_compilation_target("test", Contract())