import hashlib
import gguf

def hash_tensor(tensor):
    return hashlib.md5(tensor.reshape(-1).tobytes())

def compute_hashes(data, hash_algorithms):
    hashes = {}
    for algo in hash_algorithms:
        hash_func = getattr(hashlib, algo)()
        hash_func.update(data)
        hashes[algo] = hash_func.hexdigest()
    return hashes

filename = "/Users/konstantinp/Downloads/codellama-7b-python.Q4_K_M.gguf"

with open(filename, "rb") as f:
    tensor_data_combined = b''
    # Load metadata
    info, tensorinfo = gguf.load_gguf(f)

    # Load tensors
    print(len(tensorinfo))
    i = 0
    for name in tensorinfo:
        weights = gguf.load_gguf_tensor(f, tensorinfo, name)

        first_32_bytes = weights.tobytes()
        # # [:32]
        # print(type(weights))
        print(hash_tensor(weights).hexdigest())
        # print(hashlib.md5(first_32_bytes).hexdigest())
        # print(first_32_bytes.hex())
        # first_32_bytes = weights.tobytes()[:32]
        # print(first_32_bytes.hex())
        # tensor_data_combined += weights.tobytes()

        # hashes = compute_hashes(weights, ['sha256', 'md5', 'sha1', 'sha512'])
        #
        # # Get the first 32 bytes correctly
        # flags = {algo: h[:32] for algo, h in hashes.items()}
        #
        # for algo, h in hashes.items():
        #     print(f"{algo.upper()} full hash: {h}")
        #     print(f"{algo.upper()} flag{{{flags[algo]}}}")
        # Compute hashes for the full tensor data
        # hashes = compute_hashes(weights, ['sha256', 'md5', 'sha1', 'sha512'])

        # Compute the hash of the first 32 bytes for the flag
        # print(hashlib.md5(first_32_bytes).hexdigest())
        # print(hashlib.sha256(first_32_bytes).hexdigest())
        # flag_hashes = compute_hashes(first_32_bytes,
        #                              ['sha256', 'md5', 'sha1', 'sha512'])
        #
        # for algo, h in flag_hashes.items():
        #     print(f"{algo.upper()} full hash: {h}")
        #     flag = flag_hashes[algo]
        #     print(f"{algo.upper()} flag{{{flag}}}")

        # print(name, type(weights), weights.shape)
        i += 1
        if i % 10 == 0:
            print(i)

    print(hashlib.md5(tensor_data_combined).hexdigest())
    print(hashlib.sha256(tensor_data_combined).hexdigest())
    print(hashlib.sha512(tensor_data_combined).hexdigest())
    print(hashlib.sha1(tensor_data_combined).hexdigest())
    print(hashlib.sha224(tensor_data_combined).hexdigest())
    print(hashlib.sha384(tensor_data_combined).hexdigest())

    # combined_hashes = compute_hashes(tensor_data_combined, ['sha256', 'md5', 'sha1', 'sha512'])
    # for algo, h in combined_hashes.items():
    #     print(f"{algo.upper()} combined full hash: {h}")
    #     print(f"{algo.upper()} combined flag{{{h}}}")
