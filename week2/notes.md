# Week 2 QA notes

## AI first-draft review

This file is a review template. Do not claim an AI mistake was observed until you have run the draft and verified it.

Record at least three actual issues below. For each one, include the test ID, the line or behavior, what happened on the page, how you identified the problem, and the correction you made.

### Issue 1
- Test ID: 07
- What the AI draft got wrong: Wrong Assertion applied on wrong locator.
- How I found it (error and what I saw on the page): I checked from website, if locator actually presents or not.
- What I changed: Added right locator assertion 

### Issue 2
- Test ID: 05
- What the AI draft got wrong: It didn't correctly apply product price sorting.
- How I found it: The test failed because prices were not in descending order.
- What I changed: Added a check to verify the selected sorting option and wait for Page Idle state.

### Issue 3
- Test ID: 09
- What the AI draft got wrong: wrong locator of product price was added
- How I found it (error and what I saw on the page): locator visibility was timing out.
- What I changed: Added Correct Product locator.


### Issue 4
- Test ID: 12
- What the AI draft got wrong: wrong locator for Delete cart items, and message mismatch in assertion for empty cart.
- How I found it (error and what I saw on the page): locator visibility was timing out.
- What I changed: Added Correct Delete cart items locator.


## One thing the assistant got right

- What it got right:
- How I verified it:

## Execution results

Record the date, command, PASS/FAIL results, and any remaining blockers here.

## Safety note

The contact-form automation may click Send only when every field is empty for required-field validation. It must never submit a completed contact form because submissions reach the shop owner's real inbox.
