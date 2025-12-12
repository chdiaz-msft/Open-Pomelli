"""
Adapter interfaces. Replace these classes with real API clients.
"""

import asyncio
from typing import List, Optional, Dict
from pathlib import Path

import os
import aiohttp
import httpx
import fal_client
from api_secrets import MUAPIAPP_API_KEY, FAL_KEY

os.environ["FAL_KEY"] = FAL_KEY


# ---------------------------------------------------------
# UTILITY FUNCTIONS
# ---------------------------------------------------------

async def ensure_url(file_path_or_url: str) -> str:
    """
    Convert a local file path to a URL using fal_client, or return the URL as-is.
    Also handles problematic image formats by downloading, converting to PNG, and re-uploading.
    
    Args:
        file_path_or_url: Either a local file path or an existing URL
        
    Returns:
        A valid URL (either the original URL or uploaded file URL)
    """
    # Check if it's already a URL
    if file_path_or_url.startswith(('http://', 'https://')):
        # Check for problematic formats that might not be supported by Nano Banana
        problematic_formats = ['.avif', '.webp', '.svg']
        if any(file_path_or_url.lower().endswith(fmt) for fmt in problematic_formats):
            print(f"[ensure_url] Detected unsupported format, converting to PNG: {file_path_or_url}")
            try:
                # Download the image
                import tempfile
                from PIL import Image
                import io
                
                async with aiohttp.ClientSession() as session:
                    async with session.get(file_path_or_url) as resp:
                        if resp.status == 200:
                            # Read image data
                            image_data = await resp.read()
                            
                            # Convert to PNG using PIL
                            print(f"[ensure_url] Converting image to PNG format...")
                            img = Image.open(io.BytesIO(image_data))
                            
                            # Convert RGBA to RGB if necessary (for compatibility)
                            if img.mode in ('RGBA', 'LA', 'P'):
                                # Create white background
                                background = Image.new('RGB', img.size, (255, 255, 255))
                                if img.mode == 'P':
                                    img = img.convert('RGBA')
                                background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                                img = background
                            elif img.mode != 'RGB':
                                img = img.convert('RGB')
                            
                            # Save as PNG to temp file
                            with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp:
                                img.save(tmp, format='PNG')
                                tmp_path = tmp.name
                            
                            # Re-upload through fal_client
                            print(f"[ensure_url] Re-uploading PNG through fal_client...")
                            new_url = await fal_client.upload_file_async(tmp_path)
                            
                            # Clean up temp file
                            import os
                            os.unlink(tmp_path)
                            
                            print(f"[ensure_url] Successfully converted and re-uploaded: {new_url}")
                            return new_url
                        else:
                            print(f"[ensure_url] Failed to download image (status {resp.status}), using original URL")
                            return file_path_or_url
            except Exception as e:
                print(f"[ensure_url] Error converting image: {e}, using original URL")
                import traceback
                traceback.print_exc()
                return file_path_or_url
        
        return file_path_or_url
    
    # Check if it's a valid local file
    file_path = Path(file_path_or_url)
    if file_path.exists() and file_path.is_file():
        # Upload the file and return the URL
        image_url = await fal_client.upload_file_async(str(file_path))
        return image_url
    
    # If neither URL nor valid file, raise an error
    raise ValueError(f"Invalid input: '{file_path_or_url}' is neither a valid URL nor an existing file path")


# ---------------------------------------------------------
# TEXT-ONLY ADAPTER (MuAPI GPT-5-Nano)
# ---------------------------------------------------------

class TextAdapter:
    """
    Text-only MuAPI-backed TextAdapter.
    """

    BASE_URL = "https://api.muapi.ai/api/v1"
    MODEL = "gpt-5-nano"

    def __init__(self):
        self.api_key = MUAPIAPP_API_KEY
        if not self.api_key:
            raise ValueError("MUAPIAPP_API_KEY missing in environment variables")

    async def _single_generate(self, session, prompt: str) -> str:
        submit_url = f"{self.BASE_URL}/{self.MODEL}"

        headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key,
        }

        payload = {"prompt": prompt}

        # Submit request
        print(f"[TextAdapter] Submitting prompt: {prompt}")
        async with session.post(submit_url, headers=headers, json=payload) as resp:
            if resp.status != 200:
                print(f"[TextAdapter] Submit failed: {resp.status}")
                raise RuntimeError(f"MuAPI submit failed: {resp.status} {await resp.text()}")

            data = await resp.json()
            request_id = data["request_id"]
            print(f"[TextAdapter] Request submitted. ID: {request_id}")

        # Poll results
        result_url = f"{self.BASE_URL}/predictions/{request_id}/result"

        while True:
            await asyncio.sleep(0.5)

            async with session.get(result_url, headers={"x-api-key": self.api_key}) as resp:
                if resp.status != 200:
                    raise RuntimeError(f"MuAPI poll failed: {resp.status} {await resp.text()}")

                result = await resp.json()
                status = result["status"]

                if status == "completed":
                    print(f"[TextAdapter] Request {request_id} completed.")
                    return result["outputs"][0]

                if status == "failed":
                    print(f"[TextAdapter] Request {request_id} failed.")
                    raise RuntimeError(f"MuAPI text task failed: {result.get('error')}")
                
                print(f"[TextAdapter] Polling {request_id}: {status}...")

    async def generate(self, prompt: str, n: int = 1) -> List[str]:
        async with aiohttp.ClientSession() as session:
            tasks = [self._single_generate(session, prompt) for _ in range(n)]
            return await asyncio.gather(*tasks)


