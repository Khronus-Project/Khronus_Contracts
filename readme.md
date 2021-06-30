# Khronus Protocol Contracts
## Description
The Khronus protocols is made of two parts, the contracts and the node application. This repository hosts the contracts. 
## Contracts
The Khronus protocol contracts are the following.
- Token Contract: The token contract deploys the Khron token, the Khron token is an ERC20 token that implements the ERC677 token interface which makes it capable of transmiting data upon token transfer. For this the recipient contract has to implement the onTokenTransfer function defined in the ERC677 Receiver interface. 
- Node Contract (abstract): The Node contract is an abstract contract designed to be implemented by all Khronus nodes it provides the functionality to process the data transmitted by the Khron token. It is an abstract contract, this means it is not implemented by itself, it is implemented by the node_test.sol contract which inherits all its functionality for development and testing purposes.
- Client Contract (abstract): The Client contract is an abstract contract designed to be implemented by smart contracts that wish to make use of the Khronus protocol. It is an abstract contract, this means it is not implemented by itself, it is implemented by the client_test.sol contract which inherits all its functionality for development and testing purposes.
## The development environment
- The khronus contracts are developed under brownie-eth the python framework for web3 development. The contracts are written in solidity but all interactions with the contracts is supported by Python and Python web3 library. 
- To install the contracts development environment clone this repository, create a virtual environment and then install the requirements.txt dependencies.
- The khron_brownie folder contains all the contracts. To interact with the contracts you need an Ethereum compatible network, either in a real testnet or through a local mock network through Ganache https://www.trufflesuite.com/ganache. 
- To install ganache and connected to the brownie environent follow the steps in the following video. https://www.youtube.com/watch?v=yJQJ7pw_9C0
- Once the network is configured the scripts to interact with the current demo will work. First run the 'brownie run event_prep.py' and then "brownie run send_events.py" you will see the logs of the transaction shown, if the node application is active, and listening to the right contract address the listener will react accordingly populating its database.
- The folder Contract Library and the other scripts are related to deployments in live testnets and not relevant to the development environment.
