//SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.1;

contract khron_logger {
    
    event Transfer (address indexed _to, string data);

    
    function checking() public pure returns(bytes4) {
        return this.transfer_eth.selector;
    }

    function transfer_eth(address _to, string memory data) public payable {
        emit Transfer(_to, data);
    }

}
