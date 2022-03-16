import base64
from tokenize import Token
from typing import Any
from borsh_construct import CStruct, U64, Bool, Option, Enum, U8, U32
from anchorpy import borsh_extension
from construct import Adapter, Construct, IfThenElse, Pass

AccountState = Enum("Uninitialized", "Initialized", "Frozen", enum_name="AccountState")

class Solana_COption(Adapter):
    """Borsh implementation for Solana's COption type."""

    _discriminator_key = "discriminator"
    _value_key = "value"

    def __init__(self, subcon: Construct) -> None:
        option_struct = CStruct(
            self._discriminator_key / U32, # changed from U8
            self._value_key / subcon,
        )
        super().__init__(option_struct)  # type: ignore

    def _decode(self, obj, context, path) -> Any:
        if obj[self._discriminator_key] == 0x00000000:
            return None
        return obj[self._value_key]

    def _encode(self, obj, context, path) -> dict:
        discriminator = 0x00000000 if obj is None else 0x01000000
        return {self._discriminator_key: discriminator, self._value_key: obj}

TOKEN_ACCOUNT_SCHEMA = CStruct(
    "mint" / borsh_extension._BorshPubkey,
    "owner" / borsh_extension._BorshPubkey,
    "amount" / U64,
    "delegate" / Solana_COption(borsh_extension._BorshPubkey),
    "state" / AccountState,
    "is_native" / Solana_COption(U64),
    "delegated_amount" / U64,
    "close_authority" / Solana_COption(borsh_extension._BorshPubkey),
)

f = open("FvPuwBfjpjxzELaWgNVs5Gegh5rqt4V8DRPBCjbYjMkC_base64.txt", "r").read()
decoded = base64.b64decode(str(f))

parsed = TOKEN_ACCOUNT_SCHEMA.parse(decoded)
print(parsed)