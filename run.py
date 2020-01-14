from flask_migrate import Migrate

from app import create_app, db, Account, Role, Product, Category


app = create_app('development')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Account=Account, Role=Role, Product=Product, Category=Category)


@app.cli.command()
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@app.cli.command()
def populate():
    Role.insert_roles()
    user = Account(password='123456', email='qwerty@gmail.com', confirmed=True)
    user2 = Account(password='123456', email='asdfg@gmail.com', confirmed=True)
    new_category = Category(name='Kategoria1')
    new_category2 = Category(name='Kategoria2')
    new_product = Product(name='Produkt1', description='Opis1',
                          weight=1.99, price=12.99, category=new_category, seller=user)
    new_product2 = Product(name='Produkt2', description='Opis2',
                           weight=20, price=100, category=new_category2, seller=user2)
    db.session.add_all([user, user2, new_product, new_product2, new_category, new_category2])
    db.session.commit()
