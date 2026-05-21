import sys
import os

def obfusquer_fichier(input_path, output_path):
    with open(input_path, 'rb') as f:
        data = f.read()

    # Inverser la totalité des données du fichier
    obfuscated = data[::-1]

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, 'wb') as f:
        f.write(obfuscated)

if __name__ == "__main__":
    obfusquer_fichier(sys.argv[1], sys.argv[2])