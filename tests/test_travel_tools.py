from src.travel_agent_tools import retrieve_customer_location, get_weather_data_us
from langchain_core.tools import ToolException
import unittest
import warnings
warnings.filterwarnings("ignore", category=ResourceWarning)

""" class TestTravelTools(unittest.TestCase):
    def test_retrieve_customer_location(self):
        self.assertEqual(
            retrieve_customer_location.invoke("New York"),
            {"latitude": 40.7127753, "longitude": -74.0059728}
        )

    def test_retrive_customer_location_invalid(self):
        with self.assertRaises(ToolException):
            retrieve_customer_location.invoke("InvalidLocation")

    def test_get_weather_data_us(self):
        # Test with valid coordinates for New York City
        result = get_weather_data_us.invoke({"latitude": 40.7127753, "longitude": -74.0059728})
        self.assertIsInstance(result, dict)
        self.assertTrue(all(isinstance(k, str) for k in result.keys()))
        self.assertTrue(all(isinstance(v, str) for v in result.values()))

    def test_get_weather_data_us_invalid_coordinates(self):
        # Test with invalid coordinates
        with self.assertRaises(ToolException):
            get_weather_data_us.invoke({"latitude": 999.0, "longitude": 999.0})
    if __name__ == "__main__":
        unittest.main() """