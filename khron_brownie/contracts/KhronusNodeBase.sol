// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "interfaces/KhronusCoordinatorInterface.sol";

abstract contract KhronusNode {
    event RequestReceived(
        address indexed sender,
        uint256 value,
        bytes data
        );
    
    KhronusCoordinatorInterface private KhronusCoordinator;
    address owner;
    address khronusCoordinator;

    function onTokenTransfer(
        address _sender, 
        uint256 _value, 
        bytes memory _data
        ) 
        external {
            emit RequestReceived(_sender,_value,_data);
        }


}