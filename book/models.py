# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from book.views import calc_return_date, calc_end_time
from django.utils.translation import gettext_lazy as _
from django.db import models


class Base(models.Model):
    """父模型类"""
    STATUS = (
        ('RE', 'Removed'),
        ('AC', 'Active')
    )

    status = models.CharField(default='AC', choices=STATUS, max_length=5)
    create_user_id = models.IntegerField(null=True, editable=False)
    create_time = models.DateTimeField(default=timezone.now, editable=False)
    update_user_id = models.IntegerField(null=True, editable=False)
    update_time = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        abstract = True


class Category(Base):
    """图书分类"""
    name = models.CharField(max_length=20, null=False)
    desc = models.CharField(max_length=100)
    order_number = models.IntegerField(default=0)


class Shelf(Base):
    category = models.ForeignKey('Category', on_delete=models.DO_NOTHING, null=True)
    code = models.CharField(max_length=100, null=False)
    location = models.CharField(max_length=20, null=False, default='')
    floors = models.IntegerField(default=4)
    capacity = models.IntegerField(default=100)


class Book(Base):
    """书籍"""
    BOOK_STATUS = (
        ('ON', 'ON Shelf'),
        ('OUT', 'Check Out'),
        ('RE', 'Returned'),
        ('LO', 'Lost')
    )
    name = models.CharField(max_length=20, null=False)
    version = models.CharField(max_length=20, default='', blank=True)
    author = models.CharField(max_length=20, null=False)
    trans = models.CharField(max_length=20, null=False)
    press = models.CharField(max_length=20, null=False)
    ISBN = models.CharField(max_length=20, null=False)
    total_page = models.IntegerField(default=200)
    price = models.DecimalField(default=50.00, max_digits=10, decimal_places=2)
    real_price = models.DecimalField(default=40.00, max_digits=10, decimal_places=2)
    score = models.FloatField(default=4.0, editable=False)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, null=True)
    shelf = models.ForeignKey(Shelf, on_delete=models.DO_NOTHING, null=True)
    shelf_floor = models.IntegerField(default=1)
    book_status = models.CharField(choices=BOOK_STATUS, default='ON', null=False, max_length=10)
    series = models.CharField(max_length=20, default='', blank=True)
    seres_number = models.IntegerField(default=0)


class UserProfile(Base):
    """用户资料"""
    SEX = (
        ('M', 'Male'),
        ('F', 'Female')
    )

    user = models.OneToOneField(User, on_delete=models.DO_NOTHING, null=False)
    mobile = models.CharField(max_length=11, default='', blank=True)
    sex = models.CharField(choices=SEX, default='M', null=False, max_length=1)
    birth = models.DateField(null=False, blank=True)
    job = models.CharField(null=False, max_length=50)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateTimeField(default=calc_end_time)
    wx_id = models.CharField(max_length=100, default='', editable=False)


class CheckOut(Base):
    """借阅"""

    TYPE = (
        ('SC', 'Scan Code'),
        ('SH', 'Shift'),
    )

    BOOK_STATUS = (
        ('ON', 'ON Shelf'),
        ('OUT', 'Check Out'),
        ('RE', 'Returned'),
        ('LO', 'Lost')
    )

    user_profile = models.ForeignKey(UserProfile, null=False, on_delete=models.DO_NOTHING)
    book = models.ForeignKey(Book, null=True, on_delete=models.DO_NOTHING)
    book_status = models.CharField(choices=BOOK_STATUS, default='NO', null=False, max_length=10)
    time = models.DateField(default=timezone.now)
    type = models.CharField(choices=TYPE, max_length=5, default='SC')
    return_date = models.DateField(default=calc_return_date)
    returned_date = models.DateTimeField(null=False, blank=True)
    allow_shift = models.BooleanField(default=True)


class Comment(Base):
    """书评"""
    checkout = models.ForeignKey(CheckOut, on_delete=models.DO_NOTHING, null=False)
    score = models.FloatField(default=5.0)
    content = models.TextField(max_length=500)


class Note(Base):
    checkout = models.ForeignKey(CheckOut, on_delete=models.DO_NOTHING, null=False)
    page = models.FloatField(default=1)
    content = models.TextField(max_length=500)


class Rent(Base):
    """租阅"""
    PAY_STATUS = (
        (-2, 'Failed'),
        (0, 'Paying'),
        (2, 'Success'),
    )

    checkout = models.ForeignKey(CheckOut, on_delete=models.DO_NOTHING, null=False)
    days = models.IntegerField(default=1)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    order_no = models.CharField(max_length=50, blank=True)
    trade_no = models.CharField(max_length=50, blank=True)
    pay_status = models.IntegerField(choices=PAY_STATUS, default=0)


class Shift(Base):
    """转借"""

    SHIFT_STATUS = (
        ('Req', 'Requested'),
        ('Arg', 'Agreed'),
        ('Com', 'Completed'),
        ('Abr', 'Abort'),
        ('Ref', 'Refused')
    )

    checkout = models.ForeignKey(CheckOut, on_delete=models.DO_NOTHING, null=True)
    request_user_profile = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING, null=True)
    reason = models.TextField(max_length=100)
    agreed = models.BooleanField(default=False)
    reply = models.TextField(max_length=100, blank=True)
    shift_status = models.CharField(choices=SHIFT_STATUS, default='Req', max_length=3)
    request_time = models.DateTimeField(default=timezone.now)
    reply_time = models.DateTimeField(null=True, blank=True)
    complete_time = models.DateTimeField(null=True, blank=True)


class FeedBack(Base):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING, null=True)
    content = models.TextField(max_length=100)
    wx_form_id = models.CharField(max_length=100, null=True, editable=False)
    reply = models.TextField(max_length=200, blank=True)
    reply_time = models.DateTimeField(null=True, blank=True)
