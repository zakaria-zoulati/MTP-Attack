"""In this function what I will do is to apply the space voting and store the key in the key.text"""

from utils import getMaxLength, isValid

# Getting the ciphers
ciphers = []
with open("output.txt") as f:
    for line in f:
        ciphers.append(bytes.fromhex(line.strip()))

n = getMaxLength(ciphers)
new_key = bytearray(n)

for pos in range(n):
    best_score = -1
    best_key_byte = 0x20

    for i in range(len(ciphers)):
        if pos >= len(ciphers[i]):
            continue
        candidate_byte = 0x20 ^ ciphers[i][pos]
        score = sum(
            1
            for j in range(len(ciphers))
            if j != i
            and pos < len(ciphers[j])
            and isValid(candidate_byte ^ ciphers[j][pos])
        )
        if score > best_score:
            best_score = score
            best_key_byte = candidate_byte

    new_key[pos] = best_key_byte

new_key = new_key.hex()
print(new_key)
with open("key.txt", "w") as f:
    f.write(new_key)
