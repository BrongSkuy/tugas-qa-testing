"""
Performance Testing Script (Playwright + aiohttp) - ISO/IEC/IEEE 29119-1:2022, 29119-5:2024, & ISO/IEC 25010:2023
Objek: Portal Booking GOR Permata Badminton Hall (https://gorpermatabadminton.com)
Cakupan: TC-PERF-01 s.d. TC-PERF-10 (Web Vitals Cold/Warm Desktop/Mobile, Payload, Client Interaction, Concurrent GET 1/5/10 VUs)
Guardrail: Non-destruktif - GET-only, max 10 VUs, think-time 500ms, auto-abort circuit breaker jika error > 5% atau HTTP 429.

Cara & Tempat Menjalankan File Ini:
  - JANGAN copy-paste isi kode ini ke Terminal, dan jangan klik 2x langsung dari File Explorer
    (karena jendela hitam akan langsung menutup saat selesai).
  - Jalankan lewat Terminal (Command Prompt / CMD, PowerShell, atau Terminal VS Code):
      1. Arahkan Terminal ke folder proyek `tugas-qa-testing`:
         cd "...\tugas-qa-testing"
      2. Instal alat bantu (cukup 1 kali saja):
         pip install playwright aiohttp
         playwright install chromium
      3. Jalankan script ini dengan mengetik:
         python 03-hasil-pengujian/automation-scripts/test_performance_gor_permata.py
  - Alternatif di VS Code: buka file ini di VS Code, pastikan Python extension terpasang, lalu klik tombol Run (`▶`) di pojok kanan atas.
  - Hasil otomatis tersimpan ke `performance-log.txt` dan `evidence/performance-metrics.json`.
"""
from __future__ import annotations

import asyncio
import json
import math
import statistics
import time
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any

import aiohttp
from playwright.sync_api import sync_playwright

SCRIPT_DIR = Path(__file__).resolve().parent
BASE_DIR = SCRIPT_DIR.parent
PROFILE_PATH = BASE_DIR / "test-data" / "performance-profiles.json"
METRICS_JSON_PATH = BASE_DIR / "evidence" / "performance-metrics.json"
LOG_PATH = SCRIPT_DIR / "performance-log.txt"


def percentile(sorted_vals: list[float], p: float) -> float:
    if not sorted_vals:
        return 0.0
    if len(sorted_vals) == 1:
        return round(sorted_vals[0], 2)
    k = (len(sorted_vals) - 1) * (p / 100.0)
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return round(sorted_vals[int(k)], 2)
    d0 = sorted_vals[f] * (c - k)
    d1 = sorted_vals[c] * (k - f)
    return round(d0 + d1, 2)


