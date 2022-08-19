from brownie import accounts, EscrowInfrastructure
from datetime import datetime, timezone
import json

def current_utc_timestamp():
    return int(datetime.now(timezone.utc).timestamp())

def main():
    # Constants
    escrowDepositor = accounts.load('testing_account')
    escrowBeneficiary = "0xb04195e45174D5a55e660C0D1127f182EFdb8cD9"
    agent = "0xb04195e45174D5a55e660C0D1127f182EFdb8cD9"
    timestamp = current_utc_timestamp()+120
    with open ('../contract_library/contract_addresses_deployment.json') as f:
        addresses = json.load(f)
    clientContract = EscrowInfrastructure.at(addresses["KhronusClient"])
    txt = clientContract.openEscrow(escrowBeneficiary, timestamp, agent, {'from':escrowDepositor,'value':"0.005 ether"})
    print( txt.events, timestamp)