# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from book.models import *
# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    site_order = 1
    list_display = ('name', 'desc', 'order_number', 'status')
    fields = ('name', 'desc', 'order_number', 'status')
