from django.shortcuts import render
import random
import random
from .forms import CryptoForm
from sympy import isprime

def generate_prime_number(length=10):
    while True:
        p = random.getrandbits(length)
        if isprime(p):
            return p

def find_primitive_root(p):
    for g in range(2, p - 1):
        if all(pow(g, (p - 1) // q, p) != 1 for q in factorize(p - 1)):
            return g

def factorize(n):
    factors = []
    for i in range(2, n + 1):
        while n % i == 0:
            factors.append(i)
            n //= i
    return factors

def modular_inverse(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1

def generate_key(length=5):
    p = generate_prime_number(length)
    alpha = find_primitive_root(p)
    k = random.randint(2, p - 2)
    y = pow(alpha, k, p)
    return f"{p},{alpha},{k}", k   

def encrypt(x, public_key, private_key):
    k = int(private_key)
    p,alpha,beta = public_key
    y1 = pow(alpha,k,p)
    y2 = (x * pow(beta, k, p)) % p
    return f'{y1,y2}'

def decrypt(y,private_key,p):
    y1,y2 = y.split(",")
    y1, y2, k = int(y1), int(y2), int(private_key), int(p)
    x = (y2 * modular_inverse(pow(y1, k, p), p)) % p
    return str(x)

def crypto_view(request):
    if request.method == 'POST':
        form = CryptoForm(request.POST)
        if form.is_valid():
            operation = form.cleaned_data['operation']
            input = form.cleaned_data['input']
            public_key = form.cleaned_data['public_key']
            private_key = form.cleaned_data['private_key']
            if public_key == "" or private_key == "":
                public_key,private_key = generate_key()
            else:
                private_key = public_key.split(",")[0]
            
            if operation == 'encrypt':
                result = encrypt(input, public_key, private_key)
            else:
                p = public_key.split(",")[0]
                result = decrypt(input,private_key,p)

            context = {'public_key': public_key,'private_key': public_key, 'result': result}
            context['form'] = form
            return render(request, 'ELGAMAL.html', context)

    else:
        form = CryptoForm()

    context = {'form': form}
    return render(request, 'ELGAMAL.html', context)