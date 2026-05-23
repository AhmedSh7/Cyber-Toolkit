from colorama import Fore, Style, init

init(autoreset=True)


def identify_hash(hash_value):
    hash_value = hash_value.strip()
    hash_length = len(hash_value)

    hash_types = {
        32: ["MD5", "MD4", "NTLM"],
        40: ["SHA1", "RIPEMD-160"],
        56: ["SHA224"],
        64: ["SHA256", "SHA3-256", "BLAKE2s"],
        96: ["SHA384"],
        128: ["SHA512", "SHA3-512", "BLAKE2b"]
    }

    print(Fore.YELLOW + "\nAnalyzing hash...\n")

    if hash_length in hash_types:
        print(Fore.GREEN + "[+] Possible hash type(s):")
        for hash_type in hash_types[hash_length]:
            print(Fore.CYAN + f"    - {hash_type}")
    else:
        print(Fore.RED + "[-] Unknown hash type")


print(Fore.MAGENTA + "=== HASH IDENTIFIER TOOL ===")

user_hash = input("\nEnter a hash value: ")

identify_hash(user_hash)

print(Style.RESET_ALL)