from brownie import accounts, EscrowInfrastructure
from datetime import datetime, time
import json


def main():
    # Constants
    escrowDepositor = accounts[2]
    escrowBeneficiary = accounts[3]
    timestamp = int(datetime.utcnow().timestamp())+120
    with open ('../contract_library/contract_addresses.json') as f:
        addresses = json.load(f)
    clientContract = EscrowInfrastructure.at(addresses["KhronusClient"])
    txt = clientContract.openEscrow(escrowBeneficiary, timestamp, {'from':escrowDepositor})
    print(txt.events['Transfer'][1]['data'], str(txt.events['AlertDispatched']['_alertID']), timestamp)