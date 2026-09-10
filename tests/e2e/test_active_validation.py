"""E2E tests for the active validation example."""

from playwright.async_api import Page, expect


async def test_loads_sign_up_page(page: Page, example_server: str):
    """The sign up page loads correctly."""
    await page.goto(example_server)
    await expect(page.locator("text=Sign Up")).to_be_visible()
    await expect(page.get_by_label("Choose a username: ")).to_be_visible()


async def test_too_short_error(page: Page, example_server: str):
    """Typing a short username shows an error message."""
    await page.goto(example_server)
    await page.get_by_label("Choose a username: ").type("ab", delay=50)
    await page.wait_for_timeout(500)
    await expect(page.locator(".error")).to_contain_text("Too short")


async def test_taken_username_error(page: Page, example_server: str):
    """Typing a taken username shows an error message."""
    await page.goto(example_server)
    await page.get_by_label("Choose a username: ").type("admin", delay=50)
    await page.wait_for_timeout(500)
    await expect(page.locator(".error")).to_contain_text("taken")


async def test_valid_username(page: Page, example_server: str):
    """Typing a valid username shows a success message."""
    await page.goto(example_server)
    await page.get_by_label("Choose a username: ").type("gooduser123", delay=50)
    await page.wait_for_timeout(500)
    await expect(page.locator(".ok")).to_contain_text("Looks good")
