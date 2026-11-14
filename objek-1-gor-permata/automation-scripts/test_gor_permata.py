"""
Automation Test Script (Playwright Python) - Objek 1: GOR Permata Badminton Hall
Non-Destructive Verification Suite (berhenti pada validasi sisi klien, memblokir POST /bookings/store)
"""
from datetime import date, timedelta
from pathlib import Path
import urllib.request
import urllib.error
from playwright.sync_api import sync_playwright

BASE_URL = "https://gorpermatabadminton.com"
LOG_PATH = Path(__file__).with_name("execution-log.txt")
results = []


def record(tc_id: str, name: str, passed: bool, detail: str) -> None:
    status = "PASS" if passed else "FAIL"
    line = f"[{status}] {tc_id} - {name}: {detail}"
    results.append(line)
    print(line)


def http_status(url: str) -> int:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code


def run() -> None:
    # 1. Verifikasi HTTP status seluruh rute publik
    public_routes = [
        "/",
        "/booking",
        "/login",
        "/fasilitas/lapangan",
        "/fasilitas/umum",
        "/fasilitas/tunggu",
        "/fasilitas/parkir",
    ]
    statuses = {r: http_status(BASE_URL + r) for r in public_routes}
    all_200 = all(code == 200 for code in statuses.values())
    record("TC-GOR-01", "Rute Publik HTTP 200", all_200, str(statuses))

    reg_code = http_status(BASE_URL + "/register")
    record("TC-GOR-02", "Cek Defect /register 404", reg_code == 404, f"HTTP {reg_code}")

    tomorrow = (date.today() + timedelta(days=1)).isoformat()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 800})
        page = context.new_page()

        # Hard guardrail: gagalkan segala request POST booking agar tidak pernah menyentuh DB UMKM
        blocked_posts = []

        def guard_booking(route):
            blocked_posts.append(route.request.url)
            route.abort()

        page.route("**/bookings/store", guard_booking)

        dialogs = []

        def on_dialog(dialog):
            dialogs.append(dialog.message)
            dialog.accept()

        page.on("dialog", on_dialog)

        # 2. Akses grid booking tanggal besok
        target_booking = f"{BASE_URL}/booking?start_date={tomorrow}"
        page.goto(target_booking, wait_until="domcontentloaded")
        slot_locator = page.locator('[onclick*="openBooking("]')
        slot_count = slot_locator.count()
        record("TC-GOR-03", "Load Grid Booking & Slot Tersedia", slot_count > 0, f"Ditemukan {slot_count} slot openBooking untuk {tomorrow}")

        if slot_count > 0:
            # 3. Buka modal booking slot pertama
            slot_locator.first.click()
            modal_visible = page.locator("#bookingModal").is_visible()
            default_total = page.locator("#dispTotal").inner_text().strip()
            record(
                "TC-GOR-04",
                "Buka Modal & Tarif Default 1 Jam",
                modal_visible and "40.000" in default_total,
                f"visible={modal_visible}, dispTotal={default_total!r}",
            )

            # 4. Uji updateTotal() untuk durasi 2 jam
            page.select_option("#custDuration", "2")
            total_2h = page.locator("#dispTotal").inner_text().strip()
            record("TC-GOR-05", "Kalkulasi Durasi 2 Jam (updateTotal)", "80.000" in total_2h, f"dispTotal={total_2h!r}")

            # 5. Negative Test: nama & WA kosong
            dialogs.clear()
            page.fill("#custName", "")
            page.fill("#custPhone", "")
            page.click("#btnSubmit")
            msg_empty = dialogs[-1] if dialogs else ""
            record(
                "TC-GOR-06",
                "Validasi Input Kosong (Stop Sebelum Fetch)",
                "harus diisi lengkap" in msg_empty and len(blocked_posts) == 0,
                f"alert={msg_empty!r}, post_attempts={len(blocked_posts)}",
            )

            # 6. Negative Test: format WA salah
            dialogs.clear()
            page.fill("#custName", "Test QA")
            page.fill("#custPhone", "12345")
            page.click("#btnSubmit")
            msg_invalid_wa = dialogs[-1] if dialogs else ""
            record(
                "TC-GOR-07",
                "Validasi Format WA Tidak Valid",
                "Nomor WA belum benar" in msg_invalid_wa and len(blocked_posts) == 0,
                f"alert={msg_invalid_wa!r}",
            )

            # 7. White Box Defect Repro: format '+62 08123456789' ditolak normPhone()
            dialogs.clear()
            page.fill("#custName", "Test QA")
            page.fill("#custPhone", "+62 08123456789")
            page.click("#btnSubmit")
            msg_620 = dialogs[-1] if dialogs else ""
            record(
                "TC-GOR-08",
                "Reproduksi Bug normPhone('+62 08...')",
                "Nomor WA belum benar" in msg_620 and len(blocked_posts) == 0,
                f"alert={msg_620!r}",
            )

            # 8. Tutup modal & pastikan input di-reset oleh closeModal()
            page.evaluate("closeModal()")
            modal_hidden = not page.locator("#bookingModal").is_visible()
            cleared = page.input_value("#custName") == "" and page.input_value("#custPhone") == ""
            record("TC-GOR-10", "Close Modal & Reset Form Input", modal_hidden and cleared, f"hidden={modal_hidden}, cleared={cleared}")

        browser.close()

    LOG_PATH.write_text("\n".join(results) + "\n", encoding="utf-8")
    print(f"\nLog eksekusi disimpan ke: {LOG_PATH}")


if __name__ == "__main__":
    run()

