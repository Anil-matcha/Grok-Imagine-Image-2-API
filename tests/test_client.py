import unittest
from unittest.mock import Mock

from grok_imagine_image_2_api import GrokImagineImage2API


def response_with(payload):
    response = Mock()
    response.json.return_value = payload
    return response


class GrokImagineImage2APITest(unittest.TestCase):
    def test_text_to_image_posts_to_model_endpoint(self):
        session = Mock()
        session.post.return_value = response_with({"request_id": "req_123", "status": "processing"})
        api = GrokImagineImage2API(api_key="test-key", session=session)

        result = api.text_to_image("A geometric sunset", aspect_ratio="16:9")

        self.assertEqual(result["request_id"], "req_123")
        session.post.assert_called_once_with(
            "https://api.muapi.ai/api/v1/grok-imagine-image-2",
            json={"prompt": "A geometric sunset", "aspect_ratio": "16:9"},
            headers={"x-api-key": "test-key", "Content-Type": "application/json"},
            timeout=120,
        )

    def test_edit_image_rejects_more_than_five_references(self):
        api = GrokImagineImage2API(api_key="test-key", session=Mock())

        with self.assertRaises(ValueError):
            api.edit_image("Combine these references", ["https://example.com/a.png"] * 6)

    def test_wait_for_completion_polls_until_done(self):
        session = Mock()
        session.get.side_effect = [
            response_with({"request_id": "req_123", "status": "processing"}),
            response_with(
                {
                    "request_id": "req_123",
                    "status": "completed",
                    "output": {"image": "https://example.com/out.png"},
                }
            ),
        ]
        api = GrokImagineImage2API(api_key="test-key", session=session)

        result = api.wait_for_completion("req_123", poll_interval=0, timeout=1)

        self.assertEqual(result["status"], "completed")
        self.assertEqual(session.get.call_count, 2)


if __name__ == "__main__":
    unittest.main()
