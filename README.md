# Grok Imagine Image 2.0 API (Grok Imagine Image 2 API) — Python SDK & MCP Server

[![Powered by MuAPI](https://img.shields.io/badge/Powered%20by-MuAPI-6366f1?style=flat-square)](https://muapi.ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)

A focused Python SDK and MCP server for the Grok Imagine Image 2.0 API through MuAPI. Also known as the Grok Imagine Image 2 API or Grok Imagine API, it provides xAI image generation, text-to-image, image-to-image editing, multi-reference generation, local uploads, and asynchronous job polling from Python or an MCP-capable agent.

> **Availability:** The grok-imagine-image-2 endpoint is listed as upcoming in MuAPI's latest model catalog. This client targets the production endpoint contract and is ready to use as soon as access is enabled for your API key.

## Related projects

- [Grok Imagine Image 2.0 on MuAPI](https://muapi.ai/grok-imagine-image-2) — model overview and access.
- [MuAPI image-generation docs](https://muapi.ai/docs/image-generation) — shared authentication and polling patterns.
- [Wan-3.0-API](https://github.com/Anil-matcha/Wan-3.0-API) — the companion Python SDK and MCP server for Wan video generation.
- [Flux-3-Dev-API](https://github.com/Anil-matcha/Flux-3-Dev-API) — MuAPI access to FLUX image and video workflows.
- [Open-Generative-AI](https://github.com/Anil-matcha/Open-Generative-AI) — open-source image and video studio powered by MuAPI.

## Install

~~~bash
git clone https://github.com/Anil-matcha/Grok-Imagine-Image-2-API.git
cd Grok-Imagine-Image-2-API
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
~~~

Set **MUAPI_API_KEY** in the env file. The client uses **https://api.muapi.ai/api/v1** by default. Set **GROK_IMAGINE_IMAGE_2_API_BASE_URL** to target a compatible self-hosted or proxy endpoint instead. **GROK_API_BASE_URL** is also accepted as a shorter alias.

## Quick start

~~~python
from grok_imagine_image_2_api import GrokImagineImage2API

api = GrokImagineImage2API()

job = api.text_to_image(
    "A high-contrast halftone portrait in fine white dots on a black background",
    aspect_ratio="1:1",
)

result = api.wait_for_completion(job["request_id"])
print(result)
~~~

The API is asynchronous: submit a prompt, keep the returned request ID, and poll until the task is completed.

## Image editing and multi-reference generation

Pass one or more public image URLs to **edit_image()**. The model accepts up to five references in one request, which is useful for combining a subject, location, props, and a target style.

~~~python
job = api.edit_image(
    prompt="Place the subject in a rainy neon street while preserving their face and clothing.",
    images_list=[
        "https://example.com/subject.jpg",
        "https://example.com/street.jpg",
    ],
    aspect_ratio="9:16",
)

result = api.wait_for_completion(job["request_id"])
print(result)
~~~

For a single method that handles both modes, use **generate(prompt, images_list=...)**.

## Upload a local reference

~~~python
uploaded = api.upload_file("reference.png")
print(uploaded)
~~~

Use the URL returned by the upload endpoint in **images_list** for a later generation or edit request.

## API surface

| Method | Purpose |
| --- | --- |
| **text_to_image()** | Create an image from a text prompt. |
| **edit_image()** | Edit or combine one to five reference image URLs. |
| **generate()** | Unified text-to-image and image-edit entrypoint. |
| **upload_file()** | Upload a local reference asset. |
| **get_result() / wait_for_completion()** | Retrieve an asynchronous job and wait for its output. |

## Supported aspect ratios

The current catalog contract supports:

**1:1**, **1:2**, **2:1**, **9:16**, **16:9**, **2:3**, **3:2**, **3:4**, and **4:3**.

## MCP server

Expose the model to MCP-capable clients:

~~~bash
python mcp_server.py
~~~

The server provides **text_to_image**, **edit_image**, **generate_image**, and **get_task_status** tools. Configure it in an MCP client with the repository's Python interpreter and pass **MUAPI_API_KEY** through the process environment.

Example configuration:

~~~json
{
  "mcpServers": {
    "grok-imagine-image-2": {
      "command": "/absolute/path/to/.venv/bin/python",
      "args": ["/absolute/path/to/Grok-Imagine-Image-2-API/mcp_server.py"],
      "env": {
        "MUAPI_API_KEY": "your_muapi_api_key"
      }
    }
  }
}
~~~

## Endpoint compatibility

The client calls these MuAPI paths beneath the configured base URL:

- **POST /grok-imagine-image-2**
- **POST /upload_file**
- **GET /predictions/{request_id}/result**

The SDK uses the **x-api-key** header and JSON request bodies. The model endpoint accepts **prompt**, optional **images_list**, and **aspect_ratio**.

## Development

Run the local tests and syntax checks with:

~~~bash
python -m unittest discover -s tests -v
python -m py_compile grok_imagine_image_2_api.py mcp_server.py
~~~

## License

[MIT](LICENSE)
