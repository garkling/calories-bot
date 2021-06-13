from datetime import datetime

from database import DBManager, Product
from formatter import prepare_product_info, show_dishes_list, show_user_diary


class UserCaloriesDayList:

    def __init__(self, today: datetime):
        self.dishes = []
        self.total_calories = 0
        self.today = today

    def save_dish(self, product: Product, weight: float):
        proteins, carbs, fats, calories = self.calculate_calories(product, weight)
        dish = dict(name=product.product,
                    per_100=product.cal_per_100,
                    weigth=weight,
                    proteins=proteins,
                    carbs=carbs,
                    fats=fats,
                    calories=calories,
                    time=self.today.time()
                    )

        self.dishes.append(dish)
        self.total_calories += calories

    def remove_dish(self, order_number: int):
        self.dishes.pop(order_number)

    def show_list(self):
        return show_dishes_list(self.dishes, self.today.date())

    @staticmethod
    def calculate_calories(prod: Product, weight):

        total_proteins = prod.proteins * weight
        total_carbs = prod.carbs * weight
        total_fats = prod.fats * weight
        calories = prod.cal_per_100 / 100 * weight

        return total_proteins, total_carbs, total_fats, calories


class UserCaloriesDiary:

    def __init__(self, username, user_id):
        self.user = username
        self.user_id = user_id
        self.days = {}

    def start_day(self):
        today = datetime.today()
        calories_list = UserCaloriesDayList(today)

        self.days[today.date()] = calories_list

    def show_diary(self):
        return show_user_diary(self.days, self.user)


class ProductManager:

    current_products = {}

    def __init__(self):
        self.users = {}
        self.db = DBManager()

    def get_diary(self, user_id) -> UserCaloriesDiary:
        return self.users[user_id]

    async def register_new_user(self, user):
        user_id = user.id
        self.users[user_id] = UserCaloriesDiary(user.username, user_id)

    async def get_product_info(self, product_id: int):
        product_info = self.current_products.get(product_id)
        ready_info = prepare_product_info(product_info)

        return ready_info

    async def get_products_pages(self, request: str):
        product_list = await self.db.get_products_by_request(request.lower())
        page_content = []

        if not product_list:
            return False
        else:
            for prod in product_list:
                prod_id = prod.id
                self.current_products[prod_id] = prod
                page_content.append((prod.product, prod_id))

            return page_content

    def registered(self, user_id):
        return user_id in self.users
