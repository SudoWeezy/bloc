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

## Smart contract Workshop:

### Intitilize your algokit project:
- `$ algokit init`
- Choose `Smart Contracts` `Python`
- Name the project `testnet`
- Name the smart contract app `testnet`
- Choose `Production` `Python`
- Skip `CD`
- Type `Y` for bootstrap

### Reset local net:
- `$ algokit localnet reset`

### Start local net:
- `$ algokit localnet start`

### Build Smart Contract:
- `$ algokit project run build`

### Test Smart Contract:
- `$ algokit project run test`

### Create a testnet account
- `$ source projects/testnet/.venv/bin/activate`
- `$ python`

```python
from utils import get_accounts
from algosdk import account, mnemonic

private_key, address = account.generate_account()
print(f"address: {address}")
print(f"mnemonic: {mnemonic.from_private_key(private_key)}")
```

copy mnemonic and address

CTRL + D (exit)
- `$ deactivate`
- `$ algokit project deploy testnet`


### Explore testnet:
- `$ algokit explore`
