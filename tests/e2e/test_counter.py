"""E2E tests for the counter example."""

from playwright.async_api import Page, expect


async def test_counter_loads(page: Page, example_server: str):
    """The counter page loads with Count: 0."""
    await page.goto(example_server)
    await expect(page.locator("text=Count: 0")).to_be_visible()


async def test_increment(page: Page, example_server: str):
    """Clicking Increment increases the count."""
    await page.goto(example_server)
    await page.get_by_role("button", name="Increment").click()
    await expect(page.locator("text=Count: 1")).to_be_visible(timeout=3000)


async def test_decrement(page: Page, example_server: str):
    """Clicking Decrement decreases the count."""
    await page.goto(example_server)
    await page.get_by_role("button", name="Decrement").click()
    await expect(page.locator("text=Count: -1")).to_be_visible(timeout=3000)
