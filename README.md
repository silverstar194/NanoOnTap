# Nano On Tap
## Overview
Nano On Tap is a stateless flow control and orchestration system for Nano transactions. It introduces a 2nd layer ACL system to easily implement flow rules for the transfer of Nano from account to account within the system you design. It provides an API for programmatic interactions along with a UI for quick inspection and easy modeling.

Additionally flow state systems can be modeled, exported and imported through json templates. This allows for creation of complex use cases with ease.

The core advantage of Nano On Tap is allowing any developer to quickly build and scale out a Nano based application. It reduces the need to deal in the details of transaction generation, proccessing, PoW mangement or manage business rules around where and how transaction should or can take place.

## Architecture
Nano On Tap uses small modular components to define complexy flow states. The below outlines the indiviual components and provides an example flow state system.

### Components
#### Application
The highest level component is the Application. An Application holds all objects defined in the flow state system. One _Nano On Tap_ backend can support multiple different applications.

#### Account
Model for a Nano account. Holds information about the Nano wallet, Nano address, the current balance of that account in raw. It also contains its Account Policies.

#### Account Policy
These are the limits set for the Accounts. This involves how much Nano can be sent from and received to the Account. The Account can also have an Action limit for how many times it will send Nano from the account and receive money to the Account.

#### Device
Devices hold Action Sets that contain actions that can be triggered as a whole.

#### Token
Tokens hold action policies that determine if an action can be triggered .

....

### Flow State Execution
Once the flow state system is defined: how does a transaction actually go through?

To initial trigger an action a token has to interact with a device. Once the interaction has been initiated, account and action polices are evaluated to determine if the an action set can execute. The following policy rules are evaluated on each device token interaction:

#### Action Policy Rules
* Device whitelisting and blacklisted
* Origin account(s) whitelisting and blacklisted
* Destination account(s) whitelisting and blacklisted
* Number of Action(s) in Action Set in below action # threshold
* Total Nano transferred is below Nano transferred limit

#### Account Policy Rules
* Total Nano transferred to or from a Nano account if below account send/receive transferred limit
* Number of Action(s) from or from a Nano account is below account Nano send/receive transferred limit
* The highest priority Action Set on the device to met all the above criteria is executed. Only a single action set is ever executed per device token interaction.

## Flow State Programming API
Each flow state component has a corresponding POST endpoint allows for adding, removing and updating the flow state objects. Please see additional wiki pages for specifics. This allows dynamic updates to your defined system.

### Example Scenario
Bob uses his Token to interact with a Device to send 1 Nano in order to enter a raffle. Bob's token can now be reprogrammed to remove the Action Policy allowing Bob to trigger any additional 1 Nano Actions.

The reprogramming would utilize the `action/token/update` POST endpoint.

## Import and Export Flow State Definitions
### Import

### Export

## Real World Example

For a complete and more complex read world example visit [Nano Poker - Play Nano with NFC stickers and readers](https://github.com/silverstar194/NanoPoker)
```

