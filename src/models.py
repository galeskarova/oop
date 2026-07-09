class Product:
    """
    Класс товара.
    """

    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.__price = price  # приватный атрибут
        self.quantity = quantity

    @property
    def price(self) -> float:
        return self.__price

    @price.setter
    def price(self, value: float):
        if value <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        else:
            self.__price = value

    @classmethod
    def new_product(cls, data: dict, existing_products: list = None):
        """
        Создаёт продукт из словаря.
        Если existing_products передан и в нём есть продукт с таким же именем,
        то увеличивает количество и выбирает максимальную цену.
        Возвращает объект Product (новый или обновлённый).
        """
        name = data["name"]
        description = data["description"]
        price = data["price"]
        quantity = data["quantity"]

        if existing_products:
            for prod in existing_products:
                if prod.name == name:
                    # Обновляем количество и цену (максимальную)
                    prod.quantity += quantity
                    if price > prod.price:
                        prod.price = price
                    return prod

        # Если не нашли дубликат или existing_products не передан
        return cls(name, description, price, quantity)

    def __str__(self) -> str:
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: "Product") -> float:
        if not isinstance(other, Product):
            raise TypeError("Складывать можно только объекты класса Product")
        return self.price * self.quantity + other.price * other.quantity


class Category:
    """
    Класс категории товаров.
    """

    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: list[Product]):
        self.name = name
        self.description = description
        self.__products = products

        # Увеличиваем общее количество категорий
        Category.category_count += 1
        # Увеличиваем общее количество товаров на количество продуктов в категории
        Category.product_count += len(products)

    @property
    def products(self) -> str:
        """
        Возвращает строковое представление всех товаров в категории,
        каждый на новой строке. В конце добавляется перевод строки,
        если список не пуст.
        """
        if not self.__products:
            return ""
        return "\n".join(str(p) for p in self.__products) + "\n"

    def add_product(self, product: Product):
        """Добавляет товар в категорию и увеличивает общий счётчик товаров."""
        self.__products.append(product)
        Category.product_count += 1

    def __str__(self) -> str:
        total_quantity = sum(p.quantity for p in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def __iter__(self):
        return CategoryIterator(self)


class CategoryIterator:
    """
    Итератор для перебора товаров категории.
    """

    def __init__(self, category: Category):
        self._category = category
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self) -> Product:
        products = self._category._Category__products
        if self._index < len(products):
            product = products[self._index]
            self._index += 1
            return product
        raise StopIteration
