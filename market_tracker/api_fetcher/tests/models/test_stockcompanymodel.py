from django.test import TestCase
from api_fetcher.models import StockCompany


class StockCompanyModelTest(TestCase):
    def setUp(self):
        self.test_name = "test_1"
        self.test_stock_company = StockCompany.objects.create(Name=self.test_name,
                                                              Symbol="t_1",
                                                              Default=True)

    def test_if_test_stock_company_is_instance_of_StockCompany(self):
        self.assertTrue(isinstance(self.test_stock_company, StockCompany))

    def test_if_instance_of_StockCompanyModel_returns_name_when_its_called(self):
        stock_company_representation = str(self.test_stock_company)
        self.assertEqual(stock_company_representation, self.test_name)

    def test_if_stock_company_name_max_length_is_100(self):
        expected_max_length = 100
        max_length = self.test_stock_company._meta.get_field('Name').max_length
        self.assertEqual(max_length, expected_max_length)

    def test_if_stock_company_symbol_max_length_is_100(self):
        expected_max_length = 100
        max_length = self.test_stock_company._meta.get_field('Symbol').max_length
        self.assertEqual(max_length, expected_max_length)
