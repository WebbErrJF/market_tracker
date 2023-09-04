from django.db import models


class StockCompany(models.Model):
    Name = models.CharField(max_length=100)
    Symbol = models.CharField(max_length=100)
    Default = models.BooleanField(default=False)

    def __str__(self):
        return self.Name


class StockData(models.Model):
    Price = models.FloatField()
    Change_point = models.FloatField()
    Change_percentage = models.FloatField()
    Total_vol = models.TextField()
    Stock_symbol = models.ForeignKey(StockCompany, on_delete=models.CASCADE)


class StockDate(models.Model):
    Date = models.DateTimeField()
    Stock_data = models.ForeignKey(StockData, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.Date)
