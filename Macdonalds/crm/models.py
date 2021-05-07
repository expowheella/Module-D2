# пример с рестораном McDonald's
from django.db import models

# импортируем модуль, позволяющий получить текущее время
from datetime import datetime

# Модель выступает в качестве посредника между базой данных и логикой приложения за счёт ORM.
# создаем модель продукта: одна модель - одна таблица в базе данных
# Переделываем SQL-таблицу в класс Django Python:
"""
CREATE TABLE PRODUCTS (
    product_id INT AUTO_INCREMENT NOT NULL,
    name CHAR(255) NOT NULL,
    price FLOAT NOT NULL,

    PRIMARY KEY (product_id))
"""


# реализуем модель Product
class Product(models.Model):
    name = models.CharField(max_length=255)  # установили максимальную длину строки с названием равное 255
    price = models.FloatField(default=0.0)  # установили значение по умолчанию для цены равное 0.0
    composition = models.TextField(default="Состав не указан")  # установили значение по умолчанию для состава продукта


# создаем модель сотрудника
"""
CREATE TABLE STAFF (
    staff_id INT AUTO_INCREMENT NOT NULL,
    full_name CHAR(255) NOT NULL,    
    position CHAR(255) NOT NULL,
    labor_contract INT NOT NULL,

    PRIMARY KEY (staff_id));
"""


class Staff(models.Model):
    director = 'DI'
    admin = 'AD'
    cook = 'CO'
    cashier = 'CA'
    cleaner = 'CL'

    POSITIONS = [
        (director, "Директор"),
        (admin, "Администратор"),
        (cook, "Повар"),
        (cashier, "Кассир"),
        (cleaner, "Кассир")
    ]
    full_name = models.CharField(max_length=255)  # строка длиной 255 символов -> ФИО сотрудника
    position = models.CharField(max_length=2,
                                choices=POSITIONS,
                                default=cashier)  # строка длиной 2 символа -> должность сотрудника
    labor_contract = models.IntegerField()  # число -> номер договора

    # запишем метод, возращающий фамилию сотрудника
    def get_last_name(self):
        last_name = self.full_name.split()[0]
        return last_name


# напишем метод, который при завершении заказа,
# устанавливал бы текущее время в поле time_out.
def finish_order(self):
    # 1) в поле time.out запишем текущее время через функцию now()
    self.time_out = datetime.now()
    # 2) установим флаг "Завершен" в логическую переменную complete
    self.complete = True
    # 3) сохраним объект в базу данных
    self.save()


#   создадим связь "один ко многим"
"""
CREATE TABLE ORDERS (
    order_id INT AUTO_INCREMENT NOT NULL,
    time_in DATETIME NOT NULL,
    time_out DATETIME,
    cost FLOAT NOT NULL,
    take_away INT NOT NULL,
    staff INT NOT NULL,

    PRIMARY KEY (order_id),
    FOREIGN KEY (staff) REFERENCES STAFF (staff_id));
"""


class Order(models.Model):  # создали класс Order унаследованный от базовой модели models.Model
    # дата и время оформления заказа
    time_in = models.DateTimeField(auto_now_add=True)  # автоматически устанавливает в это поле дату создания объекта
    # дата и время выдачи заказа
    time_out = models.DateTimeField(null=True)  # аргумент null = True указывает, что здесь может быть пустая ячейка
    # общая стоимость заказа
    cost = models.FloatField(default=0.0)
    # заказ "на месте" или "с собой"
    take_away = models.BooleanField(default=False)
    # реализация связи "один ко многим" staff = models.ForeignKey(Staff)
    # каскадное удаление "on_delete=models.CASCADE" удалит все заказы,
    # связанные с данным сотрудником в случае его увольнения
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)

    # зададим явно промежуточную модель ProductOrder, которая связывает модели Order и Product
    products = models.ManyToManyField(Product, through='ProductOrder')

    # запишем метод, возвращающий время выполнения заказа в минутах (округл.)
    # если заказ ещё не выполнен, возвращающий количество минут с начала выполнения заказа
    def get_duration(self):
        if self.complete:  # если заказ завершен
            minutes = (self.time_out - self.time_in).total_seconds() // 60
            return minutes
        else:  # если заказ ещё не завершен
            minutes = (datetime.now() - self.time_in).total_seconds() // 60
            return minutes


# реализуем промежуточную таблицу для связи Order и Product
class ProductOrder(models.Model):
    # количество продуктов в заказе
    _amount = models.IntegerField(default=1, db_column='amount')  # задали явно название колонки: db_column='amount'
    # связь с таблицей Order с каскадным удалением
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    # связь с таблицей Product с каскадным удалением
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    # объявим свойство getter с помощью декоратора property
    @property
    def amount(self):
        # просто вернем значение поля _amount
        return self._amount

    # объявим свойство setter, чтобы проверить значение поля _amount на условия
    @amount.setter
    def amount(self, value):  # value = _amount
        # проверяем, чтобы _amount не был меньше нуля
        # если _amount больше нуля, то _amount остается равным себе: _amount = _amount
        # если же _amount меньше нуля, то _amount = 0
        self._amount = int(value) if value >= 0 else 0
        # сохраняем объект в базу данных
        self.save()

    # создадим метод, возвращающий стоимость продуктов (product)
    # в зависимости от их количества (amount)
    def product_sum(self):  # def product_sum(product):
        # Сам объект продукта содержится в переменной self в виде поля product. Оно, в свою очередь, само является
        # объектом модели Product, которая содержит поле price. Создаем такую цепочку: self -> product -> price
        product_price = self.product.price

        # возвращаем стоимость продукта, умноженное на количество
        return product_price * self.amount


# # создадим систему авторизации пользователей
# class AbstractBaseUser(models.Model):
#     # пароль пользователя
#     password = models.CharField(('password'), max_length=128)
#
#     # дата и время последней активности в веб-приложении
#     last_login = models.DateTimeField(('last login'), blank=True, null=True)
#
#     is_active = True


# class AbstractUser(AbstractBaseUser, PermissionsMixin):
#     """
#     An abstract base class implementing a fully featured User model with
#     admin-compliant permissions.
#
#     Username and password are required. Other fields are optional.
#     """
#     username_validator = UnicodeUsernameValidator()
#
#     username = models.CharField(_('username'),
#                                 max_length=150,
#                                 unique=True,
#                                 help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
#                                 validators=[username_validator],
#                                 error_messages={'unique': _("A user with that username already exists."), }, )
#
#     # поля, хранящие имя и фамилию пользователей
#     first_name = models.CharField(_('first name'), max_length=150, blank=True)
#     last_name = models.CharField(_('last name'), max_length=150, blank=True)
#
#     # электронная почта пользователей
#     email = models.EmailField(_('email address'), blank=True)
#
#     # данное поле будет определять, может ли пользователь заходить на панель администратора
#     is_staff = models.BooleanField(_('staff status'), default=False,
#                                    help_text=_('Designates whether the user can log into this admin site.'), )
#
#     # данное поле будет определять, может ли пользователь заходить на сайт в целом
#     is_active = models.BooleanField(_('active'), default=True,
#                                     help_text=_('Designates whether this user should be treated as active. '
#                                                 'Unselect this instead of deleting accounts.'), )
#
#     # дата и время регистрации пользователя
#     date_joined = models.DateTimeField(_('date joined'), default=timezone.now)



