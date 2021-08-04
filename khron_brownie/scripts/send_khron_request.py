from brownie import accounts, EscrowInfrastructure
import json


def main():
    # Constants
    escrowDepositor = accounts[2]
    escrowBeneficiary = accounts[3]
    timestamp = 1626521216
    with open ('../contract_library/contract_addresses.json') as f:
        addresses = json.load(f)
    clientContract = EscrowInfrastructure.at(addresses["KhronusClient"])
    txt = clientContract.openEscrow(escrowBeneficiary, timestamp, {'from':escrowDepositor})
    print(txt.events)