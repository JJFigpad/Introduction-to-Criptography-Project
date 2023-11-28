from sympy import mod_inverse
from .forms import CryptoForm
from django.shortcuts import render
from .forms import CryptoForm
import random

# Función que representa una curva elíptica
def elliptic_curve(a, b, p):
    # Definimos la ecuación de la curva elíptica: y^2 = x^3 + ax + b
    return lambda x: (x**3 + a*x + b) % p

def sum_curve(x,y,a,p):
    x_1,x_2 = x
    y_1,y_2 = y
    if x_1!=x_2:
        lambda_value = ((y_2-y_1)*mod_inverse(x_2-x_1,p)) % p
    else:
        lambda_value = ((3*x_1*x_1+a)*mod_inverse(2*y_1,p)) % p
    x_3 = (lambda_value*lambda_value - x_1 - x_2) % p
    y_3 = (lambda_value*(x_1-x_3)-y_1) % p

    return (x_3,y_3)

def product_curve(k,alpha,a,p):
    product = alpha
    for i in range(1,k):
        product = sum_curve(alpha,product,a,p)
    return product

# Raíz cuadrada modular
def mod_sqrt(a, p):
    for i in range(p):
        if (i * i) % p == a:
            return i
    return None

# Función para encontrar puntos de la curva
def find_all_points_on_curve(ec, p):
    points = []
    for x_val in range(p):
        y_squared = ec(x_val)
        y_val = mod_sqrt(y_squared, p)
        # Añadir el punto si se encuentra una raíz cuadrada válida
        if y_val is not None:
            # Añadir ambos puntos (x, y) y (x, -y mod p)
            points.append((x_val, y_val))
            points.append((x_val, (-y_val % p)))
    return points

def generate_key(p):
    k = random.randint(0,p)
    return k
    
def crypto_view(request):
    if request.method == 'POST':
        form = CryptoForm(request.POST)
        if form.is_valid():
            # Eliptic curve params y^2 = x^3 + ax + b mod p
            a,b,p = 1,6,11
            ec = elliptic_curve(a, b, p)
            operation = form.cleaned_data['operation']
            input = form.cleaned_data['input']
            alpha = form.cleaned_data['public_alpha']
            beta = form.cleaned_data['public_beta']
            private_key = form.cleaned_data['private_key'] or generate_key(p)

            # Eliptic curve points
            points_curve = find_all_points_on_curve(ec, p)
            if alpha=="" or beta=="":
                alpha,beta = random.sample(points_curve,2)
            else:
                alpha = alpha.split(",")
                alpha = (int(alpha[0]),int(alpha[1]))
                beta = beta.split(",")
                beta = (int(beta[0]),int(beta[1]))

            # Encrypt
            k = int(private_key)
            if operation=="encrypt":
                x = input.split(",")
                x = (int(x[0]),int(x[1]))
                x_1,x_2 = x
                y_0 = product_curve(k,alpha,a,p)
                c_1,c_2 = product_curve(k,beta,a,p)
                y_1 = (c_1*x_1)%p
                y_2 = (c_2*x_2)%p
                result = f'{y_0[0]},{y_0[1]},{y_1},{y_2}'
            else:
                y = input.split(",")
                y_0_1,y_0_2,y_1,y_2 = int(y[0]), int(y[1]), int(y[2]), int(y[3])
                y_0 = (y_0_1,y_0_2)
                c_1,c_2 = product_curve(k,y_0)
                x_1 = (y_1*mod_inverse(c_1)) % p  
                x_2 = (y_2*mod_inverse(c_2)) % p
                result = f'{x_1},{x_2}'

            context = {'Eliptic Curve':f"y^2 = x^3 + {a}x + {b} mod {p}",
                       'public_alpha':f'{alpha}','public_beta':f'{beta}',
                       'private_key': private_key, 'result': result}
            context['form'] = form
            return render(request, 'Menezes.html', context)

    else:
        form = CryptoForm()

    context = {'form': form}
    return render(request, 'Menezes.html', context)