import json


if __name__ == "__main__":
    decryptor_json = None
    with open('decryptors.json', 'r') as decryptor_file:
        decryptor_json = json.load(decryptor_file)
        decryptor_json = {decryptor['name']: decryptor for decryptor in decryptor_json}
        for _, decryptor in decryptor_json.items():
            del decryptor['name']
    with open('decryptors.json', 'w') as decryptor_file:
        decryptor_file.write(json.dumps(decryptor_json, indent=4, sort_keys=True))
