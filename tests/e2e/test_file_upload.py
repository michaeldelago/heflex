"""E2E tests for the file upload example."""

import io
from pathlib import Path

from playwright.async_api import Page, expect


async def test_loads_page(page: Page, example_server: str):
    """The page loads with the upload form."""
    await page.goto(example_server)
    await expect(page.locator("text=Upload")).to_be_visible()
    await expect(page.locator("text=Title:")).to_be_visible()
    # File input is inside the form
    await expect(page.locator("form input[type=file]").first).to_be_visible()


async def test_validation_errors(page: Page, example_server: str):
    """Submitting without title or file shows validation errors."""
    await page.goto(example_server)
    # Submit without title or file
    await page.get_by_role("button", name="Submit").click()
    await page.wait_for_timeout(200)
    # Should show error
    await expect(page.locator(".error")).to_contain_text("Title is required")


async def test_file_upload_success(page: Page, example_server: str):
    """Uploading a file with a title shows success."""
    await page.goto(example_server)
    # Create a test file
    test_file = Path("/tmp/test_upload.txt")
    test_file.write_text("Hello, world!")
    
    # Fill in title and select file
    await page.locator("form input[name=title]").fill("My Test File")
    await page.locator("form input[type=file]").first.set_input_files(str(test_file))
    
    # Submit
    await page.get_by_role("button", name="Submit").click()
    await page.wait_for_timeout(300)
    
    # Should show success
    await expect(page.locator(".ok")).to_contain_text("File uploaded successfully")
    await expect(page.locator("text=My Test File")).to_be_visible()
    await expect(page.locator("text=test_upload.txt")).to_be_visible()


async def test_file_preserved_on_error(page: Page, example_server: str):
    """File selection is preserved when form is re-rendered with errors."""
    await page.goto(example_server)
    # Create a test file
    test_file = Path("/tmp/test_upload2.txt")
    test_file.write_text("Preserved file content")
    
    # Select file but don't fill title
    await page.locator("form input[type=file]").first.set_input_files(str(test_file))
    
    # Submit (should show error for missing title)
    await page.get_by_role("button", name="Submit").click()
    await page.wait_for_timeout(300)
    
    # Should show error
    await expect(page.locator(".error")).to_contain_text("Title is required")
    
    # File should still be selected (check that the file input still has a value)
    file_input = page.locator("form input[type=file]").first
    files = await file_input.evaluate("el => el.files.length")
    assert files == 1
