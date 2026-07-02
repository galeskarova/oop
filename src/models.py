from typing import Dict, List, Union


class Product:
    """Класс для представления товара."""

    name: str
    description: str
    __price: float  # приватный атрибут
    quantity: int

    def __init__(
        self, name: str, description: str, price: float, quantity: int
    ) -> None:
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    @property
    def price(self) -> float:
        """Геттер для приватного атрибута цены."""
        return self.__price

    @price.setter
    def price(self, new_price: float) -> None:
        """Сеттер для цены с проверкой на положительное значение."""
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        else:
            # Дополнительное задание: если цена понижается, запросить подтверждение
            if new_price < self.__price:
                answer = input(
                    f"Вы действительно хотите понизить цену с {self.__price} до {new_price}? (y/n): "
                )
                if answer.lower() == "y":
                    self.__price = new_price
                # Если ответ не 'y', цена не меняется
            else:
                self.__price = new_price

    @classmethod
    def new_product(
        cls,
        product_data: Dict[str, Union[str, float, int]],
        existing_products: List["Product"] = None,
    ) -> "Product":
        """
        Класс-метод для создания нового продукта из словаря.
        Если передан список существующих продуктов, то ищет товар с таким же именем:
        - увеличивает количество,- выбирает максимальную цену.
        """
        name = product_data["name"]
        description = product_data.get("description", "")
        price = float(product_data["price"])
        quantity = int(product_data["quantity"])

        # Дополнительная проверка дубликатов
        if existing_products:
            for product in existing_products:
                if product.name == name:
                    # Увеличиваем количество
                    product.quantity += quantity
                    # Устанавливаем максимальную цену
                    if price > product.price:
                        product.price = price  # используем сеттер
                    return product

        # Если дубликат не найден, создаём новый объект
        return cls(name, description, price, quantity)


class Category:
    """Класс для представления категории товаров."""

    name: str
    description: str
    __products: List[Product]  # приватный атрибут

    category_count: int = 0
    product_count: int = 0

    def __init__(self, name: str, description: str, products: List[Product]) -> None:
        self.name = name
        self.description = description
        self.__products = products

        Category.category_count += 1
        Category.product_count += len(products)

    def add_product(self, product: Product) -> None:
        """Добавляет продукт в категорию и увеличивает счётчик товаров."""
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        """Геттер, возвращающий строковое представление списка товаров."""
        result = ""
        for product in self.__products:
            result += f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт.\n"
        return result
