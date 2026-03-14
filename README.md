# MTP Attack — Many-Time Pad Cryptanalysis

A Python toolkit for breaking stream ciphers (or OTP) when the same key is reused across multiple messages. This is a well-known cryptographic vulnerability known as the **Many-Time Pad (MTP)** attack.

The ciphertexts used in this project come from the OliCyber training platform:
[https://training.olicyber.it/challenges#challenge-331](https://training.olicyber.it/challenges#challenge-331)

---

## The Vulnerability: Why Reusing a Key Breaks Everything

A **One-Time Pad (OTP)** is theoretically unbreakable — but only if the key is used exactly once and is as long as the message. The encryption is a simple XOR:

```
C = M XOR K
```

When the same key `K` is reused to encrypt two different messages `M1` and `M2`:

```
C1 = M1 XOR K
C2 = M2 XOR K
```

An attacker can XOR the two ciphertexts together and the key cancels out:

```
C1 XOR C2 = M1 XOR M2
```

Now the attacker has the XOR of two plaintexts. If any part of either plaintext is known or guessable, the other can be recovered — and once any plaintext byte is known, the corresponding key byte is immediately revealed:

```
K[i] = C[i] XOR M[i]
```

---

## The Space Voting Heuristic

The initial key estimate is produced by a technique called **space voting**. It exploits the fact that natural language messages contain many space characters (`0x20`).

The insight comes from a property of ASCII encoding: when a letter (uppercase or lowercase) is XORed with a space (`0x20`), the result is the same letter in the opposite case. Both cases are still valid letters.

For each position `i` across all ciphertexts:

1. For each ciphertext `Cj`, assume `Cj[i]` is a space in the plaintext. Compute the candidate key byte: `k_candidate = 0x20 XOR Cj[i]`.
2. Test this candidate against all other ciphertexts at the same position. Count how many of them produce a valid letter (A-Z or a-z) when XORed with `k_candidate`.
3. The candidate that scores the most votes wins and is stored as the key byte for position `i`.

This gives a rough but often accurate first approximation of the key.

---

## Crib Dragging (Manual Refinement)

**Crib dragging** is the technique used to refine the key after space voting. A "crib" is a short known or guessed plaintext fragment — a word or phrase likely to appear somewhere in one of the messages.

The process:
1. Decrypt all messages with the current key and look for partially readable text.
2. Identify a fragment that looks almost correct in one of the messages.
3. Use `update-key.py` to state: "at position `p` in message `i`, the plaintext is `word`". The script recomputes the key bytes at those positions directly from the known plaintext and the ciphertext.
4. Re-run `print-messages.py` and check whether other messages improved. A correct guess at one position improves the decryption of all messages simultaneously, because they all share the same key.
5. Repeat until all messages are readable and the full key is recovered.

---

## Project Structure

```
MTP-Attack/
├── output.txt          # The ciphertexts (hex-encoded, one per line)
├── key.txt             # The current key candidate (hex-encoded, persisted across steps)
├── utils.py            # Shared helper functions
├── space-voting.py     # Step 1: generates initial key estimate using space voting
├── print-messages.py   # Step 2: decrypts and prints all messages with the current key
└── update-key.py       # Step 3: refines the key using a known plaintext fragment
```

### `utils.py`

Provides two helpers:
- `getMaxLength(messages)` — returns the length of the longest ciphertext.
- `isValid(b)` — returns `True` if the byte `b` corresponds to an ASCII letter (A-Z or a-z).

### `space-voting.py`

Implements the space voting attack. For every byte position, scores each candidate key byte by counting how many ciphertexts produce a valid letter at that position, then writes the best key estimate to `key.txt`.

### `print-messages.py`

Reads `key.txt` and `output.txt`, XORs each ciphertext with the current key, and prints all decrypted messages. Run this after every key update to assess progress.

### `update-key.py`

Accepts three command-line arguments and patches `key.txt`:

| Argument | Description |
|---|---|
| `cipher_idx` | Index (0-based) of the message where the plaintext is known |
| `start_pos` | Byte offset where the known fragment starts |
| `new_message` | The known plaintext string at that position |

Internally it recomputes `key[pos] = plaintext[pos] XOR ciphertext[pos]` for each byte in the fragment.

---

## How to Run: Step-by-Step

### Step 1 — Generate the initial key with space voting

```bash
python space-voting.py
```

This writes the estimated key to `key.txt` and prints it to stdout.

### Step 2 — Inspect the current decryption

```bash
python print-messages.py
```

All messages are printed indexed from `[0]`. Some will be fully readable, others will contain garbled characters where the key bytes are still wrong.

### Step 3 — Refine the key with a known plaintext fragment

When you spot a message that looks almost correct — for example, message `[3]` at position `5` looks like it might say `the` — run:

```bash
python update-key.py 3 5 "the"
```

This updates `key.txt` at positions 5, 6, 7 using message 3 as the plaintext reference.

### Step 4 — Repeat

Go back to Step 2 and inspect all messages again. Each correct plaintext guess propagates across all ciphertexts because they all share the same key. Continue until all messages are fully decrypted.

---

## Example Workflow

```bash
# 1. Bootstrap the key
python space-voting.py

# 2. Read the current state
python print-messages.py
# [0]: Jhe quick brXwn fox...
# [1]: garbled text...

# 3. Message [0] clearly says "The quick" — fix position 0
python update-key.py 0 0 "The quick"

# 4. Re-read — all messages improved at those positions
python print-messages.py
# [0]: The quick brXwn fox...

# 5. Keep iterating
python update-key.py 0 10 "brown"
python print-messages.py
# ...
```

---

## Files Reference

| File | Role |
|---|---|
| `output.txt` | Input: hex-encoded ciphertexts, one per line. Never modified. |
| `key.txt` | State: the current key candidate in hex. Updated by `space-voting.py` and `update-key.py`. |
