#!/usr/bin/env python3
# brand_analyzer.py
"""
Enhanced Brand DNA Analyzer
Uses vision AI to analyze website screenshots and extract visual brand elements.
"""

import json
from typing import Dict, Any, List, Optional
import re
import sys
import os
from urllib.parse import urlparse

from adapters import VisionAdapter, WebScrapingAdapter, TextAdapter


class BrandAnalyzer:
    """
    Advanced brand DNA analyzer that combines:
    1. Website screenshot analysis (visual elements)
    2. Text content analysis (messaging, tone)
    3. CSS/HTML analysis (colors, fonts)
    """
    
    def __init__(self):
        self.vision_adapter = VisionAdapter()
        self.web_adapter = WebScrapingAdapter()
        self.text_adapter = TextAdapter()
    
    async def analyze_website(self, url: str) -> Dict[str, Any]:
        """
        Comprehensive website analysis to extract brand DNA.
        
        Args:
            url: Website URL to analyze
            
        Returns:
            Complete brand DNA with visual and textual elements
        """
        print(f"[BrandAnalyzer] 🔍 Analyzing {url}...")
        
        # Step 1: Fetch website content (text, HTML, assets)
        print(f"[BrandAnalyzer] Fetching website content and assets...")
        web_content = await self.web_adapter.fetch_url(url)
        assets = web_content.get('assets', {})
        
        # Step 2: Take screenshot and analyze visually
        print(f"[BrandAnalyzer] Capturing and analyzing visual elements...")
        visual_analysis = await self._analyze_visual_elements(url, assets)
        
        # Step 3: Extract text-based brand elements
        print(f"[BrandAnalyzer] Extracting brand messaging...")
        text_analysis = await self._analyze_text_content(web_content)
        
        # Step 4: Extract specific assets
        print(f"[BrandAnalyzer] Extracting specific brand assets...")
        brand_images = self._extract_brand_images(assets)
        brand_guidelines = self._extract_brand_guidelines(assets)
        logo_data = await self._extract_and_analyze_logo(assets, web_content, visual_analysis)
        
        # Step 5: Combine all analyses into comprehensive brand DNA
        print(f"[BrandAnalyzer] Synthesizing brand DNA...")
        brand_dna = await self._synthesize_brand_dna(
            url=url,
            visual_analysis=visual_analysis,
            text_analysis=text_analysis,
            web_content=web_content,
            brand_images=brand_images,
            brand_guidelines=brand_guidelines,
            logo_data=logo_data
        )

        # Step 6: Enrich brand DNA if extractors failed or returned incomplete data
        print(f"[BrandAnalyzer] Checking if enrichment is needed...")
        brand_dna = await self.enrich_brand_dna(brand_dna, url)

        print(f"[BrandAnalyzer] ✅ Brand DNA extracted for {brand_dna.get('brand_name', 'Unknown')}")

        return brand_dna
    
    async def _analyze_visual_elements(self, url: str, assets: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze website visually using screenshot and scraped assets.
        """
        
        # Capture screenshot using Playwright adapter
        print(f"[BrandAnalyzer] Capturing screenshot of {url}...")
        screenshot_url = await self.web_adapter.capture_screenshot(url)
        
        vision_analysis = {}
        if screenshot_url:
            # Prompt for vision analysis
            analysis_prompt = """Analyze this website screenshot and extract:

1. **Primary Colors**: List the main brand colors (hex codes)
2. **Secondary Colors**: Supporting colors
3. **Typography**: Font styles (serif, sans-serif, modern, classic)
4. **Logo Style**: Describe the logo (wordmark, icon, combination)
5. **Imagery Style**: Photography style (professional, casual, illustrated)
6. **Layout**: Design approach (modern, classic, minimalist)
7. **Overall Vibe**: Brand feeling (professional, playful, luxury)

Return as JSON."""
            
            try:
                print(f"[BrandAnalyzer] Analyzing screenshot with Vision AI...")
                vision_analysis = await self.vision_adapter.analyze(analysis_prompt, screenshot_url)
            except Exception as e:
                print(f"[BrandAnalyzer] Visual analysis error: {e}")

        # Merge with scraped assets
        scraped_colors = assets.get('colors', [])
        scraped_fonts = assets.get('fonts', [])
        
        # If vision failed, use scraped data as fallback or primary
        return {
            "vision_analysis": vision_analysis,
            "scraped_colors": scraped_colors,
            "scraped_fonts": scraped_fonts,
            "screenshot_url": screenshot_url
        }
    
    async def _analyze_text_content(self, web_content: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze text content to extract messaging, tone, and brand personality.
        """
        
        text = web_content.get('text', '')[:5000]  # Increased limit
        title = web_content.get('title', '')
        metadata = web_content.get('metadata', {})
        
        prompt = f"""Analyze this website content and extract brand messaging elements:

Title: {title}
Description: {metadata.get('description', '')}
Keywords: {metadata.get('keywords', '')}
Content Sample: {text}

Extract and return as JSON:
{{
  "brand_name": "string",
  "tagline": "string",
  "value_proposition": "string",
  "tone_of_voice": ["trait1", "trait2"],
  "brand_personality": ["trait1", "trait2"],
  "target_audience": "description",
  "key_messages": ["message1", "message2"],
  "industry": "string",
  "brand_language": "string (e.g., 'Professional English', 'Casual French')"
}}"""

        try:
            responses = await self.text_adapter.generate(prompt, n=1)
            response_text = responses[0]
            
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            
            analysis = json.loads(response_text)
            return analysis
            
        except Exception as e:
            print(f"[BrandAnalyzer] Text analysis error: {e}")
            return {
                "brand_name": title,
                "tone_of_voice": ["professional"],
                "brand_personality": ["trustworthy"],
                "industry": "general"
            }

    def _extract_brand_images(self, assets: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract high-quality brand images."""
        images = assets.get('images', [])
        # Sort by size (area) to find hero images
        sorted_images = sorted(images, key=lambda x: x['width'] * x['height'], reverse=True)
        return sorted_images[:10]  # Return top 10 largest images

    def _extract_brand_guidelines(self, assets: Dict[str, Any]) -> List[Dict[str, str]]:
        """Find links to brand guidelines or media kits."""
        links = assets.get('links', [])
        guideline_keywords = ['brand', 'media kit', 'press', 'style guide', 'logo', 'assets']
        
        found_links = []
        for link in links:
            text = link['text'].lower()
            href = link['href'].lower()
            if any(k in text or k in href for k in guideline_keywords):
                found_links.append(link)
        
        return found_links[:5]

    async def _extract_and_analyze_logo(self, assets: Dict[str, Any], web_content: Dict[str, Any], visual_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Find the best logo candidate and analyze it."""
        
        # 1. Check OpenGraph image (often a logo or hero)
        og_image = assets.get('og_image')
        
        # 2. Check icons
        icons = assets.get('icons', [])
        
        # 3. Check images with 'logo' in src/alt
        logo_images = [img['src'] for img in assets.get('images', []) 
                      if 'logo' in img['src'].lower() or 'logo' in img['alt'].lower()]
        
        # Pick best candidate
        logo_url = None
        if logo_images:
            logo_url = logo_images[0]
        elif og_image:
            logo_url = og_image
        elif icons:
            logo_url = icons[0]
            
        # Analyze if found
        logo_analysis = {}
        if logo_url:
            # Use vision analysis from screenshot if available, or analyze specific logo URL
            # For now, we'll rely on the screenshot analysis for style, but return the URL
            pass
            
        return {
            "url": logo_url,
            "candidates": logo_images + icons,
            "analysis": visual_analysis.get("vision_analysis", {}).get("logo", {})
        }

    async def _synthesize_brand_dna(
        self,
        url: str,
        visual_analysis: Dict[str, Any],
        text_analysis: Dict[str, Any],
        web_content: Dict[str, Any],
        brand_images: List[Dict[str, Any]],
        brand_guidelines: List[Dict[str, str]],
        logo_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Combine all analyses into comprehensive brand DNA.
        """
        
        vision_data = visual_analysis.get("vision_analysis", {})
        
        # Merge colors: Vision colors + Scraped colors
        vision_colors = vision_data.get("primary_colors", []) + vision_data.get("secondary_colors", [])
        scraped_colors = visual_analysis.get("scraped_colors", [])
        # Simple deduplication
        all_colors = list(set(vision_colors + scraped_colors))[:8]
        
        # Merge fonts
        vision_fonts = vision_data.get("typography", {})
        scraped_fonts = visual_analysis.get("scraped_fonts", [])
        
        brand_dna = {
            "brand_name": text_analysis.get("brand_name", web_content.get("title", "Brand")),
            "industry": text_analysis.get("industry", "General"),
            "tagline": text_analysis.get("tagline", ""),
            "value_proposition": text_analysis.get("value_proposition", ""),
            
            "tone_of_voice": text_analysis.get("tone_of_voice", ["professional"]),
            "brand_personality": text_analysis.get("brand_personality", ["trustworthy"]),
            "brand_language": text_analysis.get("brand_language", "English"),
            
            "visual_style": {
                "colors": all_colors,
                "primary_colors": all_colors[:2] if all_colors else [],
                "secondary_colors": all_colors[2:] if len(all_colors) > 2 else [],
                "typography": {
                    "style": vision_fonts.get("style", "modern"),
                    "scraped_families": scraped_fonts
                },
                "logo": logo_data,
                "imagery_style": vision_data.get("imagery_style", "professional"),
                "layout_style": vision_data.get("layout_style", "modern")
            },
            
            "assets": {
                "logo_url": logo_data.get("url"),
                "images": [img['src'] for img in brand_images],
                "guidelines": brand_guidelines,
                "screenshot_url": visual_analysis.get("screenshot_url")
            },
            
            "target_audience": text_analysis.get("target_audience", "General audience"),
            "key_messages": text_analysis.get("key_messages", []),
            "brand_vibe": vision_data.get("brand_vibe", ["professional"]),
            
            "source_url": url,
            "extracted_from": "automated_analysis_v2"
        }
        
        # Fallback colors
        if not brand_dna["visual_style"]["colors"]:
            brand_dna["visual_style"]["colors"] = self._get_default_colors(brand_dna["industry"])
            brand_dna["visual_style"]["primary_colors"] = brand_dna["visual_style"]["colors"][:2]
        
        return brand_dna

    async def enrich_brand_dna(self, brand_dna: Dict[str, Any], url: str) -> Dict[str, Any]:
        """
        Enrich brand_dna by using AI to fill missing or default values.

        This addresses cases where structural extraction fails but we can
        infer brand information from the URL, basic context, or AI reasoning.

        Args:
            brand_dna: Potentially incomplete brand DNA from extractors
            url: Source URL for context

        Returns:
            Enriched brand DNA with filled gaps
        """
        # Check which fields need enrichment
        needs_enrichment = self._check_if_needs_enrichment(brand_dna)

        if not needs_enrichment:
            print("[BrandAnalyzer] Brand DNA is complete, no enrichment needed")
            return brand_dna

        print("[BrandAnalyzer] Enriching incomplete brand DNA fields with AI...")

        # Build enrichment prompt
        prompt = f"""You are a brand analysis expert. Given a website URL and partial brand information, infer and complete the missing fields.

URL: {url}

Current Brand DNA (may have empty/default values):
{json.dumps(brand_dna, indent=2)}

Instructions:
1. Analyze the URL and any available context
2. Infer missing information based on:
   - Domain name and URL structure
   - Industry knowledge
   - Common brand patterns
3. For each empty or generic field, provide a reasonable inference
4. If truly uncertain, use "Unknown" rather than making up facts

Return ONLY the fields that need updating as JSON:
{{
  "brand_name": "inferred name from URL/context",
  "industry": "specific industry (not 'general' or 'General')",
  "tagline": "inferred or 'Unknown' if not inferrable",
  "value_proposition": "inferred or 'Unknown'",
  "tone_of_voice": ["inferred", "traits"],
  "brand_personality": ["inferred", "traits"],
  "target_audience": "inferred audience",
  "key_messages": ["inferred messages if any"]
}}

Only include fields that you can meaningfully improve. Be specific, not generic."""

        try:
            responses = await self.text_adapter.generate(prompt, n=1)
            response_text = responses[0]

            # Clean and parse JSON
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()

            enriched_fields = json.loads(response_text)

            # Merge enriched fields into brand_dna
            brand_dna_enriched = brand_dna.copy()
            for key, value in enriched_fields.items():
                # Only update if the enriched value is better than current
                if self._is_better_value(brand_dna.get(key), value):
                    brand_dna_enriched[key] = value
                    print(f"[BrandAnalyzer] Enriched field '{key}': {value}")

            # Mark as enriched
            brand_dna_enriched["enrichment_applied"] = True
            brand_dna_enriched["enrichment_method"] = "ai_inference"

            return brand_dna_enriched

        except json.JSONDecodeError as e:
            print(f"[BrandAnalyzer] Failed to parse AI enrichment response: {e}")
            # Fallback to basic URL parsing
            return self._basic_url_fallback_enrichment(brand_dna, url)
        except Exception as e:
            print(f"[BrandAnalyzer] Enrichment error: {e}")
            return self._basic_url_fallback_enrichment(brand_dna, url)

    def _check_if_needs_enrichment(self, brand_dna: Dict[str, Any]) -> bool:
        """Check if brand_dna has empty or generic default values."""
        empty_checks = [
            not brand_dna.get("brand_name") or brand_dna.get("brand_name") == "Brand",
            brand_dna.get("industry", "").lower() in ["general", ""],
            not brand_dna.get("tagline"),
            not brand_dna.get("value_proposition"),
            len(brand_dna.get("tone_of_voice", [])) <= 1,
            len(brand_dna.get("brand_personality", [])) <= 1
        ]
        return any(empty_checks)

    def _is_better_value(self, current_value: Any, new_value: Any) -> bool:
        """Determine if new_value is better than current_value."""
        # Empty/None check
        if not current_value and new_value:
            return True

        # String checks
        if isinstance(current_value, str):
            generic_values = ["general", "brand", "business", "unknown", "n/a"]
            if current_value.lower() in generic_values and new_value.lower() not in generic_values:
                return True
            if not current_value.strip() and new_value.strip():
                return True

        # List checks
        if isinstance(current_value, list):
            generic_list_items = ["professional", "trustworthy"]
            if len(current_value) <= 1 and len(new_value) > 1:
                return True
            if all(item.lower() in generic_list_items for item in current_value) and new_value:
                return True

        return False

    def _basic_url_fallback_enrichment(self, brand_dna: Dict[str, Any], url: str) -> Dict[str, Any]:
        """Fallback enrichment using simple URL parsing."""
        print("[BrandAnalyzer] Using fallback URL parsing for enrichment...")

        parsed = urlparse(url)
        domain = parsed.netloc.replace('www.', '')
        brand_name = domain.split('.')[0].title()

        brand_dna_copy = brand_dna.copy()

        # Extract brand name from domain
        if not brand_dna_copy.get("brand_name") or brand_dna_copy.get("brand_name") == "Brand":
            brand_dna_copy["brand_name"] = brand_name
            print(f"[BrandAnalyzer] Fallback: Extracted brand_name '{brand_name}' from URL")

        # Infer industry from TLD
        if brand_dna_copy.get("industry", "").lower() in ["general", ""]:
            tld = parsed.netloc.split('.')[-1]
            industry_map = {
                'edu': 'Education',
                'gov': 'Government',
                'org': 'Non-profit',
                'health': 'Healthcare',
                'bank': 'Finance',
                'shop': 'E-commerce',
                'tech': 'Technology',
                'io': 'Technology',
                'ai': 'Artificial Intelligence'
            }
            brand_dna_copy["industry"] = industry_map.get(tld, "Business Services")
            print(f"[BrandAnalyzer] Fallback: Inferred industry '{brand_dna_copy['industry']}' from TLD")

        brand_dna_copy["enrichment_applied"] = True
        brand_dna_copy["enrichment_method"] = "url_parsing_fallback"

        return brand_dna_copy

    def _get_default_colors(self, industry: str) -> List[str]:
        """Get default color palette based on industry."""
        industry_colors = {
            "technology": ["#0066CC", "#FFFFFF", "#00CC66"],
            "finance": ["#003366", "#FFFFFF", "#FFD700"],
            "healthcare": ["#0099CC", "#FFFFFF", "#00CC99"],
            "food": ["#FF6B35", "#FFFFFF", "#FFA500"],
            "fashion": ["#000000", "#FFFFFF", "#FF1493"],
            "education": ["#4169E1", "#FFFFFF", "#FFD700"],
            "real_estate": ["#2C5F2D", "#FFFFFF", "#DAA520"],
            "entertainment": ["#FF0000", "#FFFFFF", "#FFD700"],
        }
        return industry_colors.get(industry.lower(), ["#0066CC", "#FFFFFF", "#00CC66"])

    # Removed old extract_logo and analyze_logo as they are now integrated

