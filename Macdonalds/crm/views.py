from models import Product, Staff

"""Способы создания объектов"""
"""<<<<<< Способ 1 >>>>>>>"""
# создадим объект класса Product
cap = Product(name="Капучино 0.3", price=99.0)
# чтобы добавить этот объект в строку базы данных, нужно его сохранить
cap.save()

# создадим объект картошки фри
french_fries_std = Product(name="Картофель фри (станд.)", price=93.0)
french_fries_std.save()

"""<<<<<< Способ 2 >>>>>>>"""
# применение менеджера модели
cap_big = Product.objects.create(name="Капучино 0.4", price=109.0)
# создадим объект картошки фри
french_fries_big = Product.objects.create(name="Картофель фри (бол.)", price=106.0)

"""<<<<<< Создаем сотрудников >>>>>>>"""
cashier1 = Staff.objects.create(full_name="Иванов Иван Иванович",
                                position=Staff.cashier,
                                labor_contract=1754)
cashier2 = Staff.objects.create(full_name="Петров Петр Петрович",
                                position=Staff.cashier,
                                labor_contract=4355)
direct = Staff.objects.create(full_name="Максимов Максим Максимович",
                              position=Staff.director,
                              labor_contract=1254)
