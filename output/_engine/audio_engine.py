"""Audio engine dùng chung: SFX + nhạc tự tổng hợp (epic / cute / tense), ducking theo giọng, SRT không có tên nhân vật.\n   build(E, SFX, MUSIC): E = cute_engine đã configure; SFX = [(scene, t, kind, dur, gain)]; MUSIC = [(style, start_s, end_s, gain)]"""
import os, sys, json, wave
import numpy as np

SR = 48000
rng = np.random.default_rng(11)


def tv(d):
    return np.arange(int(d * SR)) / SR


def lp(x, k):
    return np.convolve(x, np.ones(k) / k, mode="same") if k > 1 else x


def nz(n):
    return rng.uniform(-1, 1, n)


def norm(y):
    return y / (np.abs(y).max() + 1e-9)


def sfx(kind, d):
    t = tv(d)
    n = len(t)
    fade = np.minimum(1, np.minimum(t / 0.004, (d - t) / 0.03 + 1e-9))
    if kind == "boom":
        f = 70 * np.exp(-t * 3) + 38
        y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 3.5) + 0.3 * lp(nz(n), 20) * np.exp(-t * 12)
    elif kind == "whoosh":
        x = nz(n)
        y = lp(x - lp(x, 8), 3) * np.sin(np.pi * t / d) ** 2
    elif kind == "zap":
        y = np.sign(np.sin(2 * np.pi * (300 + 900 * rng.random(n)) * t)) * lp(nz(n), 2) * np.exp(-t * 4)
    elif kind == "shimmer":
        y = sum(np.sin(2 * np.pi * f * t + i) for i, f in enumerate((1047, 1319, 1568, 2093))) * np.sin(np.pi * t / d) / 4
    elif kind == "steps":
        y = np.zeros(n)
        for s in np.arange(0, d, 0.15):
            m = t >= s
            y[m] += np.sin(2 * np.pi * 180 * (t[m] - s)) * np.exp(-(t[m] - s) * 40)
    elif kind == "riser":
        f = 200 + 1600 * (t / d) ** 2
        x = nz(n)
        y = (0.5 * np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.5 * (x - lp(x, 5))) * (t / d) ** 1.5
    elif kind == "thud":
        y = np.sin(2 * np.pi * 60 * t) * np.exp(-t * 14) + 0.5 * lp(nz(n), 6) * np.exp(-t * 30)
    elif kind == "pop":
        f = 1000 * np.exp(-t * 20) + 400
        y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 26)
    elif kind == "meow":
        f0 = 560 + 300 * np.sin(np.pi * t / d) ** 0.8 - 140 * t / d
        ph = 2 * np.pi * np.cumsum(f0) / SR
        y = lp(sum(np.sin(k * ph) / k for k in range(1, 8)), 4) * np.sin(np.pi * t / d) ** 1.4
    elif kind == "yawn":
        f0 = 420 - 160 * t / d
        ph = 2 * np.pi * np.cumsum(f0) / SR
        y = lp(sum(np.sin(k * ph) / k for k in range(1, 6)), 8) * np.sin(np.pi * t / d) ** 2 * 0.7
    elif kind == "heart":
        y = np.zeros(n)
        for i, f in enumerate((784, 988, 1175, 1568)):
            s = i * 0.12
            m = t >= s
            y[m] += np.sin(2 * np.pi * f * (t[m] - s)) * np.exp(-(t[m] - s) * 6)
    elif kind == "chime":
        y = sum(np.sin(2 * np.pi * f * t) * np.exp(-t * 3) for f in (659, 784, 988, 1319)) / 4
    elif kind == "alarm":
        y = np.sign(np.sin(2 * np.pi * 1760 * t)) * (np.sin(2 * np.pi * 8 * t) > 0) * 0.5
    elif kind == "ding":
        y = np.sin(2 * np.pi * 1320 * t) * np.exp(-t * 5) + 0.4 * np.sin(2 * np.pi * 2640 * t) * np.exp(-t * 8)
    elif kind == "boing":
        f = 240 + 160 * np.sin(2 * np.pi * 9 * t) * np.exp(-t * 4)
        y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 5)
    elif kind == "slurp":
        f = 300 + 500 * (t / d)
        x = nz(n)
        y = (x - lp(x, 4)) * (0.5 + 0.5 * np.sin(2 * np.pi * 22 * t)) * np.sin(np.pi * t / d) + 0.3 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / d)
    elif kind == "huff":
        x = lp(nz(n), 12)
        y = x * np.exp(-t * 5) * np.sin(np.pi * np.minimum(1, t / 0.05))
    elif kind == "stamp":
        y = np.sin(2 * np.pi * 95 * t) * np.exp(-t * 22) + 0.35 * lp(nz(n), 4) * np.exp(-t * 40)
    elif kind == "flip":
        x = nz(n)
        y = (x - lp(x, 3)) * np.exp(-t * 18)
    else:
        raise ValueError(kind)
    return norm(y * fade)


