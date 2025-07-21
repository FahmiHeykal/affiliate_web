from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Product, Category
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Div, HTML
from crispy_bootstrap5 import bootstrap5
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

class StaffLoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(
        required=False, 
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'mt-4'
        self.helper.layout = Layout(
            'username',
            'password',
            Div(
                Row(
                    Column(
                        Div(
                            'remember_me',
                            css_class='form-check'
                        ),
                        css_class='col-md-6'
                    ),
                    Column(
                        HTML('<a href="#" class="float-end text-decoration-none">Lupa Password?</a>'),
                        css_class='col-md-6'
                    )
                ),
                css_class='mb-3'
            ),
            Submit('submit', 'Login', css_class='btn-primary w-100 py-2')
        )

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'is_active']
        labels = {
            'name': 'Nama Kategori',
            'is_active': 'Aktif'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_tag = True
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='col-md-12')
            ),
            Row(
                Column('is_active', css_class='col-md-12')
            ),
            Div(
                Submit('submit', 'Simpan', css_class='btn-primary me-2'),
                HTML('<a href="{% if object %}{% url "dashboard_category_update" object.pk %}{% else %}{% url "dashboard_category_list" %}{% endif %}" class="btn btn-secondary">Batal</a>'),
                css_class='d-flex justify-content-end mt-4'
            )
        )

class ProductForm(forms.ModelForm):
    def clean_affiliate_link(self):
        affiliate_link = self.cleaned_data.get('affiliate_link')
        validator = URLValidator()
        try:
            validator(affiliate_link)
        except ValidationError:
            raise forms.ValidationError("Masukkan URL yang valid")
        return affiliate_link

    class Meta:
        model = Product
        fields = [
            'category', 'name', 'description', 'price', 
            'image', 'affiliate_link', 'meta_title', 
            'meta_description', 'is_featured', 'is_active'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'meta_description': forms.Textarea(attrs={'rows': 2}),
        }
        labels = {
            'category': 'Kategori',
            'name': 'Nama Produk',
            'description': 'Deskripsi',
            'price': 'Harga',
            'image': 'Gambar Produk',
            'affiliate_link': 'Link Afiliasi',
            'meta_title': 'Meta Title (SEO)',
            'meta_description': 'Meta Description (SEO)',
            'is_featured': 'Produk Unggulan',
            'is_active': 'Aktif'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(is_active=True)
        
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_tag = True
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.layout = Layout(
            Row(
                Column('category', css_class='col-md-6'),
                Column('name', css_class='col-md-6')
            ),
            Row(
                Column('description', css_class='col-md-12')
            ),
            Row(
                Column('price', css_class='col-md-4'),
                Column('affiliate_link', css_class='col-md-8')
            ),
            Row(
                Column('image', css_class='col-md-6'),
                Column(Div(
                    HTML("""
                        {% if form.image.value %}
                            <img src="{{ form.instance.image.url }}" class="img-thumbnail mb-2" style="max-height: 150px;">
                        {% endif %}
                    """),
                    css_class='mb-3'
                ), css_class='col-md-6')
            ),
            Row(
                Column('meta_title', css_class='col-md-6'),
                Column('meta_description', css_class='col-md-6')
            ),
            Row(
                Column('is_featured', css_class='col-md-6'),
                Column('is_active', css_class='col-md-6')
            ),
            Div(
                Submit('submit', 'Simpan', css_class='btn-primary me-2'),
                HTML('<a href="{% if object %}{% url "dashboard_product_update" object.pk %}{% else %}{% url "dashboard_product_list" %}{% endif %}" class="btn btn-secondary">Batal</a>'),
                css_class='d-flex justify-content-end mt-4'
            )
        )
    
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise forms.ValidationError("Harga tidak boleh negatif")
        return price