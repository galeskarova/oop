import pytest

from src.models import Category, LawnGrass, Product, Smartphone


@pytest.fixture(autouse=True)
def reset_counters():
    """Сбрасываем счётчики категорий и продуктов перед каждым тестом."""
    Category.category_count = 0
    Category.product_count = 0


@pytest.fixture
def sample_products():
    return [
        Product("Товар 1", "Описание 1", 100.0, 5),
        Product("Товар 2", "Описание 2", 200.0, 10),
    ]


class TestProduct:

    def test_product_initialization(self):
        p = Product("Тест", "Тестовое описание", 50.5, 2)
        assert p.name == "Тест"
        assert p.description == "Тестовое описание"
        assert p.price == 50.5
        assert p.quantity == 2

    def test_product_attributes_types(self):
        p = Product("Имя", "Описание", 99.99, 10)
        assert isinstance(p.name, str)
        assert isinstance(p.description, str)
        assert isinstance(p.price, float)
        assert isinstance(p.quantity, int)

    def test_price_setter_positive(self):
        p = Product("Товар", "Описание", 100.0, 5)
        p.price = 150.0
        assert p.price == 150.0

    def test_price_setter_zero_or_negative(self, capsys):
        p = Product("Товар", "Описание", 100.0, 5)
        p.price = 0
        captured = capsys.readouterr()
        assert "Цена не должна быть нулевая или отрицательная" in captured.out
        assert p.price == 100.0

        p.price = -10
        captured = capsys.readouterr()
        assert "Цена не должна быть нулевая или отрицательная" in captured.out
        assert p.price == 100.0

    def test_new_product_from_dict(self):
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
        existing = sample_products
        data = {
            "name": "Товар 1",
            "description": "Новое описание",
            "price": 150.0,
            "quantity": 5,
        }
        result = Product.new_product(data, existing)
        assert result is sample_products[0]
        assert result.quantity == 10
        assert result.price == 150.0

        data_low = {
            "name": "Товар 1",
            "description": "...",
            "price": 80.0,
            "quantity": 2,
        }
        Product.new_product(data_low, existing)
        assert result.price == 150.0  # цена не изменилась

    # Тесты сложения
    def test_add_same_class(self):
        p1 = Product("A", "", 10.0, 2)  # 20
        p2 = Product("B", "", 15.0, 3)  # 45  -> 65
        assert p1 + p2 == 65.0

    def test_add_same_inherited_class(self):
        s1 = Smartphone("S1", "", 1000.0, 1, 0.9, "M1", 64, "Black")
        s2 = Smartphone("S2", "", 2000.0, 2, 0.95, "M2", 128, "White")
        # 1000*1 + 2000*2 = 5000
        assert s1 + s2 == 5000.0

    def test_add_different_class_raises_typeerror(self):
        p = Product("P", "", 10.0, 1)
        s = Smartphone("S", "", 1000.0, 1, 0.9, "M", 64, "Black")
        with pytest.raises(TypeError, match="Нельзя складывать товары разных классов"):
            p + s

    def test_add_product_and_lawn_grass_raises(self):
        s = Smartphone("S", "", 1000.0, 1, 0.9, "M", 64, "Black")
        g = LawnGrass("G", "", 500.0, 2, "Россия", "7 дней", "Зеленый")
        with pytest.raises(TypeError, match="Нельзя складывать товары разных классов"):
            s + g


class TestSmartphone:

    def test_smartphone_initialization(self):
        s = Smartphone("Samsung", "Desc", 50000.0, 2, 95.5, "S23", 256, "Серый")
        assert s.name == "Samsung"
        assert s.description == "Desc"
        assert s.price == 50000.0
        assert s.quantity == 2
        assert s.efficiency == 95.5
        assert s.model == "S23"
        assert s.memory == 256
        assert s.color == "Серый"

    def test_smartphone_is_product(self):
        s = Smartphone("S", "D", 100.0, 1, 0.8, "M", 16, "Red")
        assert isinstance(s, Product)


class TestLawnGrass:

    def test_lawn_grass_initialization(self):
        g = LawnGrass("Трава", "Элитная", 500.0, 20, "Россия", "7 дней", "Зеленый")
        assert g.name == "Трава"
        assert g.price == 500.0
        assert g.country == "Россия"
        assert g.germination_period == "7 дней"
        assert g.color == "Зеленый"

    def test_lawn_grass_is_product(self):
        g = LawnGrass("G", "D", 100.0, 1, "США", "5 дней", "Темно-зеленый")
        assert isinstance(g, Product)


class TestCategory:

    def test_category_initialization(self, sample_products):
        cat = Category("Кат1", "Описание", sample_products)
        assert cat.name == "Кат1"
        assert len(cat._Category__products) == 2

    def test_category_count_increment(self, sample_products):
        assert Category.category_count == 0
        Category("Кат1", "Описание", sample_products)
        assert Category.category_count == 1

    def test_product_count_increment(self, sample_products):
        assert Category.product_count == 0
        Category("Кат1", "Описание", sample_products)
        assert Category.product_count == 2

    def test_add_product(self, sample_products):
        cat = Category("Кат", "Описание", sample_products)
        new_p = Product("Новый", "", 100.0, 1)
        cat.add_product(new_p)
        assert new_p in cat._Category__products
        assert Category.product_count == 3

    def test_add_product_invalid_type_raises(self):
        cat = Category("Кат", "Описание", [])
        with pytest.raises(
            TypeError, match="В категорию можно добавлять только продукты"
        ):
            cat.add_product("не продукт")

    def test_add_product_smartphone_works(self):
        cat = Category("Кат", "Описание", [])
        s = Smartphone("S", "D", 500.0, 1, 0.9, "M", 64, "Black")
        cat.add_product(s)
        assert s in cat._Category__products

    def test_products_getter_format(self, sample_products):
        cat = Category("Кат", "Описание", sample_products)
        result = cat.products
        assert "Товар 1, 100.0 руб. Остаток: 5 шт." in result
        assert "Товар 2, 200.0 руб. Остаток: 10 шт." in result
        assert result.endswith("\n")
