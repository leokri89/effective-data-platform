import os


class Phrases:
    @staticmethod
    def load_pvk_file():
        with open("../keys/jwtRS256.key") as priv:
            return priv.read()

    @staticmethod
    def load_pbk_file():
        with open("../keys/jwtRS256.key.pub") as pub:
            return pub.read()
