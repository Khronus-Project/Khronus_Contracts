//SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.1;

contract khron_logger {
    
    event Transfer (address indexed _to, string data);

    function transfer_eth(address _to, string memory data) public payable {
        emit Transfer(_to, data);
    }

}
