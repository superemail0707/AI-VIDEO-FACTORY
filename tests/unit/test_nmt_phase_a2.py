# -*- coding: utf-8 -*-
"""Giai đoạn A2 (D-029): chấm kịch bản tự động, tự duyệt cổng kịch bản, tạo tranh tự động. Codex được giả lập."""
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import numpy as np
from PIL import Image

ENGINE = Path(__file__).resolve().parents[2] / "output" / "_engine"
sys.path.insert(0, str(ENGINE))

import art_auto as AA  # noqa: E402
import codex_client as C  # noqa: E402
import gates as G  # noqa: E402
import script_review as SR  # noqa: E402

IDEATION = {"concepts": [
    {"name": "Ghế của boss", "type": "A", "score": 86, "logline": "l", "hook": "h", "twist": "t"},
    {"name": "Mimi tên lửa", "type": "B", "score": 78, "logline": "l", "hook": "h", "twist": "t"},
    {"name": "Điều tra ghế", "type": "C", "score": 80, "logline": "l", "hook": "h", "twist": "t"}],
    "chosen": "Ghế của boss", "reason": "twist hình ảnh mạnh nhất"}
GOOD_META = {"title": "Thử", "brief": "Tí giành chỗ của Mimi", "logline": "x", "notes": {"F01": "Mimi chiếm ghế"},
             "duration_s": [25, 32], "ideation": IDEATION, "comedy": {"main": "role_reversal", "support": ["deadpan"]},
             "twist_seed": "vương miện nhỏ trên ghế ở cảnh đầu", "visual_styles": ["A", "B"]}
SCENES = [("F01", 6.0, "Mở", "cut", 0.0), ("F02", 8.0, "Leo thang", "cut", 0.0), ("F03", 14.0, "Chốt", "cut", 0.0)]
STARTS = {"F01": 0.0, "F02": 6.0, "F03": 14.0}
VOICE = [("V1", "F01", 0.05, "ti", "Ơ, ghế của anh mà!"), ("V2", "F03", 0.35, "ngang", "Ghế của boss rồi anh.")]
CRIT_HIGH = {"hook": 1.5, "visual_comedy": 2, "twist": 2, "escalation": 1, "relatable": 1, "character_brief": 1, "producible": 1}
CRIT_MID = {"hook": 1.5, "visual_comedy": 1.5, "twist": 1.5, "escalation": 1, "relatable": 1, "character_brief": 1, "producible": 1}  # 8.5
CRIT_NINE = {"hook": 1.5, "visual_comedy": 2, "twist": 1.5, "escalation": 1, "relatable": 1, "character_brief": 1, "producible": 1}  # 9.0
CRIT_LOW = {"hook": 1, "visual_comedy": 1, "twist": 1, "escalation": 1, "relatable": 0.5, "character_brief": 1, "producible": 1}


def viewer_obj(yes_all=True, no=()):
    roles = []
    for r in range(3):
        roles.append({"role": "vai %d" % r, "answers": [{"q": q, "yes": yes_all and (r, q) not in no, "why": "-"}
                                                        for q in range(1, 9)]})
    return {"roles": roles, "fixes": ["x"], "score": 99, "pass": True}   # score/pass tự khai bị bỏ qua


def judge(crit, claimed_total=None):
    obj = {"criteria": crit, "reasons": {}, "fixes": ["Thêm nhịp 2"]}
    if claimed_total is not None:
        obj["total"] = claimed_total
    return lambda prompt: {"judge": "codex", "thread_id": "t1", "raw": json.dumps(obj), "obj": obj, "seconds": 1.0}


class CodexClientTests(unittest.TestCase):
    def test_extract_json_outer_object_and_fence(self):
        txt = 'Kết quả:\n```json\n{"criteria": {"hook": 2}, "fixes": []}\n```'
        self.assertEqual(C.extract_json(txt)["criteria"], {"hook": 2})
        with self.assertRaises(ValueError):
            C.extract_json("không có json")

    def test_ask_wraps_errors_and_validates(self):
        with mock.patch.object(C, "RUNNER", side_effect=RuntimeError("usage limit")):
            with self.assertRaises(C.CodexUnavailable):
                C.ask("x")
        with mock.patch.object(C, "RUNNER", return_value={"answer": "ok", "thread_id": "t"}):
            self.assertEqual(C.ask("x")["answer"], "ok")
        with self.assertRaises(ValueError):
            C.ask("x", mode="danger-full-access")


