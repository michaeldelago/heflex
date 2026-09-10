"""E2E tests for the lazy load example."""

from playwright.async_api import Page, expect


async def test_loads_page(page: Page, example_server: str):
    """The page loads with the dashboard heading."""
    await page.goto(example_server)
    await expect(page.locator("text=Dashboard")).to_be_visible()


async def test_weather_section_loads(page: Page, example_server: str):
    """The weather section loads its content."""
    await page.goto(example_server)
    # Wait for the weather content to load
    await expect(page.locator("text=5-Day Forecast")).to_be_visible()
    # Check for weather data
    await expect(page.locator("text=Weekday 1")).to_be_visible()


async def test_parallel_sections_load(page: Page, example_server: str):
    """All parallel sections load their content."""
    await page.goto(example_server)
    # Wait for all sections to load
    await expect(page.locator("text=Sales are up 12%")).to_be_visible()
    await expect(page.locator("text=Bounce rate 34%")).to_be_visible()
    await expect(page.locator("text=No new notifications")).to_be_visible()


async def test_loading_text_replaced(page: Page, example_server: str):
    """The initial loading text is replaced with actual content."""
    await page.goto(example_server)
    # Wait for content to load
    await page.wait_for_timeout(500)
    # The loading text should no longer be visible
    await expect(page.locator("text=Loading weather")).not_to_be_visible()
    await expect(page.locator("text=Loading sales")).not_to_be_visible()
    await expect(page.locator("text=Loading analytics")).not_to_be_visible()
    await expect(page.locator("text=Loading notifications")).not_to_be_visible()
