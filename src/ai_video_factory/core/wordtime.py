# -*- coding: utf-8 -*-
"""Uoc luong thoi diem tung tu trong MOT cau da doc (A07), tu chinh am thanh cua cau do.

Khong phai can chinh cuong buc (forced alignment): khong co Whisper trong MVP. Cach lam: (1) tim cac quang lang ben trong cau tu
bao nang luong; (2) chia deu theo trong so am tiet tren truc thoi gian CO TIENG (bo qua quang lang); (3) hieu chinh moi ranh gioi
tu ve cho nang luong thap nhat gan do (am tiet thuong co thung lung nang luong o giua cac tu). Sai so thuc te chua do duoc bang
du lieu goc; nguoi xem danh gia."""
import re

import numpy as np

_VOWELS = re.compile(r"[aeiouyAEIOUY]+")


def syllables(word, code):
    w = re.sub(r"[^\w]", "", word)
    if not w:
        return 0.5
    if code == "vi":
        return 1.0 + (0.25 if len(w) >= 6 else 0.0)   # tieng Viet: moi tu ~ mot am tiet
    n = len(_VOWELS.findall(w.lower()))
    if w.lower().endswith("e") and n > 1 and not w.lower().endswith(("le", "ee")):
        n -= 1
    return float(max(1, n))


def envelope(x, rate, hop_s=0.01):
    hop = max(1, int(rate * hop_s))
    n = len(x) // hop
    if n == 0:
        return np.zeros(1, dtype=np.float32), hop_s
    e = np.sqrt(np.mean(x[:n * hop].reshape(n, hop) ** 2, axis=1))
    k = np.ones(3) / 3.0
    return np.convolve(e, k, mode="same").astype(np.float32), hop_s


def estimate(x, rate, words, code="vi", min_pause_s=0.11):
    """words: list chuoi. Tra ve list (start_s, end_s) tuong doi dau mang x, dung thu tu, khong chong len nhau."""
    n = len(words)
    total = len(x) / float(rate)
    if n == 0:
        return []
    env, hop = envelope(x, rate)
    if n == 1 or env.max() <= 0:
        return [(0.0, total)] if n == 1 else [(total * i / n, total * (i + 1) / n) for i in range(n)]
    ref = float(np.percentile(env, 90))
    voiced = env > 0.12 * ref
    # quang lang ben trong (bo dau/cuoi)
    pauses, i, m = [], 0, len(voiced)
    first = int(np.argmax(voiced)) if voiced.any() else 0
    last = m - 1 - int(np.argmax(voiced[::-1])) if voiced.any() else m - 1
    while i < m:
        if not voiced[i] and first < i < last:
            j = i
            while j < m and not voiced[j]:
                j += 1
            if (j - i) * hop >= min_pause_s and j <= last:
                pauses.append((i, j))
            i = j
        else:
            i += 1
    # truc co tieng: ban do chi so khung tho -> chi so khung co tieng (bo quang lang)
    keep = np.ones(m, dtype=bool)
    for a, b in pauses:
        keep[a:b] = False
    keep[:first] = False
    keep[last + 1:] = False
    vidx = np.where(keep)[0]
    if len(vidx) < n:
        return [(total * i / n, total * (i + 1) / n) for i in range(n)]
    wts = np.array([syllables(w, code) for w in words], dtype=np.float64)
    cum = np.concatenate([[0.0], np.cumsum(wts)])
    cum /= cum[-1]
    # ranh gioi tu trong truc co tieng (chi so vao vidx)
    bidx = np.rint(cum * (len(vidx) - 1)).astype(int)
    frames = vidx[bidx]                         # khung tho cua ranh gioi (n + 1 gia tri)
    frames = frames.astype(float)
    # hieu chinh: ve cho nang luong thap nhat gan ranh gioi trong (khong ra ngoai 40% do dai tu hai ben)
    for k in range(1, n):
        wl = frames[k] - frames[k - 1]
        wr = frames[k + 1] - frames[k]
        reach = int(max(1, min(0.4 * wl, 0.4 * wr, 8)))
        c = int(round(frames[k]))
        lo, hi = max(1, c - reach), min(m - 2, c + reach)
        if hi > lo:
            seg = env[lo:hi + 1]
            frames[k] = lo + int(np.argmin(seg))
    frames[0] = first
    frames[-1] = last + 1
    for k in range(1, n + 1):                   # don dieu
        frames[k] = max(frames[k], frames[k - 1] + 1)
    out = []
    for k in range(n):
        a = frames[k] * hop
        b = frames[k + 1] * hop
        out.append((round(min(a, total), 3), round(min(max(b, a + 0.02), total), 3)))
    # moc tu khong duoc roi vao quang lang: dau tu doi ra cuoi quang lang, cuoi tu doi ve dau quang lang
    pset = [(a * hop, b * hop) for a, b in pauses]
    fixed = []
    for a, b in out:
        for pa, pb in pset:
            if pa < a < pb:
                a = pb
            if pa < b <= pb:
                b = pa
            elif a < pa and b > pb:
                b = pa
        fixed.append((a, max(b, a + 0.03)))
    return [(round(a, 3), round(b, 3)) for a, b in fixed]
