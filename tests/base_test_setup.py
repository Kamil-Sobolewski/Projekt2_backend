import unittest
from app import create_app, db, Role, Account


class BaseTestSetup(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app('testing')
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        db.create_all()
        Role.insert_roles()
        cls.acc = Account(password='qwerty', email='qwerty@gmail.com')
        db.session.add(cls.acc)
        db.session.commit()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()
