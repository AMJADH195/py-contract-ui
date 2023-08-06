                                                


# PyContractUI

**PyContractUI** is a Python package that simplifies the process of creating interactive HTML user interfaces for Ethereum smart contracts. It automates the conversion of smart contract ABIs into web-based UIs, making it easier for developers to build GUIs .

## Features

- Convert Ethereum smart contract ABIs into HTML user interfaces.
- Seamless integration with popular Ethereum wallets for smooth execution of smart contract functions.

## Installation

You can install PyConttractUI using pip:

```bash
pip install py-conttract-ui

```
## Serving the GUI on Local server

If you want to interact with your smart contracts you might want to generate the GUI on a local server (without exporting it). If you want to export the GUI please read the next section.

To start the server you can execute the command below in the same folder where your smart contract ABI is located:

```bash
contract-ui-gen --serve
```
For example, if your ABIS is placed on the folder named contract/abis
first you have to navigate into the folder contract/abis and then execute the command above command 
After running the local server, the GUI is available on the URL
http://0.0.0.0:8000

If you want instead to specify a custom path of the directory of the smart contract ABIs, you can add the optional parameter as per below:

```bash
contract-ui-gen  --contract /contracts/abis --serve
```
The command above generates the GUI using the ABI found in the folder contracts/abis

## Exporting the GUI

You can export your smart contract ABIs into HTML using the below command
```bash
contract-ui-gen
```

The command will create a folder with the GUI in the directory where the command has been executed.
Alternatively, you can add optional parameters to the source folder of the ABI and/or the destination folder where the GUI has to be exported to. For example:
```
contract-ui-gen --contract /contracts/abis --output gui_output
```

The command above generates the GUI using the ABI found in the folder
/contracts/abis and exports to the gui_output folder
