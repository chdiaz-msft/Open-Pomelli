# API Secrets Configuration
# Copy this file to api_secrets.py and add your actual API keys

# ===================================================================
# LEGACY KEYS (Being phased out - see FULL_MIGRATION_CHECKLIST.md)
# ===================================================================

# MuAPI Key - LEGACY - Being replaced by Azure OpenAI
# Get yours at https://muapi.ai
MUAPIAPP_API_KEY = "your_muapi_key_here"

# FAL Key - LEGACY - Being replaced by Azure Blob Storage
# Get yours at https://fal.ai
FAL_KEY = "your_fal_key_here"

# ===================================================================
# NEW: AZURE SERVICES (Primary)
# ===================================================================

# Azure Blob Storage - File hosting and uploads
# Get from: Azure Portal > Storage Account > Access Keys
AZURE_STORAGE_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=YOUR_ACCOUNT;AccountKey=YOUR_KEY;EndpointSuffix=core.windows.net"
AZURE_STORAGE_CONTAINER_NAME = "marketing-assets"

# Alternative: Use Account Name + Key separately
AZURE_STORAGE_ACCOUNT_NAME = "your_storage_account_name"
AZURE_STORAGE_ACCOUNT_KEY = "your_storage_account_key"

# Azure OpenAI Service - Text, Vision, Image Generation
# Get from: Azure Portal > Azure OpenAI > Keys and Endpoint
AZURE_OPENAI_ENDPOINT = "https://your-resource.openai.azure.com"
AZURE_OPENAI_API_KEY = "your_azure_openai_api_key_here"
AZURE_OPENAI_API_VERSION = "2024-02-01"

# Azure OpenAI Model Deployments
# Set these to match your deployment names in Azure OpenAI Studio
AZURE_OPENAI_GPT4_DEPLOYMENT = "gpt-4o"              # Text generation
AZURE_OPENAI_VISION_DEPLOYMENT = "gpt-4-vision"      # Vision analysis
AZURE_OPENAI_DALLE_DEPLOYMENT = "dall-e-3"           # Image generation

# ===================================================================
# NEW: ALTERNATIVE SERVICES (For capabilities not in Azure)
# ===================================================================

# Stability AI - Reference-based image generation (logo integration)
# Get yours at https://platform.stability.ai
# OPTIONAL: Only needed if using Stability AI instead of Replicate
STABILITY_AI_API_KEY = "your_stability_key_here"

# Replicate - Reference-based image generation alternative
# Get yours at https://replicate.com/account/api-tokens
# OPTIONAL: Only needed if using Replicate instead of Stability AI
REPLICATE_API_TOKEN = "your_replicate_token_here"

# Runway ML - Video generation (T2V, I2V)
# Get yours at https://app.runwayml.com/settings/api
RUNWAY_API_TOKEN = "your_runway_token_here"

# ===================================================================
# CONFIGURATION OPTIONS
# ===================================================================

# Choose image generation strategy for reference-based generation:
# Options: "stability", "replicate", "azure_only"
# "stability" = Use Stability AI for reference-based (ControlNet/IP-Adapter)
# "replicate" = Use Replicate for reference-based (various models)
# "azure_only" = Use only DALL-E 3 (no reference support, logo won't integrate)
IMAGE_REFERENCE_STRATEGY = "stability"

# Choose video generation service:
# Options: "runway", "stability"
VIDEO_GENERATION_SERVICE = "runway"
