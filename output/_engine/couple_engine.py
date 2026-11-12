"""Compatibility launcher for the former couple-engine name.
Canonical CLI: python3 output/_engine/nmt_engine.py list|status|new "<chủ đề>".
"""
from nmt_engine import ENGINE, OUTPUT, TEMPLATE, episodes, main, new, status  # noqa: F401

if __name__ == "__main__":
    main()
