// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "Khronus-Project/Khronus_TimeCog@0.9.9/libraries/KhronusTimeCog.sol";

library KhronTimestampUtils {

    //this function might not be needed
    function closestMinuteRounded(uint256 _timestamp) internal pure returns (uint256){
        uint256 _extraSeconds = _timestamp % 60;
        uint256 _interimAnswer = _timestamp - _extraSeconds;
        if (_extraSeconds < 30 ){
            return _interimAnswer;
        }
        else{
            return KhronusTimeCog.nextMinute(_timestamp);
        }
    }

    function closestMinuteExact(uint256 _timestamp) internal pure returns (uint256){
        return KhronusTimeCog.nextMinute(_timestamp) - 1 minutes;
    }

    function isValidKhronTimestamp(uint256 _timestamp) internal pure returns (bool){
        if (_timestamp % 60 == 0 && KhronusTimeCog.isValidTimestamp(_timestamp)){
            return true;
        }
        else{
            return false;
        }
    }

}