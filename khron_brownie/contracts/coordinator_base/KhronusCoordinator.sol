// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "interfaces/token/KhronTokenInterface.sol";

contract KhronusCoordinator {

    event ClientFunded(address indexed _client, address indexed _requester, uint256 _amount);
    KhronTokenInterface private khronus;

    // Data Variables

    struct clientContract {
        uint balance;
        uint requests;
        uint standing;
    }

    mapping (address => clientContract) clientRegistry;

    constructor () {
    }

    // Business Logic Function Section

    /* Registry Client Contract function
    */

    function fundClient(address clientContract, uint256 deposit) external returns(bool){
        require (khronus.balanceOf(msg.sender) >= deposit, "Not enough funds to transfer");
        require (khronus.allowance(msg.sender, address(this)) >= deposit, "Not enough allowance to transfer funds");
        khronus.transferFrom(msg.sender, clientContract, deposit);
        clientRegistry[clientContract].balance += deposit;
        emit ClientFunded(clientContract, msg.sender, deposit);
        return true;
    }

    //View functions

    function creditOf(address clientContract) public view returns (uint256){
        return clientRegistry[clientContract].balance;
    }

    //Request to node functions
    function setKhronTokenAddress(
        address khronAddress
        )
        external
        {
            khronus = KhronTokenInterface(khronAddress);
        }

    function setKhronTab(
        address _nodeContract, //this has to be a khron token recipient identifies the khron_node handling the request 
        uint256 _khronFee,
        bytes memory _data
        )
        external
        returns (bool)
        {
            return khronus.transferAndCall(_nodeContract,_khronFee,_data);
        }
}