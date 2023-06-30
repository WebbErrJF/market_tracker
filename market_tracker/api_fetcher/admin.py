from django.contrib import admin

from .models import StockData, StockCompany, StockDate

admin.site.register(StockData)
admin.site.register(StockCompany)
admin.site.register(StockDate)