class HardRuleTests(unittest.TestCase):
    def test_good_script_passes(self):
        self.assertEqual(SR.hard_rules(GOOD_META, VOICE, SCENES, STARTS), [])

    def test_each_rule(self):
        cases = [
            ([("V1", "F01", 0.05, "ti", "x" * 46)], GOOD_META, "ký tự"),
            ([("V1", "F01", 0.05, "mimi", "Meo")], GOOD_META, "Mimi"),
            ([("V1", "F01", 0.05, "ngang", "Cú twist: đại sư chỉ ngủ!")], GOOD_META, "nhãn cấu trúc"),
            (VOICE, dict(GOOD_META, logline="TODO"), "TODO"),
            (VOICE, dict(GOOD_META, brief="", logline=""), "brief"),
            (VOICE, dict(GOOD_META, assets=[{"name": "nhạc X"}]), "giấy phép"),
        ]
        for voice, meta, needle in cases:
            errs = SR.hard_rules(meta, voice, SCENES, STARTS)
            self.assertTrue(any(needle in e for e in errs), (needle, errs))

    def test_duration_and_hook(self):
        long_sc = [("F01", 30.0, "a", "cut", 0), ("F02", 30.0, "b", "cut", 0)]
        self.assertTrue(any("thời lượng" in e for e in SR.hard_rules(GOOD_META, VOICE, long_sc, {"F01": 0, "F02": 30})))
        self.assertEqual([e for e in SR.hard_rules(dict(GOOD_META, duration_s=[55, 65]), VOICE, long_sc,
                                                   {"F01": 0, "F02": 30}) if "thời lượng" in e], [])
        for bad in (None, "TODO", [55]):   # D-030: bắt buộc khai thời lượng theo topic, mọi loại video
            meta = {k: v for k, v in GOOD_META.items() if k != "duration_s"}
            if bad is not None:
                meta["duration_s"] = bad
            self.assertTrue(any("duration_s" in e for e in SR.hard_rules(meta, VOICE, SCENES, STARTS)), bad)
        no_hook = dict(GOOD_META, notes={})
        late = [("V1", "F01", 2.5, "ti", "Muộn quá")]
        self.assertTrue(any("hook" in e for e in SR.hard_rules(no_hook, late, SCENES, STARTS)))


class IdeationRuleTests(unittest.TestCase):
    """Agent V2.0: 3 concept A/B/C có điểm, chọn đúng, cơ chế hài ≤ 1 + 2, gieo twist, style A–G."""

    def errs(self, **over):
        import copy
        meta = copy.deepcopy(GOOD_META)
        meta.update(over)
        return SR.ideation_rules(meta)

    def test_good(self):
        self.assertEqual(self.errs(), [])

    def test_violations(self):
        import copy
        two = copy.deepcopy(IDEATION); two["concepts"] = two["concepts"][:2]
        same_type = copy.deepcopy(IDEATION); same_type["concepts"][2]["type"] = "A"
        low_pick = copy.deepcopy(IDEATION); low_pick["chosen"] = "Mimi tên lửa"
        combined = copy.deepcopy(low_pick); combined["combined"] = True
        no_twist = copy.deepcopy(IDEATION); no_twist["concepts"][0]["twist"] = ""
        cases = [({"ideation": None}, "ideation"), ({"ideation": two}, "đúng 3"), ({"ideation": same_type}, "A (relatable)"),
                 ({"ideation": low_pick}, "điểm cao nhất"), ({"ideation": no_twist}, "thiếu twist"),
                 ({"comedy": {"main": "slapstick"}}, "comedy']['main"),
                 ({"comedy": {"main": "callback", "support": ["deadpan", "escalation", "rule_of_three"]}}, "tối đa 2"),
                 ({"twist_seed": ""}, "twist_seed"), ({"visual_styles": ["A", "B", "C", "D"]}, "visual_styles"),
                 ({"visual_styles": ["S1"]}, "visual_styles")]
        for over, needle in cases:
            self.assertTrue(any(needle in e for e in self.errs(**over)), (over, self.errs(**over)))
        self.assertEqual(self.errs(ideation=combined), [])


