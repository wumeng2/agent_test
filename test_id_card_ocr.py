import unittest
import requests
import json
import os
from unittest.mock import patch, MagicMock
from io import BytesIO
from base64 import b64encode

# Import the main script's logic
# For this test, we'll create a simple function to test


def create_id_card_request_payload(image_path: str) -> dict:
    """Create the request payload for ID card OCR"""
    return {
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": f"file://{os.path.abspath(image_path)}"},
                    },
                    {
                        "type": "text",
                        "text": """请按下列JSON格式输出图中信息:
{
"身份证号": "",
"姓名": "",
"性别": "",
"出生日期": "",
"民族":"",
"地址": "",
"有效期限": "",
"签发机关": ""
}""",
                    },
                ],
            }
        ]
    }


def call_id_card_api(url: str, image_path: str, timeout: int = 60) -> dict:
    """Call the ID card OCR API"""
    data = create_id_card_request_payload(image_path)
    response = requests.post(url, json=data, timeout=timeout)
    response.raise_for_status()
    return response.json()


class TestIDCardOCR(unittest.TestCase):
    """Unit tests for ID Card OCR"""

    API_URL = "http://192.168.6.198:8080/v1/chat/completions"

    def test_create_payload(self):
        """Test payload creation"""
        test_path = "/tmp/test_image.jpg"
        payload = create_id_card_request_payload(test_path)

        self.assertIn("messages", payload)
        self.assertEqual(len(payload["messages"]), 1)
        self.assertEqual(payload["messages"][0]["role"], "user")
        self.assertEqual(len(payload["messages"][0]["content"]), 2)
        self.assertEqual(payload["messages"][0]["content"][0]["type"], "image_url")
        self.assertEqual(payload["messages"][0]["content"][1]["type"], "text")

    def test_payload_contains_required_fields(self):
        """Test that payload contains all required fields in prompt"""
        test_path = "/tmp/test_image.jpg"
        payload = create_id_card_request_payload(test_path)
        text_content = payload["messages"][0]["content"][1]["text"]

        required_fields = [
            "身份证号", "姓名", "性别", "出生日期",
            "民族", "地址", "有效期限", "签发机关"
        ]

        for field in required_fields:
            self.assertIn(field, text_content)

    @patch('requests.post')
    def test_api_call_success(self, mock_post):
        """Test successful API call"""
        # Mock the response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [
                {
                    "message": {
                        "content": '{"身份证号": "110101199001011234", "姓名": "张三"}'
                    }
                }
            ]
        }
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response

        # Test the call
        result = call_id_card_api(self.API_URL, "/tmp/test.jpg")

        # Verify
        mock_post.assert_called_once()
        self.assertEqual(result["choices"][0]["message"]["content"],
                         '{"身份证号": "110101199001011234", "姓名": "张三"}')

    @patch('requests.post')
    def test_api_call_failure(self, mock_post):
        """Test API call failure handling"""
        mock_post.side_effect = requests.exceptions.ConnectionError("Connection refused")

        with self.assertRaises(requests.exceptions.ConnectionError):
            call_id_card_api(self.API_URL, "/tmp/test.jpg")

    def test_image_url_format(self):
        """Test that image URL is formatted correctly"""
        test_path = "/tmp/test_image.jpg"
        payload = create_id_card_request_payload(test_path)
        image_url = payload["messages"][0]["content"][0]["image_url"]["url"]

        self.assertTrue(image_url.startswith("file://"))
        self.assertTrue(image_url.endswith("test_image.jpg"))


# Integration test helper (only run if you have a real image)
def create_test_image():
    """Create a simple test image using PIL (if available)"""
    try:
        from PIL import Image, ImageDraw, ImageFont

        # Create a blank white image
        img = Image.new('RGB', (600, 400), color='white')
        draw = ImageDraw.Draw(img)

        # Draw some text (simulating an ID card)
        draw.text((50, 50), "姓名: 张三", fill='black')
        draw.text((50, 100), "身份证号: 110101199001011234", fill='black')
        draw.text((50, 150), "性别: 男", fill='black')
        draw.text((50, 200), "地址: 北京市东城区测试路123号", fill='black')

        # Save the test image
        test_image_path = "/home/py/test_claude/test_id_card.jpg"
        img.save(test_image_path)
        print(f"Test image created at: {test_image_path}")
        return test_image_path

    except ImportError:
        print("PIL not available. Install with: pip install Pillow")
        return None


def run_real_api_test():
    """Run a real API test (requires actual server running)"""
    print("\n=== Real API Test ===")

    # Create or use a test image
    test_image = create_test_image()
    if not test_image:
        print("Skipping: No test image available")
        return

    try:
        result = call_id_card_api(
            "http://192.168.6.198:8080/v1/chat/completions",
            test_image
        )
        print("API Response:")
        print(json.dumps(result, ensure_ascii=False, indent=2))

    except Exception as e:
        print(f"API test failed: {e}")


if __name__ == '__main__':
    # Run unit tests
    print("=== Running Unit Tests ===")
    unittest.main(argv=[''], exit=False, verbosity=2)

    # Optionally run real API test
    # Uncomment the line below to test with real API
    # run_real_api_test()
