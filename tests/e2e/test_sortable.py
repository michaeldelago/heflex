"""E2E tests for the sortable example."""

from playwright.async_api import Page, expect


async def test_loads_page(page: Page, example_server: str):
    """The page loads with all items."""
    await page.goto(example_server)
    items = page.locator(".zz-sortable-item")
    await expect(items).to_have_count(5)


async def test_items_in_order(page: Page, example_server: str):
    """Items appear in the correct initial order."""
    await page.goto(example_server)
    items = page.locator(".zz-sortable-item")
    texts = await items.all_text_contents()
    assert texts == ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5"]


async def test_drag_reorders_items(page: Page, example_server: str):
    """Dragging an item to a new position reorders the items."""
    await page.goto(example_server)
    
    # Get the first item
    items = page.locator(".zz-sortable-item")
    first_item = items.first
    second_item = items.nth(1)
    
    # Drag the first item after the second item
    await first_item.drag_to(second_item, target_position={"x": 0, "y": 20})
    await page.wait_for_timeout(800)
    
    # Check that the items have been reordered
    # The server responds with the new order, so the items should be re-rendered
    items = page.locator(".zz-sortable-item")
    texts = await items.all_text_contents()
    # After dragging Item 1 after Item 2, the order should be: Item 2, Item 1, Item 3, Item 4, Item 5
    assert texts == ["Item 2", "Item 1", "Item 3", "Item 4", "Item 5"]