# ---------------------------------------------------------
# VISION ADAPTER (MuAPI GPT-5-Nano Vision)
# ---------------------------------------------------------

class VisionAdapter:
    """
    Vision-capable adapter using GPT-5-Nano:
    - Accepts image URLs
    - Produces structured analysis + description
    """

    BASE_URL = "https://api.muapi.ai/api/v1"
    MODEL = "gpt-5-nano"

    def __init__(self):
        self.api_key = MUAPIAPP_API_KEY
        if not self.api_key:
            raise ValueError("MUAPIAPP_API_KEY missing in environment variables")

    async def analyze(
        self,
        prompt: str,
        image_url: str
    ) -> dict:
        """
        Given an image URL or local file path, produce structured analysis.
        Returns a dict: { summary, tags, objects, colors, suggestions }
        """
        # Ensure we have a URL (upload if local file)
        image_url = await ensure_url(image_url)

        submit_url = f"{self.BASE_URL}/{self.MODEL}"

        headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key,
        }

        payload = {
            "prompt": f"Analyze these images and return structured JSON: {prompt}",
            "image_url": image_url,
        }

        async with aiohttp.ClientSession() as session:
            # Submit
            print(f"[VisionAdapter] Submitting analysis request for {image_url}")
            async with session.post(submit_url, headers=headers, json=payload) as resp:
                if resp.status != 200:
                    print(f"[VisionAdapter] Submit failed: {resp.status}")
                    raise RuntimeError(f"MuAPI vision submit error {resp.status}: {await resp.text()}")
                data = await resp.json()
                request_id = data["request_id"]
                print(f"[VisionAdapter] Request submitted. ID: {request_id}")

            # Poll
            result_url = f"{self.BASE_URL}/predictions/{request_id}/result"

            while True:
                await asyncio.sleep(0.5)

                async with session.get(result_url, headers={"x-api-key": self.api_key}) as resp:
                    if resp.status != 200:
                        raise RuntimeError(f"MuAPI poll error {resp.status}: {await resp.text()}")

                    result = await resp.json()
                    status = result["status"]

                    if status == "completed":
                        print(f"[VisionAdapter] Request {request_id} completed.")
                        output_text = result["outputs"][0]

                        # Try to parse JSON (if model outputs JSON)
                        try:
                            import json
                            return json.loads(output_text)
                        except:
                            # If it's plain text, wrap it
                            return {"summary": output_text}

                    if status == "failed":
                        print(f"[VisionAdapter] Request {request_id} failed.")
                        raise RuntimeError(f"MuAPI vision task failed: {result.get('error')}")
                    
                    print(f"[VisionAdapter] Polling {request_id}: {status}...")


