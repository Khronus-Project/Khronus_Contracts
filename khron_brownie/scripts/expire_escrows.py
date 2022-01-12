from brownie import accounts, EscrowInfrastructure
import json

def main():
    latestdate = "2021-12-27T08:58:55.318Z"
    path = "../references/escrows.json"
    escrowInfrastructureAddress = "0xdf75F4D728812d76113a48E0da18F3AfA96E5179"
    escrowDepositor = accounts.load('testing_account')
    with open(path) as json_object:
        escrow_object = json.load(json_object)
    escrowInfrastructure = EscrowInfrastructure.at("0xdf75F4D728812d76113a48E0da18F3AfA96E5179")
    for escrow in escrow_object:
        status = escrowInfrastructure.getStatus(escrow["escrowID"])
        if status == 1:
            print(f'epirying escrow {escrow["escrowID"]}')
            escrowInfrastructure.expiryManually(escrow["escrowID"],{"from":escrowDepositor})
        else:
            print(f'escrow {escrow["escrowID"]} already expired')
    
