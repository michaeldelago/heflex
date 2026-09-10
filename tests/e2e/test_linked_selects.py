"""E2E tests for the linked selects example."""

from playwright.async_api import Page, expect


async def test_loads_page(page: Page, example_server: str):
    """The page loads with both selects."""
    await page.goto(example_server)
    await expect(page.locator("text=Cars")).to_be_visible()
    # Both selects should be visible
    selects = page.locator("select")
    await expect(selects).to_have_count(2)


async def test_selecting_make_updates_models(page: Page, example_server: str):
    """Selecting a car make populates the model dropdown."""
    await page.goto(example_server)
    # Select Toyota using JavaScript to avoid Playwright select_option hanging
    await page.evaluate("""
        const select = document.querySelector('select[name="make"]');
        select.value = 'Toyota';
        select.dispatchEvent(new Event('change'));
    """)
    await page.wait_for_timeout(300)
    # Check that the model dropdown has Toyota options
    model_select = page.locator("#models")
    options = await model_select.locator("option").all_text_contents()
    assert "Corolla" in options
    assert "Camry" in options
    assert "RAV4" in options


async def test_selecting_different_make_updates_models(page: Page, example_server: str):
    """Selecting a different make updates the model options."""
    await page.goto(example_server)
    # Select Toyota using JavaScript
    await page.evaluate("""
        const select = document.querySelector('select[name="make"]');
        select.value = 'Toyota';
        select.dispatchEvent(new Event('change'));
    """)
    await page.wait_for_timeout(300)
    # Check Toyota options
    model_select = page.locator("#models")
    options = await model_select.locator("option").all_text_contents()
    assert "Corolla" in options
    
    # Select Honda using JavaScript
    await page.evaluate("""
        const select = document.querySelector('select[name="make"]');
        select.value = 'Honda';
        select.dispatchEvent(new Event('change'));
    """)
    await page.wait_for_timeout(300)
    # Check Honda options
    options = await model_select.locator("option").all_text_contents()
    assert "Civic" in options
    assert "Accord" in options
    assert "CR-V" in options
    # Toyota options should no longer be present
    assert "Corolla" not in options


async def test_invalid_make_shows_empty(page: Page, example_server: str):
    """Selecting an invalid make shows an empty option."""
    await page.goto(example_server)
    # Select an invalid make using JavaScript
    await page.evaluate("""
        const select = document.querySelector('select[name="make"]');
        select.value = 'Ford';
        select.dispatchEvent(new Event('change'));
    """)
    await page.wait_for_timeout(300)
    # Check that the model dropdown has only an empty option
    model_select = page.locator("#models")
    options = await model_select.locator("option").all_text_contents()
    assert options == [""]