def measure_page_vitals(page, url: str) -> dict[str, Any]:
    """Muat halaman dan kumpulkan Navigation Timing, FCP, LCP, CLS, serta Resource Timing."""
    page.add_init_script(
        """() => {
            window.__qaPerf = { fcp: null, lcp: null, cls: 0 };
            try {
                new PerformanceObserver((list) => {
                    for (const entry of list.getEntries()) {
                        if (entry.name === 'first-contentful-paint') {
                            window.__qaPerf.fcp = entry.startTime;
                        }
                    }
                }).observe({ type: 'paint', buffered: true });

                new PerformanceObserver((list) => {
                    const entries = list.getEntries();
                    if (entries.length) {
                        window.__qaPerf.lcp = entries[entries.length - 1].startTime;
                    }
                }).observe({ type: 'largest-contentful-paint', buffered: true });

                new PerformanceObserver((list) => {
                    for (const entry of list.getEntries()) {
                        if (!entry.hadRecentInput) {
                            window.__qaPerf.cls += entry.value;
                        }
                    }
                }).observe({ type: 'layout-shift', buffered: true });
            } catch (e) {}
        }"""
    )

    failed_assets: list[dict[str, Any]] = []
    page.on(
        "response",
        lambda res: failed_assets.append({"url": res.url, "status": res.status})
        if res.status >= 400
        else None,
    )

    t0 = time.perf_counter()
    resp = page.goto(url, wait_until="load", timeout=30000)
    wall_load_ms = (time.perf_counter() - t0) * 1000.0
    # Beri jeda singkat untuk stabilisasi observer LCP/CLS
    page.wait_for_timeout(400)

    metrics = page.evaluate(
        """() => {
            const nav = performance.getEntriesByType('navigation')[0];
            const res = performance.getEntriesByType('resource');
            const paintFcp = performance.getEntriesByName('first-contentful-paint')[0];
            const totalTransfer = res.reduce((acc, r) => acc + (r.transferSize || 0), 0);
            const totalDecoded = res.reduce((acc, r) => acc + (r.decodedBodySize || 0), 0);
            return {
                dns_ms: nav ? Math.max(0, nav.domainLookupEnd - nav.domainLookupStart) : 0,
                tcp_ms: nav ? Math.max(0, nav.connectEnd - nav.connectStart) : 0,
                tls_ms: nav && nav.secureConnectionStart > 0 ? Math.max(0, nav.connectEnd - nav.secureConnectionStart) : 0,
                ttfb_ms: nav ? Math.max(0, nav.responseStart - nav.requestStart) : 0,
                dcl_ms: nav ? Math.max(0, nav.domContentLoadedEventEnd - nav.startTime) : 0,
                load_ms: nav ? Math.max(0, nav.loadEventEnd - nav.startTime) : 0,
                doc_transfer_bytes: nav ? (nav.transferSize || 0) : 0,
                doc_encoded_bytes: nav ? (nav.encodedBodySize || 0) : 0,
                doc_decoded_bytes: nav ? (nav.decodedBodySize || 0) : 0,
                resource_count: res.length,
                resources_transfer_bytes: totalTransfer,
                resources_decoded_bytes: totalDecoded,
                fcp_ms: window.__qaPerf?.fcp ?? (paintFcp ? paintFcp.startTime : null),
                lcp_ms: window.__qaPerf?.lcp ?? null,
                cls: Number((window.__qaPerf?.cls ?? 0).toFixed(4))
            };
        }"""
    )

    return {
        "url": url,
        "http_status": resp.status if resp else None,
        "wall_load_ms": round(wall_load_ms, 2),
        "dns_ms": round(metrics["dns_ms"], 2),
        "tcp_ms": round(metrics["tcp_ms"], 2),
        "tls_ms": round(metrics["tls_ms"], 2),
        "ttfb_ms": round(metrics["ttfb_ms"], 2),
        "dcl_ms": round(metrics["dcl_ms"], 2),
        "load_ms": round(metrics["load_ms"], 2),
        "fcp_ms": round(metrics["fcp_ms"], 2) if metrics["fcp_ms"] is not None else None,
        "lcp_ms": round(metrics["lcp_ms"], 2) if metrics["lcp_ms"] is not None else None,
        "cls": metrics["cls"],
        "doc_transfer_bytes": metrics["doc_transfer_bytes"],
        "doc_encoded_bytes": metrics["doc_encoded_bytes"],
        "doc_decoded_bytes": metrics["doc_decoded_bytes"],
        "resource_count": metrics["resource_count"],
        "resources_transfer_bytes": metrics["resources_transfer_bytes"],
        "failed_assets_count": len(failed_assets),
        "failed_assets": failed_assets,
    }


