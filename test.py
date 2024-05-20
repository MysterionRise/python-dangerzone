import base64
def xor_byte_string(data, key):
    repeated_key = (key * (len(data) // len(key) + 1))[:len(data)]
    xor_bytes = bytes(a ^ b for a, b in zip(data, repeated_key))

    return xor_bytes

data = b"+\x7ft1*iK\x1c[Io\x16\x1a\x00o\x1aYS\x03+\x10\x00B\t"
# Encode the byte string into Base64
encoded_base64 = base64.b64encode(data)

# Print the Base64 encoded string
print(encoded_base64.decode('ascii'))
key = bytes([104, 48, 48, 116])
result = xor_byte_string(data, key)
print(result)
