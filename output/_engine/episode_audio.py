"""Âm thanh dùng chung cho tập mới (từ EP23, 13/11/2026): SFX tự tổng hợp numpy + nhạc CC0 khoá SHA.

Gom phần đã chép tay ở ep20_audio … ep22_audio (tape, tick, heartbeat, purr, scratch, squeak) và thêm SFX đời thường
cho các tập hài: xèo, nước phun, ừng ực, bình cứu hỏa, chuông cửa, rắc, tách (máy ảnh), meo trầm, ho, xoảng, vỗ tay,
gõ phím, thông báo. Không tải gì; nhạc là file Owner đã cho tải (SHA khoá trong TRACKS của tập).

    import episode_audio as EA
    EA.install(EP_DIR, {'cute': (rel_path, sha256, title, author, url)})
    # MUSIC trong scenes: ('cute', t0, t1, vol); EA.OFFSETS['cute'] = [...] để nhạc chạy liền theo thời gian video
"""
import hashlib
import json
import os
import subprocess

import numpy as np

import audio_engine as A

SR = A.SR
_original = A.sfx
TRACKS, OFFSETS, _calls = {}, {}, {}
_EP = {'dir': None}


def _env(t, d, a=0.01, r=0.05):
    return np.minimum(1, t / a) * np.minimum(1, np.maximum(0, (d - t) / r))


def _noise(n, seed):
    return np.random.default_rng(seed).normal(0, 1, n)


def _lp(x, k):
    return np.convolve(x, np.ones(k) / k, 'same')


