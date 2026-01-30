"""
Entry point for NoKeyFinance.

Run the Streamlit dashboard from project root with:
  streamlit run finance_app/main.py

Or:
  python -m finance_app.main
"""
from __future__ import annotations

import sys


def main() -> None:
    """Launch the Streamlit dashboard."""
    from finance_app.visualization.dashboard import run
    run()


if __name__ == "__main__":
    # When run as "python -m finance_app.main", __package__ is set; launch streamlit so the app runs.
    # When run as "streamlit run finance_app/main.py", streamlit executes this file and we render the app.
    if __package__:
        import os
        import subprocess
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        result = subprocess.run(
            [sys.executable, "-m", "streamlit", "run", os.path.abspath(__file__), "--"],
            cwd=project_root,
        )
        sys.exit(result.returncode)
    else:
        main()
