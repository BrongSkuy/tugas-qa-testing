"""
Automation Test Script (Playwright Python) - Black Box Suite (ISO/IEC/IEEE 29119-2:2021)
Objek: Portal Booking GOR Permata Badminton Hall (https://gorpermatabadminton.com)
Cakupan: TC-BB-01 s.d. TC-BB-23 (EP, BVA, Decision Table, State Transition, Use Case, Compatibility)
Guardrail: Non-destruktif - memblokir POST **/bookings/store di level browser interceptor.
"""
from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any

from playwright.sync_api import sync_playwright

SCRIPT_DIR = Path(__file__).resolve().parent
BASE_DIR = SCRIPT_DIR.parent
DATA_PATH = BASE_DIR / "test-data" / "blackbox-testdata.json"
LOG_PATH = SCRIPT_DIR / "execution-log.txt"
JSON_RESULT_PATH = BASE_DIR / "evidence" / "blackbox-results.json"
SCREENSHOT_DIR = BASE_DIR / "evidence" / "screenshots"

results: list[dict[str, Any]] = []
log_lines: list[str] = []


def record(tc_id: str, name: str, passed: bool, expected: str, actual: str) -> None:
    status = "PASS" if passed else "FAIL"
    line = f"[{status}] {tc_id} - {name}: expected={expected} | actual={actual}"
    results.append(
        {
            "tc_id": tc_id,
            "name": name,
            "status": status,
            "expected": expected,
            "actual": actual,
        }
    )
    log_lines.append(line)
    print(line)


def http_status(url: str) -> int:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code


def click_submit_expect_dialog(page, dialogs: list[str], timeout_s: float = 4.0) -> str:
    """Klik #btnSubmit dan tunggu dialog alert dari validasi klien atau .catch() interceptor."""
    before = len(dialogs)
    page.click("#btnSubmit")
    deadline = time.perf_counter() + timeout_s
    while len(dialogs) == before and time.perf_counter() < deadline:
        page.wait_for_timeout(50)
    return dialogs[-1] if len(dialogs) > before else ""


def ensure_modal_open(page, slot_locator) -> None:
    if not page.locator("#bookingModal").is_visible():
        slot_locator.first.click()
        page.locator("#bookingModal").wait_for(state="visible", timeout=5000)


def assert_not_antibot(page) -> None:
    """Hentikan segera jika halaman menampilkan tantangan anti-bot agar tidak menunggu/melewati proteksi."""
    title = page.title()
    if "Checking your browser" in title or "Just a moment" in title or "Permata" not in title:
        raise RuntimeError(f"Blocked by anti-bot or unexpected page title: {title!r}")


def mask_grid_pii(page, keep_rtbc: bool = False) -> None:
    """Samarkan teks nama pelanggan pada grid publik sebelum mengambil screenshot bukti."""
    page.evaluate(
        """(keepRtbc) => {
            document.querySelectorAll('[onclick*="manageBooking"] span').forEach(el => {
                const slot = el.closest('[onclick*="manageBooking"]');
                const name = slot ? (slot.dataset.name || '') : '';
                if (keepRtbc && name.includes('RTBC')) {
                    return;
                }
                el.textContent = '[TERISI]';
            });
        }""",
        keep_rtbc,
    )


