# Complete Migration Plan: fal.ai + muapi.ai → Microsoft Azure + Alternatives

**Goal**: Completely transition off fal.ai and muapi.ai to Microsoft Azure services and strategic alternatives

**Status**: Planning
**Started**: 2026-02-02
**Azure Account**: testeng1
**Container**: chdiaz-test

---

## Migration Overview

### Current Stack
- **fal.ai**: File hosting and uploads
- **muapi.ai**: AI generation services
  - GPT-5-Nano (text generation)
  - GPT-5-Nano Vision (image analysis)
  - Nano Banana (text-to-image)
  - Nano Banana Edit (reference-based image generation)
  - SeeDance Lite (text-to-video, image-to-video)

### Target Stack
- **Azure Blob Storage**: File hosting (replacing fal.ai)
- **Azure OpenAI Service**: Text & vision (replacing GPT-5-Nano)
- **Azure OpenAI DALL-E 3**: Image generation (replacing Nano Banana)
- **Stability AI / Replicate**: Reference-based image generation (replacing Nano Banana Edit)
- **Runway ML**: Video generation (replacing SeeDance Lite)

---

## PART A: FILE HOSTING MIGRATION (fal.ai → Azure Blob Storage)

### Phase A1: Azure Blob Storage Setup ✅

- [x] Create Azure account
- [x] Create Storage Account (testeng1)
- [x] Create Container (chdiaz-test)
- [x] Get connection string
- [x] Configure container public access level
- [x] Update api_secrets.py with credentials

### Phase A2: Python Environment

- [ ] Install Azure Blob Storage SDK
  ```bash
  pip install azure-storage-blob>=12.19.0
  ```

- [ ] Update requirements.txt
  - [ ] Add `azure-storage-blob>=12.19.0`
  - [ ] Mark `fal_client` for removal

### Phase A3: Code Implementation

- [ ] Create `AzureBlobUploader` class in adapters.py
  - [ ] `__init__()` with BlobServiceClient
  - [ ] `upload_file_async()` method
  - [ ] `_get_content_type()` helper
  - [ ] Error handling and logging

- [ ] Update `ensure_url()` function
  - [ ] Replace fal_client.upload_file_async() calls
  - [ ] Update format conversion logic (lines 71-73)
  - [ ] Update local file upload logic (line 96)

- [ ] Update `WebScrapingAdapter.capture_screenshot()`
  - [ ] Replace fal_client call (line 680)

### Phase A4: Testing & Cleanup

- [ ] Test file uploads
- [ ] Test format conversion (AVIF/WebP → PNG)
- [ ] Test screenshot uploads
- [ ] Remove fal_client dependency
- [ ] Remove FAL_KEY from api_secrets.py

---

## PART B: TEXT GENERATION MIGRATION (muapi GPT-5-Nano → Azure OpenAI)

### Phase B1: Azure OpenAI Setup

- [ ] Request Azure OpenAI Service access
  - [ ] Go to https://aka.ms/oai/access
  - [ ] Fill out application form
  - [ ] Wait for approval (can take 1-2 business days)

- [ ] Create Azure OpenAI resource
  - [ ] Navigate to Azure Portal
  - [ ] Create new "Azure OpenAI" resource
  - [ ] Choose region (e.g., East US)
  - [ ] Get endpoint URL and API key

- [ ] Deploy models in Azure OpenAI Studio
  - [ ] Deploy GPT-4o (for text generation)
  - [ ] Deploy GPT-4-Vision (for vision analysis)
  - [ ] Deploy DALL-E 3 (for image generation)
  - [ ] Note deployment names

- [ ] Update api_secrets.py
  ```python
  # Azure OpenAI
  AZURE_OPENAI_ENDPOINT = "https://your-resource.openai.azure.com"
  AZURE_OPENAI_API_KEY = "your_api_key_here"
  AZURE_OPENAI_API_VERSION = "2024-02-01"

  # Model deployment names
  AZURE_OPENAI_GPT4_DEPLOYMENT = "gpt-4o"
  AZURE_OPENAI_VISION_DEPLOYMENT = "gpt-4-vision"
  AZURE_OPENAI_DALLE_DEPLOYMENT = "dall-e-3"
  ```

### Phase B2: Python Environment

- [ ] Install OpenAI Python SDK
  ```bash
  pip install openai>=1.10.0
  ```

- [ ] Update requirements.txt
  - [ ] Add `openai>=1.10.0`