def episode_sfx(kind, d):
    t = np.arange(int(SR * d)) / SR
    n = len(t)
    env = _env(t, d)
    seed = 2023 + int(d * 100) + len(kind)
    if kind == 'sizzle':      # xèo: nhiễu cao lách tách
        x = _noise(n, seed)
        crack = (np.random.default_rng(seed).random(n) > 0.9993) * 6.0
        y = (x - _lp(x, 3)) * (0.6 + 0.4 * np.sin(2 * np.pi * 13 * t)) + _lp(crack, 2)
        return A.norm(y * env * np.exp(-t * 0.6))
    if kind == 'spray':       # nước phun/vòi: nhiễu dải giữa đều
        x = _noise(n, seed)
        return A.norm((_lp(x, 2) - _lp(x, 9)) * env)
    if kind == 'splash':
        x = _noise(n, seed)
        return A.norm((x - _lp(x, 6)) * np.exp(-t * 7) + 0.4 * np.sin(2 * np.pi * 90 * t) * np.exp(-t * 18))
    if kind == 'gulp':        # nước rút ừng ực: bong bóng cao độ tăng dần
        y = np.zeros(n)
        for k, s in enumerate(np.arange(0, d - 0.12, 0.22)):
            m = (t >= s) & (t < s + 0.14)
            tt = t[m] - s
            y[m] += np.sin(2 * np.pi * np.cumsum(180 + 900 * tt / 0.14 + 30 * k) / SR) * np.sin(np.pi * tt / 0.14)
        return A.norm(y)
    if kind == 'extinguisher':  # bình cứu hỏa: xì mạnh, ồ ạt
        x = _noise(n, seed)
        return A.norm((x - _lp(x, 2) * 0.5) * env * (0.8 + 0.2 * np.sin(2 * np.pi * 3 * t)))
    if kind == 'doorbell':    # đinh — đong
        y = np.zeros(n)
        for s, f in ((0.0, 988), (0.45, 784)):
            m = t >= s
            tt = t[m] - s
            y[m] += (np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(4 * np.pi * f * tt)) * np.exp(-tt * 3)
        return A.norm(y * env)
    if kind == 'crack':       # rắc: gãy giòn
        x = _noise(n, seed)
        y = (x - _lp(x, 2)) * np.exp(-t * 60) + 0.6 * np.sin(2 * np.pi * 140 * t) * np.exp(-t * 40)
        return A.norm(y)
    if kind == 'click':       # tách: màn trập máy ảnh (dấu hiệu "Mimi phán xét")
        x = _noise(n, seed)
        y = (x - _lp(x, 2)) * (np.exp(-t * 300) + 0.6 * np.exp(-np.maximum(0, t - 0.06) * 300) * (t > 0.06))
        return A.norm(y)
    if kind == 'meow_low':    # meo trầm, chán đời
        f0 = 330 + 90 * np.sin(np.pi * t / d) ** 0.8 - 90 * t / d
        ph = 2 * np.pi * np.cumsum(f0) / SR
        y = _lp(sum(np.sin(k * ph) / k for k in range(1, 9)), 5) * np.sin(np.pi * t / d) ** 1.2
        return A.norm(y)
    if kind == 'cough':       # ho khụ khụ
        y = np.zeros(n)
        for s in (0.0, 0.32):
            m = (t >= s) & (t < s + 0.22)
            tt = t[m] - s
            y[m] += _lp(_noise(m.sum(), seed + int(s * 10)), 5) * np.exp(-tt * 14) + 0.5 * np.sin(2 * np.pi * 150 * tt) * np.exp(-tt * 20)
        return A.norm(y)
    if kind == 'crash':       # xoảng: cốc sứ vỡ — nhiễu cao + nhiều tông leng keng
        x = _noise(n, seed)
        y = (x - _lp(x, 2)) * np.exp(-t * 9)
        rng = np.random.default_rng(seed)
        for _ in range(9):
            s, f = rng.uniform(0, 0.35), rng.uniform(2500, 6000)
            m = t >= s
            y[m] += 0.5 * np.sin(2 * np.pi * f * (t[m] - s)) * np.exp(-(t[m] - s) * 25)
        return A.norm(y)
    if kind == 'clap':        # vỗ tay đồng loạt
        y = np.zeros(n)
        rng = np.random.default_rng(seed)
        for s in np.sort(rng.uniform(0, max(0.05, d - 0.1), int(d * 22))):
            m = (t >= s) & (t < s + 0.05)
            y[m] += (rng.normal(0, 1, m.sum())) * np.exp(-(t[m] - s) * 80)
        return A.norm(y * env)
    if kind == 'typing':      # gõ phím lách cách
        y = np.zeros(n)
        rng = np.random.default_rng(seed)
        s = 0.0
        while s < d - 0.03:
            m = (t >= s) & (t < s + 0.03)
            y[m] += rng.normal(0, 1, m.sum()) * np.exp(-(t[m] - s) * 200)
            s += rng.uniform(0.06, 0.16)
        return A.norm(y)
    if kind == 'notif':       # thông báo tin nhắn: 2 nốt lên
        y = np.zeros(n)
        for s, f in ((0.0, 1175), (0.11, 1568)):
            m = t >= s
            y[m] += np.sin(2 * np.pi * f * (t[m] - s)) * np.exp(-(t[m] - s) * 12)
        return A.norm(y)
    if kind == 'tick':        # tích tắc 0,5 s
        y = np.zeros(n)
        for k, s in enumerate(np.arange(0, d, 0.5)):
            m = t >= s
            y[m] += np.sin(2 * np.pi * (2400 if k % 2 else 1800) * (t[m] - s)) * np.exp(-(t[m] - s) * 300)
        return A.norm(y)
    if kind == 'heartbeat':
        y = np.zeros(n)
        for s in np.arange(0, d, 0.62):
            for o, a in ((0, 1.0), (0.16, 0.7)):
                m = t >= s + o
                tt = t[m] - s - o
                y[m] += a * np.sin(2 * np.pi * (60 + 30 * np.exp(-tt * 20)) * tt) * np.exp(-tt * 14)
        return A.norm(y)
    if kind == 'purr':
        x = _lp(_noise(n, seed), 60)
        y = x * (0.6 + 0.4 * np.sin(2 * np.pi * 25 * t)) * (0.7 + 0.3 * np.sin(2 * np.pi * t / 1.4))
        return A.norm(y * env) * 0.8
    if kind == 'scratch':     # rít đĩa than (khựng hình)
        f = 300 + 900 * np.abs(np.sin(2 * np.pi * 3.5 * t))
        y = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * 0.5 + 0.5 * _noise(n, seed)
        return A.norm(_lp(y, 3) * env)
    if kind == 'squeak':
        y = np.sin(2 * np.pi * np.cumsum(1500 + 900 * np.sin(np.pi * t / d)) / SR)
        return A.norm(y * np.sin(np.pi * t / d) ** 0.5)
    if kind == 'tada':        # "ta-da" kèn đồ chơi: hai hợp âm
        y = np.zeros(n)
        for s, fs in ((0.0, (523, 659, 784)), (0.18, (659, 784, 1047))):
            m = t >= s
            tt = t[m] - s
            for f in fs:
                ph = 2 * np.pi * f * tt
                y[m] += (np.sin(ph) + 0.4 * np.sin(2 * ph) + 0.2 * np.sin(3 * ph)) * np.exp(-tt * (2.5 if s else 9))
        return A.norm(y * env)
    if kind == 'scream':      # thét câm (Ngang) — tiếng rít mỏng cao độ trượt, không phải giọng người
        f = 900 + 500 * np.sin(np.pi * t / d)
        y = np.sin(2 * np.pi * np.cumsum(f) / SR) * (0.7 + 0.3 * np.sin(2 * np.pi * 11 * t))
        return A.norm(y * np.sin(np.pi * t / d) ** 0.7) * 0.7
    # EP29 (19/11/2026): máy tính tiền, violin bi kịch, chim hót, cánh bướm, gió hiu hiu
    if kind == 'cash':        # "ka-ching" lặp: tiếng tách cơ khí + chuông cao
        y = np.zeros(n)
        for s in np.arange(0, max(0.01, d - 0.3), 0.32):
            m = t >= s
            tt = t[m] - s
            y[m] += 0.5 * _noise(m.sum(), seed + int(s * 100)) * np.exp(-tt * 120)
            for f in (2093, 2637):
                y[m] += np.sin(2 * np.pi * f * np.maximum(0, tt - 0.06)) * np.exp(-np.maximum(0, tt - 0.06) * 9) * (tt > 0.06)
        return A.norm(y * env)
    if kind == 'sad_violin':  # violin bi kịch: nốt trượt xuống có rung
        f = 660 * 2 ** (-np.minimum(t, d) / max(d, 0.1) * 0.6) * (1 + 0.012 * np.sin(2 * np.pi * 5.5 * t))
        ph = 2 * np.pi * np.cumsum(f) / SR
        y = np.sin(ph) + 0.5 * np.sin(2 * ph) + 0.3 * np.sin(3 * ph) + 0.15 * np.sin(4 * ph)
        return A.norm(y * env * np.minimum(1, t / 0.15))
    if kind == 'birds':       # chim hót: chuỗi tiếng líu lo cao độ trượt
        y = np.zeros(n)
        rng = np.random.default_rng(seed)
        for s in np.arange(0, max(0.01, d - 0.12), 0.18):
            m = (t >= s) & (t < s + 0.09)
            tt = t[m] - s
            f0 = 2800 + 900 * rng.random()
            y[m] += np.sin(2 * np.pi * np.cumsum(f0 + 1800 * tt / 0.09) / SR) * np.sin(np.pi * tt / 0.09)
        return A.norm(y * env) * 0.6
    if kind == 'flutter':     # cánh bướm phạch phạch: nhiễu điều biên nhanh
        x = _lp(_noise(n, seed), 4)
        return A.norm(x * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 14 * t))) * env) * 0.7
    if kind == 'wind':        # gió hiu hiu: nhiễu trầm dâng hạ
        x = _lp(_noise(n, seed), 40)
        return A.norm(x * (0.6 + 0.4 * np.sin(np.pi * t / max(d, 0.1))) * env) * 0.6
    return _original(kind, d)


