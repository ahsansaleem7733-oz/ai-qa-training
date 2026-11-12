# Week 3 Assignment – Data-Driven Product Sorting + API Testing

I am working on Week 3 of my Python Playwright QA training. I want you to help me create the first draft of the code based on my existing Week 2 project.

**Important: I am a beginner learning Python and Playwright. Keep the code simple, readable, and beginner-friendly. Do not overcomplicate it. I must understand every line of code.**

## 1. Existing project

Website:
https://practicesoftwaretesting.com

API base URL:
https://api.practicesoftwaretesting.com

I have selected my Week 2 test_TC_05, which verifies product sorting by price (High - Low).

I want to expand this into a data-driven sorting test.

I will provide my existing Week 2 test script and helpers.py. Reuse the existing helper functions wherever possible.

## 2. Files to create

Create the following files inside the week3 folder:

- test_week3.py
- data.csv
- prompt.md
- notes.md

Also copy helpers.py into the week3 folder.

## 3. Data-driven sorting test

Use pytest.mark.parametrize to execute one sorting test with multiple input values.

The test should cover these six scenarios:

1. Name (A - Z)
2. Name (Z - A)
3. Price (Low - High)
4. Price (High - Low)
5. Default sorting
6. An invalid sorting value that the website refuses or corrects.

Important:
- Do not assume dropdown values or option labels.
- Inspect the existing Week 2 helper functions and actual website dropdown options.
- Use the exact option values supported by the website.
- Ask me if actual manual testing observations or expected results are missing.
- Do not invent expected results for invalid inputs.

## 4. CSV file

Create data.csv containing the six sorting scenarios.

Include appropriate columns, such as:

- test_id
- sort_option
- expected_order

The CSV should contain the actual sorting values and expected results verified through manual testing.

Load the CSV using Python's csv module.

## 5. Parametrized Playwright test

Create one reusable test function using:

@pytest.mark.parametrize

Requirements:

- Read test inputs from data.csv.
- Execute the same test once for every CSV row.
- Give each test a meaningful ID so pytest -v displays understandable test names.
- Verify product sorting using the displayed product names or prices.
- Verify that the selected sorting option is correct.
- Handle the invalid option according to the actual observed website behavior.
- Use Playwright expect() for assertions about elements displayed on the page.
- Use normal Python assert statements for Python values and comparisons.
- Do not use time.sleep().

## 6. API test

Create at least one API test using Playwright's APIRequestContext.

Requirements:

- Use GET requests only.
- Use the public Practice Software Testing API.
- Verify HTTP status code.
- Validate at least three meaningful response fields.
- Compare at least one API response value with the corresponding value displayed on the website.
- Use the API endpoint and response structure only after confirming them from the public website or its available API information.
- Do not invent API endpoints or response fields.
- Do not use login or authentication.
- Do not use POST, PUT, PATCH or DELETE requests.

## 7. Coding requirements

- Keep the code beginner-friendly.
- Reuse existing helpers.py functions.
- Avoid unnecessary functions and complex logic.
- Use meaningful variable and function names.
- Add short comments explaining important steps.
- Follow the existing Week 2 coding style.
- Do not change my Week 2 files.
- Do not introduce unnecessary dependencies.
- Ensure the tests can run using pytest -v.

## 8. Important assignment rules

- The first generated version must remain untouched as my AI first draft.
- Do not silently change my manually verified CSV values.
- If something is unclear, ask me rather than making assumptions.
- Do not submit the contact form.
- Do not use any company code or private data.

## 9. Final deliverables

Generate:

1. test_1_sort_in_code.py
2. test2_sort_in_csv
3. test3_api_sort
4. test4_api_vs_page
5. data.csv
6. prompt.md containing this prompt
7. notes.md with placeholders for my review findings.

Before finishing, explain:
- How pytest.mark.parametrize works.
- How CSV data is loaded.
- How each CSV row becomes an individual test.
- How the API test works.
- How the API response is compared with the UI.

Remember: This is a learning assignment. I want to understand and review the generated code, not just receive code that works.