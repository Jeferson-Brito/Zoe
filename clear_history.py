import os
import sys
import django

# Add project root to python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lia_project.settings')
django.setup()

from chat.models import ChatMessage, ChatSession
from django.contrib.auth import get_user_model

try:
    print("Deleting all chat sessions...")
    ChatSession.objects.all().delete()
    print("✅ Chat History Cleared.")
except Exception as e:
    print(f"❌ Error clearing history: {e}")
