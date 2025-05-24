from django.core.mail import send_mail

send_mail(
    'Subject here',
    'Here is the message.',
    'todd427@gmail.com',
    ['todd427@gmail.com'],
    fail_silently=False,
)

