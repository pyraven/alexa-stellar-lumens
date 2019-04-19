import json
from stellar_base.keypair import Keypair
from pprint import pprint
import requests

def get_balance(addr):
	bank = "https://horizon-testnet.stellar.org/accounts/"
	account = bank + addr
	r = requests.get(account)
	balances = r.json()['balances']
	amount = float(''.join(i['balance'] for i in balances))
	total = round(amount, 2)
	return total

def create_account():
    key_pair = Keypair.random()
    friendbot_url = 'https://friendbot.stellar.org'
    r = requests.get(friendbot_url, params={'addr': key_pair.address().decode()})
    public_key = key_pair.address().decode()
    private_key = key_pair.seed().decode()
    return {"public": public_key, "private": private_key}

# mine
account_one = create_account()

# friend a
account_two = create_account()

# friend b
account_three = create_account()

# balances
account_one_balance = get_balance(account_one['public'])
account_two_balance = get_balance(account_two['public'])
account_three_balance = get_balance(account_three['public'])

print("First Account, Balance")
print(account_one, account_one_balance)
print("=============")
print("Second Account")
print(account_two, account_two_balance)
print("=============")
print("Third Account")
print(account_three, account_three_balance)
print("=============")
