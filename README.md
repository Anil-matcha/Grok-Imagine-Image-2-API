# Grok Imagine Image 2.0 API (Grok Imagine Image 2 API) — Python SDK & MCP Server

[![Powered by MuAPI](https://img.shields.io/badge/Powered%20by-MuAPI-6366f1?style=flat-square)](https://muapi.ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)

A focused Python SDK and MCP server for the Grok Imagine Image 2.0 API through MuAPI. Also known as the Grok Imagine Image 2 API or Grok Imagine API, it provides xAI image generation, text-to-image, chained follow-up image editing, local uploads, and asynchronous job polling from Python or an MCP-capable agent.

> **Availability:** Live on MuAPI as two endpoints — `grok-imagine-image-2` for text-to-image and `grok-imagine-image-2-edit` for follow-up edits.

## Related Projects

- [MuAPI](https://muapi.ai) — Unified API for image, video, and audio generation across hundreds of AI models.
- [Grok Imagine Image 2.0 on MuAPI](https://muapi.ai/grok-imagine-image-2) — Official model landing page for Grok Imagine Image 2.0 generation and editing.
- [Grok Imagine Image 2.0 playground](https://muapi.ai/playground/grok-imagine-image-2) — Try the model in the browser when access is enabled.
- [MuAPI API reference](https://muapi.ai/docs/api-reference) — REST endpoint and asynchronous prediction lifecycle documentation.
- [MuAPI access keys](https://muapi.ai/access-keys) — Create the x-api-key credential required by this SDK.
- [awesome-ai-image-models](https://github.com/Anil-matcha/awesome-ai-image-models) — Compare image models by API, price, quality, and use case.
- [Awesome-GPT-Image-2-API-Prompts](https://github.com/Anil-matcha/Awesome-GPT-Image-2-API-Prompts) — Reusable prompt patterns for image generation, typography, editing, and visual design.
- [Open-Generative-AI](https://github.com/Anil-matcha/Open-Generative-AI) — Open-source image and video studio powered by MuAPI.
- [Generative-Media-Skills](https://github.com/SamurAIGPT/Generative-Media-Skills) — Agent-ready skills for driving image, video, and audio models from coding assistants.
- [muapi-cli](https://github.com/SamurAIGPT/muapi-cli) — Command-line access to MuAPI image, video, and audio endpoints.
- [Wan-3.0-API](https://github.com/Anil-matcha/Wan-3.0-API) — the companion Python SDK and MCP server for Wan video generation.
- [Flux-3-Dev-API](https://github.com/Anil-matcha/Flux-3-Dev-API) — MuAPI access to FLUX image and video workflows.

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

## Follow-up editing

Grok Imagine Image 2.0's edit model doesn't take a freshly uploaded photo — it applies a targeted edit to an image it previously generated, referenced by that job's `request_id`. Pass **edit_image()** the `request_id` from a prior `text_to_image()` (or `edit_image()`) call along with a prompt describing the change:

~~~python
job = api.text_to_image("A raccoon in a teal Hawaiian shirt at a beach club table", aspect_ratio="1:1")
base = api.wait_for_completion(job["request_id"])

edit_job = api.edit_image(
    prompt="Change the Hawaiian shirt to a plain white t-shirt, keep everything else unchanged.",
    request_id=job["request_id"],
)
result = api.wait_for_completion(edit_job["request_id"])
print(result)
~~~

Pass an optional `mask_indexs` list of integers to scope the edit to specific segments of the source image instead of the whole frame. Each edit call returns its own `request_id`, so edits can be chained repeatedly to keep refining the same image.

## Upload a local reference

~~~python
uploaded = api.upload_file("reference.png")
print(uploaded)
~~~

Useful for storing your own reference assets alongside a job; note that Grok Imagine Image 2.0 itself doesn't accept uploaded images as edit input — see **Follow-up editing** above.

## API surface

| Method | Purpose |
| --- | --- |
| **text_to_image()** | Create an image from a text prompt. |
| **edit_image()** | Apply a follow-up edit to a prior generation, referenced by its request_id. |
| **upload_file()** | Upload a local reference asset. |
| **get_result() / wait_for_completion()** | Retrieve an asynchronous job and wait for its output. |

## Supported aspect ratios

The current catalog contract supports:

**1:1**, **2:3**, **3:2**, **16:9**, and **9:16**.

## MCP server

Expose the model to MCP-capable clients:

~~~bash
python mcp_server.py
~~~

The server provides **text_to_image**, **edit_image**, and **get_task_status** tools. Configure it in an MCP client with the repository's Python interpreter and pass **MUAPI_API_KEY** through the process environment.

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

- **POST /grok-imagine-image-2** — `{prompt, aspect_ratio}`
- **POST /grok-imagine-image-2-edit** — `{prompt, request_id, mask_indexs?}`
- **POST /upload_file**
- **GET /predictions/{request_id}/result**

The SDK uses the **x-api-key** header and JSON request bodies.

## Development

Run the local tests and syntax checks with:

~~~bash
python -m unittest discover -s tests -v
python -m py_compile grok_imagine_image_2_api.py mcp_server.py
~~~

## License

[MIT](LICENSE)
