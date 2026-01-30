from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_http_methods
from .models import ChatSession
from .services import ChatService
import json

# @login_required  # Temporariamente desabilitado
def chat_view(request, session_id=None):
    """View principal do chat - exibe sessão específica ou cria nova"""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    # Get or create user
    if request.user.is_authenticated:
        user = request.user
    else:
        user = User.objects.filter(is_superuser=True).first()
        if not user:
            user, created = User.objects.get_or_create(
                username='demo',
                defaults={'email': 'demo@lia.com', 'role': 'admin'}
            )
            if created:
                user.set_password('demo')
                user.save()
    
    # Get all user sessions
    all_sessions = ChatSession.objects.filter(user=user).order_by('-updated_at')
    
    # Get or create current session
    if session_id:
        session = get_object_or_404(ChatSession, id=session_id, user=user)
    else:
        session = all_sessions.first()
        if not session:
            session = ChatSession.objects.create(user=user, title="Nova Conversa")
    
    messages = session.messages.all().order_by('created_at')
    
    return render(request, 'chat/chat.html', {
        'session': session,
        'messages': messages,
        'all_sessions': all_sessions,
    })

# @login_required
def new_session_view(request):
    """Cria uma nova sessão de chat"""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    if request.user.is_authenticated:
        user = request.user
    else:
        user = User.objects.filter(is_superuser=True).first()
        if not user:
            user = User.objects.get(username='demo')
    
    session = ChatSession.objects.create(user=user, title="Nova Conversa")
    return redirect('chat_session', session_id=session.id)

# @login_required
@require_http_methods(["DELETE", "POST"])
def delete_session_view(request, session_id):
    """Deleta uma sessão de chat"""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    if request.user.is_authenticated:
        user = request.user
    else:
        user = User.objects.filter(is_superuser=True).first()
        if not user:
            user = User.objects.get(username='demo')
    
    session = get_object_or_404(ChatSession, id=session_id, user=user)
    session.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})
    return redirect('chat')

# @login_required
def list_sessions_api(request):
    """API para listar todas as sessões do usuário"""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    if request.user.is_authenticated:
        user = request.user
    else:
        user = User.objects.filter(is_superuser=True).first()
        if not user:
            user = User.objects.get(username='demo')
    
    sessions = ChatSession.objects.filter(user=user).order_by('-updated_at')
    
    data = [{
        'id': s.id,
        'title': s.title,
        'created_at': s.created_at.isoformat(),
        'message_count': s.messages.count()
    } for s in sessions]
    
    return JsonResponse({'sessions': data})

# @login_required
@require_POST
def api_chat_message(request):
    """API para enviar mensagem no chat"""
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

