import unittest
import json
import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import app

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_get_cards(self):
        """Test the GET /api/cards endpoint"""
        response = self.app.get('/api/cards')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_post_card_valid(self):
        """Test the POST /api/post endpoint with valid data"""
        test_card = {
            'title': '测试',
            'pinyin': 'cè shì',
            'meaning': 'test',
            'con': 'This is a test connection'
        }
        response = self.app.post('/api/post',
                               data=json.dumps(test_card),
                               content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')

    def test_post_card_invalid(self):
        """Test the POST /api/post endpoint with invalid data"""
        # Missing required field
        test_card = {
            'title': '测试',
            'pinyin': 'cè shì',
            'meaning': 'test'
            # Missing 'con' field
        }
        response = self.app.post('/api/post',
                               data=json.dumps(test_card),
                               content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_result_chinese_character(self):
        """Test the POST /api/result endpoint with Chinese character"""
        test_input = {'user_input': '水'}
        response = self.app.post('/api/result',
                               data=json.dumps(test_input),
                               content_type='application/json')
        # Accept both 200 (success) and 500 (fallback) as valid responses
        # since external API might be unavailable
        self.assertIn(response.status_code, [200, 500])
        data = json.loads(response.data)
        if response.status_code == 200:
            self.assertIn('result', data)
            self.assertIn('cards', data)
        else:
            self.assertIn('error', data)
            self.assertIn('cards', data)

    def test_result_non_chinese(self):
        """Test the POST /api/result endpoint with non-Chinese input"""
        test_input = {'user_input': 'hello'}
        response = self.app.post('/api/result',
                               data=json.dumps(test_input),
                               content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('result', data)
        self.assertIn('cards', data)

    def test_result_empty_input(self):
        """Test the POST /api/result endpoint with empty input"""
        test_input = {'user_input': ''}
        response = self.app.post('/api/result',
                               data=json.dumps(test_input),
                               content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_result_no_input(self):
        """Test the POST /api/result endpoint with no input"""
        response = self.app.post('/api/result',
                               data=json.dumps({}),
                               content_type='application/json')
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