def pluck(freq, d, decay=0.995):
    n = int(d * SR)
    p = int(SR / freq)
    buf = rng.uniform(-1, 1, p)
    out = np.zeros(n)
    for i in range(n):
        out[i] = buf[i % p]
        buf[i % p] = decay * 0.5 * (buf[i % p] + buf[(i + 1) % p])
    return out


def epic(d):
    """Pad trầm D thứ + trống timpani: hoành tráng giả, để xì hơi ở màn đen."""
    t = tv(d)
    pad = sum(np.sin(2 * np.pi * f * t) + 0.5 * np.sin(2 * np.pi * f * 2.003 * t) for f in (73.4, 110.0, 146.8, 174.6)) / 6
    pad *= np.minimum(1, t / 0.6) * (0.8 + 0.2 * np.sin(2 * np.pi * 0.5 * t))
    y = pad * 0.6
    beat = 60 / 84
    for s in np.arange(0, d, beat):
        tt = tv(0.5)
        hit = np.sin(2 * np.pi * (90 * np.exp(-tt * 6) + 55) * tt) * np.exp(-tt * 7)
        a = int(s * SR)
        y[a:a + len(hit)] += hit[: len(y) - a] * 0.7
    return norm(y)


def cute(d):
    """Ukulele gảy G–Em–C–D 108 BPM + chuông nhỏ."""
    beat = 60 / 108
    n = int(d * SR)
    y = np.zeros(n + SR)
    chords = [(196.0, 246.9, 293.7), (164.8, 196.0, 246.9), (130.8, 164.8, 196.0), (146.8, 185.0, 220.0)]
    cache = {}
    tt, bar = 0.0, 0
    while tt < d:
        ch = chords[bar % 4]
        for b in range(4):
            for k, f in enumerate(ch):
                key = (f, b % 2)
                if key not in cache:
                    cache[key] = pluck(f * 2, beat * 1.4) * (0.9 if b % 2 == 0 else 0.55)
                s = int((tt + b * beat + k * 0.02) * SR)
                seg = cache[key][: max(0, len(y) - s)]
                y[s:s + len(seg)] += seg * 0.3
            if b in (1, 3):
                bt = tv(0.3)
                bell = np.sin(2 * np.pi * ch[2] * 4 * bt) * np.exp(-bt * 12) * 0.12
                s = int((tt + b * beat + beat / 2) * SR)
                y[s:s + len(bell)] += bell[: max(0, len(y) - s)]
        tt += 4 * beat
        bar += 1
    return norm(y[:n])


def rd(p):
    with wave.open(p) as w:
        sr, ch, n = w.getframerate(), w.getnchannels(), w.getnframes()
        a = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float32) / 32768
    if ch > 1:
        a = a.reshape(-1, ch).mean(1)
    if sr != SR:
        a = np.interp(np.arange(0, len(a), sr / SR), np.arange(len(a)), a)
    return a


def wr(p, y):
    with wave.open(p, "w") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((np.clip(y, -1, 1) * 32767).astype(np.int16).tobytes())


