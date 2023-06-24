import asyncio
import aiohttp
from .models import StockCom, StockData


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
    print(f"Response status: {resp.status}")
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
    stock_symbols = {'Apple': 'AAPL', 'IBM': 'IBM', 'NVIDIA': 'NVDA', 'AMD': 'AMD', 'Intel': 'INTC'}
    results = asyncio.run(main(stock_symbols))
    save_to_db(results)


def save_to_db(results):
    for result in results:
        company_name = result['company_name']
        del result['company_name']
        stock_symbol = result['stock_symbol']
        del result['stock_symbol']
        new_comp, created = StockCom.objects.get_or_create(Name=company_name, Symbol=stock_symbol)
        new_data = StockData.objects.create(Price=result['price'], Change_point=result['change_point'],
                                            Change_percentage=result['change_percentage'], Total_vol=result['total_vol'],
                                            Stock_symbol=new_comp)
