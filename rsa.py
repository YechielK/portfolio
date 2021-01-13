def mod(p, q):
    return p * q

def phi(p, q):
    return (p - 1) * (q - 1)

def find_encryption_key(totient, modulus):
    return [num for num in list(range(2,totient)) if coprime(num, totient) and coprime(num, modulus)][5]

def coprime(a, b):
    return True if (gcd(a,b) == 1) else False

def gcd(a, b):
    return a if (b == 0) else gcd(b, a % b)

def find_decryption_key(totient, encryption_key):
    return [num for num in list(range(encryption_key+1, encryption_key * totient)) if num * encryption_key % totient == 1][0]

def rsa(base, exponent, modulus):
    return (base ** exponent) % modulus

def get_keys(p,q):
    modulus = mod(p,q)
    totient = phi(p, q)
    encryption_key = find_encryption_key(totient, modulus)
    decryption_key = find_decryption_key(totient, encryption_key)

    dict = {'p': p, 'q': q, 'modulus': modulus, 'totient': totient, 'encryption_key': encryption_key, 'decryption_key': decryption_key}


    return dict

def calculate(msg, p, q):
    dict = {}
    modulus = mod(p,q)
    totient = phi(p, q)
    encryption_key = find_encryption_key(totient, modulus)
    decryption_key = find_decryption_key(totient, encryption_key)

    lst = list(msg)
    nums = [ord(i) for i in lst]
    encrypted_nums = [rsa(i, encryption_key, modulus) for i in nums]
    encrypted_msg = [chr(i) for i in encrypted_nums]
    decrypted_nums = [rsa(i, decryption_key, modulus) for i in encrypted_nums]
    decrypted_msg = [chr(i) for i in decrypted_nums]
    
    dict = {'encrypted_nums': encrypted_nums, 'encrypted_msg': encrypted_msg, 'decrypted_nums': decrypted_nums, 'decrypted_msg': decrypted_msg}
    dict['msg'] = msg
    dict['p'] = p
    dict['q'] = q
    dict['lst'] = lst
    dict['nums'] = nums
    dict['modulus'] = modulus
    dict['totient'] = totient
    dict['encryption_key'] = encryption_key
    dict['decryption_key'] = decryption_key
    # print(encrypted_nums)
    # print(''.join(encrypted_msg))
    # print(decrypted_nums)
    # print(''.join(decrypted_msg))
    return dict



