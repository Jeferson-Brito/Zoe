from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import ChatSession
from .services import ChatService
import json

# @login_required  # Temporariamente desabilitado
def chat_view(request):
    # Get or create a session for today/latest or just list sessions
    # For simplicity: Always get the latest session or create new
    # A real app would have a sidebar list of sessions.
    
    # Use default user for anonymous users
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    if request.user.is_authenticated:
        user = request.user
    else:
        # Use first superuser as default
        user = User.objects.filter(is_superuser=True).first()
        if not user:
            # Create a default user if none exists
            user = User.objects.create_user(username='demo', email='demo@lia.com', password='demo', role='admin')
    
    session = ChatSession.objects.filter(user=user).order_by('-created_at').first()
    if not session:
        session = ChatSession.objects.create(user=user, title="Nova Conversa")
    
    messages = session.messages.all().order_by('created_at')
    
    return render(request, 'chat/chat.html', {
        'session': session,
        'messages': messages
    })

# @login_required  # Temporariamente desabilitado
@require_POST
def api_chat_message(request):
    data = json.loads(request.body)
    message_text = data.get('message')
    session_id = data.get('session_id')
    
    if not message_text:
        return JsonResponse({'error': 'Message required'}, status=400)
        
    session = get_object_or_404(ChatSession, id=session_id)
    
    try:
        service = ChatService()
        response_text = service.chat(session, message_text)
        return JsonResponse({'response': response_text})
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({'error': f"Erro interno no servidor: {str(e)}"}, status=500)

# @login_required  # Temporariamente desabilitado
def new_session(request):
    ChatSession.objects.create(user=request.user, title="Nova Conversa")
    return redirect('chat')
