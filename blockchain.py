import json
import os
from web3 import Web3

WEB3_PROVIDER = "https://bsc-dataseed.binance.org/"
CONTRACT_ADDRESS = "0xd5baB4C1b92176f9690c0d2771EDbF18b73b8181"
AIRDROP_WALLET = "0xd5F168CFa6a68C21d7849171D6Aa5DDc9307E544"
PRIVATE_KEY = os.getenv("PRIVATE_KEY")

web3 = Web3(Web3.HTTPProvider(WEB3_PROVIDER))
contract_abi = [...]  # اینجا ABI توکن وارد شود
contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=contract_abi)

# 🔹 ارسال توکن به کاربر
def send_tokens(user_wallet, amount):
    nonce = web3.eth.get_transaction_count(AIRDROP_WALLET)
    tx = contract.functions.transfer(user_wallet, amount).build_transaction({
        'chainId': 56,
        'gas': 200000,
        'gasPrice': web3.to_wei('5', 'gwei'),
        'nonce': nonce
    })
    signed_tx = web3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    return web3.to_hex(tx_hash)

# 🔹 ذخیره تراکنش در JSON
def save_transaction(telegram_id, tx_hash, amount):
    transactions = {}
    if os.path.exists("transactions.json"):
        with open("transactions.json", "r") as file:
            transactions = json.load(file)

    transactions[str(telegram_id)] = {"tx_hash": tx_hash, "amount": amount, "status": "Completed"}
    
    with open("transactions.json", "w") as file:
        json.dump(transactions, file, indent=4)