def run_browser_tier(profiles: dict[str, Any], tomorrow: str) -> dict[str, Any]:
    base_url = profiles["metadata"]["base_url"]
    desktop_vp = profiles["browser_viewports"]["desktop"]
    mobile_vp = profiles["browser_viewports"]["mobile"]

    route_map = {
        "/": f"{base_url}/",
        "/booking": f"{base_url}/booking?start_date={tomorrow}",
        "/login": f"{base_url}/login",
        "/fasilitas/lapangan": f"{base_url}/fasilitas/lapangan",
    }

    cold_desktop: dict[str, Any] = {}
    warm_desktop: dict[str, Any] = {}
    cold_mobile: dict[str, Any] = {}
    interactions: dict[str, Any] = {}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        # Tier 1A: Cold Cache Desktop
        for key, url in route_map.items():
            ctx = browser.new_context(viewport=desktop_vp)
            page = ctx.new_page()
            cold_desktop[key] = measure_page_vitals(page, url)
            ctx.close()

        # Tier 1B: Warm Cache Desktop (/ and /booking)
        ctx_warm = browser.new_context(viewport=desktop_vp)
        for key in ("/", "/booking"):
            page = ctx_warm.new_page()
            _ = measure_page_vitals(page, route_map[key])  # Priming cache
            warm_desktop[key] = measure_page_vitals(page, route_map[key])  # Warm run
            page.close()
        ctx_warm.close()

        # Tier 1C: Cold Cache Mobile (/ and /booking)
        for key in ("/", "/booking"):
            ctx_m = browser.new_context(viewport=mobile_vp)
            page_m = ctx_m.new_page()
            cold_mobile[key] = measure_page_vitals(page_m, route_map[key])
            ctx_m.close()

        # Tier 2: Client-Side Interaction Timing pada /booking
        ctx_int = browser.new_context(viewport=desktop_vp)
        page_int = ctx_int.new_page()
        page_int.route("**/bookings/store", lambda r: r.abort())
        page_int.goto(route_map["/booking"], wait_until="load", timeout=30000)

        slots = page_int.locator('[onclick*="openBooking("]')
        if slots.count() > 0:
            t_open0 = time.perf_counter()
            slots.first.click()
            page_int.locator("#bookingModal").wait_for(state="visible", timeout=5000)
            open_ms = (time.perf_counter() - t_open0) * 1000.0

            dur_timings: list[float] = []
            for d in ("2", "3", "4", "5"):
                t_d0 = time.perf_counter()
                page_int.select_option("#custDuration", d)
                dur_timings.append((time.perf_counter() - t_d0) * 1000.0)

            page_int.evaluate("closeModal()")

            day_after = (date.today() + timedelta(days=2)).isoformat()
            t_cd0 = time.perf_counter()
            page_int.evaluate(f"changeDate('{day_after}')")
            page_int.wait_for_load_state("load", timeout=30000)
            change_date_ms = (time.perf_counter() - t_cd0) * 1000.0

            interactions = {
                "openBooking_ms": round(open_ms, 2),
                "updateTotal_avg_ms": round(statistics.mean(dur_timings), 2),
                "updateTotal_max_ms": round(max(dur_timings), 2),
                "changeDate_reload_ms": round(change_date_ms, 2),
            }
        ctx_int.close()
        browser.close()

    return {
        "cold_desktop": cold_desktop,
        "warm_desktop": warm_desktop,
        "cold_mobile": cold_mobile,
        "client_interactions": interactions,
    }


