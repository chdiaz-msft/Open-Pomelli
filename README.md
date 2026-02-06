# Marketing Agent - AI Marketing Department in a Box

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**Inspired by Google's Pomelli**

An AI-powered marketing agent that helps small and medium businesses create on-brand marketing campaigns. Analyzes your brand, suggests campaigns, and generates professional marketing assets with intelligent reference-based generation.

## 🎯 What is This?

This is an open-source implementation similar to **Google's Pomelli** - an AI marketing tool that acts as a "marketing department in a box" for SMBs. It helps you:

1. **Understand Your Brand** - Deep analysis using Vision AI and web scraping to extract comprehensive "Brand DNA"
2. **Generate Campaign Ideas** - Suggests tailored marketing campaigns based on your brand identity
3. **Create On-Brand Assets** - Generates social posts, banners, ads with automatic logo integration
4. **Maintain Consistency** - All assets match your brand identity through reference-based generation

## ✨ Key Features

### 1. **Advanced Brand DNA Analysis**
   - **🎨 Visual Analysis**: 
     - Captures website screenshots using Playwright
     - Analyzes with Vision AI to extract colors, fonts, and layout patterns
     - Identifies logo and brand imagery automatically
   - **📝 Content Analysis**: 
     - Renders JavaScript-heavy sites for complete content extraction
     - Extracts messaging, tone of voice, and brand personality
     - Identifies target audience and value proposition
   - **🔗 Asset Extraction**:
     - Automatically finds and extracts logos (OpenGraph, icons, logo images)
     - Discovers brand guidelines and media kit links
     - Collects high-quality brand images
   - **🧬 Synthesis**: 
     - Combines visual and textual data for complete brand profile
     - Structured Brand DNA with colors, fonts, imagery style, and messaging

### 2. **Reference-Based Image Generation**
   - **🎯 Automatic Logo Integration**: 
     - Auto-detects brand logo from website analysis
     - Intelligently uses logo as reference for all generated assets
     - Ensures brand consistency across all marketing materials
   - **🖼️ Smart Image Format Handling**:
     - Automatically converts unsupported formats (AVIF, WebP, SVG) to PNG
     - Downloads, converts, and re-uploads for API compatibility
     - Seamless handling of any image format
   - **✨ Reference Image Support**:
     - Use ANY image as reference (products, previous designs, brand elements)
     - Explicit `reference_image_url` parameter for custom references
     - Powered by Nano Banana Edit for high-quality results

### 3. Brand DNA Analysis
- **Comprehensive Website Analysis**:
  - Brand identity (tone of voice, personality, language)
  - Visual style (colors, fonts, imagery, layout)
  - Logo detection and analysis
  - Target audience identification
  - Value proposition extraction
  - Key products/services discovery
  - Brand guidelines and media kit links

### 4. **Campaign Idea Generation**
Suggests tailored campaigns for:
- **Product Launch** - Introduce new products/services with on-brand visuals
- **Brand Awareness** - Increase visibility with consistent brand assets
- **Lead Generation** - Capture potential customers with compelling creatives
- **Engagement** - Build community with interactive content
- **Sales/Promotion** - Drive purchases with promotional graphics
- **Thought Leadership** - Establish expertise with professional content

### 5. **On-Brand Asset Creation**
Generates marketing materials for:
- **Social Media** - Instagram, LinkedIn, Facebook, Twitter posts with logo integration
- **Web** - Banners, hero images, graphics using brand colors and style
- **Ads** - Display ads, video ads with brand consistency
- **Email** - Headers, graphics matching your brand identity
- **Copy** - Taglines, subject lines, captions in your brand voice

### 6. **Multi-Channel Support**
Platform-specific content optimization:
- **Instagram**: Visual and engaging (2200 chars, 30 hashtags)
- **LinkedIn**: Professional and insightful (3000 chars, 5 hashtags)
- **Twitter**: Concise and punchy (280 chars, 2 hashtags)
- **Facebook**: Conversational and friendly (unlimited, 3 hashtags)

## 🆕 Recent Updates & Improvements

### Version 2.0 - Enhanced Brand Intelligence (December 2024)