class ImageAdapter:
    def __init__(self):
        self.api_key = MUAPIAPP_API_KEY
        self.base_url = "https://api.muapi.ai/api/v1"

        self.headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key
        }

    async def _poll_result(self, request_id: str) -> dict:
        """Polls the prediction result until completed."""
        result_url = f"{self.base_url}/predictions/{request_id}/result"

        async with httpx.AsyncClient(timeout=30.0) as client:
            while True:
                res = await client.get(result_url, headers=self.headers)
                if res.status_code != 200:
                    raise Exception(f"Polling error {res.status_code}: {res.text}")

                data = res.json()
                status = data["status"]

                if status == "completed":
                    print(f"[ImageAdapter] Request {request_id} completed.")
                    return data
                elif status == "failed":
                    print(f"[ImageAdapter] Request {request_id} failed.")
                    raise Exception(f"Task failed: {data.get('error')}")
                
                print(f"[ImageAdapter] Polling {request_id}: {status}...")

                await asyncio.sleep(0.5)

    # -----------------------------------------------------
    #  IMAGE GENERATION  (Nano Banana)
    # -----------------------------------------------------
    async def generate_image(self, prompt: str, size=(1024, 1024)) -> List[str]:
        """
        Generates an image using Nano Banana model.

        Returns: list of image URLs
        """
        width, height = size
        # Convert size to aspect ratio
        if width == height:
            aspect_ratio = "1:1"
        elif width > height:
            aspect_ratio = "16:9"
        else:
            aspect_ratio = "9:16"
        
        url = f"{self.base_url}/nano-banana"

        payload = {
            "prompt": prompt,
            "aspect_ratio": aspect_ratio
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            print(f"[ImageAdapter] Generating image with Nano Banana: {prompt}")
            res = await client.post(url, headers=self.headers, json=payload)

        if res.status_code != 200:
            print(f"[ImageAdapter] Generation failed: {res.status_code}")
            raise Exception(f"Generation error {res.status_code}: {res.text}")

        request_id = res.json()["request_id"]
        print(f"[ImageAdapter] Request submitted. ID: {request_id}")

        result = await self._poll_result(request_id)

        return result["outputs"]   # list of URLs

    # -----------------------------------------------------
    #  IMAGE EDITING & REFERENCE GENERATION (Nano Banana Edit)
    # -----------------------------------------------------
    async def edit_image(self, image_url: str, instructions: str, aspect_ratio="1:1") -> str:
        """
        Edits an existing image using Nano Banana Edit.
        Accepts either a URL or local file path.
        """
        # Ensure we have a URL (upload if local file, convert problematic formats)
        print(f"[ImageAdapter] Processing reference image: {image_url}")
        image_url = await ensure_url(image_url)
        print(f"[ImageAdapter] Using reference URL: {image_url}")
        
        url = f"{self.base_url}/nano-banana-edit"

        payload = {
            "prompt": instructions,
            "images_list": [image_url],
            "aspect_ratio": aspect_ratio
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            print(f"[ImageAdapter] Sending Nano Banana Edit request...")
            print(f"[ImageAdapter] Prompt: {instructions[:100]}...")
            print(f"[ImageAdapter] Aspect Ratio: {aspect_ratio}")
            res = await client.post(url, headers=self.headers, json=payload)

        if res.status_code != 200:
            error_msg = f"Nano Banana Edit request failed with status {res.status_code}: {res.text}"
            print(f"[ImageAdapter] ERROR: {error_msg}")
            raise Exception(error_msg)

        request_id = res.json()["request_id"]
        print(f"[ImageAdapter] Request submitted successfully. ID: {request_id}")

        result = await self._poll_result(request_id)

        return result["outputs"][0]   # edited image URL

    async def generate_with_reference(self, prompt: str, reference_image_url: str, aspect_ratio="1:1") -> str:
        """
        Generates an image using a reference image (e.g. logo) using Nano Banana Edit.
        This is effectively an edit operation where the reference image is the base.
        """
        return await self.edit_image(reference_image_url, prompt, aspect_ratio)

class VideoAdapter:
    def __init__(self):
        self.api_key = MUAPIAPP_API_KEY
        self.base_url = "https://api.muapi.ai/api/v1"

        self.headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key,
        }

    async def _poll_result(self, request_id: str) -> dict:
        """Poll the MuAPI result endpoint until finished."""
        url = f"{self.base_url}/predictions/{request_id}/result"

        async with httpx.AsyncClient(timeout=60.0) as client:
            while True:
                res = await client.get(url, headers=self.headers)
                if res.status_code != 200:
                    raise Exception(f"Polling Error {res.status_code}: {res.text}")

                data = res.json()
                status = data["status"]

                if status == "completed":
                    print(f"[VideoAdapter] Request {request_id} completed.")
                    return data
                elif status == "failed":
                    print(f"[VideoAdapter] Request {request_id} failed.")
                    raise Exception(f"Video generation failed: {data.get('error')}")
                
                print(f"[VideoAdapter] Polling {request_id}: {status}...")

                await asyncio.sleep(0.5)

    # ----------------------------------------------------------
    # Main render() function — decides T2V or I2V automatically
    # ----------------------------------------------------------
    async def render(self, storyboard: Dict) -> str:
        """
        storyboard dict must contain:
        • prompt (required)
        • aspect_ratio (optional, for T2V only)
        • resolution
        • duration
        • image_url  (if present → I2V, else → T2V)
                     Can be a URL or local file path

        Returns: direct URL of generated video
        """
        # If image_url is provided, ensure it's a URL (upload if local file)
        if "image_url" in storyboard:
            storyboard["image_url"] = await ensure_url(storyboard["image_url"])
            return await self._generate_i2v(storyboard)
        else:
            return await self._generate_t2v(storyboard)

    # ----------------------------------------------------------
    # Text-to-Video (T2V)
    # ----------------------------------------------------------
    async def _generate_t2v(self, data: Dict) -> str:
        url = f"{self.base_url}/seedance-lite-t2v"

        payload = {
            "prompt": data["prompt"],
            "aspect_ratio": data.get("aspect_ratio", "16:9"),
            "resolution": data.get("resolution", "480p"),
            "duration": data.get("duration", 5),
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            print(f"[VideoAdapter] Generating T2V: {data['prompt']}")
            res = await client.post(url, headers=self.headers, json=payload)

        if res.status_code != 200:
            print(f"[VideoAdapter] T2V failed: {res.status_code}")
            raise Exception(f"T2V Error {res.status_code}: {res.text}")

        request_id = res.json()["request_id"]
        print(f"[VideoAdapter] Request submitted. ID: {request_id}")
        result = await self._poll_result(request_id)

        return result["outputs"][0]  # video URL

    # ----------------------------------------------------------
    # Image-to-Video (I2V)
    # ----------------------------------------------------------
    async def _generate_i2v(self, data: Dict) -> str:
        url = f"{self.base_url}/seedance-lite-i2v"

        payload = {
            "prompt": data["prompt"],
            "image_url": data["image_url"],
            "resolution": data.get("resolution", "480p"),
            "duration": data.get("duration", 5),
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            print(f"[VideoAdapter] Generating I2V: {data['prompt']}")
            res = await client.post(url, headers=self.headers, json=payload)

        if res.status_code != 200:
            print(f"[VideoAdapter] I2V failed: {res.status_code}")
            raise Exception(f"I2V Error {res.status_code}: {res.text}")

        request_id = res.json()["request_id"]
        print(f"[VideoAdapter] Request submitted. ID: {request_id}")
        result = await self._poll_result(request_id)

        return result["outputs"][0]  # video URL


# ---------------------------------------------------------
# WEB SCRAPING ADAPTER
# ---------------------------------------------------------

# ---------------------------------------------------------
# WEB SCRAPING ADAPTER (Playwright)
# ---------------------------------------------------------

class WebScrapingAdapter:
    """
    Web scraping adapter using Playwright.
    Capable of rendering JavaScript, capturing screenshots, and extracting computed styles.
    """
    
    def __init__(self):
        self.user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    
    async def fetch_url(self, url: str, timeout: int = 30) -> Dict[str, any]:
        """
        Fetch content from a URL using Playwright.
        Extracts text, HTML, metadata, and visual assets (colors, fonts, images).
        """
        print(f"[WebScrapingAdapter] Fetching URL with Playwright: {url}")
        
        try:
            from playwright.async_api import async_playwright
            from bs4 import BeautifulSoup
        except ImportError:
            print("[WebScrapingAdapter] Playwright or BeautifulSoup not installed.")
            print("Please run: pip install playwright beautifulsoup4 && playwright install")
            return {"error": "Dependencies missing"}

        try:
            async with async_playwright() as p:
                # Launch browser
                try:
                    browser = await p.chromium.launch(headless=True)
                except Exception as e:
                    print(f"[WebScrapingAdapter] Failed to launch browser: {e}")
                    print("Try running: playwright install")
                    return {"error": "Browser launch failed"}

                context = await browser.new_context(
                    user_agent=self.user_agent,
                    viewport={"width": 1280, "height": 800}
                )
                page = await context.new_page()
                
                # Navigate
                try:
                    response = await page.goto(url, timeout=timeout*1000, wait_until="domcontentloaded")
                    status_code = response.status if response else 0
                    
                    # Wait for some dynamic content
                    await page.wait_for_timeout(2000)
                    
                    # Get content
                    content = await page.content()
                    title = await page.title()
                    
                    # Extract detailed assets via DOM evaluation
                    assets = await page.evaluate("""() => {
                        const getStyle = (el, prop) => getComputedStyle(el).getPropertyValue(prop);
                        
                        const colors = new Set();
                        const fonts = new Set();
                        
                        // Sample common elements for styles
                        const elements = document.querySelectorAll('body, h1, h2, h3, p, a, button, .btn, header, footer, div');
                        elements.forEach(el => {
                            const style = getComputedStyle(el);
                            if (style.color && style.color !== 'rgba(0, 0, 0, 0)') colors.add(style.color);
                            if (style.backgroundColor && style.backgroundColor !== 'rgba(0, 0, 0, 0)') colors.add(style.backgroundColor);
                            if (style.fontFamily) fonts.add(style.fontFamily);
                        });

                        // Images (filter small ones)
                        const images = Array.from(document.images)
                            .filter(img => img.naturalWidth > 50 && img.naturalHeight > 50)
                            .map(img => ({
                                src: img.src,
                                width: img.naturalWidth,
                                height: img.naturalHeight,
                                alt: img.alt
                            }));

                        // Links (for finding guidelines, social media)
                        const links = Array.from(document.links).map(a => ({
                            text: a.innerText.trim(),
                            href: a.href
                        }));

                        // Icons/Logos from head
                        const icons = Array.from(document.querySelectorAll('link[rel*="icon"], link[rel="apple-touch-icon"]'))
                            .map(l => l.href);
                            
                        // OpenGraph Image
                        const ogImage = document.querySelector('meta[property="og:image"]');
                        const ogImageUrl = ogImage ? ogImage.content : null;

                        return {
                            colors: Array.from(colors).slice(0, 50), // Limit to top 50
                            fonts: Array.from(fonts),
                            images: images.slice(0, 20), // Limit to top 20
                            links: links,
                            icons: icons,
                            og_image: ogImageUrl
                        };
                    }""")
                    
                    # Parse with BeautifulSoup for meta tags
                    soup = BeautifulSoup(content, 'html.parser')
                    
                    # Extract meta
                    metadata = {}
                    desc_tag = soup.find('meta', attrs={'name': 'description'})
                    if desc_tag: metadata['description'] = desc_tag.get('content', '')
                    
                    keywords_tag = soup.find('meta', attrs={'name': 'keywords'})
                    if keywords_tag: metadata['keywords'] = keywords_tag.get('content', '')
                    
                    # Clean text
                    for script in soup(["script", "style", "noscript"]):
                        script.decompose()
                    text = soup.get_text(separator=' ', strip=True)
                    
                    print(f"[WebScrapingAdapter] Successfully fetched {len(text)} chars")
                    
                    return {
                        "url": url,
                        "status_code": status_code,
                        "title": title,
                        "text": text,
                        "html": content,
                        "metadata": metadata,
                        "assets": assets  # New field with extracted assets
                    }
                    
                except Exception as e:
                    print(f"[WebScrapingAdapter] Navigation error: {e}")
                    return {
                        "url": url,
                        "status_code": 0,
                        "error": str(e),
                        "text": "",
                        "title": "",
                        "metadata": {},
                        "assets": {}
                    }
                finally:
                    await browser.close()
                    
        except Exception as e:
            print(f"[WebScrapingAdapter] Critical error: {e}")
            return {"error": str(e)}

    async def capture_screenshot(self, url: str, output_path: str = None) -> str:
        """
        Capture a screenshot of the website.
        Returns the path to the screenshot or a URL if uploaded.
        """
        print(f"[WebScrapingAdapter] Capturing screenshot: {url}")
        
        try:
            from playwright.async_api import async_playwright
        except ImportError:
            return None

        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(
                    user_agent=self.user_agent,
                    viewport={"width": 1280, "height": 800}
                )
                page = await context.new_page()
                
                await page.goto(url, wait_until="networkidle", timeout=30000)
                
                # Generate filename if not provided
                if not output_path:
                    import time
                    filename = f"screenshot_{int(time.time())}.png"
                    output_path = os.path.abspath(filename)
                
                await page.screenshot(path=output_path, full_page=False)
                print(f"[WebScrapingAdapter] Screenshot saved to {output_path}")
                
                await browser.close()
                
                # Upload to Fal for URL access if needed
                if os.environ.get("FAL_KEY"):
                    try:
                        image_url = await fal_client.upload_file_async(output_path)
                        print(f"[WebScrapingAdapter] Screenshot uploaded: {image_url}")
                        return image_url
                    except Exception as e:
                        print(f"[WebScrapingAdapter] Upload failed: {e}")
                        return output_path
                
                return output_path
                
        except Exception as e:
            print(f"[WebScrapingAdapter] Screenshot failed: {e}")
            return None

    async def search_and_fetch(self, query: str, num_results: int = 3) -> List[Dict[str, any]]:
        """Placeholder for search functionality."""
        print(f"[WebScrapingAdapter] Search not implemented.")
        return []

