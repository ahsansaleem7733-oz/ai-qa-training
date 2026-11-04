# Week 2 AI test-generation prompt

You are helping me draft Python UI automation tests for the Practice Software Testing shop:
https://practicesoftwaretesting.com/

Use Python and Playwright's synchronous API (`playwright.sync_api`). Follow these rules:

1. Read the requirements and test cases I provide.
2. Generate a first-draft `tests_week2.py` with one function per selected test case. Function names must match their IDs, for example `test_TC_01`.
3. Every test function must accept `page` as its only argument.
4. Cover search, sorting, cart, and contact form. Include at least six tests.
5. Use helper functions for repeated actions such as opening the home page, reading product names/prices, and navigating to a category.
6. Use Playwright locators and `expect`; do not use `time.sleep`.
7. Do not hard-code product names or prices. Read current product names and prices from the page. Handle changing product data and out-of-stock products.
8. The contact form must never be submitted when populated. It is acceptable to click Send only when all fields are empty to test required-field validation.
9. The runner must execute each test independently, print PASS or FAIL for each, continue after an individual test fails, close pages/browser, and exit with code 1 if any test failed.
10. Use clear Python guide style, useful assertion messages, and comments only when the reason is not obvious.
11. Do not invent selectors. If a selector is uncertain, clearly mark it for inspection and explain how to confirm it using the browser's Inspect tool and `data-test` attributes.
12. Explain assumptions and any requirement gaps rather than silently deciding expected behavior.

Requirements:
- Search by clicking Search or pressing Enter; both produce the same products.
- An unmatched search displays a no-results message and no products.
- Clear empties the search field and restores the full product list.
- Sort by price high-to-low and name Z-to-A.
- Sorting works inside Power Tools and the category remains identified.
- Product page accepts a customer-entered quantity and cart reflects it.
- Changing cart quantity updates line price, cart total, and cart icon count.
- Eco products may have an intentional cart-level discount; verify line price and do not flag the discount as a bug.
- Customers can remove an item; removing the last item displays an empty-cart state.
- Contact form has first name, last name, email, subject dropdown, and message. All are required.
- Empty submission shows a message under each empty field.
- Entered contact values and chosen subject remain populated while completing the form.
- Some products are out of stock and must not be addable to cart. Exact UI message is undecided.
- Login, checkout, payment, and order history are out of scope.

Selected test cases to automate:
TC_01 search using Search button
TC_02 search using Enter and compare with button search
TC_03 unmatched search
TC_05 sort price descending
TC_07 sort Power Tools by price descending
TC_09 update cart quantity and verify totals/count
TC_12 remove last item and verify empty cart
TC_14 empty contact form validation
TC_15 retain contact form values without submitting

Here are my test cases CSV and the website's current DOM/locator observations:


Draft the code, but distinguish confirmed selectors from selectors that still need inspection. Do not claim that unverified tests are ready to run.
