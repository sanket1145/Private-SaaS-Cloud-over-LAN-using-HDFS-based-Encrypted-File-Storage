import os
import math
import base64

BLOCK_SIZE = 1024
NODES = ["storage/node1", "storage/node2", "storage/node3"]

for node in NODES:
    os.makedirs(node, exist_ok=True)

def encrypt(data):
    return base64.b64encode(data)

def decrypt(data):
    return base64.b64decode(data)

def upload(file_path):
    with open(file_path, "rb") as f:
        data = f.read()

    total_blocks = math.ceil(len(data) / BLOCK_SIZE)

    print("Uploading...")

    for i in range(total_blocks):
        block = data[i*BLOCK_SIZE:(i+1)*BLOCK_SIZE]
        enc_block = encrypt(block)

        node = NODES[i % len(NODES)]
        block_name = f"{os.path.basename(file_path)}_block{i}"

        with open(f"{node}/{block_name}", "wb") as bf:
            bf.write(enc_block)

    print("Upload Complete!")

def download(file_name, output_file):
    blocks = []
    i = 0

    while True:
        found = False

        for node in NODES:
            block_path = f"{node}/{file_name}_block{i}"

            if os.path.exists(block_path):
                with open(block_path, "rb") as bf:
                    enc_data = bf.read()
                    blocks.append(decrypt(enc_data))
                found = True
                break

        if not found:
            break

        i += 1

    with open(output_file, "wb") as out:
        for block in blocks:
            out.write(block)

    print("Download Complete!")

while True:
    print("\n1. Upload File")
    print("2. Download File")
    print("3. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        path = input("Enter file path: ")
        upload(path)

    elif choice == "2":
        name = input("Enter file name: ")
        out = input("Enter output file name: ")
        download(name, out)

    elif choice == "3":
        break