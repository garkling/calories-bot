from database import Product


def prepare_product_info(prod: Product):
    return (f'`{prod.product}\n'
            f'Протеїни        - {prod.proteins}\n'
            f'Вуглеводи       - {prod.carbs}\n'
            f'Жири            - {prod.fats}\n'
            f'Калорій на 100г - {prod.cal_per_100}`'
            )


def show_dishes_list(dishes, date):
    dishes_info_list = []

    for order, info in enumerate(dishes):
        dishes_info_list.append(
            f'`{order + 1}. {info["name"]}\n'
            f'Калорій на 100г - {info["per_100"]}\n'
            f'Вага - {info["weight"]}г\n'
            f'____________________________'
            f'Білків        - {info["proteins"]}\n'
            f'Вуглеводів    - {info["carbs"]}\n'
            f'Жирів         - {info["fats"]}\n'
            f'К-сть калорій - {info["calories"]}\n\n'
            f'Час           - {info["time"]}`'
        )

    return f'**{date}**\n' + \
           ('`\n--------------------------\n`'.join(dishes_info_list) or '\nЗаписів не знайдено')


def show_user_diary(days, username):
    days_str = f'Привіт, {username}!\n' \
               f'Тут ти можеш подивитись свої записи калорійності\n\n'

    for cal_list in days.values():
        days_str += cal_list.show_list()

    return days_str if days else days_str + 'Записів не знайдено'
