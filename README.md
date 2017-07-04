# ChainGang

A series of blockchain-related classes produced by Logan Graba. First up is the generation of Merkle Trees (MT)! Next is Logan's wildest BlockChain yet, Nutchain; A simple blockchain using my knowledge of MT generation that will allow me to learn about all the components necessary to create a BlockChain. I hope to introduce features such as Centralized-Server operation, Distributed Operation, Transaction Fees, Mining Discovery, Format mutability/treeing, MT -> Directory/Files -> DB conversion, and Partial-Chain Operability via Light Clients.

July 03, 2017

ToDo:
1. ScriptSig and ScriptPubKey [Transaction Verification]
2. Account ownership
3. Mining and Transaction Fees
4. Coin assignment and Coin Provenance (Every coin may be traced from Mining to Inputs/Outputs of Related Transactions)
5. Change Transaction class to accept multiple inputs/outputs [After Coin Provenance complete]
6. Planning: centralized vs. distributed operations
7. Alter server to start up in Centralized (no coin, only server mines?) or Distributed (Mining Rewards, Value, Supply considerations) via CLI Arguments
8. Alter client to detect server mode and use that mode
9. Planning: Can we make this thing an actual tree?
10. Conversion: MT -> Directories/Files -> DB
11. Alter client to start up in Full or Partial Modes (Doesn't download everything, only enough to verify...stuff)

Comparisons:
1. Bitcoin Source
2. Ethereum Source
3. Multichain Utlity

### Components
1. tree.py: A script to generate MTs from directory structures
2. NutChain: A Server/Client designed to add transactions submitted client->server to a NutChain.
 - nutchain.py : Building the NutChain
 - nutserver.py : Collecting Transactions submitted from clients
 - nutclient.py : Submitting Transactions to server from CL
 - transaction.py : Transaction Model

### Dependencies
- Python 3.6.1

### Getting Started

### Merkle Tree
1. Make two directories: testA and testB in the newly-cloned project directory
2. Fill each directory with whatever you'd like
3. `python tree.py`


#### Nutchain

1. Go ahead and use the default genesis.nut or make your own
2. Configure Server Parameters and Start NutChain/Server on one computer/shell
3. Confgiure Client Parameters and Start NutChain/Client on another computer/shell
4. Type Transactions in the following format into the NutChain/Client shell, one per line:
```
Give [recipient] [amount] from [sender]; [comment]
(eg.)
Give sarah 10 from logan; First transaction!
```
5. Submit all typed transactions by submitting an empty transaction line. *What the magic happen in both shells!*

**Example NutChain/Client Output:**
```
·> python nutclient.py
Connecting to localhost:10000...
Please enter your transactions, one line at a time:

Give marxist 10 from logan; First tranny
Give sarah 2 from marxist; Second!

Sending 10.0 to marxist from logan
Sending 2.0 to sarah from marxist
Received:
Tx(input={'logan': 10.0}, output={'marxist': 10.0}, time=1499052842.660342, version='.01', comment='First tranny')
Tx(input={'marxist': 2.0}, output={'sarah': 2.0}, time=1499052851.8730009, version='.01', comment='Second!')
Closing Socket...
Complete!
```

**Example NutChain/Server Output:**
```
·> python nutchain.py
Starting up server...
Host: localhost
Port: 10000

Genesis block read
---------------------------------------->>
Waiting for a connection...

Connection from ('127.0.0.1', 65273)
No more data from ('127.0.0.1', 65273), the filthy animal!
Submitting 2 transactions to NutChain
---------------------------------------->>
We're going to make a new Nut with the following shit:
Previous Block:
{'header': {'hash': '7991db1f811c45a9a69fe0a1042450ee', 'version': '.01', 'previous': '', 'crush': '303c04763907dfbe0b12b7fc91d48958', 'time': '1498802641.595125', 'difficulty': '1', 'nonce': '0'}, 'transactions': {'1': 'Give Logan 100n from GOD at 1498802641.595125; What a pimp!'}, 'accounts': {'logan': 100.0}}
New Transactions:
Tx(input={'logan': 10.0}, output={'marxist': 10.0}, time=1499052842.660342, version='.01', comment='First tranny')
Created 'marxist' account to receive 10.0 from logan!
Tx(input={'marxist': 2.0}, output={'sarah': 2.0}, time=1499052851.8730009, version='.01', comment='Second!')
Created 'sarah' account to receive 2.0 from marxist!
---------------------------------------->>
{'header': {'hash': '4c79bd85da313a343bc65280ff818c87', 'version': '.01', 'previous': '7991db1f811c45a9a69fe0a1042450ee', 'crush': '8785b0b391e93ce86eef8363c4b06217', 'time': 1499052852.377651, 'difficulty': 1, 'nonce': 0}, 'transactions': {'c8a8f5c8ad2a0a4249b423cc69118403': Tx(input={'logan': 10.0}, output={'marxist': 10.0}, time=1499052842.660342, version='.01', comment='First tranny'), 'b61fe205e8b1e6c5ec68b4d866ecfe6b': Tx(input={'marxist': 2.0}, output={'sarah': 2.0}, time=1499052851.8730009, version='.01', comment='Second!')}, 'accounts': {'logan': 90.0, 'marxist': 8.0, 'sarah': 2.0}}
Waiting for a connection...
```
