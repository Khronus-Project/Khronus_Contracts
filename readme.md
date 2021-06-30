# Khronus Protocol Contracts
## Description
The Khronus protocols is made of two parts, the contracts and the node application. This repository hosts the contracts. 
## Contracts
The Khronus protocol contracts are the following.
- Token Contract: The token contract deploys the Khron token, the Khron token is an ERC20 token that implements the ERC677 token interface which makes it capable of transmiting data upon token transfer. For this the recipient contract has to implement the onTokenTransfer function defined in the ERC677 Receiver interface. 
- Node Contract (abstract): The Node contract is an abstract contract designed to be implemented by all Khronus nodes it provides the functionality to process the data transmitted by the Khron token. It is an abstract contract, this means it is not implemented by itself, it is implemented by the node_test.sol contract which inherits all its functionality for development and testing purposes.
- Client Contract (abstract): The Client contract is an abstract contract designed to be implemented by smart contracts that wish to make use of the Khronus protocol. It is an abstract contract, this means it is not implemented by itself, it is implemented by the client_test.sol contract which inherits all its functionality for development and testing purposes.