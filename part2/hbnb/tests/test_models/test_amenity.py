import unittest
from app.models.amenity import Amenity

class TestAmenity(unittest.TestCase):
    def test_valid_amenity(self):
        amenity = Amenity("WiFi")
        self.assertEqual(amenity.name, "WiFi")

    def test_invalid_name_empty(self):
        with self.assertRaises(ValueError):
            Amenity("")

    def test_invalid_name_too_long(self):
        with self.assertRaises(ValueError):
            Amenity("A" * 51)

    def test_to_dict(self):
        amenity = Amenity("Pool")
        amenity_dict = amenity.to_dict()
        self.assertIn('id', amenity_dict)
        self.assertEqual(amenity_dict['name'], "Pool")

    def test_update(self):
        amenity = Amenity("Gym")
        amenity.update({"name": "Fitness Center"})
        self.assertEqual(amenity.name, "Fitness Center")

if __name__ == '__main__':
    unittest.main()
