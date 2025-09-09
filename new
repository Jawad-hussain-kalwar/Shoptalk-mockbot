# PRD — “ShopTalk”: Terminal Q\&A + Ordering Agent (Gemini)

## 1) Overview

A lightweight, multi-turn conversational agent that runs in a Python terminal, powered by Gemini. The agent answers product questions for a mock shop and can place simple orders. It demonstrates:

* Tool calling (multiple tools, chained calls, retry/fallback).
* Structured outputs (clearly delineated summaries, actions taken, and next steps rendered in the terminal).
* A concise agentic loop with memory of the ongoing session.

The demo targets fast setup, clear observability (what tool was called and why), and resilient behavior with ambiguous queries.

---

## 2) Primary User Stories

1. “Tell me about product X” → The agent explains features, availability, and price; offers comparisons or alternatives.
2. “Do you have Y in stock?” → The agent checks inventory and returns availability with delivery estimates.
3. “I want to buy Z” → The agent guides a short order flow, confirms details, places the order, and returns an order ID.
4. “What’s the status of my order?” → The agent retrieves status using an order identifier and summarizes progress.
5. “I have a budget/need” → The agent suggests suitable products and explains tradeoffs.

---

## 3) UX & Interaction Model (Terminal)

* **Input**: Free-form user text, one turn at a time.
* **Output**:

  * Conversational answer.
  * A compact “What I did” panel that lists tools invoked and high-level results.
  * A short “Next step” nudge (e.g., confirm size/color, confirm address).
* **Session Memory (ephemeral)**: Current intent, active product reference(s), cart-in-progress, and user-provided contact/shipping details until the session ends.

---

## 4) Agentic Loop (Description)

**Goal:** Convert user intent into helpful answers or completed actions (orders), while minimizing unnecessary tool calls and clarifying ambiguities quickly.

1. **Interpret**

   * Parse the latest user message in the context of conversation state.
   * Identify intent (informational Q\&A, availability check, price check, order creation, order status, comparison, or alternative suggestions).
   * Detect missing slots (e.g., product variant) and uncertainties.

2. **Plan**

   * Decide which tool(s) are required now versus after clarifications.
   * Prefer a single, most-informative tool call per step. Chain tools only when needed (e.g., find → inventory → pricing).

3. **Act (Tool Calling)**

   * Invoke the selected tool(s) via Gemini’s function-calling interface.
   * Include minimal, relevant arguments (derived from the user turn + session state).
   * Enforce guardrails (e.g., do not place orders without explicit confirmation).

4. **Observe**

   * Evaluate tool results for completeness, plausibility, and conflicts (e.g., price vs. discount policy).
   * If results are inconclusive or contradictory, branch to a clarification turn.

5. **Synthesize (Structured Output)**

   * Produce a terminal-friendly response with:

     * A clear, human-readable answer.
     * A compact action summary (“What I did”).
     * Optional next-step prompt if information is missing.

6. **Update State**

   * Store new facts relevant to the session (e.g., chosen product, contact info, shipping city, order ID).
   * Clear or revise state when the user pivots.

7. **Recover**

   * On tool failures or empty results, retry with adjusted parameters, request clarification, or propose alternatives.
   * Always provide a safe, understandable fallback response.

---

## 5) Tools (Descriptions)

> Each tool includes a purpose, when to use it, high-level inputs/outputs (conceptual only), and failure considerations.
> The demo should visibly log tool calls (name + short reason) so viewers can see the “agentic” behavior.

### A) Product Catalog: **SearchProducts**

* **Purpose:** Find products by name, keywords, category, or constraints (price band, features).
* **When:** User asks for options, comparisons, or can’t name a specific product; first step of most flows.
* **Inputs (conceptual):** Query text and optional filters.
* **Outputs (conceptual):** A shortlist of matching products with essential attributes for decision-making.
* **Failure considerations:** No matches, too many matches (ambiguity); propose refinement or categories.

### B) Product Catalog: **GetProductDetails**

* **Purpose:** Retrieve authoritative details for a specific product (description, variants, specs).
* **When:** The user references a specific product or the agent needs precise info for follow-up.
* **Inputs:** Product reference.
* **Outputs:** Canonical details sufficient to answer specs/feature questions and drive availability/price checks.
* **Failure considerations:** Stale references; prompt the user to confirm the exact product.

### C) Inventory: **CheckInventory**

* **Purpose:** Confirm availability, including variant-level stock.
* **When:** Before quoting availability/delivery or creating an order.
* **Inputs:** Product (and variant, if applicable).
* **Outputs:** Stock state (e.g., in stock/low stock/out of stock) with optional restock estimate.
* **Failure considerations:** Variant unspecified; guide the user to choose size/color; if out of stock, branch to alternatives.

### D) Pricing & Delivery: **EstimatePrice**