**🎨 Advanced Brand DNA Analysis**
- Integrated **Playwright** for JavaScript-rendered website scraping
- Added **Vision AI** screenshot analysis for visual brand elements
- Implemented multi-source **logo detection** (OpenGraph, icons, image analysis)
- Enhanced **DOM evaluation** for accurate color and font extraction
- Added **brand guidelines discovery** from website links

**🖼️ Reference-Based Image Generation**
- **Automatic logo integration** - Detects and uses brand logo as reference
- **Smart format conversion** - Converts AVIF, WebP, SVG to PNG automatically
- **Explicit reference support** - Pass any image URL for custom references
- **Dual generation modes** - Nano Banana Edit (with reference) + Nano Banana (text-only)

**🔧 Technical Improvements**
- New `BrandAnalyzer` class for comprehensive brand analysis
- Enhanced `ensure_url()` utility with format conversion
- Improved error handling and logging throughout
- Better asset extraction and organization
- Structured Brand DNA v2 format with richer metadata

**📦 Dependencies**
- Added `Pillow` for image format conversion
- Added `playwright` for advanced web scraping
- Added `beautifulsoup4` for HTML parsing
- All adapters now support async operations

## 🚀 Quick Start

### Installation

1. **Navigate to the marketing_agent directory**:
```bash
cd marketing_agent
```

2. **Install Python dependencies**:
```bash
pip install -r requirements.txt
```

Required packages:
- `aiohttp` - Async HTTP client
- `httpx` - HTTP client for API calls
- `fal_client` - File upload service
- `playwright` - Browser automation for web scraping
- `beautifulsoup4` - HTML parsing
- `Pillow` - Image processing and format conversion

3. **Install Playwright browsers**:
```bash
playwright install
```

4. **Install Playwright system dependencies** (Linux/WSL only):
```bash
playwright install-deps chromium
```

Or install manually:
```bash
sudo apt-get update
sudo apt-get install -y libasound2 libatk-bridge2.0-0 libatk1.0-0 \
  libatspi2.0-0 libcairo2 libcups2 libdbus-1-3 libdrm2 libgbm1 \
  libglib2.0-0 libgtk-3-0 libnspr4 libnss3 libpango-1.0-0 \
  libx11-6 libxcb1 libxcomposite1 libxdamage1 libxext6 libxfixes3 \
  libxkbcommon0 libxrandr2 xvfb
```

> **Note**: This step is only required on Linux/WSL. macOS and Windows users can skip this.

5. **Set up API keys** in `api_secrets.py`:
```python
MUAPIAPP_API_KEY = "your_muapi_key_here"
FAL_KEY = "your_fal_key_here"
```

### Usage

Run the CLI:
```bash
python cli_marketing.py
```

## 📖 Example Workflow

### Step 1: Analyze Your Brand
```
You: Create a marketing campaign for https://mycompany.com

Agent: I'm analyzing your website to understand your brand identity...

Brand DNA Extracted:
  Brand: MyCompany
  Industry: Technology
  Tone: Professional, Innovative, Friendly
  Colors: #0066CC, #FFFFFF, #00CC66
  Target Audience: Tech-savvy professionals aged 25-45
```

### Step 2: Define Your Goal
```
Agent: What's your marketing goal for this campaign?
  1. Increase brand awareness
  2. Generate leads
  3. Drive sales
  4. Build engagement

You: Generate leads
```

### Step 3: Choose a Campaign
```
Agent: Here are 3 lead generation campaigns for you:

Campaign 1: Free Tool Giveaway
- Offer a free calculator/template
- Capture emails for download
- Follow-up nurture sequence

Campaign 2: Webinar Series
- Educational content on industry topics
- Registration required
- Post-webinar consultation offers

Campaign 3: Case Study Showcase
- Highlight customer success stories
- Downloadable PDF with email gate
- Social proof for credibility

Which campaign resonates with you?

You: Campaign 1
```

### Step 4: Get Your Assets
```
Agent: Creating your campaign assets...

Generated Assets:
  1. LinkedIn Post: https://...
  2. Instagram Post: https://...
  3. Web Banner: https://...
  4. Email Header: https://...

Copy Variants:
  1. Get Your Free Productivity Calculator - No Credit Card Required
  2. Boost Your Efficiency with Our Free Tool
  3. Limited Time: Free Calculator for Professionals

What would you like to adjust?
```