### Phase B3: Implement Azure OpenAI TextAdapter

- [ ] Create new `AzureTextAdapter` class
  - [ ] Initialize AzureOpenAI client
  - [ ] Implement `generate()` method
  - [ ] Map to Azure OpenAI chat completions
  - [ ] Handle streaming (optional)
  - [ ] Add retry logic

- [ ] Test Azure TextAdapter
  - [ ] Single prompt generation
  - [ ] Multiple variants (n>1)
  - [ ] Compare output quality with muapi

- [ ] Replace muapi TextAdapter usage
  - [ ] Update instantiation in marketing_agent_core.py
  - [ ] Update campaign_generator.py
  - [ ] Update variation_generator.py

### Phase B4: Implement Azure OpenAI VisionAdapter

- [ ] Create new `AzureVisionAdapter` class
  - [ ] Initialize AzureOpenAI client
  - [ ] Implement `analyze()` method
  - [ ] Support image URL input
  - [ ] Parse JSON responses
  - [ ] Handle vision-specific errors

- [ ] Test Azure VisionAdapter
  - [ ] Screenshot analysis
  - [ ] Brand DNA extraction
  - [ ] Logo detection
  - [ ] Compare accuracy with muapi

- [ ] Replace muapi VisionAdapter usage
  - [ ] Update brand_analyzer.py
  - [ ] Update any vision analysis workflows

---

## PART C: IMAGE GENERATION MIGRATION (muapi Nano Banana → Azure DALL-E 3)

### Phase C1: Implement Azure DALL-E 3 Adapter

- [ ] Create `AzureImageAdapter` class
  - [ ] Initialize AzureOpenAI client
  - [ ] Implement `generate_image()` method
  - [ ] Support size parameters (1024x1024, 1792x1024, 1024x1792)
  - [ ] Handle quality settings (standard, hd)
  - [ ] Add retry logic
  - [ ] Download and upload to Azure Blob Storage

- [ ] Test Azure DALL-E 3
  - [ ] Text-to-image generation
  - [ ] Multiple sizes
  - [ ] Quality comparison with Nano Banana
  - [ ] Speed comparison

### Phase C2: Handle Reference-Based Generation

**Problem**: DALL-E 3 does NOT support reference images (no logo integration)

**Solution Options**:

