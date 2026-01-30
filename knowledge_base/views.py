from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import DocumentForm
from .models import Document
from .services import DocumentProcessor, VectorStoreService
import os
import shutil

# @login_required  # Temporariamente desabilitado
def upload_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            # Handle anonymous user for upload
            if request.user.is_authenticated:
                doc.uploaded_by = request.user
            else:
                from django.contrib.auth import get_user_model
                User = get_user_model()
                # Use first superuser or create default
                user = User.objects.filter(is_superuser=True).first()
                if not user:
                    user = User.objects.create_user(username='demo', email='demo@lia.com', password='demo', role='admin')
                doc.uploaded_by = user

            doc.save()
            
            try:
                # Process document
                processor = DocumentProcessor()
                # Include visibility in metadata
                extra_metadata = {"visibility": doc.visibility}
                splits = processor.process(doc.file.path, extra_metadata=extra_metadata)
                
                # Check for API Key before calling Vector Service
                if not os.getenv("GOOGLE_API_KEY"):
                    messages.warning(request, "Documento salvo, mas não processado. GOOGLE_API_KEY não configurada.")
                else:
                    vector_service = VectorStoreService()
                    vector_service.add_documents(splits)
                    doc.processed = True
                    doc.save()
                    messages.success(request, "Documento processado e indexado com sucesso!")
            except Exception as e:
                import traceback
                traceback.print_exc()
                messages.error(request, f"Erro ao processar documento: {str(e)}")
            
            return redirect('upload_document')
    else:
        form = DocumentForm()
    
    documents = Document.objects.all().order_by('-uploaded_at')
    return render(request, 'knowledge_base/upload.html', {'form': form, 'documents': documents})
