// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "interfaces/clients/KhronClientInterface.sol";

contract InterestDeposit {

    struct account {
        uint256 initialCapital;
        uint256 openingTimeStamp;
        uint256 balance;
        string lastCall; //only for testing this will be bytes if needed in production
    }
    uint256 constant INTEREST = 1;

    mapping (address => account) private accounts; 

    constructor() {

    }
    function openAccount(address _address, uint _initialCapital) external {
        accounts[_address].initialCapital = _initialCapital;
        accounts[_address].openingTimeStamp = block.timestamp;
        accounts[_address].balance = _initialCapital;
        accounts[_address].lastCall = "";
    }

    function seeBalance() external view returns(uint256) {
        return accounts[msg.sender].balance;
    }

    function deposit(address _address, uint256 _amount) external {
        _deposit(_address, _amount);
    }

    function _deposit(address _address, uint256 _amount) internal {
        accounts[_address].balance += _amount;
    }

    function KhronTask_lever(bytes memory requestID, address actionID) external{ // signature '0x33c731c3'
        accounts[actionID].balance += INTEREST;
    }
}