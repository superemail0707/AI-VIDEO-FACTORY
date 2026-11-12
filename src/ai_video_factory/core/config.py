"""Cau hinh MVP. Moi duong dan ghi ra nam trong workspace/ (ngoai Git)."""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
WORKSPACE = Path(os.environ.get("AVF_WORKSPACE", ROOT / "workspace"))
RUNS_DIR = WORKSPACE / "runs"

OLLAMA_URL = "http://127.0.0.1:11434"  # chi localhost
LLM_MODEL = os.environ.get("AVF_LLM_MODEL", "qwen3:4b-q4_K_M")
LLM_MODEL_STRONG = os.environ.get("AVF_LLM_MODEL_STRONG", "qwen3:8b-q4_K_M")   # Athena/Leonardo: noi dung va kiem tra su that

# TTS: "vieneu" (Owner chon giong Ngoc Huyen, thu nghiem noi bo) hoac "say" (macOS Linh, du phong)
VIENEU_HOME = Path(os.environ.get("AVF_VIENEU_HOME", ROOT / "workspace"))   # moi truong TTS dung chung, khong theo workspace tam cua test
VIENEU_PYTHON = Path(os.environ.get("AVF_VIENEU_PYTHON", str(VIENEU_HOME / "venv-vieneu" / "bin" / "python")))   # ghi de: chay thu ngoai macOS
VIENEU_VOICE = os.environ.get("AVF_VIENEU_VOICE", "Ngọc Huyền")
TTS_ENGINE = os.environ.get("AVF_TTS", "vieneu" if VIENEU_PYTHON.exists() else "say")

FPS = 24
WIDTH = 1920
HEIGHT = 1080
VOICE = "Linh"
VIENEU_TEMPERATURE = float(os.environ.get("AVF_VIENEU_TEMP", "1.0"))   # cao hon 0.8 mac dinh: giong bieu cam hon
SAY_RATE = int(os.environ.get("AVF_SAY_RATE", "140"))   # tu/phut cua say; mac dinh he thong ~3.15 tu/giay la qua nhanh
SENTENCE_GAP_S = 0.38
SCENE_GAP_S = 0.70
LEAD_S = 1.8      # tieu de dau video, chua co loi dan
TAIL_S = 1.6
TRANSITION_FRAMES = 14
SAMPLE_RATE = 48000     # VieNeu xuat 48 kHz; say duoc dat cung toc do lay mau

FONT_REGULAR = "/System/Library/Fonts/Supplemental/Arial.ttf"
FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

MIN_DURATION_S = 45.0   # Owner: video 45-90 giay
MAX_DURATION_S = 90.0
MIN_FREE_DISK_GB = 5.0

# Khai bao cac buoc la stub / thay the (ghi vao render_report.json)
DECLARED_STUBS = [
    "Tesla: STUB - chi tao publish_package.json, KHONG dang len dau",
    "Newton: STUB - bao cao tu log cua run, khong co du lieu nen tang",
    "Pixar: lip-sync theo bien do am thanh (khong co viseme)",
    "Pixar/Spielberg: ve bang Pillow tu scene spec, khong rasterize SVG (lech D-012/D-013, MVP)",
    "Athena: khong dung web, chi kien thuc cua mo hinh, chua kiem chung",
    "Leonardo: storyboard (bo cuc) sinh bang quy tac, khong phai LLM",
    "Edison: giong tong hop VieNeu v3 Turbo (Ngoc Huyen, Owner chon) hoac macOS say (du phong); chi thu nghiem noi bo, nhom A ve license, chua duoc cap phep thuong mai",
    "Spielberg: minh hoa la thu vien hinh ve vector 2D hoat dong bang Pillow (khong phai anh/AI sinh anh)",
    "Font Arial cua macOS cho phu de va chu bang trang, chi noi bo",
    "Factory Manager: chay tuan tu bang tep, khong co hang doi SQLite, API hay dashboard",
]


def fast():
    """Che do nhanh: bo cac buoc LLM phu (tu kiem tra Athena, soat loi Leonardo). Dat bang --fast hoac AVF_FAST=1."""
    return os.environ.get("AVF_FAST") == "1"
