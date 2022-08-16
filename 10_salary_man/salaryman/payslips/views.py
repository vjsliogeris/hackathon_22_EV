from django.shortcuts import render

from django.http import HttpResponse

from .forms import PayslipForm 

from main import handle_payslip

def index(request):
    if request.method == 'POST':
        form = PayslipForm(request.FILES)
        handle_payslip(request.FILES['payslip_doc'])
        return HttpResponse('Poggers')
    else:
        form = PayslipForm()

    return render(request, 'payslips/index.html', {'form':form})
