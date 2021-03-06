![Logo](https://i.imgur.com/A9uFrQt.jpg)

# Overview
Nano On Tap is a stateless flow control and orchestration system for Nano transactions. It introduces a 2nd layer ACL system to easily implement flow rules for the transfer of Nano from account to account within the system you design. It provides an API for programmatic interactions along with a UI for quick inspection and easy modeling.

Additionally flow state systems can be modeled, exported and imported through json templates. This allows for creation of complex use cases with ease.

The core advantage of Nano On Tap is allowing any developer to quickly build and scale out a Nano based application. It reduces the need to deal in the details of transaction generation, processing, PoW management or manage business rules around where and how transaction should or can take place.

# Architecture
Nano On Tap uses small modular components to define complex flow states. The below outlines the individual components and provides an example flow state system.

[Please see our Wiki for extensive flow state examples](https://github.com/silverstar194/NanoOnTap/wiki)

## Components
### Application
The highest level component is the Application. An Application holds all objects defined in the flow state system. One _Nano On Tap_ backend can support multiple different applications.
![Application](https://i.imgur.com/PvpHQj7.png)

### Account
Model for a Nano account. Holds information about the Nano wallet, Nano address, the current balance of that account in raw. An account also contains Account Policies.
![Account](https://i.imgur.com/DCYW5fd.png)

### Account Policy
These are the limits set for the Accounts. This includes how much Nano can be sent from and received to the Account. The Account can also have an Action limit for how many times it will send Nano from the account and receive money to the Account.
![Account Policy](https://i.imgur.com/diWJ7v4.png)

### Action Policy
These are the limits set for the action set. This includes where Nano can be sent, how much Nano can be sent, how many transactions can be sent and more. Action sets only execute if there is a action policy with proper permissions.
![Action Policy](https://i.imgur.com/KRHBCI1.png)

### Device
Devices hold Action Sets that contain actions that can be triggered as a whole.
![Device](https://i.imgur.com/YcCNLrY.png)

### Token
Tokens hold Action Policies that determine if an Action Set can be triggered.
![Token](https://i.imgur.com/652xZTR.png)

### Action Set
An Action Set contains multiple Actions. When a device interacts with a Token either all Actions in an Action Set execute of none of them do.
![Action Set](https://i.imgur.com/AodcJDC.png)

### Action
An Action defines a Nano transaction between two accounts. Multiple Actions make up an Action Set.
![Action](https://i.imgur.com/PO6sLsK.png)

### Node
Nano node to publish transactions to the Nano network.

### Wallet
Holds Nano accounts. Relates 1-1 with the wallet on Nano nodes.

# Flow State Execution
Once the flow state system is defined: how does a transaction actually go through?

To initial trigger an action a token has to interact with a device. Once the interaction has been initiated, account and action policies are evaluated to determine if an action set can execute. The following policy rules are evaluated on each device token interaction:

### Action Policy Rules
* Device whitelisting and blacklisted
* Origin account(s) whitelisting and blacklisted
* Destination account(s) whitelisting and blacklisted
* Number of Action(s) in Action Set in below action # threshold
* Total Nano transferred is below Nano transferred limit

### Action Policy Rules
* Total Nano transferred to or from a Nano account if below account send/receive transferred limit
* Number of Action(s) from or from a Nano account is below account Nano send/receive transferred limit
* The highest priority Action Set on the device to meet all the above criteria is executed. Only a single action set is ever executed per device token interaction.

# Flow State Programming API
Each flow state component has a corresponding POST endpoint allows for adding, removing and updating the flow state objects. Please see additional [wiki pages](https://github.com/silverstar194/NanoOnTap/wiki) for specifics. This allows dynamic updates to your defined system.

### Example Scenario
Bob uses his Token to interact with a Device to send 1 Nano in order to enter a raffle. Bob's token can now be reprogrammed to remove the Action Policy allowing Bob to trigger any additional 1 Nano Actions.

The reprogramming would utilize the `action/token/update` POST endpoint.

# Import and Export Flow State Definitions
Flow states can be imported and exported via JSON templates. This allows for easy modeling, transfer, modification and archiving of real world scenarios. [See Wiki for details.](https://github.com/silverstar194/NanoOnTap/wiki)

# Real World Example

For a complete and more complex real world example visit [Nano Poker - Play Nano with NFC stickers and readers](https://github.com/silverstar194/NanoPoker)
