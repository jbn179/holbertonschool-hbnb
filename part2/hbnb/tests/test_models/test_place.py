import unittest
from app.models.place import Place
from app.models.user import User

class TestPlace(unittest.TestCase):
    def setUp(self):
        self.owner = User("John", "Doe", "john.doe@example.com")

    def test_valid_place(self):
        place = Place("Test Place", "A test description", 100.0, 40.7128, -74.0060, self.owner)
        self.assertEqual(place.title, "Test Place")
        self.assertEqual(place.description, "A test description")
        self.assertEqual(place.price, 100.0)
        self.assertEqual(place.latitude, 40.7128)
        self.assertEqual(place.longitude, -74.0060)
        self.assertEqual(place.owner, self.owner)

    def test_invalid_title(self):
        with self.assertRaises(ValueError):
            place = Place("", "A test description", 100.0, 40.7128, -74.0060, self.owner)
            place.validate()
        with self.assertRaises(ValueError):
            place = Place("A" * 101, "A test description", 100.0, 40.7128, -74.0060, self.owner)
            place.validate()

    def test_invalid_price(self):
        with self.assertRaises(ValueError):
            Place("Test Place", "A test description", -100.0, 40.7128, -74.0060, self.owner)
        with self.assertRaises(ValueError):
            Place("Test Place", "A test description", "not a number", 40.7128, -74.0060, self.owner)

    def test_invalid_latitude(self):
        with self.assertRaises(ValueError):
            Place("Test Place", "A test description", 100.0, -91, -74.0060, self.owner)
        with self.assertRaises(ValueError):
            Place("Test Place", "A test description", 100.0, 91, -74.0060, self.owner)

    def test_invalid_longitude(self):
        with self.assertRaises(ValueError):
            Place("Test Place", "A test description", 100.0, 40.7128, -181, self.owner)
        with self.assertRaises(ValueError):
            Place("Test Place", "A test description", 100.0, 40.7128, 181, self.owner)

    def test_to_dict(self):
        place = Place("Test Place", "A test description", 100.0, 40.7128, -74.0060, self.owner)
        place_dict = place.to_dict()
        self.assertIn('id', place_dict)
        self.assertEqual(place_dict['title'], "Test Place")
        self.assertEqual(place_dict['description'], "A test description")
        self.assertEqual(place_dict['price'], 100.0)
        self.assertEqual(place_dict['latitude'], 40.7128)
        self.assertEqual(place_dict['longitude'], -74.0060)
        self.assertEqual(place_dict['owner_id'], self.owner.id)

if __name__ == '__main__':
    unittest.main()
