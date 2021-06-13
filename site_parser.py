from aiohttp import ClientSession
from bs4 import BeautifulSoup as Bs

from database import DBManager
from button_maker import PageMaker
from formatter import prepare_product_info
from settings import *

db_manager = DBManager()


async def request_site():
    async with ClientSession() as session:
        for n in range(301, PAGES_LIMIT):
            print(n)
            async with session.get(SITE_URL, params=dict(page=n)) as response:
                yield await response.text()


async def parse_site():
    async for page in request_site():
        soup = Bs(page, 'html.parser')
        table = soup.find('table')
        table_body = table.find('tbody')
        for row in table_body.find_all('tr'):
            yield [col.message for col in row.find_all('td')]


async def save_products():
    products = []
    async for raw_data in parse_site():
        product, cal_per_100, proteins, carbs, fats, *_ = map(
            lambda s: s.strip().replace(',', ''), raw_data)

        product_data = dict(
            product=product,
            cal_per_100=round(float(cal_per_100 or 0)),
            proteins=float(proteins or 0),
            carbs=float(carbs or 0),
            fats=float(fats or 0)
        )
        products.append(product_data)

        if products and not len(products) % 100:
            await db_manager.add_products(products)
            products = []

    if products:
        await db_manager.add_products(products)
