import asyncio
import aiohttp
from .models import StockCompany, StockData, StockDate
from django.utils import timezone


async def get(
        session: aiohttp.ClientSession,
        stock_symbol: str,
        company_name: str,
        **kwargs
) -> dict:
    url = f'https://realstonks.p.rapidapi.com/{stock_symbol}'
    headers = {
        'x-rapidapi-host': "realstonks.p.rapidapi.com",
        'x-rapidapi-key': "5cf2d47ba9msh43646e2b2b9757bp12f0efjsn0e28881478e2"
    }
    resp = await session.request('GET', url=url, headers=headers, **kwargs)
    data = await resp.json()
    data['stock_symbol'] = stock_symbol
    data['company_name'] = company_name
    return data


async def main(stock_symbols, **kwargs):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for company_name, stock_symbol in stock_symbols.items():
            tasks.append(get(session=session, stock_symbol=stock_symbol, company_name=company_name, **kwargs))
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return results


def update_stock_db():
    singleton_company_reader = StockCompanyReader()
    singleton_company_reader.read_database()
    results = asyncio.run(main(singleton_company_reader.data))
    save_to_db(results)


def save_to_db(results):
    for result in results:
        company_name = result['company_name']
        del result['company_name']
        stock_symbol = result['stock_symbol']
        del result['stock_symbol']
        new_comp, created = StockCompany.objects.get_or_create(Name=company_name, Symbol=stock_symbol)
        new_data = StockData.objects.create(Price=result['price'], Change_point=result['change_point'],
                                            Change_percentage=result['change_percentage'],
                                            Total_vol=result['total_vol'],
                                            Stock_symbol=new_comp)
        new_date = StockDate.objects.create(Date=timezone.now(), Stock_data=new_data)


class StockCompanyReader:
    _instance = None
    _initialized = False
    _data = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def read_database(self):
        if not self._initialized:
            stock_query_set = StockCompany.objects.values('Name', 'Symbol')
            for query in stock_query_set:
                self._data[query['Name']] = query['Symbol']
            self._initialized = True

    @property
    def data(self):
        return self._data