## 🛠️ Technical Architecture

### Core Components

1. **MarketingAgent** (`marketing_agent_core.py`)
   - Main agent orchestrator with multi-turn reasoning
   - Tool execution engine with smart decision-making
   - State management for brand DNA and campaigns
   - Auto-detects and uses brand logo for all generations

2. **BrandAnalyzer** (`brand_analyzer.py`) - **NEW**
   - **Visual Analysis**: Screenshot capture + Vision AI analysis
   - **Text Analysis**: Deep content extraction and synthesis
   - **Logo Detection**: Multi-source logo discovery (OG, icons, images)
   - **Asset Extraction**: Colors, fonts, images, guidelines
   - **Smart Synthesis**: Combines all data into comprehensive Brand DNA

3. **Adapters** (`adapters.py`)
   - **TextAdapter** - LLM for strategy and copy (GPT-5-Nano)
   - **ImageAdapter** - Visual asset generation with reference support
     - `generate_image()` - Text-to-image (Nano Banana)
     - `generate_with_reference()` - Reference-based generation (Nano Banana Edit)
     - `edit_image()` - Image editing and manipulation
     - **Auto format conversion** for AVIF, WebP, SVG → PNG
   - **VideoAdapter** - Video ad creation (SeeDance Lite T2V/I2V)
   - **VisionAdapter** - Image analysis and understanding (GPT-5-Nano Vision)
   - **WebScrapingAdapter** - Enhanced website analysis
     - Playwright-based rendering for JS-heavy sites
     - DOM evaluation for colors, fonts, images
     - Screenshot capture and upload
     - Asset discovery and extraction

4. **Campaign Generator** (`campaign_generator.py`)
   - Multi-asset campaign creation
   - Brand-consistent asset generation
   - Campaign strategy and planning

5. **Variation Generator** (`variation_generator.py`)
   - Design variation creation
   - A/B testing asset generation
   - Style and content variations

6. **CLI** (`cli_marketing.py`)
   - User interface for interaction
   - Conversation management
   - Asset display and feedback

### Workflow

```
User Input
    ↓
Extract Brand DNA (Playwright + Vision AI)
    ├─ Screenshot Analysis
    ├─ DOM Asset Extraction
    ├─ Logo Detection
    └─ Text Content Analysis
    ↓
Understand Marketing Goals
    ↓
Generate Campaign Ideas
    ↓
Create On-Brand Assets (with auto logo reference)
    ├─ Auto-detect logo from Brand DNA
    ├─ Convert formats if needed (AVIF/WebP/SVG → PNG)
    ├─ Generate with reference (Nano Banana Edit)
    └─ Ensure brand consistency
    ↓
Present to User & Iterate
```

## 🎨 Brand DNA Structure

The enhanced Brand DNA extraction provides a comprehensive profile:

```json
{
  "brand_name": "MyCompany",
  "industry": "Technology",
  "tagline": "Innovating the Future",
  "value_proposition": "Simplifying complex workflows with AI",
  
  "tone_of_voice": ["professional", "innovative", "friendly"],
  "brand_personality": ["trustworthy", "innovative", "customer-focused"],
  "brand_language": "Professional English",
  
  "visual_style": {
    "colors": ["#0066CC", "#FFFFFF", "#00CC66"],
    "primary_colors": ["#0066CC", "#FFFFFF"],
    "secondary_colors": ["#00CC66"],
    "typography": {
      "style": "modern sans-serif",
      "scraped_families": ["Inter", "Roboto", "Arial"]
    },
    "logo": {
      "url": "https://example.com/logo.png",
      "candidates": ["https://...", "https://..."],
      "analysis": {
        "style": "wordmark with icon",
        "colors": ["#0066CC"]
      }
    },
    "imagery_style": "Professional photography with tech elements",
    "layout_style": "Modern and minimalist"
  },
  
  "assets": {
    "logo_url": "https://example.com/logo.png",
    "images": ["https://...", "https://..."],
    "guidelines": [
      {"text": "Brand Guidelines", "href": "https://..."}
    ],
    "screenshot_url": "https://..."
  },
  
  "target_audience": "Tech-savvy professionals aged 25-45",
  "key_messages": ["Innovation", "Reliability", "Customer Success"],
  "brand_vibe": ["professional", "modern", "trustworthy"],
  
  "source_url": "https://example.com",
  "extracted_from": "automated_analysis_v2"
}
```

