"""E2E tests for the LLM streaming response example."""

from playwright.async_api import Page, expect


async def test_loads_page(page: Page, example_server: str):
    """The page loads with the input and transcript."""
    await page.goto(example_server)
    await expect(page.locator("text=Ask the model")).to_be_visible()
    await expect(page.locator('input[name="prompt"]')).to_be_visible()
    await expect(page.get_by_role("button", name="Ask")).to_be_visible()
    await expect(page.get_by_role("button", name="Clear")).to_be_visible()


async def test_ask_submits_and_streams(page: Page, example_server: str):
    """Submitting a prompt streams the response into the transcript."""
    await page.goto(example_server)
    # Fill in the prompt
    await page.locator('input[name="prompt"]').fill("What is hypermedia?")
    # Click Ask
    await page.get_by_role("button", name="Ask").click()
    # Wait for the streaming response to complete
    # The response takes about 3 seconds (75 tokens * 40ms each)
    await page.wait_for_timeout(4000)
    # Check that the question is in the transcript
    await expect(page.locator(".question")).to_contain_text("What is hypermedia?")
    # Check that the transcript contains the answer
    transcript = page.locator("#transcript")
    text = await transcript.text_content()
    assert "hypermedia" in text.lower()
    assert "hateoas" in text.lower()


async def test_clear_empties_transcript(page: Page, example_server: str):
    """Clicking Clear empties the transcript."""
    await page.goto(example_server)
    # Fill in the prompt and ask
    await page.locator('input[name="prompt"]').fill("Hello")
    await page.get_by_role("button", name="Ask").click()
    await page.wait_for_timeout(4000)
    # Transcript should have content
    transcript = page.locator("#transcript")
    text = await transcript.text_content()
    assert len(text) > 0
    
    # Click Clear
    await page.get_by_role("button", name="Clear").click()
    await page.wait_for_timeout(300)
    # Transcript should be empty
    text = await transcript.text_content()
    assert text.strip() == ""
