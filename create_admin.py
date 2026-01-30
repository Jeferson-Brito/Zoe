import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

if not User.objects.filter(email='jeffersonbrito2455@gmail.com').exists():
    user = User.objects.create_superuser(
        username='jefferson',
        email='jeffersonbrito2455@gmail.com',
        password='memphisac39bk',
        role='admin'
    )
    print("✅ Usuário criado com sucesso!")
    print(f"Username: jefferson")
    print(f"Email: {user.email}")
else:
    print("⚠️ Usuário já existe!")