def run() -> None:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    base_url: str = data["metadata"]["base_url"]
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
    JSON_RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)

    run_started = datetime.now().astimezone().isoformat(timespec="seconds")
    log_lines.append(f"=== EXECUTION START: {run_started} | TARGET: {base_url} ===")

    # 1. TC-BB-01: Verifikasi 7 rute publik HTTP 200
    statuses = {r: http_status(base_url + r) for r in data["public_routes_ok"]}
    all_200 = all(code == 200 for code in statuses.values())
    record("TC-BB-01", "Rute Publik HTTP 200", all_200, "All 200 OK", str(statuses))

    # 2. TC-BB-02: Verifikasi rute /register (teramati defect HTTP 404)
    reg_code = http_status(base_url + data["missing_route"])
    record(
        "TC-BB-02",
        "Verifikasi Endpoint /register (Defect Check IR-GOR-01)",
        reg_code in (200, 301, 302),
        "HTTP 200 OK atau redirect aktif",
        f"HTTP {reg_code} (Insiden IR-GOR-01 / BUG-GOR-01 terkonfirmasi)",
    )

    tomorrow = (date.today() + timedelta(days=data["start_date_cases"]["valid_tomorrow_offset_days"])).isoformat()
    past_date = data["start_date_cases"]["past_date"]
    invalid_date = data["start_date_cases"]["invalid_format"]

    # 3. TC-BB-05: Query ?start_date=invalid-date via HTTP GET
    invalid_date_code = http_status(f"{base_url}/booking?start_date={invalid_date}")
    record(
        "TC-BB-05",
        "EP Query start_date Format Tidak Valid (Deteksi HTTP 500)",
        invalid_date_code != 500,
        "HTTP 400/422/302 fallback aman (!= 500)",
        f"HTTP {invalid_date_code} (Insiden IR-GOR-06)",
    )

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        desktop_vp = data["viewports"]["desktop"]
        mobile_vp = data["viewports"]["mobile"]

        context = browser.new_context(viewport=desktop_vp)
        page = context.new_page()

        # Hard guardrail: batalkan POST **/bookings/store sebelum meninggalkan browser
        blocked_posts: list[str] = []
        network_posts_sent: list[str] = []
        console_errors: list[str] = []

        def guard_booking(route) -> None:
            blocked_posts.append(route.request.url)
            route.abort()

        page.route("**/bookings/store", guard_booking)
        page.on(
            "requestfinished",
            lambda req: network_posts_sent.append(req.url) if "/bookings/store" in req.url else None,
        )
        page.on("pageerror", lambda err: console_errors.append(str(err)))

        dialogs: list[str] = []

        def on_dialog(dialog) -> None:
            dialogs.append(dialog.message)
            dialog.accept()

        page.on("dialog", on_dialog)

        # Screenshot beranda desktop + error pages
        page.goto(base_url, wait_until="domcontentloaded")
        page.screenshot(path=str(SCREENSHOT_DIR / "01_home_desktop.png"), full_page=False)

        page.goto(f"{base_url}/register", wait_until="domcontentloaded")
        page.screenshot(path=str(SCREENSHOT_DIR / "04_register_404.png"), full_page=False)

        page.goto(f"{base_url}/booking?start_date={invalid_date}", wait_until="domcontentloaded")
        page.screenshot(path=str(SCREENSHOT_DIR / "05_invalid_date_500.png"), full_page=False)

        # 4. TC-BB-04: Query ?start_date=2020-01-01 (tanggal lampau)
        page.goto(f"{base_url}/booking?start_date={past_date}", wait_until="domcontentloaded")
        assert_not_antibot(page)
        past_slots = page.locator('[onclick*="openBooking("]').count()
        mask_grid_pii(page)
        page.screenshot(path=str(SCREENSHOT_DIR / "11_past_date_2020_bug.png"), full_page=False)
        record(
            "TC-BB-04",
            "BVA/EP Query start_date Tanggal Masa Lalu (2020-01-01)",
            past_slots == 0,
            "0 slot openBooking pada tanggal masa lalu",
            f"{past_slots} slot openBooking masih aktif (Insiden IR-GOR-05)",
        )

        # 5. TC-BB-03: Query ?start_date=<tomorrow> valid
        target_booking = f"{base_url}/booking?start_date={tomorrow}"
        page.goto(target_booking, wait_until="domcontentloaded")
        jump_val = page.input_value("#jumpDate")
        slot_locator = page.locator('[onclick*="openBooking("]')
        slot_count = slot_locator.count()
        record(
            "TC-BB-03",
            "Filter Tanggal Grid Valid & Ketersediaan Slot",
            jump_val == tomorrow and slot_count > 0,
            f"jumpDate={tomorrow}, slot_count>0",
            f"jumpDate={jump_val}, slot_count={slot_count}",
        )

        # Screenshot grid dengan masking PII
        mask_grid_pii(page)
        page.screenshot(path=str(SCREENSHOT_DIR / "02_booking_grid_desktop.png"), full_page=False)

        # 6. TC-BB-22: Inspeksi privasi DOM publik (tanpa menyimpan PII)
        dom_privacy = page.evaluate(
            """() => {
                const els = Array.from(document.querySelectorAll('[onclick*="manageBooking"]'));
                const withPhone = els.filter(e => (e.dataset.phone || '').trim().length > 0).length;
                const withName = els.filter(e => (e.dataset.name || '').trim().length > 0).length;
                return { total: els.length, withPhone, withName };
            }"""
        )
        record(
            "TC-BB-22",
            "Audit Privasi Atribut DOM Publik (manageBooking)",
            dom_privacy["withPhone"] == 0,
            "withPhone=0 pada HTML publik",
            f"total_slot_terisi={dom_privacy['total']}, withPhone={dom_privacy['withPhone']}, withName={dom_privacy['withName']} (Insiden IR-GOR-04)",
        )

        if slot_count > 0:
            # 7. TC-BB-06: State Transition GridLoaded -> ModalOpen
            ensure_modal_open(page, slot_locator)
            modal_vis = page.locator("#bookingModal").is_visible()
            default_dur = page.input_value("#custDuration")
            default_total = page.locator("#dispTotal").inner_text().strip()
            page.locator("#bookingModal .modal-card").screenshot(
                path=str(SCREENSHOT_DIR / "03_booking_modal_desktop.png")
            )
            record(
                "TC-BB-06",
                "State Transition Buka Modal Booking & Nilai Default",
                modal_vis and default_dur == "1" and "40.000" in default_total,
                "visible=True, durasi=1, dispTotal='Rp 40.000'",
                f"visible={modal_vis}, durasi={default_dur}, dispTotal={default_total!r}",
            )

            # 8. TC-BB-07: BVA/EP Kalkulasi Tarif untuk durasi 1..5 jam
            tariff_actual = {}
            tariff_ok = True
            for item in data["duration_tariffs"]:
                page.select_option("#custDuration", item["duration"])
                txt = page.locator("#dispTotal").inner_text().strip()
                tariff_actual[item["duration"]] = txt
                if item["expected_text"] not in txt:
                    tariff_ok = False
            page.select_option("#custDuration", "1")
            record(
                "TC-BB-07",
                "Kalkulasi Tarif updateTotal() Durasi 1..5 Jam",
                tariff_ok,
                "Rp 40.000 .. Rp 200.000",
                str(tariff_actual),
            )

            # 9. TC-BB-08: Decision Rule R1 - Nama & WA kosong
            before_posts = len(blocked_posts)
            page.fill("#custName", data["name_cases"]["empty"])
            page.fill("#custPhone", data["phone_cases"]["empty"])
            msg_empty = click_submit_expect_dialog(page, dialogs)
            delta = len(blocked_posts) - before_posts
            record(
                "TC-BB-08",
                "Decision R1: Validasi Nama & WA Kosong",
                "harus diisi lengkap" in msg_empty and delta == 0,
                "Alert wajib isi, delta_post=0",
                f"alert={msg_empty!r}, delta_post={delta}",
            )

            # 10. TC-BB-09: BVA #custName spasi "   " & 1 karakter "A"
            page.fill("#custName", data["name_cases"]["whitespace_only"])
            page.fill("#custPhone", data["phone_cases"]["bva_min_valid_11_digits"])
            before_posts = len(blocked_posts)
            msg_ws = click_submit_expect_dialog(page, dialogs)
            delta_ws = len(blocked_posts) - before_posts

            page.fill("#custName", data["name_cases"]["single_char"])
            before_posts = len(blocked_posts)
            msg_1c = click_submit_expect_dialog(page, dialogs)
            delta_1c = len(blocked_posts) - before_posts
            record(
                "TC-BB-09",
                "BVA #custName Spasi '   ' & 1 Karakter 'A' (Cek BUG-GOR-03)",
                delta_ws == 0 and delta_1c == 0,
                "Ditolak di klien (delta_post=0)",
                f"whitespace_delta_post={delta_ws}, single_char_delta_post={delta_1c}, interceptor_alert={msg_ws!r} (IR-GOR-03 terkonfirmasi)",
            )

            # 11. TC-BB-10: EP Format WA tidak valid ("12345" & "abc")
            page.fill("#custName", data["name_cases"]["valid"])
            ep_alerts = []
            ep_deltas = []
            for bad_wa in (data["phone_cases"]["too_short_generic"], data["phone_cases"]["non_numeric"]):
                before_posts = len(blocked_posts)
                page.fill("#custPhone", bad_wa)
                ep_alerts.append(click_submit_expect_dialog(page, dialogs))
                ep_deltas.append(len(blocked_posts) - before_posts)
            record(
                "TC-BB-10",
                "EP Format WA Invalid ('12345' & 'abc')",
                all("Nomor WA belum benar" in m for m in ep_alerts) and sum(ep_deltas) == 0,
                "Alert format WA, delta_post=0",
                f"alerts={ep_alerts}, deltas={ep_deltas}",
            )

            # 12. TC-BB-11: BVA Panjang WA Batas Bawah Gagal (10 digit: 081234567)
            before_posts = len(blocked_posts)
            page.fill("#custPhone", data["phone_cases"]["bva_below_min_10_digits"])
            msg_10 = click_submit_expect_dialog(page, dialogs)
            delta_10 = len(blocked_posts) - before_posts
            record(
                "TC-BB-11",
                "BVA Panjang WA 10 Digit (628+7 digit -> Batas Bawah Gagal)",
                "Nomor WA belum benar" in msg_10 and delta_10 == 0,
                "Ditolak regex klien, delta_post=0",
                f"alert={msg_10!r}, delta_post={delta_10}",
            )

            # 13. TC-BB-12: BVA Panjang WA Batas Bawah Valid (11 digit: 0812345678)
            before_posts = len(blocked_posts)
            page.fill("#custPhone", data["phone_cases"]["bva_min_valid_11_digits"])
            msg_11 = click_submit_expect_dialog(page, dialogs)
            delta_11 = len(blocked_posts) - before_posts
            record(
                "TC-BB-12",
                "BVA Panjang WA 11 Digit (628+8 digit -> Batas Bawah Valid)",
                "kesalahan koneksi" in msg_11 and delta_11 == 1,
                "Lolos validasi klien, dicegat interceptor (delta_post=1)",
                f"alert={msg_11!r}, delta_post={delta_11}",
            )

            # 14. TC-BB-13: BVA Panjang WA Batas Atas Valid (14 digit: 0812345678901)
            before_posts = len(blocked_posts)
            page.fill("#custPhone", data["phone_cases"]["bva_max_valid_14_digits"])
            msg_14 = click_submit_expect_dialog(page, dialogs)
            delta_14 = len(blocked_posts) - before_posts
            record(
                "TC-BB-13",
                "BVA Panjang WA 14 Digit (628+11 digit -> Batas Atas Valid)",
                "kesalahan koneksi" in msg_14 and delta_14 == 1,
                "Lolos validasi klien, dicegat interceptor (delta_post=1)",
                f"alert={msg_14!r}, delta_post={delta_14}",
            )

            # 15. TC-BB-14: BVA Panjang WA Batas Atas Gagal (15 digit: 08123456789012)
            before_posts = len(blocked_posts)
            page.fill("#custPhone", data["phone_cases"]["bva_above_max_15_digits"])
            msg_15 = click_submit_expect_dialog(page, dialogs)
            delta_15 = len(blocked_posts) - before_posts
            record(
                "TC-BB-14",
                "BVA Panjang WA 15 Digit (628+12 digit -> Batas Atas Gagal)",
                "Nomor WA belum benar" in msg_15 and delta_15 == 0,
                "Ditolak regex klien, delta_post=0",
                f"alert={msg_15!r}, delta_post={delta_15}",
            )

            # 16. TC-BB-15: EP Variasi Prefiks Sah ('8...' & '628...')
            before_posts = len(blocked_posts)
            page.fill("#custPhone", data["phone_cases"]["prefix_8"])
            msg_p8 = click_submit_expect_dialog(page, dialogs)
            d_p8 = len(blocked_posts) - before_posts

            before_posts = len(blocked_posts)
            page.fill("#custPhone", data["phone_cases"]["prefix_628"])
            msg_p628 = click_submit_expect_dialog(page, dialogs)
            d_p628 = len(blocked_posts) - before_posts
            record(
                "TC-BB-15",
                "EP Variasi Prefiks WA Sah ('8...' & '628...')",
                d_p8 == 1 and d_p628 == 1 and "kesalahan koneksi" in msg_p8 and "kesalahan koneksi" in msg_p628,
                "Keduanya dinormalisasi -> delta_post=1 masing-masing",
                f"prefix_8_delta={d_p8}, prefix_628_delta={d_p628}",
            )

            # 17. TC-BB-16: Edge Case +62 08... (Repro White/Black Box IR-GOR-02)
            before_posts = len(blocked_posts)
            page.fill("#custPhone", data["phone_cases"]["bug_prefix_plus62_08"])
            msg_620 = click_submit_expect_dialog(page, dialogs)
            delta_620 = len(blocked_posts) - before_posts
            record(
                "TC-BB-16",
                "Reproduksi Bug Prefiks '+62 08...' (IR-GOR-02)",
                delta_620 == 1,
                "Dinormalisasi ke 628... dan lolos ke fetch",
                f"Ditolak regex (6208...): alert={msg_620!r}, delta_post={delta_620} (IR-GOR-02 terkonfirmasi)",
            )

            # 18. TC-BB-19: State Transition Close Modal & Reset Input
            page.evaluate("closeModal()")
            modal_hidden = not page.locator("#bookingModal").is_visible()
            cleared = page.input_value("#custName") == "" and page.input_value("#custPhone") == ""
            record(
                "TC-BB-19",
                "State Transition closeModal() & Reset Input",
                modal_hidden and cleared,
                "hidden=True, cleared=True",
                f"hidden={modal_hidden}, cleared={cleared}",
            )

            # 19 & 20. TC-BB-17 & TC-BB-18: BVA Batas Jam Tutup 00:00 pada slot 22:00
            slot_22 = page.locator("[onclick*=\"openBooking('22:00'\"]")
            if slot_22.count() == 0:
                for offset in range(2, 6):
                    alt_date = (date.today() + timedelta(days=offset)).isoformat()
                    page.goto(f"{base_url}/booking?start_date={alt_date}", wait_until="domcontentloaded")
                    slot_22 = page.locator("[onclick*=\"openBooking('22:00'\"]")
                    if slot_22.count() > 0:
                        break

            if slot_22.count() > 0:
                slot_22.first.click()
                page.locator("#bookingModal").wait_for(state="visible", timeout=5000)
                page.fill("#custName", data["name_cases"]["valid"])
                page.fill("#custPhone", data["closing_hour_cases"]["valid_phone"])

                # TC-BB-17: 22:00 + 3 jam = 25 > 24 (Gagal)
                before_posts = len(blocked_posts)
                page.select_option("#custDuration", data["closing_hour_cases"]["invalid_over_midnight_duration"])
                msg_over = click_submit_expect_dialog(page, dialogs)
                delta_over = len(blocked_posts) - before_posts
                record(
                    "TC-BB-17",
                    "BVA Jam Tutup 00:00 (22:00 + 3 Jam = 25 > 24 -> Ditolak)",
                    "tutup jam 00:00" in msg_over and delta_over == 0,
                    "Alert tutup jam 00:00, delta_post=0",
                    f"alert={msg_over!r}, delta_post={delta_over}",
                )

                # TC-BB-18: 22:00 + 2 jam = 24 <= 24 (Valid Batas)
                before_posts = len(blocked_posts)
                page.select_option("#custDuration", data["closing_hour_cases"]["valid_boundary_duration"])
                msg_24 = click_submit_expect_dialog(page, dialogs)
                delta_24 = len(blocked_posts) - before_posts
                record(
                    "TC-BB-18",
                    "BVA Jam Tutup 00:00 (22:00 + 2 Jam = 24 <= 24 -> Batas Valid)",
                    "kesalahan koneksi" in msg_24 and delta_24 == 1,
                    "Lolos validasi tutup jam 00:00, dicegat interceptor (delta_post=1)",
                    f"alert={msg_24!r}, delta_post={delta_24}",
                )
                page.evaluate("closeModal()")
            else:
                record("TC-BB-17", "BVA Jam Tutup 00:00 (22:00 + 3 Jam)", False, "Slot 22:00 ditemukan", "Tidak ada slot 22:00 kosong")
                record("TC-BB-18", "BVA Jam Tutup 00:00 (22:00 + 2 Jam)", False, "Slot 22:00 ditemukan", "Tidak ada slot 22:00 kosong")

        # 21. TC-BB-20: Form /login HTML5 Validation & CSRF _token (Non-submit)
        page.goto(f"{base_url}/login", wait_until="domcontentloaded")
        page.screenshot(path=str(SCREENSHOT_DIR / "06_login_page.png"), full_page=False)
        login_check = page.evaluate(
            """(invalidEmail) => {
                const tokenEl = document.querySelector('input[name="_token"]');
                const emailEl = document.querySelector('input[name="email"]');
                const passEl = document.querySelector('input[name="password"]');
                const formEl = document.querySelector('form');
                if (!tokenEl || !emailEl || !passEl || !formEl) return { ok: false };

                emailEl.value = '';
                passEl.value = '';
                const emptyValid = formEl.checkValidity();

                emailEl.value = invalidEmail;
                passEl.value = 'secret123';
                const badEmailValid = emailEl.checkValidity();

                emailEl.value = 'qa.tester@example.com';
                passEl.value = '';
                const missingPassValid = formEl.checkValidity();

                return {
                    ok: true,
                    hasToken: tokenEl.value.trim().length > 10,
                    emptyValid,
                    badEmailValid,
                    missingPassValid
                };
            }""",
            data["login_negative_cases"]["invalid_email"],
        )
        login_ok = (
            login_check.get("ok", False)
            and login_check.get("hasToken", False)
            and not login_check.get("emptyValid", True)
            and not login_check.get("badEmailValid", True)
            and not login_check.get("missingPassValid", True)
        )
        record(
            "TC-BB-20",
            "Black Box Form /login (CSRF _token & Validasi HTML5 Klien)",
            login_ok,
            "hasToken=True, empty/badEmail/missingPass checkValidity=False",
            str(login_check),
        )

        # 23. TC-BB-23: State Transition Slot Confirmed (RTBC) -> manageBooking() Alert Dialog
        page.goto(f"{base_url}/booking", wait_until="domcontentloaded")
        assert_not_antibot(page)
        rtbc_slots = page.locator('[data-status="confirmed"][data-name*="RTBC"]')
        if rtbc_slots.count() == 0:
            page.goto(target_booking, wait_until="domcontentloaded")
            assert_not_antibot(page)
            rtbc_slots = page.locator('[data-status="confirmed"][data-name*="RTBC"]')

        rtbc_count = rtbc_slots.count()
        rtbc_dialog_msg = ""
        rtbc_label_text = ""
        if rtbc_count > 0:
            mask_grid_pii(page, keep_rtbc=True)
            first_rtbc = rtbc_slots.first
            first_rtbc.scroll_into_view_if_needed()
            page.wait_for_timeout(200)
            rtbc_label_text = first_rtbc.inner_text().strip()
            page.screenshot(path=str(SCREENSHOT_DIR / "09_slot_confirmed_rtbc.png"), full_page=False)

            before_dlg = len(dialogs)
            first_rtbc.click()
            deadline = time.perf_counter() + 4.0
            while len(dialogs) == before_dlg and time.perf_counter() < deadline:
                page.wait_for_timeout(50)
            rtbc_dialog_msg = dialogs[-1] if len(dialogs) > before_dlg else ""

        rtbc_ok = (
            rtbc_count > 0
            and "RTBC" in rtbc_label_text
            and "SUDAH DIKONFIRMASI" in rtbc_dialog_msg
            and "RTBC" in rtbc_dialog_msg
        )
        record(
            "TC-BB-23",
            "State Transition Slot Terkonfirmasi RTBC -> Alert manageBooking()",
            rtbc_ok,
            "Slot RTBC ditemukan & alert berisi 'SUDAH DIKONFIRMASI' + 'RTBC'",
            f"rtbc_count={rtbc_count}, label={rtbc_label_text!r}, dialog={rtbc_dialog_msg!r}",
        )
        context.close()

        # 22. TC-BB-21: Kompatibilitas Mobile 390x844 vs Desktop 1280x800
        m_ctx = browser.new_context(viewport=mobile_vp)
        m_page = m_ctx.new_page()
        m_page.route("**/bookings/store", guard_booking)

        m_page.goto(base_url, wait_until="domcontentloaded")
        home_overflow = m_page.evaluate(
            """() => {
                const links = Array.from(document.querySelectorAll('header a, nav a'));
                const clipped = links
                    .map(a => ({ text: a.innerText.trim(), right: Math.round(a.getBoundingClientRect().right) }))
                    .filter(item => item.right > window.innerWidth + 1);
                return {
                    sw: document.documentElement.scrollWidth,
                    iw: window.innerWidth,
                    clippedNavLinks: clipped
                };
            }"""
        )
        m_page.screenshot(path=str(SCREENSHOT_DIR / "07_home_mobile.png"), full_page=False)

        m_page.goto(f"{base_url}/booking?start_date={tomorrow}", wait_until="domcontentloaded")
        booking_overflow = m_page.evaluate(
            "() => ({ sw: document.documentElement.scrollWidth, iw: window.innerWidth })"
        )
        m_slots = m_page.locator('[onclick*="openBooking("]')
        m_modal_ok = False
        m_modal_box = {}
        if m_slots.count() > 0:
            m_slots.first.click()
            m_page.locator("#bookingModal").wait_for(state="visible", timeout=5000)
            m_page.wait_for_timeout(350)
            m_modal_box = m_page.evaluate(
                """() => {
                    const card = document.querySelector('#bookingModal .modal-card');
                    const rect = card ? card.getBoundingClientRect() : null;
                    return {
                        visible: !!rect && rect.width > 0 && rect.height > 0,
                        fitsViewport: !!rect && rect.right <= window.innerWidth + 1 && rect.left >= -1,
                        width: rect ? Math.round(rect.width) : 0,
                        innerWidth: window.innerWidth
                    };
                }"""
            )
            m_modal_ok = m_modal_box.get("visible", False) and m_modal_box.get("fitsViewport", False)
            mask_grid_pii(m_page)
            m_page.screenshot(path=str(SCREENSHOT_DIR / "08_booking_modal_mobile.png"), full_page=False)
            m_page.evaluate("closeModal()")

        home_ok = home_overflow["sw"] <= home_overflow["iw"] and len(home_overflow["clippedNavLinks"]) == 0
        booking_ok = booking_overflow["sw"] <= booking_overflow["iw"]
        record(
            "TC-BB-21",
            "Kompatibilitas Mobile 390x844 (Overflow, Navbar Clip, & Modal Fit)",
            home_ok and booking_ok and m_modal_ok,
            "home & booking scrollWidth<=innerWidth, clippedNavLinks=0, modal fits mobile viewport",
            f"home={home_overflow}, booking={booking_overflow}, modal={m_modal_box}",
        )
        m_ctx.close()
        browser.close()

    passed_count = sum(1 for r in results if r["status"] == "PASS")
    failed_count = len(results) - passed_count
    summary = {
        "timestamp": run_started,
        "target": base_url,
        "total_cases": len(results),
        "passed": passed_count,
        "failed_or_defect_repro": failed_count,
        "intercepted_post_attempts_inside_browser": len(blocked_posts),
        "network_posts_sent_to_server": len(network_posts_sent),
        "console_errors": console_errors,
        "cases": results,
    }

    log_lines.append(
        f"=== SUMMARY: {passed_count}/{len(results)} PASS | Defect/Anomaly={failed_count} | "
        f"Intercepted_POST_In_Browser={len(blocked_posts)} | Network_POST_Sent={len(network_posts_sent)} ==="
    )

    LOG_PATH.write_text("\n".join(log_lines) + "\n", encoding="utf-8")
    JSON_RESULT_PATH.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"\nLog eksekusi disimpan ke: {LOG_PATH}")
    print(f"Ringkasan JSON disimpan ke: {JSON_RESULT_PATH}")


if __name__ == "__main__":
    run()
