# Bloc
Introduction to blockchain

## Smart contract Workshop:

### Intitilize your algokit project:
- `$ algokit init`
- Choose `Smart Contracts` `Python`
- Name the project `tnet`
- Name the smart contract app `tnet`
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
