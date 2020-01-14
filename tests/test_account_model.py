import time
from app import db, Account, Permission
from tests.base_test_setup import BaseTestSetup


class AccountModelTestCase(BaseTestSetup):
    def test_password_setter(self):
        self.assertTrue(self.acc.password_hash is not None)

    def test_no_password_getter(self):
        with self.assertRaises(AttributeError):
            self.acc.password

    def test_password_verification(self):
        self.assertTrue(self.acc.verify_password("qwerty"))
        self.assertFalse(self.acc.verify_password("123456"))

    def test_password_salts_are_random(self):
        acc2 = Account(password='qwerty')
        self.assertFalse(self.acc.password_hash == acc2.password_hash)

    def test_valid_confirmation_token(self):
        token = self.acc.generate_secure_token()
        self.assertTrue(self.acc.confirm(token))

    def test_invalid_confirmation_token(self):
        acc2 = Account(password='123456')
        db.session.add(acc2)
        db.session.commit()
        token = self.acc.generate_secure_token()
        self.assertFalse(acc2.confirm(token))

    def test_expired_confirmation_token(self):
        token = self.acc.generate_secure_token(1)
        time.sleep(2)
        self.assertFalse(self.acc.confirm(token))

    def test_user_role(self):
        self.assertTrue(self.acc.can(Permission.FOLLOW))
        self.assertTrue(self.acc.can(Permission.COMMENT))
        self.assertTrue(self.acc.can(Permission.WRITE))
        self.assertFalse(self.acc.can(Permission.MODERATE))
        self.assertFalse(self.acc.can(Permission.ADMIN))