def ts(s):
    ms = int(round(s * 1000))
    return "%02d:%02d:%02d,%03d" % (ms // 3600000, ms // 60000 % 60, ms // 1000 % 60, ms % 1000)


def tense(d):
    """Nhạc rón rén: pizzicato La thứ staccato 120 BPM."""
    beat = 60 / 120
    n = int(d * SR)
    y = np.zeros(n + SR)
    seq = [110.0, 0, 130.8, 0, 146.8, 0, 130.8, 123.5]
    cache = {}
    tt, i = 0.0, 0
    while tt < d:
        f = seq[i % len(seq)]
        if f:
            if f not in cache:
                cache[f] = pluck(f * 2, 0.25, 0.97)
            s0 = int(tt * SR)
            seg = cache[f][: max(0, len(y) - s0)]
            y[s0:s0 + len(seg)] += seg
        tt += beat / 2
        i += 1
    return norm(y[:n])


def build(E, SFX, MUSIC):
    AD = os.path.join(E.OUT, "audio")
    S = E.STARTS
    os.makedirs(os.path.join(AD, "sfx"), exist_ok=True)
    E.load_voice()
    N = int(E.TOTAL * SR)
    voice, fx, music = np.zeros(N + SR), np.zeros(N + SR), np.zeros(N + SR)
    ev = []
    for vid, sid, lt, spk, text in E.VOICE:
        a = norm(rd(os.path.join(AD, "voice", vid + ".wav"))) * 0.9
        s0 = int((S[sid] + lt) * SR)
        voice[s0:s0 + len(a)] += a[: len(voice) - s0]
        ev.append({"type": "voice", "id": vid, "character": spk, "voice": E.VOICE_NAME[spk], "start": round(S[sid] + lt, 3), "duration": round(len(a) / SR, 3), "text": text})
    for i, (sid, lt, kind, d, g) in enumerate(SFX):
        y = sfx(kind, d) * g
        name = "%02d_%s_%s.wav" % (i + 1, sid, kind)
        wr(os.path.join(AD, "sfx", name), y)
        s0 = int((S[sid] + lt) * SR)
        fx[s0:s0 + len(y)] += y[: len(fx) - s0]
        ev.append({"type": "sfx", "kind": kind, "start": round(S[sid] + lt, 3), "duration": d, "file": "audio/sfx/" + name, "source": "tổng hợp numpy"})
    gen = {"epic": epic, "cute": cute, "tense": tense}
    for style, a, b, g, *opt in MUSIC:     # opt[0] (tuỳ chọn): fade-out giây — quy trình v2: outro tắt dần 1,5 s
        m = gen[style](b - a)
        fi, fo = min(len(m) // 3, int(0.5 * SR)), min(len(m) // 2, int((opt[0] if opt else 0.6) * SR))
        m[:fi] *= np.linspace(0, 1, fi)
        m[-fo:] *= np.linspace(1, 0, fo)
        s0 = int(a * SR)
        music[s0:s0 + len(m)] += m[: len(music) - s0] * g
        ev.append({"type": "music", "style": style, "start": a, "end": b, "source": "nhạc gốc tổng hợp (%s)" % style})
    act = np.convolve((np.abs(voice) > 0.02).astype(float), np.ones(int(0.15 * SR)), mode="same") > 0
    gd = np.convolve(np.where(act, 0.4, 1.0), np.ones(int(0.1 * SR)) / int(0.1 * SR), mode="same")
    mix = norm((voice + fx * 0.9 + music * 0.32 * gd)[:N]) * 0.89
    wr(os.path.join(AD, "master.wav"), mix)
    json.dump(ev, open(os.path.join(AD, "audio_events.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    with open(os.path.join(E.OUT, "subtitle.srt"), "w", encoding="utf-8") as fh:
        for i, (a, b, text) in enumerate(E.cues(), 1):
            fh.write("%d\n%s --> %s\n%s\n\n" % (i, ts(a), ts(b), text))
    print("audio ok", E.TOTAL, len(ev))
