import unittest
from app.models.user import User

class TestUser(unittest.TestCase):
    def test_valid_user(self):
        user = User("John", "Doe", "john.doe@example.com")
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        self.assertEqual(user.email, "john.doe@example.com")

    def test_invalid_first_name(self):
        with self.assertRaises(ValueError):
            User("", "Doe", "john.doe@example.com")
        with self.assertRaises(ValueError):
            User("A" * 51, "Doe", "john.doe@example.com")

    def test_invalid_last_name(self):
        with self.assertRaises(ValueError):
            User("John", "", "john.doe@example.com")
        with self.assertRaises(ValueError):
            User("John", "A" * 51, "john.doe@example.com")

    def test_invalid_email(self):
        with self.assertRaises(ValueError):
            User("John", "Doe", "")
        with self.assertRaises(ValueError):
            User("John", "Doe", "invalid_email")

    def test_to_dict(self):
        user = User("John", "Doe", "john.doe@example.com")
        user_dict = user.to_dict()
        self.assertIn('id', user_dict)
        self.assertEqual(user_dict['first_name'], "John")
        self.assertEqual(user_dict['last_name'], "Doe")
        self.assertEqual(user_dict['email'], "john.doe@example.com")

if __name__ == '__main__':
    unittest.main()
