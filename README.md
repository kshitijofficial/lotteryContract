```markdown
# Algorand Lottery Smart Contract

This repository contains the implementation of a Lottery Smart Contract on the Algorand blockchain, developed using Algorand Python (`algoPy`) and following the ARC4 standard.

## Overview

The Lottery contract allows participants to enter a lottery by paying a specified entry fee. The contract owner (creator) can then select a random winner, who will receive the accumulated funds minus a small balance retained in the contract. The contract also includes methods for creating and deleting the application.

### Features:
- **Entry Fee**: The creator sets an entry fee during the contract creation.
- **Enter Lottery**: Participants can enter the lottery by sending the required payment.
- **Pick Winner**: The contract randomly selects a winner from the participants.
- **Close Contract**: The creator can delete the contract and withdraw any remaining funds.

## Prerequisites

Ensure that you have the following dependencies:

[AlgoKit](https://algorand.co/algokit?utm_source=youtube&utm_medium=youtube&utm_campaign=codeeateryard&utm_content=download)

## Contract Structure

- **`Lottery` Contract**: The main contract that manages the lottery's state and logic.
- **Methods**:
  - `create_application`: Initializes the contract with an entry fee.
  - `enter_lottery`: Allows participants to enter the lottery by making a payment.
  - `pick_winner`: Randomly selects a winner from the participants.
  - `delete_application`: Allows the creator to close the contract and withdraw any remaining funds.

## How to Deploy

To deploy the contract on the Algorand testnet or mainnet, follow these steps:

1. Set up the Algorand environment (using Algorand Sandbox or a testnet account).
2. Create an instance of the `Lottery` contract.
3. Set the entry fee and deploy the contract using `create_application` method.
```

## Contract Logic

### Create Application

The `create_application` method sets the entry fee for the lottery and initializes the total entries to zero.

### Enter Lottery

Participants can enter the lottery by sending a payment transaction equal to the entry fee. The total number of entries is incremented with each valid payment.

### Pick Winner

The creator can invoke the `pick_winner` method, which randomly selects a winner from the participants based on the round number and group size. The winner receives all the funds collected minus 1 Algo reserved for contract closure.

### Delete Application

The creator can delete the contract, which transfers any remaining balance to the creator's account and closes the contract.