* **Purpose:** Compute a price estimate considering list price, discounts, taxes, and shipping to the user’s location.
* **When:** Before order confirmation or upon explicit price queries.
* **Inputs:** Product(s), quantity, destination city/country, and any discount context.
* **Outputs:** An itemized estimate and delivery time window (conceptually summarized in prose).
* **Failure considerations:** Missing address details or unsupported regions; request minimal info needed to proceed.

### E) Recommendations: **SuggestAlternatives**

* **Purpose:** Provide substitutes when a product is unavailable or doesn’t meet price/feature constraints.
* **When:** After a failed availability or price fit check.
* **Inputs:** The reference product and the constraint (e.g., “under X budget”).
* **Outputs:** A small set of alternatives with succinct differentiators.
* **Failure considerations:** No good substitutes; suggest broadening constraints.

### F) Orders: **CreateOrder**

* **Purpose:** Create an order after explicit user confirmation.
* **When:** The user indicates intent to buy and required details are known (product, variant, quantity, contact/shipping).
* **Inputs:** Product(s), quantities, selected variant(s), contact/shipping details, and any notes.
* **Outputs:** An order identifier and a simple human-readable confirmation summary.
* **Failure considerations:** Missing details; confirm step-by-step. If inventory changed between estimate and order, re-check.

### G) Orders: **GetOrderStatus**

* **Purpose:** Retrieve the current status of an existing order.
* **When:** User asks “where is my order?” or similar.
* **Inputs:** Order identifier (or minimal identifying info if allowed by the demo).
* **Outputs:** Current status with short explanation and any next steps.
* **Failure considerations:** Unknown ID; help the user recover (e.g., display how to find it in the previous confirmation).

---

## 6) Data Sources (Descriptions)

> The demo can back these with simple, local stores later; for now, this section defines **what** the agent relies on conceptually.

### 1) Product Catalog

* **Role:** Authoritative store of product names, categories, specs, short descriptions, and variant options.
* **Usage:** Power search, details lookup, comparisons, and recommendations.

### 2) Inventory Ledger

* **Role:** Current stock counts by product and variant; optional restock windows.
* **Usage:** Validate availability before confirming an order; inform backorder or alternative flow.

### 3) Pricing & Policy Rules

* **Role:** List prices, discount logic, tax rules, shipping fee logic, and delivery ETA heuristics.
* **Usage:** Provide transparent, consistent estimates; explain price components succinctly.

### 4) Order Ledger

* **Role:** Record of placed orders, lightweight status updates (e.g., received, packed, shipped, delivered).
* **Usage:** Return order IDs on creation and serve status queries later in the session.

---

## 7) Structured Output (Terminal Presentation)

* **Answer Section:** A concise, user-friendly explanation or result (e.g., availability, specs, or recommendation).
* **“What I Did” Panel:** One-line bullets listing tool calls and high-level outcomes (“Searched catalog”, “Checked inventory for Red/Medium”, “Estimated price with city X”).
* **Next Step / Prompt:** Minimal, direct asks to complete the task (e.g., “Which size would you like?” or “Shall I place the order with this estimate?”).
* **Notes for the Demo Host:** Ensure each turn visibly shows the reasoning trail via tool call summaries, not internal chain-of-thought.

---

## 8) Clarifications, Fallbacks, and Safety

* **Ambiguity Handling:** When the user mentions a product family without variants, the agent asks for the missing choice (size/color/capacity) before checking stock or placing an order.
* **Graceful Degradation:** If a tool times out or returns no data, the agent explains the issue simply, retries once with a narrower/broader query, or asks the user to refine the request.
* **Order Confirmation Gate:** The agent never places an order without explicit consent after presenting a price estimate and key details.
* **PII Minimization:** Collect only what’s needed to complete an order (e.g., name and shipping city); echo it back for confirmation in human-readable form.
* **Session Scope:** All memory is session-scoped and cleared at the end of the demo.

---

## 9) Demo Scenarios (for Acceptance)

1. **Simple Q\&A:** Ask for specs of a named product → agent fetches details and answers without unnecessary tools.
2. **Availability & Price:** Ask “Do you have Product X (blue, small) and how much to Karachi?” → agent checks inventory, estimates price and ETA, and presents a clear summary.
3. **Order Flow:** “Buy two of Product X in blue, small” → agent verifies availability, estimates price, confirms details, and returns an order ID.
4. **Out-of-Stock Recovery:** Request an unavailable variant → agent suggests top alternatives with brief reasons and can proceed to order one.
5. **Order Status:** Provide an order ID → agent returns the current status and a friendly explanation.

---

## 10) Observability (for the Demo)

* Log, per turn: detected intent, tools invoked (names only), terse justification for each call, and outcome summaries.
* Display a compact tool-call breadcrumb in the terminal so viewers can see the agentic loop at work without exposing raw schemas.

---

## 11) Assumptions & Constraints

* Single-user, single-session terminal demo.
* Gemini model with function-calling enabled.
* No external payments or sensitive data handling beyond minimal shipping/contact info.
* Network access for tools is optional; mock data sources are acceptable for the demo as long as behavior matches the descriptions above.

---

**End of PRD**
