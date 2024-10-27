# views.py
from django.utils import timezone
import requests
from django.shortcuts import render, redirect, get_object_or_404
from .models import Nutrition
from .forms import NutritionForm  # You'll need to create this form
import cv2
import zxingcpp
import openfoodfacts
from .forms import BarcodeImageForm ,SearchForm
import numpy as np
import sweetify
from django.http import JsonResponse
# List view
def nutrition_list(request):
       # Get the selected date from the request (if provided) or default to today
    selected_date = request.GET.get('date', timezone.now().date())
    # Filter nutrition items by the selected date
    items = Nutrition.objects.filter(created_at__date=selected_date).order_by('created_at')
    
    return render(request, 'nutrition/nutrition_list.html', {'items': items, 'selected_date': selected_date})

   # Initialize the API
api = openfoodfacts.API(user_agent="MyAwesomeApp/1.0")
def add_by_barcode(request):
    product_info = None
    if request.method == 'POST':
        form = BarcodeImageForm(request.POST, request.FILES)
        if form.is_valid():
            # Read and process the uploaded image
            image_file = form.cleaned_data['image']
            img = cv2.imdecode(np.frombuffer(image_file.read(), np.uint8), cv2.IMREAD_COLOR)
            
            # Detect barcode in the image
            results = zxingcpp.read_barcodes(img)
            if results:
                barcode = results[0].text
                # Fetch product data from OpenFoodFacts
                product_info = api.product.get(barcode, fields=["code", "product_name", "nutriments","selected_images"])
            else:
                product_info = {"error": "Could not find any barcode."}
    else:
        form = BarcodeImageForm()
    
    return render(request, 'nutrition/add_by_barcode.html', {'form': form, 'product_info': product_info})


def add_nutrition(request):
    if request.method == 'POST':
        form = NutritionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('nutrition_list')  # Redirect on successful save
        else:
            # Render the form with validation errors if invalid
            return render(request, 'nutrition/nutrition_form.html', {'form': form})

    form = NutritionForm()
    return render(request, 'nutrition/nutrition_form.html', {'form': form})

# Create view
def nutrition_create(request):
    if request.method == 'POST':
        form = NutritionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('nutrition_list')
    else:
        form = NutritionForm()
    return render(request, 'nutrition/nutrition_form.html', {'form': form})

# Update view
def nutrition_update(request, pk):
    item = get_object_or_404(Nutrition, pk=pk)
    if request.method == 'POST':
        form = NutritionForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('nutrition_list')
    else:
        form = NutritionForm(instance=item)
    return render(request, 'nutrition/nutrition_form.html', {'form': form})

# Delete view
def nutrition_delete(request, pk):
    item = get_object_or_404(Nutrition, pk=pk)
    try:
        item.delete()
        return JsonResponse({'success': True})  # JSON success response
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500) 