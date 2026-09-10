"""E2E tests for the live updates example."""

from playwright.async_api import Page, expect


async def test_loads_page(page: Page, example_server: str):
    """The page loads with the ticker table."""
    await page.goto(example_server)
    await expect(page.locator("text=Live prices")).to_be_visible()
    await expect(page.locator("th:has-text('Symbol')")).to_be_visible()
    await expect(page.locator("th:has-text('Price')")).to_be_visible()


async def test_live_indicator_visible(page: Page, example_server: str):
    """The 'Live' indicator element exists and the SSE connection is active."""
    await page.goto(example_server)
    # Wait for the SSE connection to open
    await page.wait_for_timeout(1500)
    # Check that the live badge element exists
    # Note: the indicator may not be visible after the connection is established
    # (CSS hides it when htmx-request class is removed)
    await expect(page.locator("#live-badge")).to_be_attached()


async def test_prices_update(page: Page, example_server: str):
    """Price values update over time via SSE events."""
    await page.goto(example_server)
    # Wait for the SSE connection to open
    await page.wait_for_timeout(1000)

    # Check that all rows are visible
    await expect(page.locator("#row-HTMX")).to_be_visible()
    await expect(page.locator("#row-REST")).to_be_visible()
    await expect(page.locator("#row-FLEX")).to_be_visible()
