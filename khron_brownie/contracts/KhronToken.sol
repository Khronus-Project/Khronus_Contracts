// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./KhronERC20.sol";
import "./ERC677Token.sol";

contract KhronToken is KhronERC20, ERC677Token {
  uint private constant TOTAL_SUPPLY = 10**27;
  string private constant NAME = 'Khronus Token';
  string private constant SYMBOL = 'Khron';

  /**
   * As its core the Khron token is implemented based on OpenZeppelin's version of ERC20. 
   * with some additions in order it supports atomic increase and decrease of approvals.
   * The Khron Token also implements the ERC677 which allows it to be a mechanism of data transfer.
   * This contract implements extra functionality to allow managing constructor functionality in child contracts, and avoid it sending Khron to itself.
   */
  
  constructor() ERC20(NAME, SYMBOL)
    public
  {
    _onCreate();
  }

  /**
   * @dev Hook that is called when this contract is created.
   * This allows to modify the contructor behaviour in case of derivative versions of Khron like bridges for example.
   * @notice Default implementation mints 10**27 tokens to msg.sender
   */
  function _onCreate()
    internal
    virtual
  {
    _mint(msg.sender, TOTAL_SUPPLY);
  }

  /**
   * @dev Check if recepient is a valid address before transfer
   * @inheritdoc ERC20
   */
  function _transfer(address sender, address recipient, uint256 amount)
    internal
    override
    virtual
    validAddress(recipient)
  {
    super._transfer(sender, recipient, amount);
  }

  /**
   * @dev Check if spender is a valid address before approval
   * @inheritdoc ERC20
   */
  function _approve(address owner, address spender, uint256 amount)
    internal
    override
    virtual
    validAddress(spender)
  {
    super._approve(owner, spender, amount);
  }


  // MODIFIERS

  modifier validAddress(address _recipient)
    virtual
  {
    require(_recipient != address(this), "Doesn't allow to transfer funds to itself");
    _;
  }
}