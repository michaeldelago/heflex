"""E2E tests for the drag to reorder example."""

from playwright.async_api import Page, expect


async def test_loads_page(page: Page, example_server: str):
    """The page loads with all items."""
    await page.goto(example_server)
    await expect(page.locator("text=Drag to reorder")).to_be_visible()
    items = page.locator(".item")
    await expect(items).to_have_count(4)


async def test_items_in_order(page: Page, example_server: str):
    """Items appear in the correct initial order."""
    await page.goto(example_server)
    items = page.locator(".item")
    texts = await items.all_text_contents()
    assert texts == ["Item 1", "Item 2", "Item 3", "Item 4"]


async def test_drag_submits_to_server(page: Page, example_server: str):
    """After dragging, the new order is submitted and a flash message appears."""
    await page.goto(example_server)
    
    # Get the first item
    items = page.locator(".item")
    first_item = items.first
    second_item = items.nth(1)
    
    # Drag the first item after the second item
    await first_item.drag_to(second_item, target_position={"x": 0, "y": 20})
    await page.wait_for_timeout(800)
    
    # Check for flash message
    await expect(page.locator(".flash")).to_contain_text("Order saved")