class JudgementTests(unittest.TestCase):
    def test_code_sums_scores_ignoring_claimed_total(self):
        obj = {"criteria": CRIT_LOW, "total": 10, "fixes": []}
        self.assertEqual(SR.parse_judgement(obj, "dialogue")["total"], 6.5)

    def test_schema_violations(self):
        bad = [{"criteria": dict(CRIT_HIGH, extra=1)}, {"criteria": dict(CRIT_HIGH, hook=3)},
               {"criteria": dict(CRIT_HIGH, hook=1.3)}, {"criteria": dict(CRIT_HIGH, hook=True)}, {"fixes": []}]
        for obj in bad:
            with self.assertRaises(ValueError):
                SR.parse_judgement(obj, "dialogue")

    def test_prompt_contains_rubric_brief_script(self):
        p = SR.build_prompt("nondialogue", "Chill bên suối", "## F01 ...")
        self.assertIn("Chill bên suối", p)
        self.assertIn("visual_comedy", p)
        self.assertIn("HSETL", p)
        self.assertEqual(sum(m for _, m, _ in SR.RUBRIC_V2), 10)
        self.assertIn("## F01", p)


class AttemptTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.ep = Path(self.tmp.name) / "ep42_test"
        (self.ep / "render").mkdir(parents=True)
        self.files = [str(self.ep / "render" / "script.md"), str(self.ep / "render" / "lines.json")]
        self.write("v1")
        self.calib = Path(self.tmp.name) / "calib.json"
        self.p = mock.patch.object(SR, "CALIB_FILE", self.calib)
        self.p.start()
        self.ledger = Path(self.tmp.name) / "findings.jsonl"
        self.pl = mock.patch.object(SR, "FINDINGS_FILE", self.ledger)
        self.pl.start()

    def tearDown(self):
        self.pl.stop()
        self.p.stop()
        self.tmp.cleanup()

    def write(self, tag):
        Path(self.files[0]).write_text("# Kịch bản " + tag, encoding="utf-8")
        Path(self.files[1]).write_text("[]", encoding="utf-8")

    def calibrate_ok(self):
        self.calib.write_text(json.dumps({"judges": {"codex": {"pass": True, "prompt_version": SR.prompt_version()}}}))

    def run_one(self, crit, meta=GOOD_META):
        return SR.attempt(str(self.ep), self.files, meta, VOICE, SCENES, STARTS, judge_fn=judge(crit))

    def test_pass_first_attempt_when_calibrated(self):
        self.calibrate_ok()
        st, rec = self.run_one(CRIT_HIGH)
        self.assertEqual((st["status"], rec["total"], rec["auto_gate_ok"]), ("passed", 9.5, True))

    def test_pass_but_uncalibrated_goes_to_owner(self):
        st, rec = self.run_one(CRIT_NINE)   # quy trình v2: ngưỡng 9,0; đúng 9,0 chưa hiệu chỉnh -> Owner
        self.assertTrue(rec["passed"])
        self.assertEqual(st["status"], "needs_owner")
        self.assertIn("hiệu chỉnh", st["reason"])

    def test_calibration_tied_to_prompt_version(self):
        self.calib.write_text(json.dumps({"judges": {"codex": {"pass": True, "prompt_version": "khac"}}}))
        self.assertFalse(SR.calibrated("codex"))

    def test_same_script_cannot_be_rejudged(self):
        self.run_one(CRIT_LOW)
        with self.assertRaises(SR.ReviewError):
            self.run_one(CRIT_HIGH)

    def test_three_failures_then_owner_with_best(self):
        self.calibrate_ok()
        scores = [CRIT_LOW, dict(CRIT_LOW, hook=1.5), dict(CRIT_LOW, twist=1.5)]
        for i, c in enumerate(scores):
            self.write("v%d" % i)
            st, rec = self.run_one(c)
        self.assertEqual(st["status"], "needs_owner")
        self.assertEqual(st["best_attempt"], 2)
        self.write("v9")
        with self.assertRaises(SR.ReviewError):
            self.run_one(CRIT_HIGH)

    def test_hard_rule_failure_counts_and_skips_judge(self):
        called = []
        bad = dict(GOOD_META, logline="TODO")
        st, rec = SR.attempt(str(self.ep), self.files, bad, VOICE, SCENES, STARTS,
                             judge_fn=lambda p: called.append(p))
        self.assertEqual(called, [])
        self.assertFalse(rec["passed"])
        self.assertEqual(len(st["attempts"]), 1)

    def test_external_subagent_judge_recorded(self):
        obj = {"criteria": CRIT_NINE, "fixes": []}
        st, rec = SR.attempt(str(self.ep), self.files, GOOD_META, VOICE, SCENES, STARTS,
                             external={"judge": "claude-subagent", "raw": "{}", "obj": obj})
        self.assertEqual(rec["judge"], "claude-subagent")
        self.assertEqual(st["status"], "needs_owner")   # subagent chưa hiệu chỉnh, đúng 9,0

    def test_eight_and_half_no_longer_passes(self):
        # Quy trình chuẩn v2 (Owner 18/11/2026): kịch bản chỉ qua khi ≥ 9/10
        st, rec = self.run_one(CRIT_MID)
        self.calibrate_ok()
        self.assertFalse(rec["passed"])
        self.assertEqual(st["status"], "pending")

    def test_v2_process_requires_viewer_panel(self):
        meta = dict(GOOD_META, process="nmt_v2")
        st, rec = self.run_one(CRIT_HIGH, meta=meta)          # 9,5 nhưng chưa có hội đồng người xem
        self.assertFalse(rec["passed"])
        self.assertIn("người xem", rec["viewer_block"])
        self.write("v2")
        SR.record_viewer(str(self.ep), self.files, viewer_obj(yes_all=True))
        st, rec = self.run_one(CRIT_HIGH, meta=meta)
        self.assertEqual((st["status"], rec["viewer"]["score"]), ("passed", 24))

    def test_viewer_pass_rule_needs_q1_q3_q5_all_roles(self):
        res = SR.parse_viewer(viewer_obj(yes_all=True, no=[(0, 5)]))   # 23/24 nhưng vai 1 câu 5 "không"
        self.assertEqual((res["score"], res["pass"]), (23, False))
        res = SR.parse_viewer(viewer_obj(yes_all=True, no=[(0, 7), (1, 7), (2, 8), (0, 6)]))  # 20/24, câu 1/3/5 đều có
        self.assertEqual((res["score"], res["pass"]), (20, True))
        with self.assertRaises(ValueError):
            SR.parse_viewer({"roles": [{"role": "a", "answers": []}]})

    def test_above_nine_auto_approves_even_uncalibrated(self):
        # rule Owner 13/11/2026: > 90/100 thì mặc định được duyệt
        obj = {"criteria": CRIT_HIGH, "fixes": ["Rút F07"]}
        st, rec = SR.attempt(str(self.ep), self.files, GOOD_META, VOICE, SCENES, STARTS,
                             external={"judge": "claude-subagent", "raw": "{}", "obj": obj})
        self.assertEqual((st["status"], rec["total"], rec["gate_rule"]), ("passed", 9.5, "owner_above_9"))

    def test_exactly_nine_uncalibrated_still_owner(self):
        st, rec = self.run_one(CRIT_NINE)
        self.assertEqual((rec["total"], st["status"], rec["auto_gate_ok"]), (9.0, "needs_owner", False))

    def test_every_attempt_recorded_in_findings_ledger(self):
        self.run_one(CRIT_LOW)
        self.write("v2")
        self.run_one(CRIT_MID)
        rows = [json.loads(x) for x in self.ledger.read_text(encoding="utf-8").splitlines()]
        self.assertEqual([r["attempt"] for r in rows], [1, 2])
        self.assertEqual(rows[0]["episode"], "ep42_test")
        self.assertEqual(rows[0]["lost"]["twist"], 1.0)
        self.assertEqual(rows[0]["fixes"], ["Thêm nhịp 2"])
        self.assertIn("twist", SR.findings_summary())

    def test_findings_no_duplicate_and_backfill(self):
        st, rec = self.run_one(CRIT_LOW)
        self.assertFalse(SR.record_findings(str(self.ep), rec))     # cùng tập + sha -> không ghi lại
        self.assertEqual(SR.backfill_findings(self.tmp.name), 0)   # script_review.json đã có trong sổ
        other = Path(self.tmp.name) / "ledger2.jsonl"
        self.assertEqual(SR.backfill_findings(self.tmp.name, other), 1)


