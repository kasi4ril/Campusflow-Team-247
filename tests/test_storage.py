import unittest
import os
import json
from campusflow.storage import save_tickets, load_tickets

class TestStorage(unittest.TestCase):
    
    def setUp(self):
        # We will use a fake file path just for testing so we don't overwrite real data
        self.test_file = "data/test_tickets.json"
        dir_name = os.path.dirname(self.test_file)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
        
        # Ensure the file doesn't exist before we start
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def tearDown(self):
        # tearDown runs after every test to clean up the mess
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_missing_file_returns_empty_list(self):
        # Act
        tickets = load_tickets(self.test_file)
        # Assert
        self.assertEqual(tickets, [])

    def test_save_and_load_preserves_data(self):
        # Arrange
        mock_tickets = [{"id": "T001", "title": "Broken mouse"}]
        
        # Act
        save_tickets(mock_tickets, self.test_file)
        loaded_tickets = load_tickets(self.test_file)
        
        # Assert
        self.assertEqual(loaded_tickets[0]["id"], "T001")

    def test_corrupted_json_raises_error(self):
        # Arrange: create a file with garbage text that is not valid JSON
        with open(self.test_file, "w") as f:
            f.write("this is not json { [ bad data")
            
        # Act & Assert
        with self.assertRaises(ValueError):
            load_tickets(self.test_file)

if __name__ == '__main__':
    unittest.main()