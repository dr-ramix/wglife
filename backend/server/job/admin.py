from django.contrib import admin
from .models import Work, Task, TaskTemplate, WorkCycle

models = [Work, Task, TaskTemplate, WorkCycle]
for model in models:
    admin.site.register(model)