async def run_http_tier(profiles: dict[str, Any], tomorrow: str) -> dict[str, Any]:
    base_url = profiles["metadata"]["base_url"]
    routes = [
        "/" if r == "/" else (f"/booking?start_date={tomorrow}" if r == "/booking" else r)
        for r in profiles["routes"]
    ]
    breaker = profiles["circuit_breaker"]
    timeout = aiohttp.ClientTimeout(total=breaker["request_timeout_s"])
    headers = {
        "User-Agent": "Mozilla/5.0 (QA-Perf-Benchmark/1.0)",
        "Accept-Encoding": "gzip, deflate",
    }

    tier_results: list[dict[str, Any]] = []
    aborted_reason: str | None = None

    connector = aiohttp.TCPConnector(limit=15)
    async with aiohttp.ClientSession(timeout=timeout, headers=headers, connector=connector) as session:
        # Audit encoding & header ringkas per rute
        route_encoding_audit: dict[str, Any] = {}
        for r in routes:
            t0 = time.perf_counter()
            async with session.get(base_url + r) as resp:
                raw_body = await resp.read()
                dt_ms = (time.perf_counter() - t0) * 1000.0
                route_encoding_audit[r] = {
                    "status": resp.status,
                    "content_encoding": resp.headers.get("Content-Encoding"),
                    "cache_control": resp.headers.get("Cache-Control"),
                    "decoded_chars": len(raw_body.decode("utf-8", errors="replace")),
                    "probe_ms": round(dt_ms, 2),
                }

        for tier in profiles["workload_tiers"]:
            vus = tier["vus"]
            iters = tier["iterations_per_vu"]
            think_s = tier["think_time_ms"] / 1000.0
            records: list[dict[str, Any]] = []

            async def worker(vu_id: int) -> None:
                for _ in range(iters):
                    for r in routes:
                        t0 = time.perf_counter()
                        status_code = 0
                        err = None
                        try:
                            async with session.get(base_url + r) as resp:
                                await resp.read()
                                status_code = resp.status
                        except Exception as exc:
                            err = str(exc)
                        dt_ms = (time.perf_counter() - t0) * 1000.0
                        records.append(
                            {
                                "vu": vu_id,
                                "route": r,
                                "status": status_code,
                                "latency_ms": dt_ms,
                                "error": err,
                            }
                        )
                        if think_s > 0:
                            await asyncio.sleep(think_s)

            t_tier0 = time.perf_counter()
            await asyncio.gather(*(worker(i + 1) for i in range(vus)))
            tier_wall_s = time.perf_counter() - t_tier0

            total_req = len(records)
            errors = [x for x in records if x["error"] or x["status"] >= 400 or x["status"] == 0]
            has_429 = any(x["status"] == 429 for x in records)
            error_rate = (len(errors) / total_req * 100.0) if total_req else 0.0

            per_route_stats: dict[str, Any] = {}
            for r in routes:
                lats = sorted(x["latency_ms"] for x in records if x["route"] == r and not x["error"])
                r_errs = sum(1 for x in records if x["route"] == r and (x["error"] or x["status"] >= 400))
                per_route_stats[r] = {
                    "count": len(lats) + r_errs,
                    "errors": r_errs,
                    "min_ms": round(min(lats), 2) if lats else None,
                    "mean_ms": round(statistics.mean(lats), 2) if lats else None,
                    "p50_ms": percentile(lats, 50),
                    "p90_ms": percentile(lats, 90),
                    "p95_ms": percentile(lats, 95),
                    "p99_ms": percentile(lats, 99),
                    "max_ms": round(max(lats), 2) if lats else None,
                }

            all_lats = sorted(x["latency_ms"] for x in records if not x["error"])
            tier_summary = {
                "id": tier["id"],
                "name": tier["name"],
                "vus": vus,
                "total_requests": total_req,
                "wall_time_s": round(tier_wall_s, 2),
                "rps": round(total_req / tier_wall_s, 2) if tier_wall_s > 0 else 0.0,
                "error_count": len(errors),
                "error_rate_pct": round(error_rate, 2),
                "overall_p50_ms": percentile(all_lats, 50),
                "overall_p95_ms": percentile(all_lats, 95),
                "overall_max_ms": round(max(all_lats), 2) if all_lats else None,
                "per_route": per_route_stats,
            }
            tier_results.append(tier_summary)

            if (breaker["abort_on_http_429"] and has_429) or error_rate > breaker["max_error_rate_pct"]:
                aborted_reason = (
                    f"Circuit breaker triggered at {tier['id']}: error_rate={error_rate:.2f}%, has_429={has_429}"
                )
                break

            if tier["cooldown_after_s"] > 0:
                await asyncio.sleep(tier["cooldown_after_s"])

    return {
        "route_encoding_audit": route_encoding_audit,
        "tiers": tier_results,
        "aborted_reason": aborted_reason,
    }


