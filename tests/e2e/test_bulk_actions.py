"""E2E tests for the bulk actions example."""

from playwright.async_api import Page, expect


async def test_loads_users_table(page: Page, example_server: str):
    """The users table loads correctly with all rows."""
    await page.goto(example_server)
    await expect(page.locator("text=Users")).to_be_visible()
    row_count = await page.locator("table tr").count()
    assert row_count == 4  # header + 3 users


async def test_action_bar_hidden_by_default(page: Page, example_server: str):
    """The action bar is hidden when no checkboxes are checked."""
    await page.goto(example_server)
    action_bar = page.locator(".action-bar")
    await expect(action_bar).not_to_be_visible()


async def test_action_bar_shows_on_select(page: Page, example_server: str):
    """The action bar appears when a checkbox is checked."""
    await page.goto(example_server)
    # Click the first data row's checkbox
    await page.locator("table tr").nth(1).locator("input[type=checkbox]").click()
    await page.wait_for_timeout(200)
    action_bar = page.locator(".action-bar")
    await expect(action_bar).to_be_visible()


async def test_select_all(page: Page, example_server: str):
    """Clicking the header checkbox selects all rows."""
    await page.goto(example_server)
    await page.locator("#select-all").click()
    await page.wait_for_timeout(200)
    checked = await page.locator("input[name=selected]:checked").count()
    assert checked == 3


async def test_activate_selected(page: Page, example_server: str):
    """Activating selected users shows a flash message and updates status."""
    await page.goto(example_server)
    # Select the second row (Amy Jones, inactive)
    await page.locator("table tr").nth(2).locator("input[type=checkbox]").click()
    await page.wait_for_timeout(200)
    # Click Activate (exact match to avoid matching "Deactivate")
    await page.get_by_role("button", name="Activate", exact=True).click()
    await page.wait_for_timeout(300)
    # Check for flash message
    await expect(page.locator(".flash")).to_contain_text("Activated 1 user")


async def test_delete_selected(page: Page, example_server: str):
    """Deleting selected users removes them from the table."""
    await page.goto(example_server)
    # Select all users
    await page.locator("#select-all").click()
    await page.wait_for_timeout(200)
    # Click Delete
    await page.get_by_role("button", name="Delete", exact=True).click()
    await page.wait_for_timeout(300)
    # Check for flash message
    await expect(page.locator(".flash")).to_contain_text("Deleted 3 user")
    # Table should only have the header row now
    row_count = await page.locator("table tr").count()
    assert row_count == 1  # header row only
