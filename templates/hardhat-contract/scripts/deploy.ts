// eslint-disable-next-line node/no-missing-import
// eslint-disable-next-line camelcase
import { TodoList__factory } from "../typechain/factories/TodoList__factory";

// We require the Hardhat Runtime Environment explicitly here. This is optional
// but useful for running the script in a standalone fashion through `node <script>`.
//
// When running the script with `npx hardhat run <script>` you'll find the Hardhat
// Runtime Environment's members available in the global scope.
import { ethers } from "hardhat";

async function main() {
  // Hardhat always runs the compile task when running scripts with its command
  // line interface.
  //
  // If this script is run directly using `node` you may want to call compile
  // manually to make sure everything is compiled
  // await hre.run('compile');

  // We get the contract to deploy
  // eslint-disable-next-line camelcase
  // const Token: TodoList__factory = await ethers.getContractFactory("TodoList");

  // // const ownerAddress = "0x4D9d313faBe4Fc3051c276e8C7E3663Ef5A85513";
  // // const initialSupply = 1000;

  // const token = await Token.deploy();

  // console.log("Greeter deployed to:", token.address);
  const vcheckinContract = await ethers.getContractFactory("VCheckin");

  const vcheckin = await vcheckinContract.deploy(
    "VCheckin",
    "VCI",
    "0xa63854a9DbB221dB8cA865BF4559cd09d974FB60"
  );

  console.log("VCheckin deployed to:", vcheckin.address);
  return;

  const employeeIdContract = await ethers.getContractFactory("EmployeeID");
  const employeeId = await employeeIdContract.deploy("EmployeeID", "EID");
  console.log("EmployeeId deployed to:", employeeId.address);

  const tokenContract = await ethers.getContractFactory("VdtToken");
  const token = await tokenContract.deploy();
  console.log("Token deployed to:", token.address);

  const checkInContract = await ethers.getContractFactory("CheckinContract");
  const checkIn = await checkInContract.deploy(
    employeeId.address,
    token.address
  );

  console.log("CheckIn deployed to:", checkIn.address);

  // make const file
  const fs = require("fs");
  const path = require("path");
  const dt = `
  export const EMPLOYEE_CONTRACT_ADDRESS = "${employeeId.address}";
  export const TOKEN_CONTRACT_ADDRESS = "${token.address}";
  export const CHECKIN_CONTRACT_ADDRESS = "${checkIn.address}";  
  `;
  fs.writeFileSync(
    path.join(__dirname, "../../frontend/src/common/constant.ts"),
    dt
  );
}

// We recommend this pattern to be able to use async/await everywhere
// and properly handle errors.
main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
