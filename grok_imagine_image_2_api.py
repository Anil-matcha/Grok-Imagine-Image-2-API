"""A small Python client for Grok Imagine Image 2.0 image generation APIs."""

import os
import time
from typing import Any, Dict, List, Optional

import requests
from dotenv import load_dotenv

load_dotenv()

DEFAULT_BASE_URL = "https://api.muapi.ai/api/v1"
GENERATE_ENDPOINT = "grok-imagine-image-2"
EDIT_ENDPOINT = "grok-imagine-image-2-edit"
SUPPORTED_ASPECT_RATIOS = frozenset({"1:1", "2:3", "3:2", "16:9", "9:16"})


class GrokImagineImage2API:
    """Submit Grok Imagine Image 2.0 jobs and retrieve their async results."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        session: Optional[requests.Session] = None,
    ):
        self.api_key = api_key or os.getenv("MUAPI_API_KEY")
        if not self.api_key:
            raise ValueError("An API key is required. Set MUAPI_API_KEY or pass api_key.")

        configured_base_url = (
            base_url
            or os.getenv("GROK_IMAGINE_IMAGE_2_API_BASE_URL")
            or os.getenv("GROK_API_BASE_URL")
            or DEFAULT_BASE_URL
        )
        self.base_url = configured_base_url.rstrip("/")
        self.headers = {"x-api-key": self.api_key, "Content-Type": "application/json"}
        self.session = session or requests.Session()

    def text_to_image(
        self,
        prompt: str,
        *,
        aspect_ratio: str = "1:1",
    ) -> Dict[str, Any]:
        """Generate an image from a text prompt."""
        if not isinstance(prompt, str) or not prompt.strip():
            raise ValueError("prompt must be a non-empty string.")
        if aspect_ratio not in SUPPORTED_ASPECT_RATIOS:
            supported = ", ".join(sorted(SUPPORTED_ASPECT_RATIOS))
            raise ValueError(f"Unsupported aspect_ratio {aspect_ratio!r}. Choose one of: {supported}.")

        payload: Dict[str, Any] = {"prompt": prompt, "aspect_ratio": aspect_ratio}
        return self._post(GENERATE_ENDPOINT, payload)

    def edit_image(
        self,
        prompt: str,
        request_id: str,
        *,
        mask_indexs: Optional[List[int]] = None,
    ) -> Dict[str, Any]:
        """Apply a targeted follow-up edit to a prior Grok Imagine Image 2.0 generation.

        `request_id` must be the request_id returned by a previous
        `text_to_image()` (or `edit_image()`) call — this model edits its own
        prior generations, not an arbitrary uploaded image. Optionally scope
        the edit to specific segments of the source image with `mask_indexs`.
        """
        if not isinstance(prompt, str) or not prompt.strip():
            raise ValueError("prompt must be a non-empty string.")
        if not request_id:
            raise ValueError("edit_image requires the request_id of a prior generation to edit.")

        payload: Dict[str, Any] = {"prompt": prompt, "request_id": request_id}
        if mask_indexs:
            payload["mask_indexs"] = list(mask_indexs)
        return self._post(EDIT_ENDPOINT, payload)

    def upload_file(self, file_path: str) -> Dict[str, Any]:
        """Upload a local reference asset for a later generation request."""
        with open(file_path, "rb") as file_data:
            response = self.session.post(
                f"{self.base_url}/upload_file",
                headers={"x-api-key": self.api_key},
                files={"file": file_data},
                timeout=120,
            )
        response.raise_for_status()
        return response.json()

    def get_result(self, request_id: str) -> Dict[str, Any]:
        """Retrieve the current state and output of a generation job."""
        response = self.session.get(
            f"{self.base_url}/predictions/{request_id}/result",
            headers=self.headers,
            timeout=30,
        )
        response.raise_for_status()
        return response.json()

    def wait_for_completion(
        self,
        request_id: str,
        poll_interval: float = 5,
        timeout: float = 900,
    ) -> Dict[str, Any]:
        """Poll a job until it completes, fails, or reaches the timeout."""
        if poll_interval < 0:
            raise ValueError("poll_interval must be zero or greater.")
        if timeout <= 0:
            raise ValueError("timeout must be greater than zero.")

        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            result = self.get_result(request_id)
            status = str(result.get("status", "")).lower()
            if status in {"completed", "succeeded", "success", "done"}:
                return result
            if status in {"failed", "error", "cancelled", "canceled"}:
                detail = result.get("error") or result.get("message") or result
                raise RuntimeError(f"Grok Imagine Image 2.0 generation {status}: {detail}")

            remaining = deadline - time.monotonic()
            if remaining > 0:
                time.sleep(min(poll_interval, remaining))

        raise TimeoutError(f"Timed out waiting for Grok Imagine Image 2.0 job {request_id}.")

    def _post(self, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        response = self.session.post(
            f"{self.base_url}/{path}",
            json=payload,
            headers=self.headers,
            timeout=120,
        )
        response.raise_for_status()
        return response.json()
