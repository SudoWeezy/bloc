# Bloc

Introduction to blockchain

## Start

> On your own fork

1. Click on `Code` -> `Create codespace on main`.
2. Wait for the install
3. Create `main.py`
4. Enter the following:

- `$ git clone https://github.com/algorandfoundation/algokit-utils-py.git`
- `$ cd algokit-utils-py`
- `$ pip install .`
- `$ cd ..`
- `$ algokit localnet start`

5. Click on `PORTS` & change algod/kmd/indexer to `public`
6. To explore the chain : `$ algokit explore`

## Useful Links

`https://github.com/algorandfoundation/algokit-cli`
`https://developer.algorand.org/docs/get-details/algokit/`
`https://developer.algorand.org/docs/get-details/transactions/transactions/`

- #payment-transaction
- #asset-parameters
  `https://github.com/algorand-devrel/python-digital-marketplace-dapp/tree/main/projects/DigitalMarketplace-frontend`

## Smart contract Workshop

### Intitilize your algokit project

- `$ algokit init`
- Choose `Smart Contracts` `Python`
- Name the project `digital_marketplace`
- Name the smart contract app `digital_marketplace`
- Choose `Production` `Python`
- Skip `CD`
- Type `Y` for bootstrap

### Reset local net

- `$ algokit localnet reset`

### Start local net

- `$ algokit localnet start`

### Build Smart Contract

- `$ algokit project run build`

> look at:

- `smart_contracts/digital_marketplace/contract.py`
- `smart_contracts/digital_marketplace/deploy_config.py`
- `smart_contracts/artifacts/digital_marketplace/DigitalMarketplace.approval.teal`
- `tests/digital_marketplace_client_test.py`
- `tests/digital_marketplace_test.py`

### Test Smart Contract

- `$ algokit project run test`

### Explore local net

- `$ algokit explore`

### Deploy Smart Contract

- Click run & debug -> Choose Deploy then run OR `$ algokit project deploy localnet`

### DEBUG

Then follow the questionnaire and afterwards enter the workspace as prompted.
Once the local/codespace has loaded in, you need to get your localnet started:
algokit localnet start
If your having any localnet problems just do a quick reset command:
algokit localnet reset
To build your smart contract out to generate your artifacts folder run:
algokit project run build
If you are having problems building your smart contract run:
algokit project bootstrap all
To run your tests you coded for the smart contract run:
algokit project run test
Lastly to observe your tests with LORA the Explorer run:
algokit explore

FOR CODESPACE USERS, You will need to open port visbilty public for:
algod: 4001, kmd: 4002, vite: 5173, indexer 8980
Beside "terminal" you will see "ports" when clicked you will see many different ports, via the name or number identify the above and go to the "Visibility" column. Right click to view options and set "port visibility" to "public".

If you are having intense set up problems, to find out what you may be missing run:
algokit doctor

## Front end

1. install Python 3+ & Algokit `https://github.com/algorandfoundation/algokit-cli?tab=readme-ov-file#install-algokit-with-pipx-on-any-os`
2. `$ algokit init`

- Smart Contracts & DApp Frontend
- Python
- `digital_marketplace`
- `Production`
- `digital_marketplace`
- `Python`
- `Skip CD`
- `Y`

> Can also be done with algokit init on a already create backend + algokit project link

`$ cd digital_marketplace`
`$ cd projects/digital_marketplace-contracts/`
`$ algokit project run build`
`$ algokit project run test`
`$ open -a Docker`
`$ algokit localnet reset`
`$ algokit localnet start`
`$ algokit explore`
`$ algokit project deploy localnet`
`$ cd ../..`
`$ algokit project run build`

> new terminal
> `$ cd projects/digital_marketplace-frontend` > `$ npm run dev` > `$ open -n -a "Brave Browser.app" --args "--new-window" "http://localhost:5173/"`
