// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

abstract contract KhronusNode {
    event RequestReceived(
        address indexed _sender,
        uint256 _value,
        bytes _data
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