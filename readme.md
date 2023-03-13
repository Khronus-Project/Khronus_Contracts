# Khronus Protocol Contracts
## Description
The Khronus protocols is made of two parts:
- The protocol contracts
    - Protocol contracts in turn are divided in:
        - Utility contracts:
            - Khronus Client Base
            - Khronus Node Base
        - These are Contracts that are inherited by all client contracts and node operator contracts.
        - The utilities are maintained in the following repository.
            - https://github.com/Khronus-Project/Khronus_utils
        - Protocol Contracts
            - Khronus Coordinator:
                This contract is the heart of the protocol and lives here.
            - Demo Contracts:
                These are contracts that serve to test the Coordinator contract, two mock client contracts and one mock node operator contract. These also live here.
- The node application
    - This is the validator that app that serves alerts. It can be found in the following repository:
        - https://github.com/Khronus-Project/Khronus_Node 

## The development environment
- The khronus contracts are developed under brownie-eth the python framework for web3 development. The contracts are written in solidity but all interactions with the contracts is supported by Python and Python web3 library. 
- To install the contracts development environment clone this repository, create a virtual environment and then install eth-brownie.
- The khron_brownie folder contains all the contracts. To interact with the contracts you need an Ethereum compatible network, either in a real testnet or through a local mock network through Ganache https://www.trufflesuite.com/ganache. 
- To install ganache and connected to the brownie environent follow the steps in the following video. https://www.youtube.com/watch?v=yJQJ7pw_9C0
- Once the network is configured the scripts and tests to interact with the contracts will work. 
