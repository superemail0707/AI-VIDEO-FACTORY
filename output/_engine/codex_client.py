"""Gọi Codex App Server trực tiếp từ Python (D-029) — dùng lại lớp AppServer của `.claude/codex-bridge/server.py`.

Mỗi lần gọi là một phiên ephemeral mới (giám khảo không thấy lịch sử; mỗi tranh một phiên). Bridge không bị sửa.
Test thay `RUNNER` bằng hàm giả để không tiêu lượt Codex.
"""
import asyncio
import importlib.util
import json
import os
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BRIDGE = ROOT / ".claude" / "codex-bridge" / "server.py"
MODES = ("read-only", "workspace-write")


class CodexUnavailable(RuntimeError):
    """Codex không trả lời được: hết lượt, chưa đăng nhập, quá giờ, lỗi tiến trình."""


def _bridge():
    spec = importlib.util.spec_from_file_location("avf_codex_bridge", BRIDGE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _default_runner(prompt, mode, timeout):
    mod = _bridge()
    return asyncio.run(asyncio.wait_for(mod.AppServer().run(prompt, mode), timeout))


RUNNER = _default_runner


def ask(prompt, mode="read-only", timeout=180):
    """Trả {'thread_id','turn_id','answer','seconds'}; lỗi -> CodexUnavailable."""
    if mode not in MODES:
        raise ValueError("mode phải là read-only hoặc workspace-write")
    if not isinstance(timeout, int) or not 15 <= timeout <= 600:
        raise ValueError("timeout 15–600 s")
    t0 = time.time()
    try:
        res = RUNNER(prompt, mode, timeout)
    except (RuntimeError, asyncio.TimeoutError, OSError) as exc:
        raise CodexUnavailable(str(exc) or "Codex quá giờ") from exc
    if not isinstance(res, dict) or "answer" not in res:
        raise CodexUnavailable("Codex trả kết quả không hợp lệ")
    res = dict(res)
    res["seconds"] = round(time.time() - t0, 1)
    return res


def extract_json(text):
    """Lấy object JSON cuối cùng trong câu trả lời (chấp nhận khối ```json```). Không tìm thấy -> ValueError."""
    if not isinstance(text, str):
        raise ValueError("không có câu trả lời")
    dec = json.JSONDecoder()
    found, i = None, text.find("{")
    while i != -1:
        try:
            obj, end = dec.raw_decode(text[i:])
        except ValueError:
            i = text.find("{", i + 1)
            continue
        if isinstance(obj, dict):
            found = obj          # object cấp ngoài; nhảy qua toàn bộ để không lấy object con
        i = text.find("{", i + end)
    if found is None:
        raise ValueError("không tìm thấy JSON trong câu trả lời")
    return found


def available():
    """Kiểm nhanh có Codex CLI và bridge không (không gọi mạng)."""
    exe = os.environ.get("CODEX_BRIDGE_EXECUTABLE", "/opt/homebrew/bin/codex")
    return BRIDGE.exists() and os.path.exists(exe)
