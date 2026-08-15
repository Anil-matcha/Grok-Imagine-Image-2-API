"""MCP server exposing the Grok Imagine Image 2.0 Python client as agent tools."""

import json
from typing import List, Optional

from mcp.server.fastmcp import FastMCP

from grok_imagine_image_2_api import GrokImagineImage2API

mcp = FastMCP("Grok Imagine Image 2.0 API Server")


def _api() -> GrokImagineImage2API:
    return GrokImagineImage2API()


@mcp.tool()
def text_to_image(prompt: str, aspect_ratio: str = "1:1") -> str:
    """Generate a Grok Imagine Image 2.0 image from a text prompt."""
    return json.dumps(
        _api().text_to_image(prompt, aspect_ratio=aspect_ratio),
        indent=2,
        ensure_ascii=False,
    )


@mcp.tool()
def edit_image(prompt: str, request_id: str, mask_indexs: Optional[List[int]] = None) -> str:
    """Apply a targeted follow-up edit to a prior Grok Imagine Image 2.0 generation,
    identified by the request_id it returned. Optionally scope the edit to
    specific segments of the source image with mask_indexs."""
    return json.dumps(
        _api().edit_image(prompt, request_id, mask_indexs=mask_indexs),
        indent=2,
        ensure_ascii=False,
    )


@mcp.tool()
def get_task_status(request_id: str) -> str:
    """Get the status and output for a Grok Imagine Image 2.0 job."""
    return json.dumps(_api().get_result(request_id), indent=2, ensure_ascii=False)


if __name__ == "__main__":
    mcp.run()
