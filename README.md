# Zoe - Assistente IA Conversacional

Aplicação Django de chat com inteligência artificial usando Google Gemini e LangChain.

## 🚀 Características

- 💬 **Chat Inteligente** com IA usando Google Gemini
- 📚 **Knowledge Base** com ChromaDB para contexto
- ☁️ **Banco de Dados** Supabase PostgreSQL ou SQLite local
- 🎨 **Interface Moderna** com design responsivo
- 👤 **Sistema de Usuários** customizado

## 📋 Requisitos

- Python 3.11+
- Conta Google Cloud (para Gemini API)
- Conta Supabase (opcional, para banco em nuvem)

## 🔧 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/Jeferson-Brito/Zoe.git
cd Zoe
```

2. Crie e ative o ambiente virtual:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
```bash
cp .env.example .env
```

Edite o arquivo `.env` e adicione suas credenciais:
- `GOOGLE_API_KEY`: Sua chave da API do Google Gemini
- Para usar Supabase, configure `USE_SUPABASE=True` e adicione as credenciais do banco

5. Execute as migrações:
```bash
python manage.py migrate
```

6. Crie um superusuário:
```bash
python manage.py createsuperuser
```

7. Inicie o servidor:
```bash
python manage.py runserver
```

Acesse http://127.0.0.1:8000/

## 🗄️ Banco de Dados

O projeto suporta dois tipos de banco:

### SQLite (Padrão - Desenvolvimento)
```env
USE_SUPABASE=False
```

### Supabase PostgreSQL (Produção)
```env
USE_SUPABASE=True
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=sua_senha
DB_HOST=db.xxx.supabase.co
DB_PORT=5432
```

## 📚 Tecnologias

- **Backend**: Django 5.2
- **IA**: Google Gemini, LangChain
- **Vector Database**: ChromaDB
- **Database**: PostgreSQL (Supabase) / SQLite
- **Frontend**: HTML, CSS, JavaScript

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

## 📄 Licença

Este projeto está sob a licença MIT.

## 👤 Autor

Jeferson Brito
