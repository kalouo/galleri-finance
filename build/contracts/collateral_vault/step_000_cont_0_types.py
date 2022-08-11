import smartpy as sp

tstorage = sp.TRecord(deposits = sp.TBigMap(sp.TNat, sp.TRecord(collateral_contract = sp.TAddress, collateral_token_id = sp.TNat, deposit_amount = sp.TNat).layout(("collateral_contract", ("collateral_token_id", "deposit_amount")))), owner = sp.TAddress).layout(("deposits", "owner"))
tparameter = sp.TVariant(deposit = sp.TRecord(amount = sp.TNat, collateral_contract = sp.TAddress, collateral_token_id = sp.TNat, deposit_id = sp.TNat, depositor = sp.TAddress).layout((("amount", "collateral_contract"), ("collateral_token_id", ("deposit_id", "depositor")))), withdraw = sp.TRecord(deposit_id = sp.TNat, recipient = sp.TAddress).layout(("deposit_id", "recipient"))).layout(("deposit", "withdraw"))
tprivates = { }
tviews = { }
