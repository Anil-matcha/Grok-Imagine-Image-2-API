"""MCP server exposing the Grok Imagine Image 2.0 Python client as agent tools."""

import json
from typing import Optional

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
def edit_image(prompt: str, images_list: list[str], aspect_ratio: str = "1:1") -> str:
    """Edit or combine one to five reference image URLs."""
    return json.dumps(
        _api().edit_image(prompt, images_list, aspect_ratio=aspect_ratio),
        indent=2,
        ensure_ascii=False,
    )


@mcp.tool()
def generate_image(
    prompt: str,
    images_list: Optional[list[str]] = None,
    aspect_ratio: str = "1:1",
) -> str:
    """Generate an image with an optional list of reference images."""
    return json.dumps(
        _api().generate(prompt, images_list=images_list, aspect_ratio=aspect_ratio),
        indent=2,
        ensure_ascii=False,
    )


@mcp.tool()
def get_task_status(request_id: str) -> str:
    """Get the status and output for a Grok Imagine Image 2.0 job."""
    return json.dumps(_api().get_result(request_id), indent=2, ensure_ascii=False)


if __name__ == "__main__":
    mcp.run()
