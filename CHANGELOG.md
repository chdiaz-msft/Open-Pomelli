# Changelog

All notable changes to the Marketing Agent project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2024-12-12

### Added - Enhanced Brand Intelligence

#### Brand DNA Analysis
- **Playwright Integration**: Added browser automation for JavaScript-rendered website scraping
- **Vision AI Analysis**: Integrated GPT-5-Nano Vision for screenshot analysis
- **Multi-Source Logo Detection**: Automatically detects logos from OpenGraph, icons, and image analysis
- **DOM Evaluation**: Enhanced color and font extraction directly from computed styles
- **Brand Guidelines Discovery**: Automatically finds brand guideline and media kit links
- **BrandAnalyzer Class**: New comprehensive brand analysis component

#### Reference-Based Image Generation
- **Automatic Logo Integration**: Auto-detects and uses brand logo as reference for all assets
- **Smart Format Conversion**: Automatically converts AVIF, WebP, SVG to PNG for API compatibility
- **Explicit Reference Support**: Pass any image URL as reference via `reference_image_url` parameter
- **Dual Generation Modes**: Nano Banana Edit (with reference) + Nano Banana (text-only)
- **Enhanced ensure_url() Utility**: Handles format conversion and file uploads seamlessly

#### Technical Improvements
- **Structured Brand DNA v2**: Richer metadata including logo data, assets, and visual analysis
- **Enhanced Error Handling**: Better error messages and recovery throughout the codebase
- **Improved Logging**: More detailed logging for debugging and monitoring
- **Better Asset Organization**: Structured asset extraction and storage
- **Async Operations**: All adapters now fully support async operations

#### Dependencies
- Added `Pillow` (PIL) for image format conversion
- Added `playwright` for advanced web scraping and screenshot capture
- Added `beautifulsoup4` for HTML parsing and metadata extraction
- Updated all adapters to use async/await patterns

#### Documentation
- Comprehensive README update with all new features
- Added CONTRIBUTING.md for open source collaboration
- Added CHANGELOG.md for version tracking
- Added LICENSE (MIT) for open source distribution
- Added .gitignore for proper version control
- Added api_secrets.example.py for easy setup

### Changed
- Enhanced `ImageAdapter.generate_image()` to support reference images
- Improved `WebScrapingAdapter` with Playwright rendering
- Updated Brand DNA structure with richer metadata
- Refactored logo detection to check multiple sources
- Enhanced campaign generation with logo integration

### Fixed
- Image format compatibility issues with AVIF, WebP, SVG
- JavaScript-rendered website scraping issues
- Logo detection from various website structures
- Color and font extraction accuracy

## [1.0.0] - 2024-12-11

### Added - Initial Release

#### Core Features
- Marketing Agent orchestrator with multi-turn reasoning
- Basic Brand DNA extraction from websites
- Campaign idea generation for various marketing goals
- On-brand asset creation (images, videos, copy)
- Multi-channel support (Instagram, LinkedIn, Twitter, Facebook)
- Platform-specific content optimization

#### Components
- `MarketingAgent` - Main agent orchestrator
- `CampaignGenerator` - Campaign creation and management
- `VariationGenerator` - Asset variation generation
- Basic adapters for text, image, video, and vision

#### Tools
- `research_web()` - Basic website analysis
- `generate_image()` - Text-to-image generation
- `generate_video()` - Video ad creation
- `generate_copy()` - Marketing copy generation
- `generate_social_post()` - Platform-specific posts
- `generate_full_campaign()` - Multi-asset campaigns
- `generate_variations()` - Design variations

#### Documentation
- Initial README with project overview
- Installation instructions
- Usage examples
- API documentation

---

## Version History

- **2.0.0** (2024-12-12) - Enhanced Brand Intelligence with Vision AI and Reference-Based Generation
- **1.0.0** (2024-12-11) - Initial Release with Core Marketing Agent Features

## Upcoming Features

See [Future Enhancements](README.md#-future-enhancements) in README for planned features.
