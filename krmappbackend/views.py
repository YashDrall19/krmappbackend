from django.http import JsonResponse

def default(request):
    return JsonResponse({'message': 'Nothing Here!'})