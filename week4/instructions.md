# Assistant instructions

- Write beginner-readable Python and follow existing project conventions.
- Use pytest fixtures for browser and page setup; never launch a browser in a test.
- Put page locators and page actions in page-object classes.
- Keep test assertions in tests; page classes may use expect only for readiness waits.
- Use expect for visible UI state and clear Python assertions for values.
- Never use time.sleep().
- Keep tests limited to public Practice Software Testing pages.
- Do not use APIs, credentials, private data, or company code.
- Never submit a populated contact form.
- Preserve test intent and report assumptions or unknowns instead of guessing.
