pragma solidity ^0.4.16;


contract HeadsOrTails {
    // The keyword "public" makes those variables
    // readable from outside.

    address public p1;
    address public p2;
    uint256 private amount = 0;
    bool public head = false;
    // address private me =  0x866269d5B827Be2741775eA58cee58595d36bf23;

    // mapping (address => uint) public balances;
    
    // event test_value(uint256 indexed value1);

    // Events allow light clients to react on
    // changes efficiently.
    // event Sent(address from, address to, uint amount);

    // This is the constructor whose code is
    // run only when the contract is created.

    function HeadsOrTails (bool _head) public payable {
        p1 = msg.sender;
        head = _head;
        // me.transfer(msg.value);
        amount = amount + msg.value;
    }
    
    function joinGame() public payable {
        p2 = msg.sender;
        amount = amount + msg.value;
        uint8 res = random();
        if ((res == 0 && head == true) || (res == 1 && head == false)) {
            p1.transfer(amount);
        } else {
            p2.transfer(amount);
        } 
    }

    function random() private view returns (uint8) {
        return uint8(uint256(keccak256(block.timestamp, block.difficulty))%2);
    }
}