import json
import web3

from web3 import Web3, HTTPProvider
from solc import compile_source
from web3.contract import ConciseContract


compiled_sol = compile_source(contract_source_code) # Compiled source code
contract_interface = compiled_sol['<stdin>:Coin']
API_KEY = '95fc8c52d1e0c634eeed9056e87e6d49454d1d161cc17fa79ed6e075cebd087b'
infura_provider = HTTPProvider('https://ropsten.infura.io/')
w3 = Web3(infura_provider)

# web3.py instance
# w3 = Web3(Web3.EthereumTesterProvider())

# set pre-funded account as sender
# w3.eth.defaultAccount = '0x866269d5B827Be2741775eA58cee58595d36bf23' #w3.eth.accounts[0]
# w3.eth.defaultAccount = '0x3125035Be7B9FF6C89eeceE3cB4FFC1748FE11FE ' #w3.eth.accounts[0]
w3.eth.accounts[0] = '0x3125035Be7B9FF6C89eeceE3cB4FFC1748FE11FE'
w3.eth.defaultAccount = w3.eth.accounts[0]

# acct = w3.eth.account.privateKeyToAccount(API_KEY)

# Instantiate and deploy contract
Greeter = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])


# Submit the transaction that deploys the contract
# tx_hash = Greeter.constructor().transact()
# signed = acct.signTransaction(construct_txn)
# Wait for the transaction to be mined, and get the transaction receipt
construct_txn = Greeter.constructor().buildTransaction({
    'from': acct.address,
    'nonce': w3.eth.getTransactionCount(acct.address),
    'gas': 1728712,
    'gasPrice': w3.toWei('21', 'gwei')})

signed = acct.signTransaction(construct_txn)

tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)

tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
# Create the contract instance with the newly-deployed address
greeter = w3.eth.contract(
    address=tx_receipt.contractAddress,
    abi=contract_interface['abi'],
)

# Display the default greeting from the contract
print('Default contract greeting: {}'.format(
    greeter.functions.greet().call()
))

print('Setting the greeting to Nihao...')
tx_hash = greeter.functions.setGreeting('Nihao')

# Wait for transaction to be mined...
# w3.eth.waitForTransactionReceipt(tx_hash)

# Display the new greeting value
print('Updated contract greeting: {}'.format(
    greeter.functions.greet().call()
))

# When issuing a lot of reads, try this more concise reader:
reader = ConciseContract(greeter)
assert reader.greet() == "Nihao"