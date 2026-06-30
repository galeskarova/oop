import pytest
from src.models import Product, Category


@pytest.fixture(autouse=True)
def reset_counters():
    """Сбрасываем счётчики категорий и продуктов перед каждым тестом."""
    Category.category_count = 0
    Category.product_count = 0


@pytest.fixture
def sample_products():
    """Фикстура, возвращающая список из двух тестовых продуктов."""
    return [
        Product("Товар 1", "Описание 1", 100.0, 5),
        Product("Товар 2", "Описание 2", 200.0, 10),
    ]


class TestProduct:
    """Тесты для класса Product."""

    def test_product_initialization(self):
        """Проверка корректности инициализации объекта Product."""
        p = Product("Тест", "Тестовое описание", 50.5, 2)
        assert p.name == "Тест"
        assert p.description == "Тестовое описание"
        assert p.price == 50.5
        assert p.quantity == 2

    def test_product_attributes_types(self):
        """Проверка типов атрибутов."""
        p = Product("Имя", "Описание", 99.99, 10)
        assert isinstance(p.name, str)
        assert isinstance(p.description, str)
        assert isinstance(p.price, float)
        assert isinstance(p.quantity, int)


class TestCategory:
    """Тесты для класса Category."""

    def test_category_initialization(self, sample_products):
        """Проверка корректности инициализации объекта Category."""
        cat = Category("Категория 1", "Описание категории", sample_products)
        assert cat.name == "Категория 1"
        assert cat.description == "Описание категории"
        assert len(cat.products) == 2
        assert cat.products == sample_products

    def test_category_count_increment(self, sample_products):
        """Проверка увеличения счётчика категорий."""
        assert Category.category_count == 0
        Category("Кат1", "Описание", sample_products)  # без присваивания
        assert Category.category_count == 1
        Category("Кат2", "Описание", [sample_products[0]])  # без присваивания
        assert Category.category_count == 2

    def test_product_count_increment(self, sample_products):
        """Проверка увеличения счётчика товаров."""
        assert Category.product_count == 0
        Category("Кат1", "Описание", sample_products)  # увеличит на 2
        assert Category.product_count == 2
        Category("Кат2", "Описание", [Product("Товар 3", "Описание 3", 50.0, 3)])
        assert Category.product_count == 3

    def test_category_count_accessible_from_instance(self, sample_products):
        """Проверка, что атрибут класса доступен через экземпляр."""
        cat = Category("Кат", "Описание", sample_products)
        assert cat.category_count == Category.category_count

    def test_product_count_accessible_from_instance(self, sample_products):
        """Проверка, что атрибут класса доступен через экземпляр."""
        cat = Category("Кат", "Описание", sample_products)
        assert cat.product_count == Category.product_count
