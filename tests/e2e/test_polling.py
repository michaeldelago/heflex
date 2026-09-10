"""E2E tests for the polling example."""

from playwright.async_api import Page, expect


async def test_loads_page(page: Page, example_server: str):
    """The page loads with the polling card."""
    await page.goto(example_server)
    await expect(page.locator("text=Polling")).to_be_visible()
    await expect(page.locator("#poll-card")).to_be_visible()


async def test_card_shows_cpu_data(page: Page, example_server: str):
    """The card shows CPU data."""
    await page.goto(example_server)
    # Wait for the card to load with CPU data
    await page.wait_for_timeout(500)
    # Check that the card shows CPU data
    card = page.locator("#poll-card")
    text = await card.text_content()
    assert "CPU" in text
    assert "%" in text


async def test_pause_stops_polling(page: Page, example_server: str):
    """Clicking Pause stops the polling."""
    await page.goto(example_server)
    # Click Pause
    await page.locator("#poll-card").get_by_role("button", name="Pause").click()
    await page.wait_for_timeout(500)
    # Check that the card shows "Job complete (paused)"
    card = page.locator("#poll-card")
    text = await card.text_content()
    assert "Job complete (paused)" in text
    # Check that the Pause button is now "Resume"
    await expect(page.locator("#poll-card").get_by_role("button", name="Resume")).to_be_visible()


async def test_resume_restarts_polling(page: Page, example_server: str):
    """Clicking Resume restarts the polling."""
    await page.goto(example_server)
    # Click Pause
    await page.locator("#poll-card").get_by_role("button", name="Pause").click()
    await page.wait_for_timeout(500)
    # Check that the card shows "Job complete (paused)"
    card = page.locator("#poll-card")
    text = await card.text_content()
    assert "Job complete (paused)" in text
    
    # Click Resume
    await page.locator("#poll-card").get_by_role("button", name="Resume").click()
    await page.wait_for_timeout(500)
    # Check that the card shows CPU data again
    text = await card.text_content()
    assert "CPU" in text
    assert "%" in text
