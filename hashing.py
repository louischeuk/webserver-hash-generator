import hashlib


def hashing(filename, hash_type):
    hash = 0
    if hash_type == "md5":
        hash = hashlib.md5()
    elif hash_type == "sha1":
        hash = hashlib.sha1()
    elif hash_type == "sha256":
        hash = hashlib.sha256()

    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash.update(chunk)
    return hash.hexdigest()


def md_5(filename):
    return hashing(filename, "md5")


def sha_1(filename):
    return hashing(filename, "sha1")


def sha_256(filename):
    return hashing(filename, "sha256")
