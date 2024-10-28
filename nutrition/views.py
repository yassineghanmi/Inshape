# views.py
from django.utils import timezone
import requests
from django.shortcuts import render, redirect, get_object_or_404
from .models import Nutrition
from .forms import NutritionForm  # You'll need to create this form
import cv2
import zxingcpp
import openfoodfacts
from .forms import BarcodeImageForm, SearchForm
import numpy as np
import sweetify
from django.http import JsonResponse
from django.db.models import Sum, Count
from django.contrib.auth.decorators import login_required

# List view
def nutrition_list(request):
    # Get the selected date from the request (if provided) or default to today
    selected_date = request.GET.get('date', timezone.now().date())

    # Get the search query from the request (if provided)
    search_query = request.GET.get('search', '').strip()  # Strip whitespace from the search query

    # Filter nutrition items by the selected date

    if search_query:
        items = Nutrition.objects.filter(created_at__date=selected_date)
    else:
        items = Nutrition.objects.filter(created_at__date=selected_date, user=request.user)


    # If a search query is provided, filter items and ensure no duplicates
    if search_query:
        items = items.filter(name__icontains=search_query).distinct()  # Use distinct to avoid duplicates

    # Calculate the sum of calories using Django's aggregation
    total_calories = items.aggregate(Sum('calories'))['calories__sum'] or 0  # Use aggregate for better performance

    return render(request, 'nutrition/nutrition_list.html', {
        'items': items,
        'selected_date': selected_date,
        'total_calories': total_calories,
        'search_query': search_query,  # Pass search query to the template
    })


# Initialize the API
api = openfoodfacts.API(user_agent="MyAwesomeApp/1.0")


def add_by_barcode(request):
    product_info = None
    selected_date = request.GET.get('date')  # Get date from query parameters if available

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
                product_info = api.product.get(barcode,
                                               fields=["code", "product_name", "nutriments", "selected_images"])

                # Here you could set the selected_date or current date if necessary
                if 'selected_date' not in product_info:  # Assuming product_info is a dictionary
                    product_info[
                        'selected_date'] = selected_date or timezone.now().date()  # Default to today if no date is provided
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
@login_required
def nutrition_create(request):
    if request.method == 'POST':
        form = NutritionForm(request.POST)
        if form.is_valid():
            # Create a new Nutrition instance
            nutrition_item = form.save(commit=False)
            # Set created_at field to the current date and time
            nutrition_item.created_at = timezone.now()

            nutrition_item.user = request.user
            # Save the instance
            nutrition_item.save()
            return redirect('nutrition_list')
    else:
        # Get the data from the query parameters
        initial_data = {
            'name': request.GET.get('name', ''),
            'calories': request.GET.get('calories', ''),
            'protein': request.GET.get('protein', ''),
            'carbohydrates': request.GET.get('carbohydrates', ''),
            'sugars': request.GET.get('sugars', ''),
            'fats': request.GET.get('fats', ''),

        }
        form = NutritionForm(initial=initial_data)  # Pre-fill the fields with initial data

    return render(request, 'nutrition/nutrition_form.html', {'form': form})


# Update view
def nutrition_update(request, pk):
    item = get_object_or_404(Nutrition, pk=pk)
    if request.method == 'POST':
        form = NutritionForm(request.POST, instance=item)
        if form.is_valid():
            nutrition_item = form.save(commit=False)

            # Check if selected_date is empty and set it to today's date if necessary
            if not form.cleaned_data['selected_date']:
                nutrition_item.selected_date = timezone.now().date()

            nutrition_item.save()
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


# Detail view

def nutrition_detail(request, pk):
    item = get_object_or_404(Nutrition, pk=pk)
    return render(request, 'nutrition/nutrition_detail.html', {'item': item})
