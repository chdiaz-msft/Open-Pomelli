#!/usr/bin/env python3
"""
Brand DNA Analysis CLI Tool

Usage: python brand_dna.py <URL>
Example: python brand_dna.py https://www.northerntrust.com
"""

import sys
import asyncio
import json
import aiohttp
from contextlib import contextmanager
from datetime import datetime
from marketing_agent_core import MarketingAgent


@contextmanager
def redirect_stdout_to_file(log_file_path: str):
    """Context manager to redirect stdout to a file temporarily."""
    original_stdout = sys.stdout
    try:
        with open(log_file_path, 'w', encoding='utf-8') as log_file:
            sys.stdout = log_file
            yield log_file_path
    finally:
        sys.stdout = original_stdout


def print_brand_dna(brand_dna: dict) -> None:
    """Pretty-print Brand DNA analysis."""

    print("\n" + "=" * 80)
    print("🧬 BRAND DNA ANALYSIS RESULTS")
    print("=" * 80)

    # Basic Info
    print(f"\n📊 BRAND OVERVIEW")
    print(f"   Brand Name:       {brand_dna.get('brand_name', 'N/A')}")
    print(f"   Industry:         {brand_dna.get('industry', 'N/A')}")
    print(f"   Tagline:          {brand_dna.get('tagline', 'N/A')}")
    print(f"   Target Audience:  {brand_dna.get('target_audience', 'N/A')}")

    # Value Proposition
    if brand_dna.get('value_proposition'):
        print(f"\n💡 VALUE PROPOSITION")
        print(f"   {brand_dna['value_proposition']}")

    # Tone & Personality
    if brand_dna.get('tone_of_voice'):
        print(f"\n🗣️  TONE OF VOICE")
        for tone in brand_dna['tone_of_voice']:
            print(f"   • {tone}")

    if brand_dna.get('brand_personality'):
        print(f"\n🎭 BRAND PERSONALITY")
        for trait in brand_dna['brand_personality']:
            print(f"   • {trait}")

    # Key Messages
    if brand_dna.get('key_messages'):
        print(f"\n📢 KEY MESSAGES")
        for i, msg in enumerate(brand_dna['key_messages'], 1):
            print(f"   {i}. {msg}")

    # Visual Style
    if brand_dna.get('visual_style'):
        vs = brand_dna['visual_style']

        print(f"\n🎨 VISUAL STYLE")

        # Colors
        colors = vs.get('colors', [])
        primary_colors = vs.get('primary_colors', [])
        secondary_colors = vs.get('secondary_colors', [])

        # Check if all colors are black (indicates extraction failed)
        all_colors = colors + primary_colors + secondary_colors
        all_black = all_colors and all(c == '#000000' for c in all_colors)

        if all_black:
            print(f"   Colors: ⚠️  Could not extract colors from website")
        else:
            if colors:
                print(f"   Colors: {', '.join(colors[:8])}")
            if primary_colors:
                print(f"   Primary: {', '.join(primary_colors)}")
            if secondary_colors:
                print(f"   Secondary: {', '.join(secondary_colors)}")

        # Typography
        if vs.get('typography'):
            typo = vs['typography']
            if typo.get('primary_font'):
                print(f"   Primary Font: {typo['primary_font']}")
            if typo.get('secondary_font'):
                print(f"   Secondary Font: {typo['secondary_font']}")

        # Logo
        if vs.get('logo', {}).get('url'):
            print(f"   Logo URL: {vs['logo']['url']}")

        # Styles
        if vs.get('imagery_style'):
            print(f"   Imagery Style: {vs['imagery_style']}")
        if vs.get('layout_style'):
            print(f"   Layout Style: {vs['layout_style']}")

    # Assets
    if brand_dna.get('assets'):
        assets = brand_dna['assets']
        print(f"\n📁 EXTRACTED ASSETS")

        if assets.get('logo_url'):
            print(f"   Logo: {assets['logo_url']}")
        if assets.get('screenshot_url'):
            print(f"   Screenshot: {assets['screenshot_url']}")
        if assets.get('images'):
            print(f"   Images: {len(assets['images'])} found")
            for img_url in assets['images'][:5]:  # Show first 5
                print(f"      • {img_url}")
        if assets.get('guidelines'):
            print(f"   Guidelines: {len(assets['guidelines'])} document(s) found")

    # Source
    if brand_dna.get('source_url'):
        print(f"\n🔗 SOURCE")
        print(f"   {brand_dna['source_url']}")

    print("\n" + "=" * 80)


