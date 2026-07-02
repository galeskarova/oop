import pytest

from src.models import Category, Product


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


# ---------- Тесты Product ----------
class TestProduct:
    """Тесты для класса Product."""

    def test_product_initialization(self):
        """Проверка корректности инициализации объекта Product."""
        p = Product("Тест", "Тестовое описание", 50.5, 2)
        assert p.name == "Тест"
        assert p.description == "Тестовое описание"
        assert p.price == 50.5  # геттер
        assert p.quantity == 2

    def test_product_attributes_types(self):
        """Проверка типов атрибутов."""
        p = Product("Имя", "Описание", 99.99, 10)
        assert isinstance(p.name, str)
        assert isinstance(p.description, str)
        assert isinstance(p.price, float)  # геттер возвращает float
        assert isinstance(p.quantity, int)

    def test_price_setter_positive(self):
        """Проверка установки корректной цены."""
        p = Product("Товар", "Описание", 100.0, 5)
        p.price = 150.0
        assert p.price == 150.0

    def test_price_setter_zero_or_negative(self, capsys):
        """Проверка, что цена 0 или отрицательная не устанавливается."""
        p = Product("Товар", "Описание", 100.0, 5)
        p.price = 0
        captured = capsys.readouterr()
        assert "Цена не должна быть нулевая или отрицательная" in captured.out
        assert p.price == 100.0  # цена не изменилась

        p.price = -10
        captured = capsys.readouterr()
        assert "Цена не должна быть нулевая или отрицательная" in captured.out
        assert p.price == 100.0

    def test_new_product_from_dict(self):
        """Тест класс-метода new_product без списка существующих."""
        data = {
            "name": "Новый товар",
            "description": "Описание",
            "price": 300,
            "quantity": 3,
        }
        p = Product.new_product(data)
        assert isinstance(p, Product)
        assert p.name == "Новый товар"
        assert p.price == 300.0
        assert p.quantity == 3

    def test_new_product_duplicate(self, sample_products):
        """Тест объединения товаров с одинаковым именем."""
        existing = sample_products  # Товар 1 уже есть
        data = {
            "name": "Товар 1",
            "description": "Новое описание",
            "price": 150.0,
            "quantity": 5,
        }
        result = Product.new_product(data, existing)
        # Проверяем, что вернулся существующий объект
        assert result is sample_products[0]
        assert result.quantity == 10  # 5 + 5
        assert result.price == 150.0  # выбрана максимальная (150 > 100)
        # Проверяем, что цена не понизилась, если новая меньше
        data_low = {
            "name": "Товар 1",
            "description": "...",
            "price": 80.0,
            "quantity": 2,
        }
        Product.new_product(data_low, existing)
        assert result.price == 150.0  # цена не изменилась


# ---------- Тесты Category ----------
class TestCategory:
    """Тесты для класса Category."""

    def test_category_initialization(self, sample_products):
        """Проверка инициализации категории с приватным списком."""
        cat = Category("Категория 1", "Описание категории", sample_products)
        assert cat.name == "Категория 1"
        assert cat.description == "Описание категории"
        # Доступ к приватному списку для проверки через name mangling
        assert len(cat._Category__products) == 2
        assert cat._Category__products == sample_products

    def test_category_count_increment(self, sample_products):
        """Проверка увеличения счётчика категорий."""
        assert Category.category_count == 0
        Category("Кат1", "Описание", sample_products)
        assert Category.category_count == 1
        Category("Кат2", "Описание", [sample_products[0]])
        assert Category.category_count == 2

    def test_product_count_increment(self, sample_products):
        """Проверка увеличения счётчика товаров при создании категорий и добавлении."""
        assert Category.product_count == 0
        Category("Кат1", "Описание", sample_products)
        assert Category.product_count == 2
        Category("Кат2", "Описание", [Product("Товар 3", "Описание 3", 50.0, 3)])
        assert Category.product_count == 3

    def test_category_count_accessible_from_instance(self, sample_products):
        """Атрибут класса доступен через экземпляр."""
        cat = Category("Кат", "Описание", sample_products)
        assert cat.category_count == Category.category_count

    def test_product_count_accessible_from_instance(self, sample_products):
        """Атрибут класса доступен через экземпляр."""
        cat = Category("Кат", "Описание", sample_products)
        assert cat.product_count == Category.product_count

    def test_add_product(self, sample_products):
        """Тест метода add_product и увеличения счётчика."""
        cat = Category("Кат", "Описание", sample_products)
        initial_product_count = Category.product_count
        new_product = Product("Новый", "Описание", 999.99, 1)
        cat.add_product(new_product)
        # Проверяем, что продукт добавился в приватный список
        assert new_product in cat._Category__products
        # Счётчик товаров увеличился на 1
        assert Category.product_count == initial_product_count + 1

    def test_products_getter(self, sample_products):
        """Геттер products возвращает строку в правильном формате."""
        cat = Category("Кат", "Описание", sample_products)
        result = cat.products
        # Проверяем, что строка содержит названия и цены
        assert "Товар 1, 100.0 руб. Остаток: 5 шт." in result
        assert "Товар 2, 200.0 руб. Остаток: 10 шт." in result
        # Проверяем, что заканчивается переносом строки
        assert result.endswith("\n")
