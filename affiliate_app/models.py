from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name="Nama Kategori")
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name="Aktif")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Kategori"
        verbose_name_plural = "Kategori"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("public_category", args=[self.slug])

    def product_count(self):
        return self.products.count()


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        related_name="products",
        on_delete=models.CASCADE,
        verbose_name="Kategori"
    )
    name = models.CharField(max_length=200, verbose_name="Nama Produk")
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(verbose_name="Deskripsi")
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Harga"
    )
    image = models.ImageField(
        upload_to="products/%Y/%m/%d/",
        verbose_name="Gambar Produk"
    )
    affiliate_link = models.URLField(verbose_name="Link Afiliasi")
    meta_title = models.CharField(max_length=500, blank=True)
    meta_description = models.CharField(max_length=500, blank=True)
    is_featured = models.BooleanField(default=False, verbose_name="Produk Unggulan")
    is_active = models.BooleanField(default=True, verbose_name="Aktif")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="products_created"
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="products_updated"
    )

    class Meta:
        verbose_name = "Produk"
        verbose_name_plural = "Produk"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["name"]),
            models.Index(fields=["category"]),
            models.Index(fields=["is_active"]),
            models.Index(fields=["is_featured"]),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if not self.meta_title:
            self.meta_title = self.name
        if not self.meta_description:
            self.meta_description = self.description[:200]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("public_product_detail", args=[self.slug])

    def get_price_display(self):
        try:
            price = float(self.price)
            formatted = f"{price:,.2f}"
            formatted = (
                formatted.replace(",", "X")
                         .replace(".", ",")
                         .replace("X", ".")
            )
            return f"Rp{formatted}"
        except (ValueError, TypeError, AttributeError):
            return "Rp0,00"

    def get_short_description(self, max_length=100):
        description = getattr(self, "description", "")
        if not description:
            return ""
        description = str(description)
        return description[:max_length] + "..." if len(description) > max_length else description
