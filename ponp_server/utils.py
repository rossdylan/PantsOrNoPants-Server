from hashlib import sha256
from random import Random


rand = Random()


def generate_apikey(username):
    return sha256(username + str(rand.getrandbits(100))).hexdigest()
