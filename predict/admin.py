from django.contrib import admin

# Register your models here.

from .models import predictionModel1, reviewModel

admin.site.register(predictionModel1)


class ReviewDisplay(admin.ModelAdmin):
    list_display = ['title', 'review', 'email']

admin.site.register(reviewModel, ReviewDisplay)