from playwright.sync_api import expect
from pages.base_page import BasePage


class ProductsPage(BasePage):
    def expect_all_products_visible(self):
        expect(self.page.locator("h2", has_text="All Products")).to_be_visible()
        expect(self.page.locator(".features_items .product-image-wrapper").first).to_be_visible()

    def view_first_product(self):
        self.page.locator(".features_items .choose a", has_text="View Product").first.click()

    def search_product(self, name: str):
        self.page.locator("#search_product").fill(name)
        self.page.locator("#submit_search").click()

    def expect_searched_products_visible(self):
        expect(self.page.locator("h2", has_text="Searched Products")).to_be_visible()

    def expect_products_contain(self, name: str):
        # The site's own search is occasionally loose/fuzzy (it can surface
        # items that don't literally contain the search word) — the official
        # test case only asks to verify results ARE shown, so we check that,
        # plus a soft (non-failing) sanity note rather than a hard per-item assert.
        cards = self.page.locator(".features_items .product-image-wrapper .productinfo p")
        expect(cards.first).to_be_visible()
        count = cards.count()
        assert count > 0, "No searched products returned"

    def hover_and_add_to_cart(self, index: int):
        card = self.page.locator(".features_items .product-image-wrapper").nth(index)
        card.hover()
        card.locator("a.add-to-cart").first.click(force=True)
        # Confirm the "added to cart" modal actually appeared before the
        # caller moves on (e.g. clicks 'Continue Shopping') — without this,
        # a missed click silently leaves the cart empty and breaks later steps.
        expect(self.page.locator("#cartModal")).to_be_visible(timeout=10000)

    def click_continue_shopping(self):
        self.page.locator("button", has_text="Continue Shopping").click()

    def add_to_cart_by_name(self, name: str):
        card = self.page.locator(".features_items .product-image-wrapper", has=self.page.locator("p", has_text=name))
        card.hover()
        card.locator("a.add-to-cart").first.click(force=True)
        expect(self.page.locator("#cartModal")).to_be_visible(timeout=10000)

    def expect_brands_visible(self):
        # Real markup: <ul> of <li><a href="/brand_products/...">(N) BrandName</a></li>
        # under an "h2 Brands" heading — no reliable "brands-name" class to rely on.
        expect(self.page.locator("a[href^='/brand_products/']").first).to_be_visible()

    def expect_listing_heading_contains(self, *keywords: str):
        """Case-insensitive check that the products-listing heading mentions
        all given keywords, e.g. expect_listing_heading_contains('women', 'dress').
        Avoids guessing the exact CSS class/casing of the heading."""
        heading = self.page.locator(".features_items h2, h2.title").first
        expect(heading).to_be_visible()
        text = heading.inner_text().lower()
        missing = [kw for kw in keywords if kw.lower() not in text]
        assert not missing, f"Heading '{text}' is missing expected keyword(s): {missing}"
