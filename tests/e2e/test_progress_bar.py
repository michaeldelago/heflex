"""E2E tests for the progress bar example."""

from playwright.async_api import Page, expect


async def test_loads_page(page: Page, example_server: str):
    """The page loads with the Start Job button."""
    await page.goto(example_server)
    await expect(page.locator("text=Background Job")).to_be_visible()
    await expect(page.get_by_role("button", name="Start Job")).to_be_visible()


async def test_start_job_creates_progress_bar(page: Page, example_server: str):
    """Clicking Start Job creates a progress bar."""
    await page.goto(example_server)
    # Click Start Job
    await page.get_by_role("button", name="Start Job").click()
    await page.wait_for_timeout(500)
    # Check that the progress bar is visible
    await expect(page.locator("#progress-container")).to_be_visible()


async def test_progress_bar_animates_to_done(page: Page, example_server: str):
    """The progress bar animates from 0% to 100% and shows Done."""
    await page.goto(example_server)
    # Click Start Job
    await page.get_by_role("button", name="Start Job").click()
    # Wait for the progress bar to complete
    # The bar updates every 400ms and increases by 15% each time
    # So it takes about 7 iterations (7 * 400ms = 2800ms) to reach 100%
    await page.wait_for_timeout(4000)
    # Check that the card shows "Done"
    card = page.locator("#progress-container")
    text = await card.text_content()
    assert "Done" in text
