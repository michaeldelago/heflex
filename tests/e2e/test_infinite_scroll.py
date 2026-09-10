"""E2E tests for the infinite scroll example."""

from playwright.async_api import Page, expect


async def test_loads_initial_rows(page: Page, example_server: str):
    """The page loads with the first batch of rows."""
    await page.goto(example_server)
    await expect(page.locator("text=Contacts")).to_be_visible()
    await expect(page.locator("text=Agent #0")).to_be_visible()
    await expect(page.locator("text=Agent #1")).to_be_visible()
    await expect(page.locator("text=Agent #2")).to_be_visible()


async def test_loading_placeholder_visible(page: Page, example_server: str):
    """The 'Loading more...' placeholder is visible initially."""
    await page.goto(example_server)
    await expect(page.locator("text=Loading more...")).to_be_visible()


async def test_loads_more_on_scroll(page: Page, example_server: str):
    """Scrolling reveals the placeholder and loads more rows."""
    await page.goto(example_server)
    # Scroll to the bottom to reveal the loading placeholder
    await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    await page.wait_for_timeout(500)
    # Should have loaded more rows
    await expect(page.locator("text=Agent #3")).to_be_visible()
    await expect(page.locator("text=Agent #4")).to_be_visible()


async def test_loads_all_rows(page: Page, example_server: str):
    """Scrolling repeatedly loads all rows."""
    await page.goto(example_server)
    # Scroll multiple times to load all rows
    for _ in range(5):
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await page.wait_for_timeout(500)

    # Should have all 15 agents
    for i in range(15):
        await expect(page.locator(f"text='Agent #{i}'")).to_be_visible()
