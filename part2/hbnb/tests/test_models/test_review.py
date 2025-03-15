import unittest
from app.models.review import Review
from app.models.user import User
from app.models.place import Place

class TestReview(unittest.TestCase):
    def setUp(self):
        self.user = User("John", "Doe", "john.doe@example.com")
        self.place = Place("Test Place", "A test description", 100.0, 40.7128, -74.0060, self.user)

    def test_valid_review(self):
        review = Review("Great place!", 5, self.user, self.place)
        self.assertEqual(review.text, "Great place!")
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.user, self.user)
        self.assertEqual(review.place, self.place)

    def test_invalid_text(self):
        with self.assertRaises(ValueError):
            Review("", 5, self.user, self.place)
        with self.assertRaises(ValueError):
            Review("A" * 1001, 5, self.user, self.place)

    def test_invalid_rating(self):
        with self.assertRaises(ValueError):
            Review("Great place!", 0, self.user, self.place)
        with self.assertRaises(ValueError):
            Review("Great place!", 6, self.user, self.place)
        with self.assertRaises(ValueError):
            Review("Great place!", "not a number", self.user, self.place)

    def test_invalid_user(self):
        with self.assertRaises(ValueError):
            Review("Great place!", 5, "not a user", self.place)

    def test_invalid_place(self):
        with self.assertRaises(ValueError):
            Review("Great place!", 5, self.user, "not a place")

    def test_to_dict(self):
        review = Review("Great place!", 5, self.user, self.place)
        review_dict = review.to_dict()
        self.assertIn('id', review_dict)
        self.assertEqual(review_dict['text'], "Great place!")
        self.assertEqual(review_dict['rating'], 5)
        self.assertEqual(review_dict['user_id'], self.user.id)
        self.assertEqual(review_dict['place_id'], self.place.id)

if __name__ == '__main__':
    unittest.main()
