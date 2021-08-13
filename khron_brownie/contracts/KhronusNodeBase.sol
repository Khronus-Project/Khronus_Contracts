// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

abstract contract KhronusNode {
    event RequestReceived(
        address indexed sender,
        uint256 value,
        bytes data
        );
    function onTokenTransfer(
        address _sender, 
        uint256 _value, 
        bytes memory _data
        ) 
        external {
            emit RequestReceived(_sender,_value,_data);
        }
}