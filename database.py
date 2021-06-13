import peewee as pw

connection = pw.SqliteDatabase('calories')


class Base(pw.Model):
    class Meta:
        database = connection


class Product(Base):
    product = pw.TextField(column_name='product')
    proteins = pw.FloatField(column_name='proteins')
    carbs = pw.FloatField(column_name='carbs')
    fats = pw.FloatField(column_name='fats')
    cal_per_100 = pw.IntegerField(column_name='cal_per_100')

    class Meta:
        table_name = 'Products'


class DBManager:

    def __init__(self):
        connection.connect()

    def __del__(self):
        connection.close()

    @staticmethod
    async def get_products_by_request(request: str):
        select_list = Product.select().where(Product.product.contains(request))

        return select_list

    @staticmethod
    async def add_product(product_data):
        insert = Product.insert(**product_data)
        insert.execute()

    @staticmethod
    async def add_products(product_data_list):
        with connection.atomic():
            insert = Product.insert_many(product_data_list)
            insert.execute()


def create_tables():
    for table in tables_list:
        try:
            if not table.table_exists():
                table.create_table()
        except pw.InternalError as e:
            print(e)


if __name__ == '__main__':
    tables_list = [Product]
    connection.connect()
    create_tables()
