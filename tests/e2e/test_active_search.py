"""E2E tests for the active search example."""

from playwright.async_api import Page, expect


async def test_loads_initial_table(page: Page, example_server: str):
    """The page loads with an empty results table."""
    await page.goto(example_server)
    await expect(page.locator("text=People")).to_be_visible()
    await expect(page.locator("#results tr").first).to_be_visible()


async def test_search_filters_results(page: Page, example_server: str):
    """Typing a query filters the table to matching rows."""
    await page.goto(example_server)
    # Use type() to trigger htmx's input changed event
    await page.get_by_placeholder("Search name or email…").type("venus", delay=50)
    # Wait for debounced request to complete (delay:200ms)
    await page.wait_for_timeout(600)
    # Should only show Venus Grimes, not other people
    assert await page.locator("#results tr").count() == 1
    await expect(page.locator("text=Venus Grimes")).to_be_visible()


async def test_search_clears(page: Page, example_server: str):
    """Clearing the search shows all results again."""
    await page.goto(example_server)
    await page.get_by_placeholder("Search name or email…").type("venus", delay=50)
    await expect(page.locator("text=Venus Grimes")).to_be_visible(timeout=5000)
    # Clear the input
    await page.get_by_placeholder("Search name or email…").fill("")
    await page.wait_for_timeout(400)
    # Should show all 4 people
    assert await page.locator("#results tr").count() == 4


async def test_no_matches_shows_message(page: Page, example_server: str):
    """Searching for something with no matches shows a 'No matches' row."""
    await page.goto(example_server)
    await page.get_by_placeholder("Search name or email…").type("zzzznonexistent", delay=50)
    await expect(page.locator("text=No matches.")).to_be_visible(timeout=5000)
