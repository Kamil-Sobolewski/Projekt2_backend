from app import db, Product, Category
from tests.base_test_setup import BaseTestSetup


class ProductModelTestCase(BaseTestSetup):
    @classmethod
    def setUpClass(cls):
        super(ProductModelTestCase, cls).setUpClass()
        cls.new_category = Category(name='Kategoria1')
        cls.new_category2 = Category(name='Kategoria2')
        cls.new_product = Product(name='Produkt1', description='Opis1',
                                  weight=1.99, price=12.99, category=cls.new_category,
                                  seller=cls.acc)
        cls.new_product2 = Product(name='Produkt2', description='Opis2',
                                   weight=20, price=100, category=cls.new_category2,
                                   seller=cls.acc)

    def test_models_exist(self):
        self.assertTrue(self.new_category is not None)
        self.assertTrue(self.new_product is not None)
        self.assertTrue(self.new_product.category is not None)
        self.assertTrue(self.new_product.seller is not None)

    def test_model_data_is_correct(self):
        self.assertTrue(self.new_category.name == 'Kategoria1')
        self.assertTrue(self.new_product.name == 'Produkt1')
        self.assertTrue(self.new_product.seller.email == 'qwerty@gmail.com')
        self.assertTrue(self.new_product2.weight == 20)
        self.assertTrue(self.new_product2.price == 100)
        self.assertTrue(self.new_product2.category.name == 'Kategoria2')