## 📊 Campaign Types

### Product Launch
- **Goal**: Introduce new product/service
- **Assets**: Product mockups, hero images, launch videos, social posts
- **Channels**: All platforms
- **Timeline**: 2-4 weeks pre-launch

### Brand Awareness
- **Goal**: Increase visibility and recognition
- **Assets**: Brand story content, thought leadership, social presence
- **Channels**: Social media, content marketing
- **Timeline**: Ongoing

### Lead Generation
- **Goal**: Capture potential customer information
- **Assets**: Gated content, webinar promotions, free tools
- **Channels**: LinkedIn, email, web
- **Timeline**: Campaign-based

### Engagement
- **Goal**: Build community and interaction
- **Assets**: Interactive content, polls, UGC campaigns
- **Channels**: Social media
- **Timeline**: Ongoing

### Sales/Promotion
- **Goal**: Drive immediate purchases
- **Assets**: Promotional graphics, discount codes, urgency messaging
- **Channels**: Email, social ads, web
- **Timeline**: Short-term (1-2 weeks)

### Thought Leadership
- **Goal**: Establish expertise and authority
- **Assets**: Educational content, case studies, whitepapers
- **Channels**: LinkedIn, blog, email
- **Timeline**: Long-term

## 🔧 API Tools

The agent can call these enhanced tools:

### Core Analysis
- `research_web(url)` - **Enhanced**: Analyze website with Playwright + Vision AI
  - Captures screenshot for visual analysis
  - Extracts colors, fonts, and layout patterns
  - Automatically detects and extracts logo
  - Discovers brand guidelines and assets

### Image Generation
- `generate_image(prompt, reference_image_url=None)` - **Enhanced**: Create marketing visuals
  - **Auto-detects logo**: Automatically uses brand logo as reference if available
  - **Reference support**: Pass any image URL as reference for brand consistency
  - **Format handling**: Automatically converts AVIF, WebP, SVG to PNG
  - **Smart generation**: Uses Nano Banana Edit for reference-based, Nano Banana for text-only
  - Example: `generate_image("Instagram post for product launch", reference_image_url="https://...")`

### Video Generation
- `generate_video(prompt, image_url=None, duration=5)` - Create video ads
  - Text-to-video or image-to-video
  - Supports local files and URLs
  - Powered by SeeDance Lite

### Content Generation
- `generate_copy(brief, num_variants)` - Generate marketing copy and taglines
- `generate_social_post(platform, campaign)` - Platform-specific posts
- `generate_ad_creative(ad_type, campaign)` - Ad creatives

### Campaign Tools
- `generate_full_campaign(campaign_type, brief)` - Complete multi-asset campaign
- `generate_variations(base_prompt, asset_type, num_variations, strategy)` - Design variations

## 📈 Comparison with Google's Pomelli

| Feature | Google Pomelli | This Agent | Status |
|---------|---------------|------------|--------|
| Brand DNA Analysis | ✅ | ✅ | **Enhanced** with Vision AI |
| Logo Auto-Detection | ✅ | ✅ | **Implemented** |
| Reference-Based Generation | ✅ | ✅ | **Implemented** |
| Screenshot Analysis | ✅ | ✅ | **Implemented** |
| Campaign Suggestions | ✅ | ✅ | Implemented |
| On-Brand Assets | ✅ | ✅ | **Enhanced** with auto logo |
| Social Media Posts | ✅ | ✅ | Implemented |
| Web Banners | ✅ | ✅ | Implemented |
| Video Ads | ✅ | ✅ | Implemented |
| Copy Generation | ✅ | ✅ | Implemented |
| Multi-Channel | ✅ | ✅ | Implemented |
| Format Conversion | ❌ | ✅ | **Bonus Feature** |
| Editable Assets | ✅ | ⏳ | Future |
| Team Collaboration | ✅ | ⏳ | Future |
| Analytics Integration | ✅ | ⏳ | Future |

