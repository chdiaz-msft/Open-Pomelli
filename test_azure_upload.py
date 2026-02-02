#!/usr/bin/env python3
"""
Test script for Azure Blob Storage upload functionality.
Tests the AzureBlobUploader class and ensure_url() function.
"""

import asyncio
import os
import tempfile
from PIL import Image
from adapters import get_azure_uploader, ensure_url


async def test_basic_upload():
    """Test basic file upload to Azure Blob Storage."""
    print("\n" + "="*60)
    print("TEST 1: Basic file upload")
    print("="*60)

    # Create a test image
    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp:
        img = Image.new('RGB', (100, 100), color='red')
        img.save(tmp, format='PNG')
        tmp_path = tmp.name

    try:
        print(f"Created test image: {tmp_path}")

        # Upload using AzureBlobUploader directly
        uploader = get_azure_uploader()
        url = await uploader.upload_file_async(tmp_path)

        print(f"✓ Upload successful!")
        print(f"✓ URL: {url}")

        # Verify URL format
        assert url.startswith('https://'), "URL should start with https://"
        assert 'testeng1' in url, "URL should contain storage account name"
        assert 'chdiaz-test' in url, "URL should contain container name"

        print(f"✓ URL format validation passed")

        return True

    except Exception as e:
        print(f"✗ Upload failed: {e}")
        import traceback
        traceback.print_exc()
        return False

    finally:
        # Clean up
        os.unlink(tmp_path)
        print(f"Cleaned up test file: {tmp_path}")


async def test_ensure_url_local_file():
    """Test ensure_url() with a local file."""
    print("\n" + "="*60)
    print("TEST 2: ensure_url() with local file")
    print("="*60)

    # Create a test image
    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp:
        img = Image.new('RGB', (200, 200), color='blue')
        img.save(tmp, format='JPEG')
        tmp_path = tmp.name

    try:
        print(f"Created test image: {tmp_path}")

        # Test ensure_url with Azure enabled
        url = await ensure_url(tmp_path, use_azure=True)

        print(f"✓ ensure_url() successful!")
        print(f"✓ URL: {url}")

        # Verify URL format
        assert url.startswith('https://'), "URL should start with https://"
        assert 'testeng1' in url, "URL should contain storage account name"

        print(f"✓ URL format validation passed")

        return True

    except Exception as e:
        print(f"✗ ensure_url() failed: {e}")
        import traceback
        traceback.print_exc()
        return False

    finally:
        # Clean up
        os.unlink(tmp_path)
        print(f"Cleaned up test file: {tmp_path}")


async def test_ensure_url_with_url():
    """Test ensure_url() with an existing URL (should return as-is)."""
    print("\n" + "="*60)
    print("TEST 3: ensure_url() with existing URL")
    print("="*60)

    test_url = "https://example.com/image.png"

    try:
        result_url = await ensure_url(test_url, use_azure=True)

        print(f"✓ Input URL: {test_url}")
        print(f"✓ Output URL: {result_url}")

        # Should return the same URL
        assert result_url == test_url, "URL should be returned unchanged"

        print(f"✓ URL passthrough validation passed")

        return True

    except Exception as e:
        print(f"✗ ensure_url() with URL failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_content_type_detection():
    """Test that content types are correctly detected."""
    print("\n" + "="*60)
    print("TEST 4: Content type detection")
    print("="*60)

    uploader = get_azure_uploader()

    test_cases = [
        ('.png', 'image/png'),
        ('.jpg', 'image/jpeg'),
        ('.jpeg', 'image/jpeg'),
        ('.gif', 'image/gif'),
        ('.webp', 'image/webp'),
        ('.svg', 'image/svg+xml'),
        ('.mp4', 'video/mp4'),
        ('.pdf', 'application/pdf'),
        ('.txt', 'text/plain'),
        ('.unknown', 'application/octet-stream'),
    ]

    all_passed = True

    for extension, expected_type in test_cases:
        result = uploader._get_content_type(f"test{extension}")
        if result == expected_type:
            print(f"✓ {extension:10} -> {expected_type}")
        else:
            print(f"✗ {extension:10} -> Expected {expected_type}, got {result}")
            all_passed = False

    return all_passed


async def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("AZURE BLOB STORAGE UPLOAD TESTS")
    print("="*60)

    results = []

    # Test 1: Basic upload
    results.append(("Basic file upload", await test_basic_upload()))

    # Test 2: ensure_url with local file
    results.append(("ensure_url() with local file", await test_ensure_url_local_file()))

    # Test 3: ensure_url with URL
    results.append(("ensure_url() with existing URL", await test_ensure_url_with_url()))

    # Test 4: Content type detection
    results.append(("Content type detection", await test_content_type_detection()))

    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)

    passed = 0
    failed = 0

    for test_name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{status:10} - {test_name}")
        if result:
            passed += 1
        else:
            failed += 1

    print("="*60)
    print(f"Total: {len(results)} tests, {passed} passed, {failed} failed")
    print("="*60)

    return failed == 0


if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)
