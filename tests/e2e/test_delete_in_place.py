"""E2E tests for the delete in place example."""

from playwright.async_api import Page, expect


async def test_loads_users_table(page: Page, example_server: str):
    """The users table loads correctly with all rows."""
    await page.goto(example_server)
    await expect(page.locator("text=Users")).to_be_visible()
    row_count = await page.locator("table tr").count()
    assert row_count == 4  # header + 3 users


async def test_delete_confirms_and_removes(page: Page, example_server: str):
    """Clicking Delete shows confirmation, accepting removes the row."""
    await page.goto(example_server)
    
    # Set up dialog handler
    async def handle_dialog(dialog):
        await dialog.accept()
    
    page.on("dialog", handle_dialog)
    
    # Click the first delete button
    await page.locator("table tr").nth(1).locator("button").click()
    await page.wait_for_timeout(800)
    
    # Row should be removed
    row_count = await page.locator("table tr").count()
    assert row_count == 3  # header + 2 users


async def test_delete_removes_row(page: Page, example_server: str):
    """Confirming delete removes the row with fade-out animation."""
    await page.goto(example_server)
    
    # Set up dialog handler
    async def handle_dialog(dialog):
        await dialog.accept()
    
    page.on("dialog", handle_dialog)
    
    # Click the second delete button
    await page.locator("table tr").nth(2).locator("button").click()
    await page.wait_for_timeout(800)
    
    # Row should be removed
    row_count = await page.locator("table tr").count()
    assert row_count == 3  # header + 2 users


async def test_delete_all_rows(page: Page, example_server: str):
    """Deleting all rows removes them one by one."""
    await page.goto(example_server)
    
    # Set up dialog handler
    async def handle_dialog(dialog):
        await dialog.accept()
    
    page.on("dialog", handle_dialog)
    
    # Delete all 3 rows
    for _ in range(3):
        row_count = await page.locator("table tr").count()
        if row_count == 1:
            break
        await page.locator("table tr").nth(1).locator("button").click()
        await page.wait_for_timeout(800)
    
    # Only header row should remain
    row_count = await page.locator("table tr").count()
    assert row_count == 1
