// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;


interface KhronusCoordinatorInterface {
   
    // Interface Functions
    // Only owner and internal functions are not provided

    function fundClient(
        address clientContract, 
        uint256 deposit
        ) 
        external 
        returns(bool);

    /* Request khronTab functions
    */

    //set khron request
    function requestKhronTab(
        uint timeStamp, 
        uint iterations, 
        string memory khronTab
        ) 
        external 
        returns(bytes32);
    //set khronAlerts pending
    
    //set khronCalendars pending

    //View functions

    function creditOf(
        address clientContract
        ) 
        external 
        returns (uint256);

    function getCallPrice() 
        external 
        returns (uint);

    //Request to node functions
    function setKhronTokenAddress(
        address khronAddress
        )
        external
        returns (bool);

    function setKhronTab(
        address _nodeContract, //this has to be a khron token recipient identifies the khron_node handling the request 
        uint256 _khronFee,
        bytes memory _data
        )
        external
        returns (bool);
}