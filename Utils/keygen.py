import base64
import hashlib

import ecdsa
from ecdsa import BadSignatureError, MalformedPointError, InvalidCurveError
import base58
import bech32


def generate_address(public_key):
    _public_key = (base64.b64decode(public_key)).hex()
    hashed_public_key = hashlib.sha256(_public_key.encode()).digest()
    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(hashed_public_key)
    hashed_public_key = ripemd160.digest()
    segwit_address = bech32.encode('ir', 0, hashed_public_key)
    return segwit_address


def generate_ecdsa_keys():
    sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
    _private_key = sk.to_string().hex()
    vk = sk.get_verifying_key()
    _public_key = vk.to_string()
    segwit_address = generate_address(base64.b64encode(_public_key))
    print(segwit_address)
    filename = input("Write the name of your new address: ") + ".txt"
    with open(filename, "w") as f:
        f.write(
            F"Private key: {base64.b64encode(bytes.fromhex(_private_key)).decode()}\n"
            F"Public key: {base64.b64encode(bytes(_public_key)).decode()}\n"
            F"Wallet address: {segwit_address}")
    print(F"Your new address and private key are now in the file {filename}")


def sign_ecdsa_msg(private_key: str, message: str) -> str:
    sk = ecdsa.SigningKey.from_string(bytes.fromhex(base64.b64decode(private_key).hex()), curve=ecdsa.SECP256k1)
    _message = hashlib.sha256(message.encode()).digest()
    _signature = base64.b64encode(sk.sign(_message))
    return _signature.decode()


def validate_signature(public_key: str, signature: str, message: str) -> bool:
    _public_key = (base64.b64decode(public_key)).hex()
    _signature = base64.b64decode(signature)
    try:
        vk = ecdsa.VerifyingKey.from_string(
            bytes.fromhex(_public_key),
            curve=ecdsa.SECP256k1
        )
    except MalformedPointError:
        return False
    _message = hashlib.sha256(message.encode()).digest()
    try:
        return vk.verify(_signature, _message)
    except BadSignatureError:
        return False


def validate_address_signature(address, public_key, signature, message):
    if address == generate_address(public_key):
        return validate_signature(public_key, signature, message)
    return False



if __name__ == '__main__':
    result = None
    while result not in [1, 2, 3, 4]:
        result = int(input('1: generate_ecdsa_keys,'
                           ' 2: sign_ecdsa_msg,'
                           ' 3: validate_signature'
                           ' 4: validate_address_signature\n'))
        match result:
            case 1:
                generate_ecdsa_keys()
            case 2:
                private_key = input('Input private key\n')
                message = input('Input message\n')
                print(sign_ecdsa_msg(private_key, message))
            case 3:
                public_key = input('Input public key\n')
                signature = input('Input signature\n')
                message = input('Input message\n')
                print(validate_signature(public_key, signature, message))
            case 4:
                address = input('Input address\n')
                public_key = input('Input public key\n')
                signature = input('Input signature\n')
                message = input('Input message\n')
                print(validate_address_signature(address, public_key, signature, message))
