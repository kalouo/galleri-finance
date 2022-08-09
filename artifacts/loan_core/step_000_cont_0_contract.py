import smartpy as sp

class Contract(sp.Contract):
  def __init__(self):
    self.init_type(sp.TRecord(borrower_note_address = sp.TAddress, collateral_vault_address = sp.TAddress, currency_precision = sp.TBigMap(sp.TAddress, sp.TNat), interest_fee = sp.TNat, lender_note_address = sp.TAddress, loan_id = sp.TNat, loans_by_id = sp.TBigMap(sp.TNat, sp.TRecord(collateral_contract = sp.TAddress, collateral_token_id = sp.TNat, loan_denomination_contract = sp.TAddress, loan_denomination_id = sp.TNat, loan_duration = sp.TInt, loan_origination_timestamp = sp.TTimestamp, loan_principal_amount = sp.TNat, maximum_interest_amount = sp.TNat, time_adjustable_interest = sp.TBool).layout(((("collateral_contract", "collateral_token_id"), ("loan_denomination_contract", "loan_denomination_id")), (("loan_duration", "loan_origination_timestamp"), ("loan_principal_amount", ("maximum_interest_amount", "time_adjustable_interest")))))), owner = sp.TAddress, permitted_currencies = sp.TBigMap(sp.TAddress, sp.TBool), processing_fee = sp.TNat).layout(((("borrower_note_address", "collateral_vault_address"), ("currency_precision", ("interest_fee", "lender_note_address"))), (("loan_id", "loans_by_id"), ("owner", ("permitted_currencies", "processing_fee"))))))
    self.init(borrower_note_address = sp.address('tz1Ke2h7sDdakHJQh8WX4Z372du1KChsksyU'),
              collateral_vault_address = sp.address('tz1Ke2h7sDdakHJQh8WX4Z372du1KChsksyU'),
              currency_precision = {},
              interest_fee = 0,
              lender_note_address = sp.address('tz1Ke2h7sDdakHJQh8WX4Z372du1KChsksyU'),
              loan_id = 0,
              loans_by_id = {},
              owner = sp.address('tz1Ke2h7sDdakHJQh8WX4Z372du1KChsksyU'),
              permitted_currencies = {},
              processing_fee = 0)

  @sp.entry_point
  def claim(self, params):
    sp.set_type(params, sp.TNat)
    sp.verify(self.data.loans_by_id.contains(params), 'NON-EXISTENT LOAN')
    sp.verify(sp.sender == sp.view("owner_of", self.data.lender_note_address, params, sp.TAddress).open_some(), 'UNAUTHORIZED CALLER')
    sp.verify(sp.now > sp.add_seconds(self.data.loans_by_id[params].loan_origination_timestamp, self.data.loans_by_id[params].loan_duration), 'NOT_EXPIRED')
    sp.transfer(sp.record(deposit_id = params, recipient = sp.view("owner_of", self.data.lender_note_address, params, sp.TAddress).open_some()), sp.tez(0), sp.contract(sp.TRecord(deposit_id = sp.TNat, recipient = sp.TAddress).layout(("deposit_id", "recipient")), self.data.collateral_vault_address, entry_point='withdraw').open_some())
    sp.set_type(params, sp.TNat)
    sp.transfer(params, sp.tez(0), sp.contract(sp.TNat, self.data.borrower_note_address, entry_point='burn').open_some())
    sp.set_type(params, sp.TNat)
    sp.transfer(params, sp.tez(0), sp.contract(sp.TNat, self.data.lender_note_address, entry_point='burn').open_some())
    del self.data.loans_by_id[params]

  @sp.entry_point
  def repay(self, params):
    sp.set_type(params, sp.TNat)
    sp.verify(self.data.loans_by_id.contains(params), 'NON-EXISTENT LOAN')
    sp.verify(sp.sender == sp.view("owner_of", self.data.borrower_note_address, params, sp.TAddress).open_some(), 'UNAUTHORIZED CALLER')
    sp.verify(sp.now <= sp.add_seconds(self.data.loans_by_id[params].loan_origination_timestamp, self.data.loans_by_id[params].loan_duration), 'EXPIRED')
    sp.set_type(self._compute_interest_rate(sp.record(currency_precision = self.data.currency_precision[self.data.loans_by_id[params].loan_denomination_contract], loan_duration = self.data.loans_by_id[params].loan_duration, loan_origination_timestamp = self.data.loans_by_id[params].loan_origination_timestamp, maximum_interest_amount = self.data.loans_by_id[params].maximum_interest_amount, time_adjustable_interest = self.data.loans_by_id[params].time_adjustable_interest)), sp.TNat)
    sp.set_type(self.data.currency_precision[self.data.loans_by_id[params].loan_denomination_contract], sp.TNat)
    sp.set_type(self._compute_interest_rate(sp.record(currency_precision = self.data.currency_precision[self.data.loans_by_id[params].loan_denomination_contract], loan_duration = self.data.loans_by_id[params].loan_duration, loan_origination_timestamp = self.data.loans_by_id[params].loan_origination_timestamp, maximum_interest_amount = self.data.loans_by_id[params].maximum_interest_amount, time_adjustable_interest = self.data.loans_by_id[params].time_adjustable_interest)), sp.TNat)
    sp.set_type(self.data.interest_fee, sp.TNat)
    sp.set_type(self.data.currency_precision[self.data.loans_by_id[params].loan_denomination_contract], sp.TNat)
    sp.set_type(sp.view("owner_of", self.data.borrower_note_address, params, sp.TAddress).open_some(), sp.TAddress)
    sp.set_type(sp.self_address, sp.TAddress)
    sp.set_type(self.data.loans_by_id[params].loan_denomination_contract, sp.TAddress)
    sp.set_type(self.data.loans_by_id[params].loan_principal_amount + self._compute_interest_rate(sp.record(currency_precision = self.data.currency_precision[self.data.loans_by_id[params].loan_denomination_contract], loan_duration = self.data.loans_by_id[params].loan_duration, loan_origination_timestamp = self.data.loans_by_id[params].loan_origination_timestamp, maximum_interest_amount = self.data.loans_by_id[params].maximum_interest_amount, time_adjustable_interest = self.data.loans_by_id[params].time_adjustable_interest)), sp.TNat)
    sp.set_type(self.data.loans_by_id[params].loan_denomination_id, sp.TNat)
    sp.transfer(sp.list([sp.set_type_expr(sp.record(from_ = sp.view("owner_of", self.data.borrower_note_address, params, sp.TAddress).open_some(), txs = sp.list([sp.record(to_ = sp.self_address, token_id = self.data.loans_by_id[params].loan_denomination_id, amount = self.data.loans_by_id[params].loan_principal_amount + self._compute_interest_rate(sp.record(currency_precision = self.data.currency_precision[self.data.loans_by_id[params].loan_denomination_contract], loan_duration = self.data.loans_by_id[params].loan_duration, loan_origination_timestamp = self.data.loans_by_id[params].loan_origination_timestamp, maximum_interest_amount = self.data.loans_by_id[params].maximum_interest_amount, time_adjustable_interest = self.data.loans_by_id[params].time_adjustable_interest)))])), sp.TRecord(from_ = sp.TAddress, txs = sp.TList(sp.TRecord(amount = sp.TNat, to_ = sp.TAddress, token_id = sp.TNat).layout(("to_", ("token_id", "amount"))))).layout(("from_", "txs")))]), sp.tez(0), sp.contract(sp.TList(sp.TRecord(from_ = sp.TAddress, txs = sp.TList(sp.TRecord(amount = sp.TNat, to_ = sp.TAddress, token_id = sp.TNat).layout(("to_", ("token_id", "amount"))))).layout(("from_", "txs"))), self.data.loans_by_id[params].loan_denomination_contract, entry_point='transfer').open_some())
    sp.set_type(sp.self_address, sp.TAddress)
    sp.set_type(sp.view("owner_of", self.data.lender_note_address, params, sp.TAddress).open_some(), sp.TAddress)
    sp.set_type(self.data.loans_by_id[params].loan_denomination_contract, sp.TAddress)
    sp.set_type(sp.as_nat((self.data.loans_by_id[params].loan_principal_amount + self._compute_interest_rate(sp.record(currency_precision = self.data.currency_precision[self.data.loans_by_id[params].loan_denomination_contract], loan_duration = self.data.loans_by_id[params].loan_duration, loan_origination_timestamp = self.data.loans_by_id[params].loan_origination_timestamp, maximum_interest_amount = self.data.loans_by_id[params].maximum_interest_amount, time_adjustable_interest = self.data.loans_by_id[params].time_adjustable_interest))) - ((self._compute_interest_rate(sp.record(currency_precision = self.data.currency_precision[self.data.loans_by_id[params].loan_denomination_contract], loan_duration = self.data.loans_by_id[params].loan_duration, loan_origination_timestamp = self.data.loans_by_id[params].loan_origination_timestamp, maximum_interest_amount = self.data.loans_by_id[params].maximum_interest_amount, time_adjustable_interest = self.data.loans_by_id[params].time_adjustable_interest)) * ((self.data.interest_fee * self.data.currency_precision[self.data.loans_by_id[params].loan_denomination_contract]) // 10000)) // self.data.currency_precision[self.data.loans_by_id[params].loan_denomination_contract])), sp.TNat)
    sp.set_type(self.data.loans_by_id[params].loan_denomination_id, sp.TNat)
    sp.transfer(sp.list([sp.set_type_expr(sp.record(from_ = sp.self_address, txs = sp.list([sp.record(to_ = sp.view("owner_of", self.data.lender_note_address, params, sp.TAddress).open_some(), token_id = self.data.loans_by_id[params].loan_denomination_id, amount = sp.as_nat((self.data.loans_by_id[params].loan_principal_amount + self._compute_interest_rate(sp.record(currency_precision = self.data.currency_precision[self.data.loans_by_id[params].loan_denomination_contract], loan_duration = self.data.loans_by_id[params].loan_duration, loan_origination_timestamp = self.data.loans_by_id[params].loan_origination_timestamp, maximum_interest_amount = self.data.loans_by_id[params].maximum_interest_amount, time_adjustable_interest = self.data.loans_by_id[params].time_adjustable_interest))) - ((self._compute_interest_rate(sp.record(currency_precision = self.data.currency_precision[self.data.loans_by_id[params].loan_denomination_contract], loan_duration = self.data.loans_by_id[params].loan_duration, loan_origination_timestamp = self.data.loans_by_id[params].loan_origination_timestamp, maximum_interest_amount = self.data.loans_by_id[params].maximum_interest_amount, time_adjustable_interest = self.data.loans_by_id[params].time_adjustable_interest)) * ((self.data.interest_fee * self.data.currency_precision[self.data.loans_by_id[params].loan_denomination_contract]) // 10000)) // self.data.currency_precision[self.data.loans_by_id[params].loan_denomination_contract])))])), sp.TRecord(from_ = sp.TAddress, txs = sp.TList(sp.TRecord(amount = sp.TNat, to_ = sp.TAddress, token_id = sp.TNat).layout(("to_", ("token_id", "amount"))))).layout(("from_", "txs")))]), sp.tez(0), sp.contract(sp.TList(sp.TRecord(from_ = sp.TAddress, txs = sp.TList(sp.TRecord(amount = sp.TNat, to_ = sp.TAddress, token_id = sp.TNat).layout(("to_", ("token_id", "amount"))))).layout(("from_", "txs"))), self.data.loans_by_id[params].loan_denomination_contract, entry_point='transfer').open_some())
    sp.transfer(sp.record(deposit_id = params, recipient = sp.view("owner_of", self.data.borrower_note_address, params, sp.TAddress).open_some()), sp.tez(0), sp.contract(sp.TRecord(deposit_id = sp.TNat, recipient = sp.TAddress).layout(("deposit_id", "recipient")), self.data.collateral_vault_address, entry_point='withdraw').open_some())
    sp.set_type(params, sp.TNat)
    sp.transfer(params, sp.tez(0), sp.contract(sp.TNat, self.data.borrower_note_address, entry_point='burn').open_some())
    sp.set_type(params, sp.TNat)
    sp.transfer(params, sp.tez(0), sp.contract(sp.TNat, self.data.lender_note_address, entry_point='burn').open_some())
    del self.data.loans_by_id[params]

  @sp.entry_point
  def set_collateral_vault(self, params):
    sp.set_type(params, sp.TAddress)
    sp.verify(self.data.owner == sp.sender, 'Ownable: caller is not the owner')
    self.data.collateral_vault_address = params

  @sp.entry_point
  def set_interest_fee(self, params):
    sp.set_type(params, sp.TNat)
    sp.verify(self.data.owner == sp.sender, 'Ownable: caller is not the owner')
    sp.verify(params <= 2000, 'INVALID_FEE')
    self.data.interest_fee = params

  @sp.entry_point
  def set_loan_note_contracts(self, params):
    sp.set_type(params.lender_note_address, sp.TAddress)
    sp.set_type(params.borrower_note_address, sp.TAddress)
    sp.verify(self.data.owner == sp.sender, 'Ownable: caller is not the owner')
    self.data.lender_note_address = params.lender_note_address
    self.data.borrower_note_address = params.borrower_note_address

  @sp.entry_point
  def set_processing_fee(self, params):
    sp.set_type(params, sp.TNat)
    sp.verify(self.data.owner == sp.sender, 'Ownable: caller is not the owner')
    sp.verify(params <= 250, 'INVALID_FEE')
    self.data.processing_fee = params

  @sp.entry_point
  def start_loan(self, params):
    sp.set_type(params.lender, sp.TAddress)
    sp.set_type(params.borrower, sp.TAddress)
    sp.set_type(params.loan_denomination_contract, sp.TAddress)
    sp.set_type(params.loan_principal_amount, sp.TNat)
    sp.set_type(params.maximum_interest_amount, sp.TNat)
    sp.set_type(params.loan_denomination_id, sp.TNat)
    sp.set_type(params.collateral_contract, sp.TAddress)
    sp.set_type(params.collateral_token_id, sp.TNat)
    sp.set_type(params.loan_duration, sp.TInt)
    sp.set_type(params.time_adjustable_interest, sp.TBool)
    sp.verify((self.data.permitted_currencies.contains(params.loan_denomination_contract)) == True, 'CURRENCY_NOT_AUTHORIZED')
    self.data.loans_by_id[self.data.loan_id] = sp.record(collateral_contract = params.collateral_contract, collateral_token_id = params.collateral_token_id, loan_denomination_contract = params.loan_denomination_contract, loan_denomination_id = params.loan_denomination_id, loan_duration = params.loan_duration, loan_origination_timestamp = sp.now, loan_principal_amount = params.loan_principal_amount, maximum_interest_amount = params.maximum_interest_amount, time_adjustable_interest = params.time_adjustable_interest)
    sp.transfer(sp.record(amount = 1, collateral_contract = params.collateral_contract, collateral_token_id = params.collateral_token_id, deposit_id = self.data.loan_id, depositor = params.borrower), sp.tez(0), sp.contract(sp.TRecord(amount = sp.TNat, collateral_contract = sp.TAddress, collateral_token_id = sp.TNat, deposit_id = sp.TNat, depositor = sp.TAddress).layout((("amount", "collateral_contract"), ("collateral_token_id", ("deposit_id", "depositor")))), self.data.collateral_vault_address, entry_point='deposit').open_some())
    sp.set_type(params.lender, sp.TAddress)
    sp.set_type(sp.self_address, sp.TAddress)
    sp.set_type(params.loan_denomination_contract, sp.TAddress)
    sp.set_type(params.loan_principal_amount, sp.TNat)
    sp.set_type(params.loan_denomination_id, sp.TNat)
    sp.transfer(sp.list([sp.set_type_expr(sp.record(from_ = params.lender, txs = sp.list([sp.record(to_ = sp.self_address, token_id = params.loan_denomination_id, amount = params.loan_principal_amount)])), sp.TRecord(from_ = sp.TAddress, txs = sp.TList(sp.TRecord(amount = sp.TNat, to_ = sp.TAddress, token_id = sp.TNat).layout(("to_", ("token_id", "amount"))))).layout(("from_", "txs")))]), sp.tez(0), sp.contract(sp.TList(sp.TRecord(from_ = sp.TAddress, txs = sp.TList(sp.TRecord(amount = sp.TNat, to_ = sp.TAddress, token_id = sp.TNat).layout(("to_", ("token_id", "amount"))))).layout(("from_", "txs"))), params.loan_denomination_contract, entry_point='transfer').open_some())
    sp.set_type(params.loan_principal_amount, sp.TNat)
    sp.set_type(self.data.currency_precision[params.loan_denomination_contract], sp.TNat)
    sp.set_type(params.loan_principal_amount, sp.TNat)
    sp.set_type(self.data.processing_fee, sp.TNat)
    sp.set_type(self.data.currency_precision[params.loan_denomination_contract], sp.TNat)
    sp.set_type(sp.self_address, sp.TAddress)
    sp.set_type(params.borrower, sp.TAddress)
    sp.set_type(params.loan_denomination_contract, sp.TAddress)
    sp.set_type(sp.as_nat(params.loan_principal_amount - ((params.loan_principal_amount * ((self.data.processing_fee * self.data.currency_precision[params.loan_denomination_contract]) // 10000)) // self.data.currency_precision[params.loan_denomination_contract])), sp.TNat)
    sp.set_type(params.loan_denomination_id, sp.TNat)
    sp.transfer(sp.list([sp.set_type_expr(sp.record(from_ = sp.self_address, txs = sp.list([sp.record(to_ = params.borrower, token_id = params.loan_denomination_id, amount = sp.as_nat(params.loan_principal_amount - ((params.loan_principal_amount * ((self.data.processing_fee * self.data.currency_precision[params.loan_denomination_contract]) // 10000)) // self.data.currency_precision[params.loan_denomination_contract])))])), sp.TRecord(from_ = sp.TAddress, txs = sp.TList(sp.TRecord(amount = sp.TNat, to_ = sp.TAddress, token_id = sp.TNat).layout(("to_", ("token_id", "amount"))))).layout(("from_", "txs")))]), sp.tez(0), sp.contract(sp.TList(sp.TRecord(from_ = sp.TAddress, txs = sp.TList(sp.TRecord(amount = sp.TNat, to_ = sp.TAddress, token_id = sp.TNat).layout(("to_", ("token_id", "amount"))))).layout(("from_", "txs"))), params.loan_denomination_contract, entry_point='transfer').open_some())
    sp.set_type(params.borrower, sp.TAddress)
    sp.transfer(sp.list([sp.set_type_expr(sp.record(token_id = self.data.loan_id, to = params.borrower, metadata = {'decimals' : sp.bytes('0x30'), 'name' : sp.bytes('0x4c656e64696e67204c6f616e4e6f7465'), 'symbol' : sp.bytes('0x4c4e')}), sp.TRecord(metadata = sp.TMap(sp.TString, sp.TBytes), to = sp.TAddress, token_id = sp.TNat).layout(("token_id", ("to", "metadata"))))]), sp.tez(0), sp.contract(sp.TList(sp.TRecord(metadata = sp.TMap(sp.TString, sp.TBytes), to = sp.TAddress, token_id = sp.TNat).layout(("token_id", ("to", "metadata")))), self.data.borrower_note_address, entry_point='mint').open_some())
    sp.set_type(params.lender, sp.TAddress)
    sp.transfer(sp.list([sp.set_type_expr(sp.record(token_id = self.data.loan_id, to = params.lender, metadata = {'decimals' : sp.bytes('0x30'), 'name' : sp.bytes('0x4c656e64696e67204c6f616e4e6f7465'), 'symbol' : sp.bytes('0x4c4e')}), sp.TRecord(metadata = sp.TMap(sp.TString, sp.TBytes), to = sp.TAddress, token_id = sp.TNat).layout(("token_id", ("to", "metadata"))))]), sp.tez(0), sp.contract(sp.TList(sp.TRecord(metadata = sp.TMap(sp.TString, sp.TBytes), to = sp.TAddress, token_id = sp.TNat).layout(("token_id", ("to", "metadata")))), self.data.lender_note_address, entry_point='mint').open_some())
    self.data.loan_id += 1

  @sp.entry_point
  def whitelist_currency(self, params):
    sp.set_type(params.currency, sp.TAddress)
    sp.set_type(params.precision, sp.TNat)
    sp.verify(self.data.owner == sp.sender, 'Ownable: caller is not the owner')
    self.data.permitted_currencies[params.currency] = True
    self.data.currency_precision[params.currency] = params.precision

  @sp.private_lambda()
  def _compute_interest_rate(_x0):
    sp.if _x0.time_adjustable_interest == True:
      sp.set_type(_x0.maximum_interest_amount, sp.TNat)
      sp.set_type((sp.as_nat(sp.now - _x0.loan_origination_timestamp) * 10000) // sp.as_nat(_x0.loan_duration), sp.TNat)
      sp.set_type(_x0.currency_precision, sp.TNat)
      sp.result((_x0.maximum_interest_amount * ((((sp.as_nat(sp.now - _x0.loan_origination_timestamp) * 10000) // sp.as_nat(_x0.loan_duration)) * _x0.currency_precision) // 10000)) // _x0.currency_precision)
    sp.else:
      sp.result(_x0.maximum_interest_amount)

sp.add_compilation_target("test", Contract())