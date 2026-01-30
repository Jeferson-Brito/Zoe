from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from knowledge_base.services import VectorStoreService
from .models import ChatMessage
from knowledge_base.models import LearnedKnowledge
import os

class ChatService:
    def __init__(self):
        self.vector_store = VectorStoreService()
        api_key = os.getenv("GOOGLE_API_KEY")
        if api_key:
            self.llm = ChatGoogleGenerativeAI(temperature=0, model="gemma-3-1b-it", google_api_key=api_key)
        else:
            self.llm = None

    def chat(self, session, message_text):
        # 1. Save user message
        ChatMessage.objects.create(session=session, role='user', content=message_text)

        if not self.llm:
            error_msg = "Erro: API Key não configurada. Configure GOOGLE_API_KEY no arquivo .env."
            ChatMessage.objects.create(session=session, role='ai', content=error_msg)
            return error_msg

        # 2. Retrieve Context
        user_role = session.user.role
        filter_criteria = None
        
        # Access Logic:
        # - Internal users see EVERYTHING (filter=None)
        # - Franchisees see ONLY 'franchisee' visibility documents
        if user_role == 'franchisee':
            filter_criteria = {'visibility': 'franchisee'}
        # If we had 'customer', we would filter by 'customer' (public)
        
        try:
            # DB Retrieval
            learned = LearnedKnowledge.objects.filter(is_active=True).order_by('-created_at')[:5]
            learned_text = "\n".join([f"- {l.content}" for l in learned])
            
            # Vector Retrieval
            results = self.vector_store.similarity_search(message_text, k=3, filter=filter_criteria)
            rag_text = ""
            if results:
                rag_text = "\n\n".join([doc.page_content for doc in results])
                
            context_text = f"MEMÓRIA:\n{learned_text}\n\nDOCUMENTOS:\n{rag_text}"
            if not learned_text and not rag_text:
                context_text = "Nenhum documento relevante encontrado."
        except Exception as e:
            context_text = ""
            print(f"Retrieval error: {e}")

        # 3. Prompt
        system_prompt = f"""Você é a LIA, assistente virtual da IKLI Tecnologia.
        Sua missão é atuar como consultor digital oficial da empresa para equipe interna, franqueados e clientes.
        
        REGRAS CRÍTICAS:
        1. Responda APENAS com base no CONTEXTO fornecido abaixo.
        2. Se a informação não estiver EXPLICITAMENTE no contexto, você DEVE responder: "Desculpe, não encontrei essa informação na minha base de conhecimento oficial."
        3. NÃO tente ajudar com conhecimentos gerais ou externos se não estiver no contexto.
        4. NÃO INVENTE INFORMAÇÕES. É melhor dizer que não sabe do que inventar.
        5. Se a pergunta for um cumprimento (ex: "Oi", "Bom dia"), responda educadamente e se apresente.
        
        CONTEXTO:
        {context_text}
        """

        # 4. Generate
        try:
            # Check if API key is set
            if not os.getenv("GOOGLE_API_KEY"):
                raise ValueError("API Key não configurada. Configure GOOGLE_API_KEY no arquivo .env")
            
            # Retrieve conversation history
            from langchain_core.messages import AIMessage
            
            history_messages = []
            # Get last 10 messages (5 turns)
            past_messages = ChatMessage.objects.filter(session=session).order_by('created_at').exclude(id=ChatMessage.objects.last().id)[:10]
            
            for msg in past_messages:
                if msg.role == 'user':
                    history_messages.append(HumanMessage(content=msg.content))
                elif msg.role == 'ai':
                    history_messages.append(AIMessage(content=msg.content))
            
            # Prepare messages
            if "gemma" in self.llm.model.lower():
                 # Gemma does not support SystemMessage (Developer Instruction)
                 # Prepend system prompt to the VERY first message in history, or the current message if history is empty
                 
                 full_system_text = f"{system_prompt}\n\n"
                 
                 if history_messages and isinstance(history_messages[0], HumanMessage):
                     # Prepend to first history item
                     history_messages[0].content = full_system_text + history_messages[0].content
                     messages_payload = history_messages + [HumanMessage(content=message_text)]
                 else:
                     # No history or starts with AI (unlikely for first), so prepend to current
                     messages_payload = history_messages + [HumanMessage(content=full_system_text + message_text)]
            else:
                # Standard Gemini supports SystemMessage
                messages_payload = [
                    SystemMessage(content=system_prompt)
                ] + history_messages + [
                    HumanMessage(content=message_text)
                ]
            
            response = self.llm.invoke(messages_payload)
            ai_text = response.content
            
            # Handle Gemini complex response (list of parts)
            if isinstance(ai_text, list):
                text_parts = []
                for part in ai_text:
                    if isinstance(part, dict):
                        text_parts.append(part.get('text', ''))
                    elif isinstance(part, str):
                        text_parts.append(part)
                ai_text = "".join(text_parts)
                ai_text = "".join(text_parts)
            elif not isinstance(ai_text, str):
                ai_text = str(ai_text)
            
            # Fallback for empty response
            if not ai_text or not ai_text.strip():
                ai_text = "Desculpe, não consegui gerar uma resposta com base nas informações disponíveis."
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            with open("debug_errors.txt", "a") as f:
                f.write(f"\\n--- Error at {os.environ.get('USERNAME')} ---\\n")
                f.write(error_details)
                f.write("\\n--------------------------------\\n")
            
            ai_text = f"ERRO DETALHADO: {str(e)}"

        # 5. Save AI message
        ChatMessage.objects.create(session=session, role='ai', content=ai_text)
        
        # 6. [MEMORY] Save to Database
        try:
             triggers = ["eu sou", "meu nome", "a regra", "o importante", "lembre-se", "mudei", "agora é"]
             if len(message_text) > 10 and any(t in message_text.lower() for t in triggers):
                 LearnedKnowledge.objects.create(
                     title=f"Aprendizado (Chat {str(session.id)[:8]})",
                     content=message_text,
                     source='chat',
                     created_by=session.user
                 )
                 print(f"MEMORY SAVED TO DB: {message_text}")
        except Exception as e:
            print(f"Memory Save Error: {e}")

        return ai_text
