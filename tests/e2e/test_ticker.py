"""E2E tests for the ticker example."""

from playwright.async_api import Page, expect


async def test_loads_page(page: Page, example_server: str):
    """The page loads with both demos."""
    await page.goto(example_server)
    await expect(page.get_by_role("button", name="Generate")).to_be_visible()
    await expect(page.get_by_role("button", name="Connect")).to_be_visible()
    await expect(page.locator("#display")).to_contain_text("waiting to connect")


async def test_generate_streams_output(page: Page, example_server: str):
    """Clicking Generate streams chunks to the output."""
    await page.goto(example_server)
    # Click Generate
    await page.get_by_role("button", name="Generate").click()
    # Wait for the streaming response to complete
    # The response takes about 0.8 seconds (4 chunks * 200ms each)
    await page.wait_for_timeout(1500)
    # Check that the output contains the full message
    output = page.locator("#output")
    text = await output.text_content()
    assert "Hello" in text
    assert "world" in text


async def test_connect_updates_display(page: Page, example_server: str):
    """Clicking Connect opens an SSE connection that updates the display."""
    await page.goto(example_server)
    # Click Connect
    await page.get_by_role("button", name="Connect").click()
    # Wait for the first tick
    await page.wait_for_timeout(1000)
    # Check that the display shows a tick
    display = page.locator("#display")
    text = await display.text_content()
    assert "tick" in text


async def test_connection_closes_on_done(page: Page, example_server: str):
    """The connection closes after the done event."""
    await page.goto(example_server)
    # Click Connect
    await page.get_by_role("button", name="Connect").click()
    # Wait for all ticks and the done event
    # The ticker sends 3 ticks with 800ms each, so it takes about 2.4 seconds
    await page.wait_for_timeout(3000)
    # Check that the display shows the last tick
    display = page.locator("#display")
    text = await display.text_content()
    assert "tick 3" in text
