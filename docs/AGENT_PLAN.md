## Minimal Agent Loop (Simplified)

### Prerequisites
- Gemini client is initialized.
- Tools are implemented and bound to the model.
- A short system prompt is defined (tone, safety, confirmation rule).

### Session Memory (Simple)
- `history`: list of prior user/assistant turns.
- `context` (optional): lastEstimate, lastOrderId.

### Loop
1) Greet once, then prompt for input using `input()`.
2) Send the user message to Gemini with:
   - system prompt
   - chat history
   - tool bindings enabled
3) If Gemini requests tool calls, execute them and stream results back to Gemini until a final text response is produced.
4) Print Gemini’s final response to the terminal.
5) Append both user message and assistant response to history.
6) Repeat from step 1 until the user types `exit`/`quit` or presses Ctrl+C.

### Safety (Minimal)
- Do not call `CreateOrder` unless the user confirms after seeing a price estimate.
- Ask only for city/country when pricing is needed; avoid extra PII.

### Observability (Optional)
- Print a compact "What I did" line listing any tools invoked.
- Log errors concisely; retry a failed tool once, otherwise ask the user to refine.

### Pseudocode
```python
print("Welcome to ShopTalk! Ask about products or place simple orders.")
history = []
while True:
    user = input("> ").strip()
    if user.lower() in {"exit", "quit"}:
        break
    response = gemini.chat(
        system=SYSTEM_PROMPT,
        history=history,
        tools=BOUND_TOOLS,
        message=user,
    )
    # Handle tool calls until final text
    while response.requires_tool_call:
        tool_result = run_tool(response.tool_name, response.tool_args)
        response = gemini.resume(tool_result)
    print(response.text)
    history.append({"role": "user", "content": user})
    history.append({"role": "assistant", "content": response.text})
```


