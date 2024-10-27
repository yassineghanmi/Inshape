from decimal import Decimal, InvalidOperation
from django import forms
from django.utils import timezone  # Import timezone
from .models import Nutrition

class NutritionForm(forms.ModelForm):
    selected_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Nutrition
        fields = ['name', 'calories', 'protein', 'carbohydrates', 'sugars', 'fats', 'selected_date']

    def __init__(self, *args, **kwargs):
        # Get the selected date if provided
        selected_date = kwargs.pop('selected_date', None)
        super().__init__(*args, **kwargs)
        # If no selected date is provided, set it to today's date
        if selected_date is None:
            self.fields['selected_date'].initial = timezone.now().date()

    # Additional validation for Decimal fields
    def clean_calories(self):
        return self._validate_decimal('calories')

    def clean_protein(self):
        return self._validate_decimal('protein')

    def clean_carbohydrates(self):
        return self._validate_decimal('carbohydrates')

    def clean_sugars(self):
        return self._validate_decimal('sugars')

    def clean_fats(self):
        return self._validate_decimal('fats')

    # Helper function to ensure the value is a valid decimal
    def _validate_decimal(self, field_name):
        value = self.cleaned_data.get(field_name)
        try:
            decimal_value = Decimal(value) if value is not None else None
            if decimal_value is not None and decimal_value < 0:
                raise forms.ValidationError(f"{field_name.capitalize()} must be a positive number.")
            return decimal_value
        except (InvalidOperation, ValueError):
            raise forms.ValidationError(f"Please enter a valid decimal number for {field_name}.")

class BarcodeImageForm(forms.Form):
    image = forms.ImageField(label='Upload an image')

class SearchForm(forms.Form):
    query = forms.CharField(label='Search for food', max_length=100)
