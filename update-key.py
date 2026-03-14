"""In this function basing on the output if you see some words in the print-messages I would update the bytes of the key"""

import sys

with open("output.txt") as f:
    ciphers = []
    for line in f:
        ciphers.append(bytes.fromhex(line.strip()))

with open("key.txt") as f:
    key = bytearray.fromhex(f.read().strip())

if __name__ == "__main__":
    cipher_idx = int(sys.argv[1])
    start_pos = int(sys.argv[2])
    new_message = sys.argv[3].encode()

    for i in range(len(new_message)):
        key[start_pos + i] = new_message[i] ^ ciphers[cipher_idx][start_pos + i]

    with open("key.txt", "w") as f:
        f.write(key.hex())
