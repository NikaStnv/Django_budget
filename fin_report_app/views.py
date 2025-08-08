from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from fin_report_app.models import UploadedFiles
from fin_report_app.signals import limit_signal

def upload_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        if not file.name.endswith('.txt'):
            return JsonResponse({'error': 'Only .txt files are allowed.'}, status=400)
        try:
            content = file.read()
            word_count = len(content.split())
            char_count = len(content)
        
            uploaded_file = UploadedFiles(
                file=file,
                file_name=file.name,
                word_count=word_count,
                char_count=char_count,
              
            )
            
            uploaded_file.save()
            limit_signal.send(sender=UploadedFiles, instance=uploaded_file) 
                        
            return JsonResponse({
                'id': uploaded_file.id,
                'file_name': file.name,
                'word_count': word_count,
                'char_count': char_count,
                'uploaded_at': uploaded_file.uploaded_at.strftime('%Y-%m-%d %H:%M:%S'),
                'file_url': uploaded_file.file.url
                })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'No file provided!'}, status=400)


def list_uploaded_files(request):
    files = UploadedFiles.objects.all().order_by('-uploaded_at')
    file_list = [{
        'id': f.id,
        'file_name': f.file_name,
        'word_count': f.word_count,
        'char_count': f.char_count,
        'uploaded_at': f.uploaded_at.strftime('%Y-%m-%d %H:%M:%S'),
        'file_url': f.file.url
    } for f in files]
    return JsonResponse({'files': file_list})

def view_uploaded_files(request, upload_file_id):
    uploaded_files = get_object_or_404(UploadedFiles, id=upload_file_id)
    
    try:
        with uploaded_files.file.open('r') as f:
            content = f.read()
        return JsonResponse({
            'id': uploaded_files.id,
            'file_name': uploaded_files.file_name,
            'word_count': uploaded_files.word_count,
            'char_count': uploaded_files.char_count,
            'content': content,
            'uploaded_at': uploaded_files.uploaded_at.strftime('%Y-%m-%d %H:%M:%S'),
            'file_url': uploaded_files.file.url
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
def delete_uploaded_file(request, upload_file_id):
    if request.method == 'POST':
        uploaded_files = get_object_or_404(UploadedFiles, id=upload_file_id)
        try:
            uploaded_files.delete()
            return JsonResponse({'message': f'File {uploaded_files.file_name} deleted successfully.'})  
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
    return JsonResponse({'error': 'Invalid method not allowed'}, status=405)
       
