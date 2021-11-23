from brownie import accounts, EscrowInfrastructure
from datetime import datetime, timezone
import json

def current_utc_timestamp():
    return int(datetime.now(timezone.utc).timestamp())

def main():
    # Constants
    escrowDepositor = accounts[2]
    escrowBeneficiary = accounts[3]
    agent = accounts[0]
    timestamp = current_utc_timestamp()+60
    with open ('../contract_library/contract_addresses.json') as f:
        addresses = json.load(f)
    clientContract = EscrowInfrastructure.at(addresses["KhronusClient"])
    txt = clientContract.openEscrow(escrowBeneficiary, timestamp, agent, {'from':escrowDepositor,'value':"1 ether"})
    print(txt.events['Transfer'][1]['data'], str(txt.events['AlertDispatched']['_alertID']), timestamp)