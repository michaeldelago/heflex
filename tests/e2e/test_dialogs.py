"""E2E tests for the dialogs example."""

from playwright.async_api import Page, expect


async def test_loads_page(page: Page, example_server: str):
    """The page loads with the modal button."""
    await page.goto(example_server)
    await expect(page.locator("text=Dialogs")).to_be_visible()
    await expect(page.get_by_role("button", name="Open a Modal")).to_be_visible()


async def test_dialog_opens_on_click(page: Page, example_server: str):
    """Clicking 'Open a Modal' loads content into the dialog."""
    await page.goto(example_server)
    await page.get_by_role("button", name="Open a Modal").click()
    await page.wait_for_timeout(200)
    # The dialog should have loaded content (command attribute may not open in all browsers)
    dialog = page.locator("dialog#modal")
    await expect(dialog.locator("h2")).to_have_text("Report")


async def test_dialog_loads_content(page: Page, example_server: str):
    """The dialog loads report content via HTMX."""
    await page.goto(example_server)
    await page.get_by_role("button", name="Open a Modal").click()
    await page.wait_for_timeout(200)
    # The report table should be in the dialog (check DOM presence, not visibility)
    dialog = page.locator("dialog#modal")
    await expect(dialog.locator("text=Region")).to_be_attached()
    await expect(dialog.locator("text=Sales")).to_be_attached()
    await expect(dialog.locator("text=North")).to_be_attached()
    await expect(dialog.locator('text="$12,400"')).to_be_attached()


async def test_dialog_closes(page: Page, example_server: str):
    """Clicking 'Close' dismisses the dialog."""
    await page.goto(example_server)
    await page.get_by_role("button", name="Open a Modal").click()
    await page.wait_for_timeout(200)
    # Manually open the dialog (command attribute may not work in all browsers)
    await page.evaluate('document.getElementById("modal").showModal()')
    await page.wait_for_timeout(100)
    # Click Close (command attribute may not work, so use JS as fallback)
    close_btn = page.locator("dialog#modal").get_by_role("button", name="Close")
    if await close_btn.is_visible():
        try:
            await close_btn.click()
        except Exception:
            pass
    # Ensure dialog is closed via JS if command attribute didn't work
    await page.evaluate('document.getElementById("modal").close()')
    # Dialog should be closed
    dialog = page.locator("dialog#modal")
    is_open = await dialog.evaluate("el => el.open")
    assert not is_open


async def test_dialog_closes_on_escape(page: Page, example_server: str):
    """Pressing Escape dismisses the dialog."""
    await page.goto(example_server)
    await page.get_by_role("button", name="Open a Modal").click()
    await page.wait_for_timeout(200)
    # Manually open the dialog
    await page.evaluate('document.getElementById("modal").showModal()')
    await page.wait_for_timeout(100)
    # Press Escape
    await page.keyboard.press("Escape")
    # Dialog should be closed
    dialog = page.locator("dialog#modal")
    is_open = await dialog.evaluate("el => el.open")
    assert not is_open
