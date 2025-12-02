from django.db import models


class Branch(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre")
    address = models.CharField(max_length=255, verbose_name="Dirección", blank=True)
    phone = models.CharField(max_length=20, verbose_name="Teléfono", blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Sucursal"
        verbose_name_plural = "Sucursales"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Professional(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre")
    specialty = models.CharField(max_length=100, verbose_name="Especialidad", blank=True)
    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name="professionals",
        verbose_name="Sucursal"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Profesional"
        verbose_name_plural = "Profesionales"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.specialty})"
