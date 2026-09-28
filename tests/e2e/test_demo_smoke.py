from playwright.sync_api import Page, expect


def test_demo_is_reachable(page: Page) -> None:
    page.goto("http://127.0.0.1:8001")
    expect(page.get_by_role("heading", name="Checkout demo")).to_be_visible()
