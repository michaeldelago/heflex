"""E2E tests for the click to load example."""

from playwright.async_api import Page, expect


async def test_loads_initial_comments(page: Page, example_server: str):
    """The page loads with the first batch of comments."""
    await page.goto(example_server)
    comments = page.locator("div > strong")
    await expect(comments).to_have_count(3)


async def test_show_more_button_visible(page: Page, example_server: str):
    """The 'Show more comments' button is visible initially."""
    await page.goto(example_server)
    await expect(page.get_by_role("button", name="Show more comments")).to_be_visible()


async def test_loads_second_page(page: Page, example_server: str):
    """Clicking 'Show more' loads the next batch of comments."""
    await page.goto(example_server)
    # Click the button
    await page.get_by_role("button", name="Show more comments").click()
    await page.wait_for_timeout(200)
    # Should now have 6 comments (3 initial + 3 loaded)
    comments = page.locator("div > strong")
    await expect(comments).to_have_count(6)


async def test_button_replaces_itself(page: Page, example_server: str):
    """After clicking, the button remains for further loading."""
    await page.goto(example_server)
    # Click once
    await page.get_by_role("button", name="Show more comments").click()
    await page.wait_for_timeout(200)
    # Button should still be visible (for next page)
    await expect(page.get_by_role("button", name="Show more comments")).to_be_visible()


async def test_loads_all_comments(page: Page, example_server: str):
    """Clicking repeatedly loads all 12 comments."""
    await page.goto(example_server)
    # Click 4 times to load all 12 comments (3 per page)
    for i in range(4):
        button = page.get_by_role("button", name="Show more comments")
        if not await button.is_visible():
            break
        await button.click()
        await page.wait_for_timeout(200)
    # Should have all 12 comments
    comments = page.locator("div > strong")
    await expect(comments).to_have_count(12)
    # Button should no longer be visible (no more pages)
    await expect(
        page.get_by_role("button", name="Show more comments")
    ).not_to_be_visible()
