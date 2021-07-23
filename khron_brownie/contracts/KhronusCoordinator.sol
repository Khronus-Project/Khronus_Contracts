// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "interfaces/KhronTokenInterface.sol";
import "OpenZeppelin/openzeppelin-contracts@4.0.0/contracts/access/Ownable.sol";

contract KhronusCoordinator is Ownable{
    //initialize interfaces

    KhronTokenInterface private khronus;
    
    // Events
    event ClientFunded(address indexed _client, address indexed _requester, uint256 _amount);
    event RequestProcessed(address indexed _client, bytes32 _requestID, bytes _data);
    
    
    // Flag variables

    enum TypeOfRequest{
        khronTab,
        powerKhron
    }

    // Data Variables

    uint callPrice;

    struct clientContract {
        address owner;
        uint credit;
        uint nonce;
        uint standing;
        uint commitedFunds;
    }

    mapping (address => clientContract) clientRegistry;

    constructor () {
        
    }

    // Business Logic Function Section

    /* Set Price Function
    */

    function setCallPrice(uint _callPrice) external onlyOwner returns(bool){
        callPrice = _callPrice;
        return true;
    }

     /* Fund Client Contract function
    */
    function fundClient(address _clientContract, uint256 _deposit) external returns(bool){
        address _owner = msg.sender;
        require (khronus.balanceOf(_owner) >= _deposit, "Not enough funds to transfer");
        require (khronus.allowance(_owner, address(this)) >= _deposit, "Not enough allowance to transfer funds");
        khronus.transferFrom(_owner, address(this), _deposit);
        clientRegistry[_clientContract].owner = _owner;
        clientRegistry[_clientContract].credit += _deposit;
        khronus.increaseApproval(_owner, _deposit);
        emit ClientFunded(_clientContract, _owner, _deposit);
        return true;
    }

    /* Request khronTab functions
    */

    //estimate cost
    function estimateKhron(TypeOfRequest _requestType, uint256 _iterations) internal returns(uint256){
        if (_requestType == TypeOfRequest.khronTab){
            if (_iterations <= 1) {
                return callPrice;
            }
            else{
                return callPrice * (_iterations+1);
            }
        }
    }

    //set khron request
    function requestKhronTab(uint _timeStamp, uint _iterations, string memory _khronTab) external returns(bytes32){
        uint _requestCost = estimateKhron(TypeOfRequest.khronTab, _iterations);
        address _requester = msg.sender;
        address _owner = clientRegistry[_requester].owner;
        require (clientRegistry[_requester].credit >= _requestCost, "Not enough funds in contract to set request");
        bytes32 _requestID = keccak256(abi.encodePacked(_requester, clientRegistry[_requester].nonce));
        clientRegistry[_requester].commitedFunds += _requestCost;
        khronus.decreaseApproval(_owner, _requestCost);
        clientRegistry[_requester].nonce += 1;
        if (_iterations <= 1){
            //create alert with the requestID
        }
        else{
            //request calendar with the requestID
        }
        emit RequestProcessed(_requester, _requestID,abi.encodePacked(_timeStamp, _iterations, _khronTab));
        return _requestID;
    }

    //set khronAlerts

    
    //set khronCalendars

    //View functions

    function creditOf(address _clientContract) public view returns (uint256){
        return clientRegistry[_clientContract].credit;
    }

    function getCallPrice() public view returns (uint){
        return callPrice;
    }

    function commitedFundsOf(address _clientContract) public view returns(uint256){
        return clientRegistry[_clientContract].commitedFunds;
    }

    //Request to node functions
    function setKhronTokenAddress(
        address _khronAddress
        )
        external
        returns (bool)
        {
            khronus = KhronTokenInterface(_khronAddress);
            return true;
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