def evaluate_tc_perf(data: dict[str, Any], sla: dict[str, Any]) -> list[dict[str, Any]]:
    """Evaluasi hasil TC-PERF-01 s.d. TC-PERF-10 terhadap ambang SLA."""
    cases: list[dict[str, Any]] = []
    cd = data["browser"]["cold_desktop"]
    wd = data["browser"]["warm_desktop"]
    cm = data["browser"]["cold_mobile"]
    inter = data["browser"]["client_interactions"]
    tiers = {t["id"]: t for t in data["http_concurrency"]["tiers"]}

    def add_case(tc_id: str, name: str, passed: bool, expected: str, actual: str) -> None:
        cases.append(
            {
                "tc_id": tc_id,
                "name": name,
                "status": "PASS" if passed else "FAIL",
                "expected": expected,
                "actual": actual,
            }
        )

    def fmt_lcp(val: Any) -> str:
        return f"{val}ms" if val is not None else "N/A(headless)"

    # TC-PERF-01: / Cold Desktop
    h = cd["/"]
    h_ok = (
        h["ttfb_ms"] <= sla["ttfb_default_max"]
        and (h["fcp_ms"] is not None and h["fcp_ms"] <= sla["fcp_max"])
        and (h["lcp_ms"] is None or h["lcp_ms"] <= sla["lcp_max"])
        and h["cls"] <= sla["cls_max"]
    )
    add_case(
        "TC-PERF-01",
        "Web Vitals Cold Desktop (/)",
        h_ok,
        f"TTFB<={sla['ttfb_default_max']}ms, FCP<={sla['fcp_max']}ms, CLS<={sla['cls_max']}",
        f"TTFB={h['ttfb_ms']}ms, DCL={h['dcl_ms']}ms, Load={h['load_ms']}ms, FCP={h['fcp_ms']}ms, LCP={fmt_lcp(h['lcp_ms'])}, CLS={h['cls']}",
    )

    # TC-PERF-02: /booking Cold Desktop
    b = cd["/booking"]
    b_ok = (
        b["ttfb_ms"] <= sla["ttfb_booking_max"]
        and (b["fcp_ms"] is not None and b["fcp_ms"] <= sla["fcp_max"])
        and (b["lcp_ms"] is None or b["lcp_ms"] <= sla["lcp_max"])
        and b["cls"] <= sla["cls_max"]
    )
    add_case(
        "TC-PERF-02",
        "Web Vitals Cold Desktop (/booking)",
        b_ok,
        f"TTFB<={sla['ttfb_booking_max']}ms, FCP<={sla['fcp_max']}ms, CLS<={sla['cls_max']}",
        f"TTFB={b['ttfb_ms']}ms, DCL={b['dcl_ms']}ms, Load={b['load_ms']}ms, FCP={b['fcp_ms']}ms, LCP={fmt_lcp(b['lcp_ms'])}, CLS={b['cls']}",
    )

    # TC-PERF-03: /login & /fasilitas/lapangan Cold Desktop
    l_m = cd["/login"]
    f_m = cd["/fasilitas/lapangan"]
    lf_ok = (
        l_m["ttfb_ms"] <= sla["ttfb_default_max"]
        and f_m["ttfb_ms"] <= sla["ttfb_default_max"]
        and (l_m["fcp_ms"] is not None and l_m["fcp_ms"] <= sla["fcp_max"])
        and (f_m["fcp_ms"] is not None and f_m["fcp_ms"] <= sla["fcp_max"])
    )
    add_case(
        "TC-PERF-03",
        "Web Vitals Cold Desktop (/login & /fasilitas/lapangan)",
        lf_ok,
        f"TTFB<={sla['ttfb_default_max']}ms, FCP<={sla['fcp_max']}ms",
        f"/login(TTFB={l_m['ttfb_ms']}ms, FCP={l_m['fcp_ms']}ms, Load={l_m['load_ms']}ms) | /fasilitas/lapangan(TTFB={f_m['ttfb_ms']}ms, FCP={f_m['fcp_ms']}ms, Load={f_m['load_ms']}ms)",
    )

    # TC-PERF-04: Warm vs Cold Cache (/ & /booking)
    w_home = wd["/"]
    w_book = wd["/booking"]
    w_ok = w_home["failed_assets_count"] == 0 and w_book["failed_assets_count"] == 0
    add_case(
        "TC-PERF-04",
        "Komparasi Warm Cache vs Cold Cache (/ & /booking)",
        w_ok,
        "Warm load tanpa error aset (0 failed_assets)",
        f"/(Cold Load={h['load_ms']}ms vs Warm={w_home['load_ms']}ms) | /booking(Cold Load={b['load_ms']}ms vs Warm={w_book['load_ms']}ms)",
    )

    # TC-PERF-05: Mobile 390x844 Web Vitals
    mh = cm["/"]
    mb = cm["/booking"]
    m_ok = (
        mh["ttfb_ms"] <= sla["ttfb_default_max"]
        and mb["ttfb_ms"] <= sla["ttfb_booking_max"]
        and (mh["fcp_ms"] is not None and mh["fcp_ms"] <= sla["fcp_max"])
        and (mb["fcp_ms"] is not None and mb["fcp_ms"] <= sla["fcp_max"])
    )
    add_case(
        "TC-PERF-05",
        "Web Vitals Mobile 390x844 (/ & /booking)",
        m_ok,
        f"/ TTFB<={sla['ttfb_default_max']}ms, /booking TTFB<={sla['ttfb_booking_max']}ms, FCP<={sla['fcp_max']}ms",
        f"Mobile /(TTFB={mh['ttfb_ms']}ms, FCP={mh['fcp_ms']}ms, Load={mh['load_ms']}ms, CLS={mh['cls']}) | Mobile /booking(TTFB={mb['ttfb_ms']}ms, FCP={mb['fcp_ms']}ms, Load={mb['load_ms']}ms, CLS={mb['cls']})",
    )

    # TC-PERF-06: Audit Payload & Kompresi HTML /booking
    booking_raw_kb = round(b["doc_decoded_bytes"] / 1024.0, 2)
    booking_enc_kb = round(b["doc_encoded_bytes"] / 1024.0, 2)
    payload_ok = booking_raw_kb <= sla["booking_html_uncompressed_warn_kb"] and b["failed_assets_count"] == 0
    add_case(
        "TC-PERF-06",
        "Audit Resource Payload & Kompresi HTML /booking",
        payload_ok,
        f"HTML raw <= {sla['booking_html_uncompressed_warn_kb']} KB, 0 failed assets",
        f"/booking HTML raw={booking_raw_kb} KB (encoded={booking_enc_kb} KB, assets={b['resource_count']}, res_transfer={round(b['resources_transfer_bytes']/1024, 1)} KB)",
    )

    # TC-PERF-07: Client Interaction Timing
    int_ok = (
        bool(inter)
        and inter["openBooking_ms"] <= sla["interaction_max"]
        and inter["updateTotal_max_ms"] <= sla["interaction_max"]
    )
    add_case(
        "TC-PERF-07",
        "Client-Side DOM Interaction Latency (/booking)",
        int_ok,
        f"openBooking & updateTotal <= {sla['interaction_max']} ms",
        str(inter),
    )

    # TC-PERF-08, 09, 10: Concurrent HTTP Tiers
    for tc_id, tier_id in [
        ("TC-PERF-08", "LEVEL-A-BASELINE"),
        ("TC-PERF-09", "LEVEL-B-NORMAL"),
        ("TC-PERF-10", "LEVEL-C-PEAK-SAFE"),
    ]:
        t = tiers.get(tier_id)
        if not t:
            add_case(tc_id, f"HTTP Benchmark {tier_id}", False, "Tier selesai dijalankan", "Dibatalkan circuit breaker")
            continue
        # Cek p95 tiap rute
        booking_key = [k for k in t["per_route"] if k.startswith("/booking")][0]
        booking_p95 = t["per_route"][booking_key]["p95_ms"] or 0
        other_p95_max = max((v["p95_ms"] or 0) for k, v in t["per_route"].items() if k != booking_key)
        t_ok = (
            t["error_rate_pct"] == 0.0
            and other_p95_max <= sla["p95_default_max"]
            and booking_p95 <= sla["p95_booking_max"]
        )
        add_case(
            tc_id,
            f"HTTP Benchmark {t['name']}",
            t_ok,
            f"Error=0%, p95 default<={sla['p95_default_max']}ms, p95 /booking<={sla['p95_booking_max']}ms",
            f"req={t['total_requests']}, err={t['error_rate_pct']}%, rps={t['rps']}, overall_p50={t['overall_p50_ms']}ms, overall_p95={t['overall_p95_ms']}ms, booking_p95={booking_p95}ms",
        )

    return cases