def _loader(style):
    def load(d):
        rel, sha, *_ = TRACKS[style]
        src = os.path.join(_EP['dir'], rel)
        h = hashlib.sha256(open(src, 'rb').read()).hexdigest()
        if h != sha:
            raise SystemExit('CHẶN: file nhạc khác SHA đã khoá (%s)' % h)
        i = _calls[style]
        _calls[style] += 1
        offs = OFFSETS.get(style, [0.0])
        off = offs[min(i, len(offs) - 1)]
        wav = os.path.join(_EP['dir'], 'audio', 'music', '%s_seg%d.wav' % (style, i))
        # Bài học EP27 (19/11/2026): bản nhạc ngắn hơn video (22,5 s) -> -ss vượt độ dài file = im lặng.
        # Lặp vô hạn (-stream_loop -1) và quy offset về trong độ dài bản nhạc.
        dur_src = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', src],
                                       capture_output=True, text=True, check=True).stdout.strip() or 0) or 1e9
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-stream_loop', '-1', '-ss', '%.3f' % (off % dur_src), '-t', str(d + 0.5),
                        '-i', src, '-ac', '1', '-ar', str(SR), wav], check=True)
        m = A.rd(wav)[:int(d * SR)]
        m = np.pad(m, (0, max(0, int(d * SR) - len(m))))
        return A.norm(m) * 1.6
    return load


def install(ep_dir, tracks):
    """Gắn SFX mở rộng + nhạc CC0 khoá SHA vào audio_engine cho tập ep_dir. tracks: {style: (rel, sha, title, author, url)}."""
    _EP['dir'] = ep_dir
    TRACKS.clear()
    TRACKS.update(tracks)
    A.sfx = episode_sfx
    for st in TRACKS:
        _calls[st] = 0
        OFFSETS.setdefault(st, [0.0])
        setattr(A, st, _loader(st))
    build = A.build if not hasattr(A, '_nmt_orig_build') else A._nmt_orig_build
    A._nmt_orig_build = build

    def episode_build(E, SFX, MUSIC):
        for k in _calls:
            _calls[k] = 0
        build(E, SFX, MUSIC)
        p = os.path.join(E.OUT, 'audio', 'audio_events.json')
        ev = json.load(open(p, encoding='utf-8'))
        cnt = {k: 0 for k in TRACKS}
        for e in ev:
            if e.get('type') == 'music' and e.get('style') in TRACKS:
                st = e['style']
                rel, sha, title, author, url = TRACKS[st]
                offs = OFFSETS.get(st, [0.0])
                off = offs[min(cnt[st], len(offs) - 1)]
                cnt[st] += 1
                e.update({'style': 'file', 'file': rel, 'title': title, 'author': author, 'url': url, 'license': 'CC0 1.0',
                          'sha256': sha, 'offset_s': off, 'source': 'Freesound CC0 (bản preview HQ công khai, Owner cho tải)'})
        json.dump(ev, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

    A.build = episode_build