class CalibrateTests(unittest.TestCase):
    def test_accuracy_and_pass(self):
        with tempfile.TemporaryDirectory() as t, mock.patch.object(SR, "CALIB_FILE", Path(t) / "c.json"):
            samples = [{"name": "g%d" % i, "expected": "good", "brief": "b", "script": "s"} for i in range(5)] + \
                      [{"name": "b%d" % i, "expected": "bad", "brief": "b", "script": "s"} for i in range(5)]
            fn = lambda p: judge(CRIT_HIGH)(p)  # chấm cao mọi bản -> bản kém bị sai
            rep = SR.calibrate(samples, judge_fn=fn)
            self.assertEqual(rep["accuracy"], 0.5)
            self.assertFalse(rep["pass"])
            seq = iter([CRIT_HIGH] * 5 + [CRIT_LOW] * 5)
            rep = SR.calibrate(samples, judge_fn=lambda p: judge(next(seq))(p))
            self.assertTrue(rep["pass"])
            self.assertTrue(SR.calibrated("codex"))

    def test_quota_error_aborts_without_writing(self):
        with tempfile.TemporaryDirectory() as t, mock.patch.object(SR, "CALIB_FILE", Path(t) / "c.json"):
            def fn(p):
                raise C.CodexUnavailable("usageLimitExceeded")
            with self.assertRaises(C.CodexUnavailable):
                SR.calibrate([{"name": "g", "expected": "good", "brief": "b", "script": "s"}], judge_fn=fn)
            self.assertFalse((Path(t) / "c.json").exists())


