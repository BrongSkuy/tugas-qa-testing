"""
Automation Test Script (Playwright Python) - Objek 2: Kolam Renang TASA Pamulang
Non-Destructive Verification Suite (memblokir segala POST request agar tidak mengirim form nyata)
"""
from pathlib import Path
import urllib.request
import urllib.error
from playwright.sync_api import sync_playwright

BASE_URL = "https://www.kolamtasa.com"
LOG_PATH = Path(__file__).with_name("execution-log.txt")
results = []


def record(tc_id: str, name: str, passed: bool, detail: str) -> None:
    status = "PASS" if passed else "FAIL"
    line = f"[{status}] {tc_id} - {name}: {detail}"
    results.append(line)
    print(line)


def fetch_status_and_headers(url: str) -> tuple[int, dict]:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.status, {k.lower(): v for k, v in r.headers.items()}
    except urllib.error.HTTPError as e:
        return e.code, {}


def run() -> None:
    # 1. Verifikasi seluruh rute publik
    public_routes = [
        "/",
        "/berenang",
        "/lesrenang",
        "/kontak",
        "/event",
        "/blog",
        "/blog/les-renang",
        "/blog/perawatan-kolam",
        "/blog/kesehatan-dan-hidroterapi",
        "/club",
        "/hidroterapi",
        "/gelombang",
        "/restoran",
        "/sekolah-cita-pelangi",
    ]
    statuses = {r: fetch_status_and_headers(BASE_URL + r)[0] for r in public_routes}
    all_200 = all(code == 200 for code in statuses.values())
    record("TC-TASA-01", "Seluruh Rute Publik HTTP 200", all_200, f"Checked {len(statuses)} routes, failures={[k for k,v in statuses.items() if v != 200]}")

    # 2. Verifikasi 404 pada footer targets & pagination boundary
    dead_routes = ["/privacy", "/terms", "/settings", "/kerjasama", "/blog/halaman/0", "/blog/halaman/5"]
    dead_statuses = {r: fetch_status_and_headers(BASE_URL + r)[0] for r in dead_routes}
    all_404 = all(code == 404 for code in dead_statuses.values())
    record("TC-TASA-02/09", "Konfirmasi 404 Footer Dead Routes & Blog Out-of-Bounds", all_404, str(dead_statuses))

    # 3. Verifikasi HTTP Security Headers pada /
    _, headers = fetch_status_and_headers(BASE_URL + "/")
    expected_missing = [
        "content-security-policy",
        "x-frame-options",
        "x-content-type-options",
        "referrer-policy",
        "permissions-policy",
    ]
    missing_found = [h for h in expected_missing if h not in headers]
    record(
        "TC-TASA-10",
        "Audit HTTP Security Headers (Temuan BUG-TASA-04)",
        len(missing_found) == 5 and "strict-transport-security" in headers,
        f"HSTS_present={'strict-transport-security' in headers}, missing={missing_found}",
    )

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 800})
        page = context.new_page()

        # Hard guardrail: blokir semua request POST agar tidak pernah menyentuh Server Action admin
        blocked_posts = []

        def guard_posts(route):
            if route.request.method == "POST":
                blocked_posts.append(route.request.url)
                route.abort()
            else:
                route.continue_()

        page.route("**/*", guard_posts)

        # 4. Audit Beranda: gambar tanpa alt & footer span mati + tahun hak cipta
        page.goto(BASE_URL + "/", wait_until="domcontentloaded")
        img_stats = page.evaluate(
            """() => {
                const imgs = Array.from(document.querySelectorAll('img'));
                const missingAlt = imgs.filter(i => !i.getAttribute('alt') || i.getAttribute('alt').trim() === '').length;
                const footerText = document.querySelector('footer')?.innerText || '';
                const privacyLinkCount = document.querySelectorAll('footer a').length;
                const hasPrivacyAnchor = Array.from(document.querySelectorAll('footer a')).some(a => /privacy|terms|settings/i.test(a.textContent || ''));
                return { totalImgs: imgs.length, missingAlt, hasCopyright2023: footerText.includes('Hak Cipta 2023'), hasPrivacyAnchor };
            }"""
        )
        record(
            "TC-TASA-11",
            "Audit Gambar Tanpa alt & Footer Span Mati (BUG-TASA-02/03/05)",
            img_stats["missingAlt"] > 0 and img_stats["hasCopyright2023"] and not img_stats["hasPrivacyAnchor"],
            str(img_stats),
        )

        # 5. Audit /blog: cek ketiadaan fitur search input
        page.goto(BASE_URL + "/blog", wait_until="domcontentloaded")
        search_inputs = page.locator('input[type="search"], input[placeholder*="cari" i]').count()
        record("TC-TASA-09B", "Konfirmasi /blog Belum Memiliki Fitur Pencarian", search_inputs == 0, f"search_inputs={search_inputs}")

        # 6. Audit /kontak: pastikan <form> tidak memiliki atribut action/method (BUG-TASA-01)
        page.goto(BASE_URL + "/kontak", wait_until="domcontentloaded")
        form_info = page.evaluate(
            """() => {
                const f = document.querySelector('form');
                return f ? { exists: true, action: f.getAttribute('action'), method: f.getAttribute('method') } : { exists: false };
            }"""
        )
        record(
            "TC-TASA-03",
            "Verifikasi Form /kontak Tanpa Action/Method (BUG-TASA-01)",
            form_info.get("exists") and form_info.get("action") is None and form_info.get("method") is None,
            str(form_info),
        )

        # 7. Uji Berulang Non-Destruktif Wizard /lesrenang (Step 1 -> Error -> Step 2 -> Error)
        page.goto(BASE_URL + "/lesrenang", wait_until="domcontentloaded")
        step1_badge = page.locator("text=1/20").is_visible() and page.locator("text=Siapa nama lengkap muridnya?").is_visible()
        page.get_by_role("button", name="Lanjut").click()
        err1_visible = page.locator("text=Nama muridnya belum diisi.").is_visible()
        record(
            "TC-TASA-04",
            "Validasi Input Kosong Step 1 Wizard /lesrenang",
            step1_badge and err1_visible,
            f"step1_visible={step1_badge}, error_shown={err1_visible}",
        )

        page.locator('input[placeholder="Nama sesuai akta"]').fill("Calon Murid QA")
        page.get_by_role("button", name="Lanjut").click()
        step2_question = page.locator("text=Nama panggilannya?").is_visible()
        page.get_by_role("button", name="Lanjut").click()
        err2_visible = page.locator("text=Nama panggilannya belum diisi.").is_visible()
        record(
            "TC-TASA-05",
            "Transisi Step 1 -> Step 2 & Validasi Kosong Step 2",
            step2_question and err2_visible and len(blocked_posts) == 0,
            f"step2_visible={step2_question}, err2_shown={err2_visible}, blocked_posts={len(blocked_posts)}",
        )

        browser.close()

    LOG_PATH.write_text("\n".join(results) + "\n", encoding="utf-8")
    print(f"\nLog eksekusi disimpan ke: {LOG_PATH}")


if __name__ == "__main__":
    run()
