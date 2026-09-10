"""E2E tests for the tabs example."""

from playwright.async_api import Page, expect


async def test_loads_page(page: Page, example_server: str):
    """The page loads with the tabs interface."""
    await page.goto(example_server)
    await expect(page.locator("text=Server-driven tabs")).to_be_visible()


async def test_first_tab_active(page: Page, example_server: str):
    """The first tab (overview) is active on page load."""
    await page.goto(example_server)
    # Check that the overview tab content is visible
    await expect(page.locator("text=Overview content")).to_be_visible()
    # Check that the overview tab is selected
    await expect(page.locator("#tab-overview")).to_have_attribute("aria-selected", "true")


async def test_switching_tabs(page: Page, example_server: str):
    """Clicking a tab button switches to that tab."""
    await page.goto(example_server)
    # Click the install tab
    await page.locator("#tab-install").click()
    await page.wait_for_timeout(300)
    # Check that the install tab content is visible
    await expect(page.locator("text=Install content")).to_be_visible()
    # Check that the install tab is selected
    await expect(page.locator("#tab-install")).to_have_attribute("aria-selected", "true")
    # Check that the overview tab is not selected
    await expect(page.locator("#tab-overview")).to_have_attribute("aria-selected", "false")


async def test_switching_to_extensions(page: Page, example_server: str):
    """Clicking the extensions tab switches to that tab."""
    await page.goto(example_server)
    # Click the extensions tab
    await page.locator("#tab-extensions").click()
    await page.wait_for_timeout(300)
    # Check that the extensions tab content is visible
    await expect(page.locator("text=Extensions content")).to_be_visible()
    # Check that the extensions tab is selected
    await expect(page.locator("#tab-extensions")).to_have_attribute("aria-selected", "true")
