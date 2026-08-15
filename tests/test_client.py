import unittest
from unittest.mock import Mock

from grok_imagine_image_2_api import GrokImagineImage2API


def response_with(payload):
    response = Mock()
    response.json.return_value = payload
    return response


class GrokImagineImage2APITest(unittest.TestCase):
    def test_text_to_image_posts_to_generate_endpoint(self):
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

    def test_text_to_image_rejects_unsupported_aspect_ratio(self):
        api = GrokImagineImage2API(api_key="test-key", session=Mock())

        with self.assertRaises(ValueError):
            api.text_to_image("A geometric sunset", aspect_ratio="4:3")

    def test_edit_image_posts_to_edit_endpoint_with_request_id(self):
        session = Mock()
        session.post.return_value = response_with({"request_id": "req_456", "status": "processing"})
        api = GrokImagineImage2API(api_key="test-key", session=session)

        result = api.edit_image("Change the jacket to teal", "req_123", mask_indexs=[0, 2])

        self.assertEqual(result["request_id"], "req_456")
        session.post.assert_called_once_with(
            "https://api.muapi.ai/api/v1/grok-imagine-image-2-edit",
            json={"prompt": "Change the jacket to teal", "request_id": "req_123", "mask_indexs": [0, 2]},
            headers={"x-api-key": "test-key", "Content-Type": "application/json"},
            timeout=120,
        )

    def test_edit_image_requires_source_request_id(self):
        api = GrokImagineImage2API(api_key="test-key", session=Mock())

        with self.assertRaises(ValueError):
            api.edit_image("Change the jacket to teal", "")

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
