from typing import Dict, List, Union


class Product:
    """Базовый класс для всех продуктов."""

    name: str
    description: str
    __price: float
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
            if new_price < self.__price:
                answer = input(
                    f"Вы действительно хотите понизить цену с {self.__price} до {new_price}? (y/n): "
                )
                if answer.lower() == "y":
                    self.__price = new_price
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
        - увеличивает количество,
        - выбирает максимальную цену.
        """
        name = product_data["name"]
        description = product_data.get("description", "")
        price = float(product_data["price"])
        quantity = int(product_data["quantity"])

        if existing_products:
            for product in existing_products:
                if product.name == name:
                    product.quantity += quantity
                    if price > product.price:
                        product.price = price
                    return product

        return cls(name, description, price, quantity)

    def __add__(self, other: "Product") -> float:
        """
        Сложение двух продуктов одного класса.
        Возвращает сумму произведений цены на количество.
        Если типы не совпадают, выбрасывается TypeError.
        """
        if type(self) is not type(other):
            raise TypeError("Нельзя складывать товары разных классов")
        return self.price * self.quantity + other.price * other.quantity


class Smartphone(Product):
    """Класс для смартфонов, наследник Product."""

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        efficiency: float,
        model: str,
        memory: int,
        color: str,
    ) -> None:
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color


class LawnGrass(Product):
    """Класс для газонной травы, наследник Product."""

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        country: str,
        germination_period: str,
        color: str,
    ) -> None:
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color


class Category:
    """Класс для представления категории товаров."""

    name: str
    description: str
    __products: List[Product]

    category_count: int = 0
    product_count: int = 0

    def __init__(self, name: str, description: str, products: List[Product]) -> None:
        self.name = name
        self.description = description
        self.__products = products

        Category.category_count += 1
        Category.product_count += len(products)

    def add_product(self, product: Product) -> None:
        """Добавляет продукт в категорию. Разрешены только экземпляры Product и его наследников."""
        if not isinstance(product, Product):
            raise TypeError(
                "В категорию можно добавлять только продукты (Product или его наследники)"
            )
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        """Геттер, возвращающий строковое представление списка товаров."""
        result = ""
        for product in self.__products:
            result += f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт.\n"
        return result
