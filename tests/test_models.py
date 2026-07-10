import pytest

from src.models import BaseProduct, Category, LawnGrass, Product, Smartphone


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


def test_base_product_is_abstract():
    with pytest.raises(TypeError):
        BaseProduct()


def test_object_creation_mixin_output(capsys):
    Product("Test", "Desc", 10.0, 1)
    captured = capsys.readouterr()
    assert "Создан объект класса Product" in captured.out
    assert "'Test'" in captured.out


def test_smartphone_creation_mixin_output(capsys):
    Smartphone("S", "D", 1000.0, 2, 0.9, "M", 64, "Black")
    captured = capsys.readouterr()
    assert "Создан объект класса Smartphone" in captured.out


class TestProduct:

    def test_product_initialization(self):
        p = Product("Тест", "Тестовое описание", 50.5, 2)
        assert p.name == "Тест"
        assert p.price == 50.5
        assert p.quantity == 2

    def test_product_zero_quantity_raises_valueerror(self):
        with pytest.raises(
            ValueError, match="Товар с нулевым количеством не может быть добавлен"
        ):
            Product("Брак", "Описание", 100.0, 0)

    def test_get_info(self):
        p = Product("A", "B", 100.0, 1)
        info = p.get_info()
        assert "A" in info and "100.0 руб" in info

    def test_price_setter_zero_or_negative(self, capsys):
        p = Product("Товар", "Описание", 100.0, 5)
        p.price = 0
        captured = capsys.readouterr()
        assert "Цена не должна быть нулевая или отрицательная" in captured.out
        assert p.price == 100.0

    def test_new_product_from_dict(self):
        data = {"name": "Новый", "description": "...", "price": 300, "quantity": 3}
        p = Product.new_product(data)
        assert p.name == "Новый"
        assert p.quantity == 3

    def test_add_same_class(self):
        p1 = Product("A", "", 10.0, 2)
        p2 = Product("B", "", 15.0, 3)
        assert p1 + p2 == 65.0

    def test_add_different_class_raises(self):
        p = Product("P", "", 10.0, 1)
        s = Smartphone("S", "", 1000.0, 1, 0.9, "M", 64, "Black")
        with pytest.raises(TypeError):
            p + s


class TestSmartphone:
    def test_inheritance(self):
        s = Smartphone("S", "D", 100.0, 1, 0.8, "X", 32, "Red")
        assert isinstance(s, Product)
        assert isinstance(s, BaseProduct)

    def test_attributes(self):
        s = Smartphone("S", "D", 100.0, 1, 0.8, "X", 32, "Red")
        assert s.efficiency == 0.8
        assert s.model == "X"
        assert s.memory == 32
        assert s.color == "Red"


class TestLawnGrass:
    def test_inheritance(self):
        g = LawnGrass("G", "D", 50.0, 5, "Россия", "7 дней", "Зелёный")
        assert isinstance(g, Product)
        assert isinstance(g, BaseProduct)

    def test_attributes(self):
        g = LawnGrass("G", "D", 50.0, 5, "Россия", "7 дней", "Зелёный")
        assert g.country == "Россия"
        assert g.germination_period == "7 дней"
        assert g.color == "Зелёный"


class TestCategory:

    def test_len_of_products(self, sample_products):
        cat = Category("Кат", "Описание", sample_products)
        assert len(cat.products) == 2

    def test_products_is_string_like(self, sample_products):
        cat = Category("Кат", "Описание", sample_products)
        representation = cat.products
        assert isinstance(representation, str)
        assert "Товар 1, 100.0 руб. Остаток: 5 шт." in representation

    def test_add_product_updates_len(self, sample_products):
        cat = Category("Кат", "Описание", sample_products)
        new_p = Product("Новый", "", 10.0, 1)
        cat.add_product(new_p)
        assert len(cat.products) == 3

    def test_add_product_raises_on_non_product(self):
        cat = Category("Кат", "Описание", [])
        with pytest.raises(TypeError):
            cat.add_product("строка")

    def test_category_count_increment(self, sample_products):
        assert Category.category_count == 0
        Category("К1", "", sample_products)
        assert Category.category_count == 1


    def test_middle_price_with_products(self, sample_products):
        cat = Category("Кат", "Описание", sample_products)
        assert cat.middle_price() == 150.0

    def test_middle_price_single_product(self):
        p = Product("Один", "", 42.0, 1)
        cat = Category("Кат", "", [p])
        assert cat.middle_price() == 42.0

    def test_middle_price_empty_category(self):
        cat = Category("Пустая", "Без товаров", [])
        assert cat.middle_price() == 0
