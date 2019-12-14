import random

def gcd(a, b):
    # Алгоритм Евклида для нахождения НОД
    while b != 0:
        a, b = b, a % b
    return a

def mulinv(e, phi):
    # Нахождение d с помощью расширенного алгоритма Евклида
    d = 0
    x1 = 0
    x2 = 1
    y1 = 1
    temp_phi = phi

    while e > 0:
        temp1 = temp_phi // e
        temp2 = temp_phi % e
        temp_phi, e = e, temp2

        x = x2 - temp1 * x1
        y = d - temp1 * y1

        x2, x1 = x1, x
        d, y1 = y1, y

        if temp_phi == 1:
            return d + phi

def getPrimes():
    # Генерация массива простых чисел
    n = 260
    a = []
    primes = []

    for i in range(n + 1):
        a.append(i)
    
    a[0], a[1] = False, False

    i = 2
    while i <= n:
        if a[i]:
            j = i * i
            while j <= n:
                a[j] = False
                j += i
        i += 1

    for i in range(128, 256):
        if a[i]:
            primes.append(a[i])

    return primes

def encrypt(pk, plaintext):
    key, n = pk
    cipher = 0
    for letter in plaintext:
        tmp = (ord(letter) ** key) % n
        cipher = cipher * 100000 + tmp

    codout = open('cod.txt', 'w')
    codout.write(str(cipher))
    codout.close()

def decrypt(pk, ciphertext):
    key, n = pk
    tmp = len(str(ciphertext))
    if tmp % 5 == 0:
        plain = [0] * (tmp // 5)
    else:
        plain = [0] * (tmp // 5 + 1)

    i = 0
    while ciphertext > 0:
        clet = ciphertext % 100000
        plet = (clet ** key) % n
        plain[len(plain) - i - 1] = plet
        i += 1
        ciphertext //= 100000

    outp = open('out.txt', 'w')
    for char in plain:
        outp.write(chr(char))
    outp.close()

# Получаю два случайных простых p и q
primes = getPrimes()

while True:
    p = random.choice(primes)
    q = random.choice(primes)
    if p != q:
        break

# Расчитываю публичный и приватный ключи
n = p * q
phi = (p - 1) * (q - 1)

while True:
    e = random.randrange(2, phi)
    if gcd(e, phi) == 1:
        break

d = mulinv(e, phi)

public = [e, n]
private = [d, n]

inp = open('in.txt', 'r')
codin = open('cod.txt', 'r')

# Произвожу кодирование сообщения и запись в файл
message = inp.readline()
encrypt(public, message)

# Произвожу декодирование сообщения и запись в файл
cipher = codin.readline()
decrypt(private, int(cipher))

inp.close()
codin.close()