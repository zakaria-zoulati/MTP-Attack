"""In this function I get the key and apply it to the ciphers and then get the current possible messages"""

# Getting the key
key = ""
with open("key.txt") as f:
    key = bytes.fromhex(f.read().strip())


# Getting the ciphers
ciphers = []
with open("output.txt") as f:
    for line in f:
        ciphers.append(bytes.fromhex(line.strip()))

for i in range(len(ciphers)):
    message = bytes(a ^ b for a, b in zip(ciphers[i], key))
    message = message.decode(encoding="utf-8", errors="replace")
    print(f"[{i}]: {message}")
