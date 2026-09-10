"""E2E tests for the edit in place example."""

from playwright.async_api import Page, expect


async def test_loads_users_page(page: Page, example_server: str):
    """The page loads with all users in view mode."""
    await page.goto(example_server)
    await expect(page.locator("text=Users")).to_be_visible()
    await expect(page.locator("text=Joe Smith")).to_be_visible()
    await expect(page.locator("text=Amy Jones")).to_be_visible()


async def test_edit_opens_form(page: Page, example_server: str):
    """Clicking Edit shows the edit form."""
    await page.goto(example_server)
    # Click Edit for Joe Smith
    await page.locator("#card-1").get_by_role("button", name="Edit").click()
    await page.wait_for_timeout(200)
    # The form should be visible
    await expect(page.locator("#card-1 input[name=name]")).to_be_visible()
    await expect(page.locator("#card-1 input[name=email]")).to_be_visible()


async def test_save_updates_user(page: Page, example_server: str):
    """Saving the form updates the user info."""
    await page.goto(example_server)
    # Click Edit
    await page.locator("#card-1").get_by_role("button", name="Edit").click()
    await page.wait_for_timeout(200)
    # Clear and fill in new values
    name_input = page.locator("#card-1 input[name=name]")
    email_input = page.locator("#card-1 input[name=email]")
    await name_input.clear()
    await name_input.fill("John Doe")
    await email_input.clear()
    await email_input.fill("john@example.com")
    # Click Save
    await page.locator("#card-1").get_by_role("button", name="Save").click()
    await page.wait_for_timeout(300)
    # Check updated values
    await expect(page.locator("#card-1")).to_contain_text("John Doe")
    await expect(page.locator("#card-1")).to_contain_text("john@example.com")


async def test_cancel_reverts(page: Page, example_server: str):
    """Clicking Cancel reverts to view mode without saving."""
    await page.goto(example_server)
    # Click Edit
    await page.locator("#card-1").get_by_role("button", name="Edit").click()
    await page.wait_for_timeout(200)
    # Fill in new values
    name_input = page.locator("#card-1 input[name=name]")
    await name_input.clear()
    await name_input.fill("Hacked User")
    # Click Cancel
    await page.locator("#card-1").get_by_role("button", name="Cancel").click()
    await page.wait_for_timeout(300)
    # Should still show original name
    await expect(page.locator("#card-1")).to_contain_text("Joe Smith")
    await expect(page.locator("#card-1")).not_to_contain_text("Hacked User")
