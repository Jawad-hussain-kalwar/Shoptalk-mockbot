"""Entry-point script.

Purpose: keep top-level clean and delegate to the agent package.
- The agent REPL and wiring live in `agent/runner.py`.
- This file only starts the demo agent.
- In future this agent can be exposed via API to be consumed by the frontend
"""

from agent import run


if __name__ == "__main__":
    run()


