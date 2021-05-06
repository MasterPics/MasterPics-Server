from django.shortcuts import render

# Create your views here.
def main_list(request):
    ctx = {}
    return render(request, 'core/main_list.html', context=ctx)
