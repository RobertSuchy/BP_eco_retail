# základnú kostru smart kontraktu, obsahujúcu metódy pre jeho kompiláciu a iné pomocné metódy
# sme použili z github repozitára vytvoreného platformou Algorand
# https://github.com/algorand-devrel/pyteal-course 

import base64
import hashlib
import sys

def sha256b64(s: str) -> str:
    return base64.b64encode(hashlib.sha256(str(s).encode("utf-8")).digest()).decode("utf-8")

if __name__ == "__main__":
    s = sys.argv[1]

    print(s)
    print(sha256b64(s))
