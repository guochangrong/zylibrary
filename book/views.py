# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.utils import timezone
# Create your views here.


def calc_end_time(*args, **kwargs):
    """用户失效期"""
    now = timezone.now()
    m6 = timezone.timedelta(days=31 * 6)

    return now + m6


def calc_return_date():
    """还书日期"""
    now = timezone.now()
    days_15 = timezone.timedelta(days=15)
    return now + days_15
