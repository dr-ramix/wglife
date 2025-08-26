from django.contrib import admin
from .models import Work, Task, Assignment

models = [Work, Task, Assignment]
for model in models:
    admin.site.register(model)