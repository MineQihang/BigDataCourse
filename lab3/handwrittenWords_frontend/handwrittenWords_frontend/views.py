from django.shortcuts import render

# Create your views here.
def handwrittenBoard(request):
    return render(request,'handwrittenBoard.html')