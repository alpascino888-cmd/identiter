from django.shortcuts import render
from django.contrib import messages


def home(request):
    return render(request, 'core/home.html')


def about(request):
    return render(request, 'core/about.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if name and email and message:
            messages.success(
                request,
                'Votre message a été envoyé avec succès ! Nous vous répondrons dans les plus brefs délais.'
            )
        else:
            messages.error(request, 'Veuillez remplir tous les champs obligatoires.')

    return render(request, 'core/contact.html')
