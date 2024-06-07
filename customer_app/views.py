from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import DocumentSet, Customer, CustomerDocument
from .forms import CustomerForm, CustomerDocumentForm
import boto3
from django.conf import settings

textract = boto3.client('textract', region_name='us-east-1') 

@login_required
def create_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.created_by = request.user
            customer.save()
            return redirect('upload_document', customer_id=customer.id)
    else:
        form = CustomerForm()
    return render(request, 'create_customer.html', {'form': form})

@login_required
def upload_document(request, customer_id):
    customer = Customer.objects.get(pk=customer_id)
    if request.method == 'POST':
        form = CustomerDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.customer = customer
            document.save()

            with open(document.attached_file.path, 'rb') as file:
                response = textract.analyze_document(
                    Document={'Bytes': file.read()},
                    FeatureTypes=["FORMS"]
                )
            
            extracted_data = {}
            for block in response['Blocks']:
                if block['BlockType'] == 'LINE':
                    extracted_data[block['Id']] = block['Text']
            
            document.extracted_json = extracted_data
            document.save()

            return redirect('customer_list')
    else:
        form = CustomerDocumentForm()
    return render(request, 'upload_document.html', {'form': form, 'customer': customer})

@login_required
def customer_list(request):
    customers = Customer.objects.filter(created_by=request.user)
    return render(request, 'customer_list.html', {'customers': customers})