#### Option 1: Use Stability AI for Reference-Based
- [ ] Sign up for Stability AI API (https://platform.stability.ai)
- [ ] Get API key
- [ ] Add to api_secrets.py:
  ```python
  STABILITY_AI_API_KEY = "your_stability_key_here"
  ```

- [ ] Install SDK
  ```bash
  pip install stability-sdk
  ```

- [ ] Implement `StabilityImageAdapter`
  - [ ] `generate_with_reference()` using ControlNet
  - [ ] Logo integration via IP-Adapter
  - [ ] Handle aspect ratios

#### Option 2: Use Replicate for Reference-Based
- [ ] Sign up for Replicate (https://replicate.com)
- [ ] Get API token
- [ ] Add to api_secrets.py:
  ```python
  REPLICATE_API_TOKEN = "your_replicate_token_here"
  ```

- [ ] Install SDK
  ```bash
  pip install replicate
  ```

- [ ] Implement `ReplicateImageAdapter`
  - [ ] Use SDXL with ControlNet
  - [ ] Use Flux with IP-Adapter
  - [ ] `generate_with_reference()` method

#### Option 3: Hybrid Approach (Recommended)
- [ ] **DALL-E 3** for text-only generation (high quality)
- [ ] **Stability AI or Replicate** for reference-based generation
- [ ] Smart routing in `generate_image()`
  ```python
  if reference_image_url:
      # Use Stability/Replicate for reference-based
      return stability_adapter.generate_with_reference(...)
  else:
      # Use DALL-E 3 for text-only
      return azure_dalle_adapter.generate_image(...)
  ```

### Phase C3: Update Image Generation Logic

- [ ] Create unified `ImageAdapter` class
  - [ ] Routes to DALL-E 3 or Stability/Replicate
  - [ ] Maintains same interface as muapi adapter
  - [ ] Handles errors from both services

- [ ] Update `generate_image()` calls throughout codebase
- [ ] Test with logo integration workflows
- [ ] Test without reference images

### Phase C4: Handle Image Editing

**Problem**: Nano Banana Edit provided image editing

**Solutions**:
- [ ] **DALL-E 3 Edit** (if available in Azure)
- [ ] **Stability AI Edit** (Stable Diffusion Inpainting)
- [ ] **Replicate Models** (various editing models)

- [ ] Implement `edit_image()` method
  - [ ] Choose appropriate backend
  - [ ] Maintain API compatibility
  - [ ] Test editing workflows

---

## PART D: VIDEO GENERATION MIGRATION (muapi SeeDance Lite → Runway ML)

### Phase D1: Choose Video Generation Service

**Options**:
1. **Runway ML** (Recommended)
   - Gen-3 Alpha model
   - High quality T2V and I2V
   - Professional results
   - ~$0.05 per second of video

2. **Stability AI Video**
   - Stable Video Diffusion
   - Open source
   - More affordable
   - Lower quality than Runway

3. **Replicate**
   - Access to multiple video models
   - Pay-per-use
   - Good for experimentation

### Phase D2: Setup Runway ML

- [ ] Sign up for Runway ML (https://runwayml.com)
- [ ] Get API key from https://app.runwayml.com/settings/api
- [ ] Add to api_secrets.py:
  ```python
  RUNWAY_API_TOKEN = "your_runway_token_here"
  ```

- [ ] Install HTTP client (already have httpx)

### Phase D3: Implement Runway VideoAdapter

- [ ] Create `RunwayVideoAdapter` class
  - [ ] Initialize with API token
  - [ ] Implement `render()` method (T2V + I2V)
  - [ ] Implement `_generate_t2v()`
  - [ ] Implement `_generate_i2v()`
  - [ ] Handle async polling
  - [ ] Download and upload to Azure Blob

- [ ] Test video generation
  - [ ] Text-to-video
  - [ ] Image-to-video
  - [ ] Various durations
  - [ ] Quality comparison with SeeDance Lite

### Phase D4: Alternative: Stability AI Video

- [ ] Sign up for Stability AI (if not already done)
- [ ] Implement `StabilityVideoAdapter`
  - [ ] Use Stable Video Diffusion model
  - [ ] Handle I2V generation
  - [ ] Poll for results

- [ ] Compare quality and cost with Runway

### Phase D5: Update Video Generation Logic

- [ ] Replace `VideoAdapter` with new implementation
- [ ] Update all video generation calls
- [ ] Test campaign video generation
- [ ] Verify video ads workflow

---

## PART E: INTEGRATION & TESTING

### Phase E1: Update Adapter Initialization

- [ ] Update adapters.py to use new adapters
  ```python
  # Old
  text_adapter = TextAdapter()
  vision_adapter = VisionAdapter()
  image_adapter = ImageAdapter()
  video_adapter = VideoAdapter()

  # New
  text_adapter = AzureTextAdapter()
  vision_adapter = AzureVisionAdapter()
  image_adapter = HybridImageAdapter()  # Routes to Azure/Stability
  video_adapter = RunwayVideoAdapter()
  ```

- [ ] Update environment variable setup
- [ ] Remove muapi API key checks
- [ ] Add Azure/Runway checks

### Phase E2: Update All Adapter Usage

- [ ] Search for adapter instantiation
  ```bash
  grep -r "TextAdapter()" --include="*.py"
  grep -r "VisionAdapter()" --include="*.py"
  grep -r "ImageAdapter()" --include="*.py"
  grep -r "VideoAdapter()" --include="*.py"
  ```

- [ ] Update marketing_agent_core.py
- [ ] Update brand_analyzer.py
- [ ] Update campaign_generator.py
- [ ] Update variation_generator.py
- [ ] Update cli_marketing.py

### Phase E3: Comprehensive Testing

#### Unit Tests
- [ ] Test Azure Blob Storage upload
- [ ] Test Azure OpenAI text generation
- [ ] Test Azure OpenAI vision analysis
- [ ] Test DALL-E 3 image generation
- [ ] Test Stability/Replicate reference generation
- [ ] Test Runway video generation

#### Integration Tests
- [ ] Test brand DNA extraction end-to-end
- [ ] Test campaign generation
- [ ] Test asset creation with logo
- [ ] Test asset creation without logo
- [ ] Test video ad creation
- [ ] Test multi-asset generation

#### Performance Tests
- [ ] Compare text generation speed
- [ ] Compare image generation speed
- [ ] Compare video generation speed
- [ ] Compare costs
- [ ] Measure upload speeds

#### Quality Tests
- [ ] Compare text quality
- [ ] Compare image quality
- [ ] Compare logo integration quality
- [ ] Compare video quality
- [ ] User acceptance testing

### Phase E4: Error Handling & Resilience

- [ ] Add retry logic for all services
- [ ] Handle rate limits gracefully
- [ ] Add fallback mechanisms
- [ ] Improve error messages
- [ ] Add logging for debugging

---

## PART F: CLEANUP & DEPRECATION

### Phase F1: Remove muapi.ai Code

- [ ] Remove muapi adapters
  - [ ] Remove old `TextAdapter` class
  - [ ] Remove old `VisionAdapter` class
  - [ ] Remove old `ImageAdapter` class
  - [ ] Remove old `VideoAdapter` class

- [ ] Remove muapi imports and dependencies
  - [ ] Remove from requirements.txt
  - [ ] Clean up imports in adapters.py

- [ ] Remove MUAPIAPP_API_KEY
  - [ ] From api_secrets.py
  - [ ] From api_secrets.example.py
  - [ ] From environment checks

### Phase F2: Remove fal.ai Code

- [ ] Remove fal_client import
- [ ] Remove all fal_client calls
- [ ] Remove FAL_KEY from api_secrets.py
- [ ] Remove from requirements.txt

### Phase F3: Code Organization

- [ ] Organize adapters by service
  ```
  adapters/
    __init__.py
    azure_text.py
    azure_vision.py
    azure_image.py
    stability_image.py
    runway_video.py
    azure_blob.py
    web_scraping.py
  ```

- [ ] Update imports throughout codebase
- [ ] Add adapter factory pattern
- [ ] Improve code documentation

---

## PART G: DOCUMENTATION UPDATES

### Phase G1: Update README.md

- [ ] Replace muapi.ai references with Azure OpenAI
- [ ] Add Azure OpenAI setup instructions
- [ ] Add Runway ML setup instructions
- [ ] Add Stability AI setup (optional)
- [ ] Update architecture diagram
- [ ] Update cost estimates
- [ ] Update comparison table
- [ ] Update API Tools section

### Phase G2: Update Configuration Files

- [ ] Update api_secrets.example.py with new keys
- [ ] Update requirements.txt
- [ ] Create SETUP.md with detailed setup steps
- [ ] Update CONTRIBUTING.md

### Phase G3: Update Migration Docs

- [ ] Create MIGRATION.md guide
- [ ] Document breaking changes
- [ ] Provide migration script (optional)
- [ ] Add troubleshooting section

### Phase G4: Update Security Docs

- [ ] Update SECURITY.md
- [ ] Document new API key management
- [ ] Add Azure security best practices
- [ ] Document key rotation procedures

---

## PART H: COST ANALYSIS & OPTIMIZATION

### Phase H1: Calculate New Costs

**Azure Blob Storage**:
- Storage: $0.018/GB/month
- Operations: $0.05/10k writes
- **Estimated**: ~$10/month

**Azure OpenAI Service**:
- GPT-4o: $2.50/1M input, $10/1M output tokens
- GPT-4 Vision: $10/1M input, $30/1M output tokens
- DALL-E 3: $0.04/image (standard), $0.08/image (HD)
- **Estimated**: ~$50-200/month (varies by usage)

**Stability AI** (optional):
- SDXL: $0.002-0.008 per image
- ControlNet: $0.008 per image
- **Estimated**: ~$10-30/month

**Runway ML**:
- Gen-3 Alpha: $0.05/second
- 5-second video: $0.25 each
- **Estimated**: ~$25-100/month (10-40 videos)

**Total Monthly Cost**: $95-340/month

Compare with muapi.ai costs:
- [ ] Document current muapi spending
- [ ] Calculate cost difference
- [ ] Identify optimization opportunities

### Phase H2: Cost Optimization

- [ ] Use GPT-4o-mini for simple tasks
- [ ] Cache common responses
- [ ] Optimize prompt lengths
- [ ] Use standard quality for DALL-E 3
- [ ] Batch operations where possible
- [ ] Set budget alerts in Azure

---

## PART I: DEPLOYMENT & MONITORING

### Phase I1: Staging Deployment

- [ ] Create staging environment
- [ ] Deploy new adapters to staging
- [ ] Run full test suite
- [ ] Performance testing
- [ ] Load testing
- [ ] User acceptance testing

### Phase I2: Production Deployment

- [ ] Create deployment plan
- [ ] Schedule maintenance window
- [ ] Deploy to production
- [ ] Monitor error rates
- [ ] Monitor performance
- [ ] Monitor costs

### Phase I3: Monitoring Setup

- [ ] Add Azure Monitor integration
- [ ] Track API latencies
- [ ] Track error rates
- [ ] Track costs per service
- [ ] Set up alerts for failures
- [ ] Create dashboard for metrics

### Phase I4: Rollback Procedures

- [ ] Document rollback steps
- [ ] Keep old adapters in separate branch
- [ ] Create feature flags for adapter selection
- [ ] Test rollback in staging

---

## PART J: OPTIONAL ENHANCEMENTS

### Phase J1: Advanced Features

- [ ] Implement prompt caching
- [ ] Add response streaming for text
- [ ] Implement batch generation
- [ ] Add A/B testing for models
- [ ] Implement model fallbacks

### Phase J2: Performance Optimization

- [ ] Parallelize independent operations
- [ ] Optimize image upload pipeline
- [ ] Add CDN for blob storage
- [ ] Implement lazy loading
- [ ] Add result caching

### Phase J3: Future Considerations

- [ ] Evaluate Azure Computer Vision for brand analysis
- [ ] Consider fine-tuning GPT-4 on brand data
- [ ] Explore Azure Video Indexer
- [ ] Research emerging video generation services
- [ ] Plan for model upgrades (GPT-5, etc.)

---

## SUCCESS CRITERIA

### Critical Requirements
- [x] Azure account and resources configured
- [ ] All adapters successfully migrated
- [ ] Zero muapi.ai dependencies
- [ ] Zero fal.ai dependencies
- [ ] All tests passing
- [ ] Documentation complete
- [ ] Production deployment successful

### Quality Requirements
- [ ] Text generation quality maintained or improved
- [ ] Image generation quality acceptable
- [ ] Logo integration working correctly
- [ ] Video generation quality acceptable
- [ ] No significant performance regression

### Business Requirements
- [ ] Cost within budget ($100-400/month target)
- [ ] Latency within acceptable range
- [ ] Reliability ≥99.9%
- [ ] Team trained on new stack

---

## RISKS & MITIGATIONS

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Azure OpenAI access denied | High | Low | Apply early, have Anthropic API as backup |
| Reference-based generation quality poor | High | Medium | Test Stability AI + Replicate, optimize prompts |
| Video quality degradation | Medium | Medium | Test Runway extensively, consider Stability |
| Cost overruns | Medium | Medium | Set budget alerts, optimize usage |
| Performance regression | Medium | Low | Benchmark before migration, optimize |
| DALL-E 3 content policy rejections | Medium | Medium | Implement retry with prompt rewording |

---

## TIMELINE ESTIMATE

**Total Estimated Time**: 2-3 weeks

- **Week 1**: Parts A-C (Blob, Text, Vision, Image)
  - Days 1-2: Azure setup, blob storage
  - Days 3-4: Text & vision adapters
  - Days 5-7: Image generation + testing

- **Week 2**: Parts D-F (Video, Integration, Cleanup)
  - Days 1-2: Video adapter
  - Days 3-4: Integration & testing
  - Days 5: Cleanup & deprecation

- **Week 3**: Parts G-I (Docs, Deployment)
  - Days 1-2: Documentation
  - Days 3-4: Staging & production deployment
  - Day 5: Monitoring & optimization

---

## CURRENT STATUS

**Completed** ✅:
- Azure account created
- Blob storage container created
- API secrets configured

**In Progress** 🔄:
- Planning migration strategy

**Blocked** ⛔:
- Azure OpenAI access (need to apply)

**Next Steps**:
1. Apply for Azure OpenAI access
2. Install Azure SDKs
3. Implement Azure Blob Storage uploader
4. Begin adapter migrations

---

## NOTES & DECISIONS

### Decision Log

**2026-02-02**:
- ✅ Decided to use Azure OpenAI for text/vision
- ✅ Decided to use DALL-E 3 + Stability AI hybrid for images
- ✅ Decided to use Runway ML for video generation
- ⏳ Need to decide: Stability AI vs Replicate for reference images
- ⏳ Need to evaluate: Cost vs quality tradeoffs

### Questions to Resolve
- [ ] Stability AI or Replicate for reference-based generation?
- [ ] Keep muapi as fallback or full removal?
- [ ] Implement adapter factory pattern?
- [ ] Use Azure AI Foundry or direct Azure OpenAI?

---

**Last Updated**: 2026-02-02
**Owner**: chdiaz
**Priority**: High
**Complexity**: High