def main() -> None:
    profiles = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
    METRICS_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    tomorrow = (date.today() + timedelta(days=1)).isoformat()
    started = datetime.now().astimezone().isoformat(timespec="seconds")

    print(f"=== PERFORMANCE TEST START: {started} | TARGET: {profiles['metadata']['base_url']} ===")
    browser_data = run_browser_tier(profiles, tomorrow)
    http_data = asyncio.run(run_http_tier(profiles, tomorrow))

    combined = {
        "metadata": {
            "timestamp": started,
            "target": profiles["metadata"]["base_url"],
            "tomorrow_param": tomorrow,
            "safety_policy": profiles["metadata"]["safety_policy"],
        },
        "browser": browser_data,
        "http_concurrency": http_data,
    }
    cases = evaluate_tc_perf(combined, profiles["sla_thresholds_ms"])
    combined["test_cases"] = cases

    METRICS_JSON_PATH.write_text(json.dumps(combined, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    lines = [f"=== PERFORMANCE EXECUTION LOG: {started} | TARGET: {profiles['metadata']['base_url']} ==="]
    for c in cases:
        line = f"[{c['status']}] {c['tc_id']} - {c['name']}: expected={c['expected']} | actual={c['actual']}"
        lines.append(line)
        print(line)

    passed = sum(1 for c in cases if c["status"] == "PASS")
    lines.append(
        f"=== SUMMARY: {passed}/{len(cases)} PASS | Aborted={http_data['aborted_reason']} ==="
    )
    LOG_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\nMetrik JSON disimpan ke: {METRICS_JSON_PATH}")
    print(f"Log performa disimpan ke: {LOG_PATH}")


if __name__ == "__main__":
    main()
