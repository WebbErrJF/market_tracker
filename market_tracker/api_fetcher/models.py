from django.db import models


class StockCom(models.Model):
    Name = models.CharField(max_length=100)
    Symbol = models.CharField(max_length=100)

    def __str__(self):
        return self.Name


class StockData(models.Model):
    Price = models.FloatField()
    Change_point = models.FloatField()
    Change_percentage = models.FloatField()
    Total_vol = models.TextField()
    Stock_symbol = models.ForeignKey(StockCom, on_delete=models.CASCADE)
