def binary(num: int) -> str:
    """Return binary representation of integer without '0b' prefix"""
    return bin(num)[2:]

def gamma_encode(value: int):
    """Gamma encode a nonnegative integer returned as a string of bits"""

    bval = binary(value)
    offset = bval[1:]
    offset_len = len(offset)
    unary_offset_len = f"{'1' * offset_len}0"
    return unary_offset_len + offset

def gamma_decode(gamma_encoded_val: str) -> int:
    """Decode gamma-encoded string of bits back to an integer"""

    i = 0
    while gamma_encoded_val[i] == "1":
        i += 1
    offset_len = i
    i += 1
    offset = gamma_encoded_val[i : i+offset_len]
    return int("1" + offset, 2)