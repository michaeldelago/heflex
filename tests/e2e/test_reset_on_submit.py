"""E2E tests for the reset on submit example."""

from playwright.async_api import Page, expect


async def test_loads_page(page: Page, example_server: str):
    """The page loads with the chat interface."""
    await page.goto(example_server)
    await expect(page.locator("text=Chat")).to_be_visible()
    # Initial bot message
    await expect(page.locator("text=Hi! How can I help?")).to_be_visible()
    await expect(page.locator('input[name="message"]')).to_be_visible()


async def test_send_message(page: Page, example_server: str):
    """Sending a message appends both user and bot messages."""
    await page.goto(example_server)
    # Type a message
    await page.locator('input[name="message"]').fill("Hello")
    # Press Enter to submit
    await page.locator('input[name="message"]').press("Enter")
    await page.wait_for_timeout(300)
    # Check that both messages are visible
    await expect(page.locator('text="Hello"')).to_be_visible()
    await expect(page.locator("text=Echo: Hello")).to_be_visible()


async def test_input_resets_after_send(page: Page, example_server: str):
    """The input field resets after each send."""
    await page.goto(example_server)
    # Type and send a message
    await page.locator('input[name="message"]').fill("Hello")
    await page.locator('input[name="message"]').press("Enter")
    await page.wait_for_timeout(300)
    # Check that the input is reset
    input_value = await page.locator('input[name="message"]').input_value()
    assert input_value == ""


async def test_multiple_messages(page: Page, example_server: str):
    """Multiple messages can be sent and all appear."""
    await page.goto(example_server)
    # Send first message
    await page.locator('input[name="message"]').fill("First")
    await page.locator('input[name="message"]').press("Enter")
    await page.wait_for_timeout(300)

    # Send second message
    await page.locator('input[name="message"]').fill("Second")
    await page.locator('input[name="message"]').press("Enter")
    await page.wait_for_timeout(300)

    # Check that all messages are visible
    await expect(page.locator('text="First"')).to_be_visible()
    await expect(page.locator("text=Echo: First")).to_be_visible()
    await expect(page.locator('text="Second"')).to_be_visible()
    await expect(page.locator("text=Echo: Second")).to_be_visible()