def print_full_response(response: dict) -> None:
    """Print complete agent response including thinking and suggestions."""

    print("\n" + "=" * 80)
    print("📋 FULL ANALYSIS RESPONSE")
    print("=" * 80)

    # Main Message
    if response.get('agent_response'):
        print(f"\n🎯 AGENT MESSAGE:")
        print(f"   {response['agent_response']}")

    # Brand DNA (detailed)
    if response.get('brand_dna'):
        print_brand_dna(response['brand_dna'])

    # Generated Assets
    if response.get('generated_assets'):
        print(f"\n🎨 GENERATED ASSETS:")
        for i, asset in enumerate(response['generated_assets'], 1):
            asset_type = asset.get('type', 'unknown')
            url = asset.get('url') or asset.get('data', {}).get('image_url')
            print(f"   {i}. {asset_type}: {url}")

    print("\n" + "=" * 80)


async def check_url_accessible(url: str) -> bool:
    """
    Check if the URL is accessible.

    Args:
        url: Website URL to check

    Returns:
        True if accessible, False otherwise
    """
    # Add headers to mimic a real browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.head(url, headers=headers, timeout=aiohttp.ClientTimeout(total=10), allow_redirects=True) as resp:
                return resp.status < 400
    except Exception as e:
        # If HEAD fails, try GET
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=10), allow_redirects=True) as resp:
                    return resp.status < 400
        except Exception:
            return False


async def analyze_brand(url: str) -> None:
    """
    Analyze a website and extract Brand DNA.

    Args:
        url: Website URL to analyze
    """
    print(f"\n🚀 Starting Brand DNA Analysis...")
    print(f"📍 Target: {url}")

    # Create log file with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = f"brand_dna_analysis_{timestamp}.log"

    print(f"⏳ Analyzing website... (this may take 30-60 seconds)")
    print(f"📝 Debug logs will be saved to: {log_file}\n")

    # Redirect all debug output to log file
    with redirect_stdout_to_file(log_file):
        # Initialize agent (logs will go to file)
        agent = MarketingAgent()

        # Call agent with analyze prompt (all debug logs go to file)
        response = await agent.process_message(f"analyze {url}")

    # Print brand DNA only (now enriched and complete)
    if response.get('brand_dna'):
        print_brand_dna(response['brand_dna'])
    else:
        print("\n❌ Error: No brand DNA was extracted")

    # Also offer JSON export option
    # print(f"\n💾 To export as JSON, run:")
    # print(f"   python brand_dna.py {url} --json > brand_dna.json")
    # print(f"\n📋 Full debug logs saved to: {log_file}")


def main():
    """Main entry point for brand_dna CLI tool."""

    # Parse arguments
    if len(sys.argv) < 2:
        print("Usage: python brand_dna.py <URL>")
        print("\nExample:")
        print("  python brand_dna.py https://www.northerntrust.com")
        print("  python brand_dna.py https://www.apple.com")
        sys.exit(1)

    url = sys.argv[1]

    # Validate URL format
    if not url.startswith(('http://', 'https://')):
        print("❌ Error: URL must start with http:// or https://")
        print(f"   You provided: {url}")
        sys.exit(1)

    # Check for JSON export flag
    export_json = '--json' in sys.argv

    if export_json:
        # Run analysis and export as JSON
        async def export():
            # Create log file with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_file = f"brand_dna_analysis_{timestamp}.log"

            # Redirect all debug output to log file
            with redirect_stdout_to_file(log_file):
                agent = MarketingAgent()
                response = await agent.process_message(f"analyze {url}")

            # Export only the brand_dna as clean JSON to stdout
            if response.get('brand_dna'):
                print(json.dumps(response['brand_dna'], indent=2))
            else:
                print(json.dumps({"error": "Could not extract brand DNA"}, indent=2))

            # Log file info goes to stderr so it doesn't interfere with JSON output
            print(f"Debug logs saved to: {log_file}", file=sys.stderr)

        asyncio.run(export())
    else:
        # Run normal analysis with full output
        asyncio.run(analyze_brand(url))


if __name__ == "__main__":
    main()