class AutoApproveTests(unittest.TestCase):
    def test_auto_approve_script_only_and_sha_locked(self):
        with tempfile.TemporaryDirectory() as t:
            ep = Path(t) / "ep42"
            (ep / "render").mkdir(parents=True)
            py = ep / "render" / "ep42.py"
            py.write_text("x=1")
            (ep / "render" / "script.md").write_text("a")
            (ep / "render" / "lines.json").write_text("[]")
            files = G.gated_files(str(ep), "script", str(py))
            sha = G._sha(files)
            with self.assertRaises(SystemExit):
                G.auto_approve(str(ep), "visual", str(py), sha, "auto-review (codex)")
            with self.assertRaises(SystemExit):
                G.auto_approve(str(ep), "script", str(py), "sai", "auto-review (codex)")
            with self.assertRaises(SystemExit):
                G.auto_approve(str(ep), "script", str(py), sha, "owner")
            wf = G.auto_approve(str(ep), "script", str(py), sha, "auto-review (codex, 8.5/10, lần 1)")
            self.assertEqual(wf["state"], "script_approved")
            self.assertTrue(G.is_approved(str(ep), wf, "script", str(py)))


def _png(path, kind="ok", seed=1):
    rng = np.random.default_rng(seed)
    blocks = lambda h, w: Image.fromarray(rng.integers(0, 255, (h // 96, w // 96, 3), dtype="uint8"), "RGB").resize(
        (w, h), Image.Resampling.NEAREST)   # khối màu lớn: mỗi seed một bố cục khác hẳn (nhiễu mịn sẽ thu về cùng màu xám)
    if kind == "ok":
        im = blocks(1536, 864)
    else:   # nền kem có viền
        im = Image.new("RGB", (864, 1536), (255, 246, 236))
        im.paste(blocks(1152, 672), (96, 192))
    im.save(path, "PNG")


class ArtAutoTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        t = Path(self.tmp.name)
        self.ep = t / "ep42_test"
        (self.ep / "art").mkdir(parents=True)
        self.prompts = self.ep / "art" / "PROMPTS_v01.md"
        self.prompts.write_text("# EP42\n\n### A01 — F01\n```\nScene one\n```\n\n### A02 — F02\n```\nScene two\n```\n",
                                encoding="utf-8")
        (t / "lib").mkdir()
        self.patches = [mock.patch.object(AA, "LIBRARY", t / "lib"), mock.patch.object(AA, "_git_dirty", lambda: set()),
                        mock.patch.object(AA, "CODEX_IMAGES", t / "codex_images")]
        for p in self.patches:
            p.start()

    def tearDown(self):
        for p in self.patches:
            p.stop()
        self.tmp.cleanup()

    def fake(self, kinds):
        it = iter(kinds)
        calls = []

        def ask(prompt, mode, timeout):
            calls.append(prompt)
            self.assertEqual(mode, "workspace-write")
            k = next(it)
            if k == "unavailable":
                raise C.CodexUnavailable("usage limit")
            target = prompt.split("exactly this path (create folders if needed, do NOT overwrite any other file):\n")[1].split("\n")[0].strip()
            if k != "none":
                _png(target, k, seed=len(calls))
            return {"answer": "{}", "thread_id": "t%d" % len(calls)}
        return ask, calls

    def test_parse_prompts(self):
        self.assertEqual(list(AA.parse_prompts(self.prompts)), ["A01", "A02"])

    def test_generates_archives_and_logs(self):
        ask, calls = self.fake(["ok", "ok"])
        rep = AA.run(str(self.ep), "ep42_test", "v01", self.prompts, ask=ask)
        self.assertIsNone(rep["stopped"])
        self.assertEqual({k: v["status"] for k, v in rep["scenes"].items()}, {"A01": "ok", "A02": "ok"})
        self.assertTrue(rep["scenes"]["A01"]["archive_id"].startswith("GEN_ep42_test_v01_A01_"))
        self.assertIn("UPPER TWO-THIRDS", calls[0])
        self.assertEqual(AA.budget(str(self.ep), 2), (2, 9))

    def test_bad_image_retried_with_fix_note_then_kept_superseded(self):
        ask, calls = self.fake(["cream", "ok"])
        rep = AA.run(str(self.ep), "ep42_test", "v01", self.prompts, scenes=["A01"], ask=ask)
        self.assertEqual(rep["scenes"]["A01"]["status"], "ok")
        self.assertEqual(rep["scenes"]["A01"]["attempt"], 2)
        self.assertIn("FIX FROM PREVIOUS ATTEMPT", calls[1])
        self.assertTrue(any("superseded" in p.name for p in (self.ep / "art" / "v01").glob("A01_*.png")))

    def test_three_failures_need_owner(self):
        ask, _ = self.fake(["cream", "cream", "cream"])
        rep = AA.run(str(self.ep), "ep42_test", "v01", self.prompts, scenes=["A01"], ask=ask)
        self.assertEqual(rep["scenes"]["A01"]["status"], "needs_owner")

    def test_codex_unavailable_stops(self):
        ask, _ = self.fake(["unavailable"])
        rep = AA.run(str(self.ep), "ep42_test", "v01", self.prompts, ask=ask)
        self.assertIn("Codex không dùng được", rep["stopped"])

    def test_no_image_and_budget(self):
        ask, _ = self.fake(["none"] * 20)
        rep = AA.run(str(self.ep), "ep42_test", "v01", self.prompts, ask=ask)
        self.assertEqual(rep["scenes"]["A01"]["status"], "needs_owner")
        rep = AA.run(str(self.ep), "ep42_test", "v01", self.prompts, scenes=["A02"], ask=ask)
        self.assertEqual(AA.budget(str(self.ep), 2)[0], 6)
        ask2, _ = self.fake(["none"] * 5)
        with mock.patch.object(AA, "budget", return_value=(9, 9)):
            rep = AA.run(str(self.ep), "ep42_test", "v01", self.prompts, scenes=["A01"], ask=ask2)
        self.assertIn("hết ngân sách", rep["stopped"])

    def test_duplicate_of_other_scene_detected(self):
        _png(self.ep / "art" / "v01_tmp.png")
        (self.ep / "art" / "v01").mkdir()
        _png(self.ep / "art" / "v01" / "A02.png", seed=7)

        def ask(prompt, mode, timeout):
            target = prompt.split("do NOT overwrite any other file):\n")[1].split("\n")[0].strip()
            Image.open(self.ep / "art" / "v01" / "A02.png").save(target)
            return {"answer": "{}"}
        rec = AA.generate_scene(str(self.ep), "ep42_test", "v01", "A01", "Scene one", [], ask=ask)
        self.assertTrue(any("repeats scene A02" in e for e in rec["machine_errors"]))


if __name__ == "__main__":
    unittest.main()
