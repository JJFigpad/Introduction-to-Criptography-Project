from django.shortcuts import render

def index(request):
    app_list1 = [
        ('desplazamiento','desplazamiento'),
        ('afin','afin'),
        ('Vigenere', 'vigenere'),
        ('permutacion','permutacion'),
        ('hillI','hillI'),
        ('hillT','hillT'),
        ('Sustitucion', 'sustitucion'),
        ('Multiplicativo', 'multiplicativo'),
        # Agrega más aplicaciones según sea necesario
    ]
    app_list2 = [
        ('DES','DES'),
        ('DESimagen','DESimagen'),
        ('AES1','image_upload'),
    ]
    app_list3 = [
        ('RSA','RSA'),
        ('RSAI','RSAI'),
        ('rabin','index'),
        ('ELGAMAL1','ELGAMAL1'),
        ('Menezes','Menezes'),
        ('DSA','DSA')    
        ]

    context = {'app_list': app_list1, 'app_list2': app_list2, 'app_list3': app_list3}
    return render(request, 'index.html', context)