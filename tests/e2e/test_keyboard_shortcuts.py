"""Debug test for keyboard shortcuts."""

from playwright.async_api import Page


async def test_debug(page: Page, example_server: str):
    """Debug: check keyboard shortcut."""
    await page.goto(example_server)

    # Enable htmx logging
    await page.evaluate("htmx.config.logAll = true;")

    # Listen for console messages
    console_messages = []
    page.on("console", lambda msg: console_messages.append(msg.text))

    # Add a listener to body to see what events are received
    await page.evaluate("""
        document.body.addEventListener('keyup', (e) => {
            console.log('keyup received on body:', {
                key: e.key,
                code: e.code,
                altKey: e.altKey,
                shiftKey: e.shiftKey,
                bubbles: e.bubbles
            });
        });
        
        // Also add a listener to the button
        const btn = document.querySelector('button');
        btn.addEventListener('keyup', (e) => {
            console.log('keyup received on button:', {
                key: e.key,
                code: e.code,
                altKey: e.altKey,
                shiftKey: e.shiftKey,
                bubbles: e.bubbles
            });
        });
    """)

    # Dispatch a keyup event on <body> with altKey, shiftKey, and code='KeyD'
    await page.evaluate("""
        const event = new KeyboardEvent('keyup', {
            key: 'd',
            code: 'KeyD',
            altKey: true,
            shiftKey: true,
            bubbles: true
        });
        document.body.dispatchEvent(event);
    """)

    await page.wait_for_timeout(500)

    # Check console messages
    print(f"Console messages: {console_messages}")
