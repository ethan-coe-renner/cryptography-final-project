import random
import TextBites

PRIME = 98561123
ROOT = 452


def chat():
    key = diffie_hellman(PRIME, ROOT)
    # Do cool chat stuff here
    return "meh"


def diffie_hellman(prime, root):
    r = random.randint(2, prime - 2)
    a = pow(root, r, prime)

    # Networking, send 'a' to other computer, receive 'b' in return
    b = 0

    # 'k' is our key
    k = pow(b, r, prime)

    return k
