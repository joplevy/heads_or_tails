import sys
import time
import pprint

# from web3.providers.eth_tester import EthereumTesterProvider
from web3 import Web3, HTTPProvider
from solc import compile_source


def compile_source_file(file_path):
   with open(file_path, 'r') as f:
      source = f.read()

   return compile_source(source)


def deploy_contract(w3, contract_interface, acct):
    gas_estimate = w3.eth.contract(
        abi=contract_interface['abi'],
        bytecode=contract_interface['bin']).constructor(True).estimateGas({
            'from': acct.address,
            'nonce': w3.eth.getTransactionCount(acct.address),
            'gasPrice': w3.toWei('21', 'gwei'),
            'value': w3.toWei('10', 'finney')})
    print("Gas estimate to deploy: {0}\n".format(gas_estimate))
    construct_txn = w3.eth.contract(
        abi=contract_interface['abi'],
        bytecode=contract_interface['bin']).constructor(True).buildTransaction({
            'from': acct.address,
            'nonce': w3.eth.getTransactionCount(acct.address),
            'gas': gas_estimate,
            'gasPrice': w3.toWei('21', 'gwei'),
            'value': w3.toWei('10', 'finney')})
    
    signed = acct.signTransaction(construct_txn)
    tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
    
    res =  w3.eth.waitForTransactionReceipt(tx_hash)
    pprint.pprint(dict(res))
    address = res['contractAddress']
    return address


def wait_for_receipt(w3, tx_hash, poll_interval):
   while True:
       tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
       if tx_receipt:
         return tx_receipt
       time.sleep(poll_interval)

API_KEY = '2df942fba0555a74a19ce543ca29755e776974abc422ad04ce933f0b88175fb9'
API_KEY2 = '96dd3da1947b094a2aea519eaf661a5e1f4f13400ffc0e98d79cec531eac569b'
infura_provider = HTTPProvider('https://ropsten.infura.io/')
w3 = Web3(infura_provider)
acct = w3.eth.account.privateKeyToAccount(API_KEY)
acct2 = w3.eth.account.privateKeyToAccount(API_KEY2)
compiled_sol = compile_source_file('HoT.sol')

contract_id, contract_interface = compiled_sol.popitem()

address = deploy_contract(w3, contract_interface, acct)
print("Deployed {0} to: {1}\n".format(contract_id, address))

store_var_contract = w3.eth.contract(
   address=address,
   abi=contract_interface['abi'],
   bytecode=contract_interface['bin'])

gas_estimate = store_var_contract.functions.joinGame().estimateGas({
                'from': acct2.address,
                'gasPrice': w3.toWei('21', 'gwei'),
                'value': w3.toWei('10', 'finney')})
print("Gas estimate to transact with joinGame: {0}\n".format(gas_estimate))

if gas_estimate < 100000:
    print("Sending transaction to joinGame()\n")
    construct_txn = store_var_contract.functions.joinGame().buildTransaction({
                'from': acct2.address,
                'nonce': w3.eth.getTransactionCount(acct2.address),
                'gas': gas_estimate,
                'gasPrice': w3.toWei('21', 'gwei'),
                'value': w3.toWei('10', 'finney')})

    signed = acct2.signTransaction(construct_txn)
    tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
    receipt =  w3.eth.waitForTransactionReceipt(tx_hash)
    print("Transaction receipt mined: \n")
    pprint.pprint(dict(receipt))
else:
    print("Gas cost exceeds 100000")