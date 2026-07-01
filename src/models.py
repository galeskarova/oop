class Product:
    """Класс для представления товара."""

    name: str
    description: str
    price: float
    quantity: int

    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity


class Category:
    """Класс для представления категории товаров."""

    name: str
    description: str
    products: list  # список объектов Product

    # Атрибуты класса для подсчёта общего количества категорий и товаров
    category_count: int = 0
    product_count: int = 0

    def __init__(self, name: str, description: str, products: list) -> None:
        self.name = name
        self.description = description
        self.products = products

        # Увеличиваем счётчики при создании нового объекта
        Category.category_count += 1
        Category.product_count += len(products)  # учитываем длину списка товаров
