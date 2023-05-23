// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface ISBT721 {
    event Attest(address indexed to, uint256 indexed tokenId);
    event Burn(address indexed from, uint256 indexed tokenId);
    event Transfer(address indexed from, address indexed to, uint256 indexed tokenId);
    function attest(address to) external returns (uint256);
    function balanceOf(address owner) external view returns (uint256);
    function ownerOf(uint256 tokenId) external view returns (address);

}
