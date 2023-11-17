from django.shortcuts import render

# Create your views here.
def area(request):
    return render(request, 'SGE_area/area.html', {})
