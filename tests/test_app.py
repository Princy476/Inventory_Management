import unittest
from app.database import get_items, add_item, delete_item

class TestInventoryApp(unittest.TestCase):
    def test_add_item(self):
        initial_count = len(get_items())
        add_item('Test Item', 10, 5)
        self.assertEqual(len(get_items()), initial_count + 1)
    
    def test_delete_item(self):
        add_item('Delete Item', 10, 5)
        initial_count = len(get_items())
        delete_item(1)  # Assuming ID 1 exists
        self.assertEqual(len(get_items()), initial_count - 1)

if __name__ == '__main__':
    unittest.main()