## 🎯 Use Cases

### Small Business Owner
"I need to promote my new coffee shop but don't have a marketing team."
- Agent analyzes your website
- Suggests a grand opening campaign
- Creates Instagram posts, Facebook ads, email graphics
- All match your cozy, artisanal brand

### Startup Founder
"We're launching a new SaaS product and need a lead gen campaign."
- Agent extracts your tech-forward brand DNA
- Suggests a free trial campaign
- Creates LinkedIn posts, web banners, email sequences
- Professional and conversion-focused

### Freelance Marketer
"I have 5 clients and need to create campaigns quickly."
- Agent learns each client's brand
- Generates campaign ideas for each
- Creates on-brand assets in minutes
- Maintains consistency across all clients

## 🚧 Limitations & Requirements

### Requirements
- Active internet connection for API calls
- Valid API keys (MUAPIAPP_API_KEY, FAL_KEY)
- Playwright browsers installed (`playwright install`)
- Playwright system dependencies (Linux/WSL: `playwright install-deps chromium`)
- Python 3.8+ recommended

### Current Limitations
- Generated assets may need human review/editing for final polish
- Brand DNA extraction quality depends on website structure and content
- Reference image generation works best with clear, high-quality logos
- Not a replacement for strategic marketing expertise
- Best suited for SMBs; may need customization for large enterprises
- Screenshot analysis requires headless browser support

### Known Issues
- Some websites with strong anti-bot protection (Cloudflare, etc.) may still block scraping despite stealth features
- Very complex websites may take longer to analyze
- Image format conversion adds slight processing time
- Linux/WSL users must install system dependencies (`playwright install-deps chromium`) for Playwright to work

## 🔜 Future Enhancements

### Planned Features
1. **Asset Editing** - In-app editing of generated assets with real-time preview
2. **Team Collaboration** - Multi-user support with role-based permissions
3. **Analytics Integration** - Track campaign performance and ROI metrics
4. **A/B Testing** - Automated variant testing with performance tracking
5. **Content Calendar** - Schedule and plan campaigns with timeline view
6. **Template Library** - Pre-built campaign templates for common use cases
7. **Export Formats** - Multiple file formats (PDF, PNG, MP4, SVG)
8. **Brand Guidelines Doc** - Auto-generate comprehensive brand books

### Potential Improvements
- **Multi-language support** for global brands
- **Video editing capabilities** for more control over video assets
- **Social media scheduling** integration
- **Performance optimization** for faster generation
- **Batch processing** for multiple campaigns
- **Custom model fine-tuning** on brand-specific data

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### What this means:
- ✅ Free to use for commercial and personal projects
- ✅ Modify and distribute as you wish
- ✅ No warranty or liability
- ✅ Must include original license and copyright notice

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Quick Start for Contributors:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add: amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Areas We Need Help:
- 🧪 Testing and bug reports
- 📚 Documentation improvements
- ✨ New features and enhancements
- 🎨 UI/UX improvements
- 🌍 Multi-language support

## 📞 Support & Community

- **Issues**: Report bugs or request features via [GitHub Issues](../../issues)
- **Discussions**: Ask questions in [GitHub Discussions](../../discussions)
- **Security**: Report security vulnerabilities privately

## 🙏 Acknowledgments

- Inspired by **Google's Pomelli** marketing AI
- Powered by **MuAPI** (GPT-5-Nano, Nano Banana, SeeDance Lite)
- Built with **Playwright**, **Pillow**, and other amazing open source tools

## 📊 Project Status

- **Version**: 2.0.0
- **Status**: Active Development
- **Last Updated**: December 2024

## 🔗 Links

- [Changelog](CHANGELOG.md) - Version history and updates
- [Contributing Guidelines](CONTRIBUTING.md) - How to contribute
- [License](LICENSE) - MIT License details

---

**Built with ❤️ for SMB Marketing Success**  
**Powered by AI • Open Source • Community Driven** 🚀
