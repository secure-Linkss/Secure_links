import binascii

email_hex = "6A626F74746572406661697468776573742E6F7267"

try:
    decoded_email = binascii.unhexlify(email_hex).decode()
    print(f"Decoded email: {decoded_email}")
except Exception as e:
    print(f"Error decoding: {e}")
