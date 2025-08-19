# import asyncio
# from playwright.sync_api import sync_playwright, TimeoutError
# import time

# # Set ProactorEventLoop for Windows compatibility
# if hasattr(asyncio, 'WindowsProactorEventLoopPolicy'):
#     asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

# def fetch_pib_links(day, month, year):
#     with sync_playwright() as p:
#         # Launch browser in non-headless mode for debugging
#         browser = p.chromium.launch(headless=False, args=["--disable-blink-features=AutomationControlled"])
#         page = browser.new_page()

#         try:
#             print("🌐 Navigating to PIB site...")
#             page.goto("https://pib.gov.in/allRel.aspx?reg=3&lang=1", timeout=60000)
#             print(f"✅ Successfully navigated to: {page.url}")

#             # Select Ministry of Power
#             ministry_dropdown = page.locator("#ContentPlaceHolder1_ddlMinistry")
#             print("⏳ Waiting for the 'Ministry' dropdown to be visible...")
#             ministry_dropdown.wait_for(state="visible", timeout=20000)
#             print("✅ 'Ministry' dropdown is now visible.")

#             print("⚙️ Selecting 'Ministry of Power'...")
#             with page.expect_response("**/allRel.aspx**") as response_info:
#                 ministry_dropdown.select_option(value="52")
#             print(f"✅ Ministry selection triggered a response with status: {response_info.value.status}")

#             # Wait for page to stabilize after postback
#             page.wait_for_load_state("networkidle", timeout=20000)

#             # Verify Ministry selection
#             selected_ministry = page.locator("#ContentPlaceHolder1_ddlMinistry").input_value()
#             if selected_ministry != "52":
#                 print("⚠️ Ministry selection reset! Re-selecting...")
#                 with page.expect_response("**/allRel.aspx**"):
#                     ministry_dropdown.select_option(value="52")
#                 page.wait_for_load_state("networkidle", timeout=20000)

#             # Select Year
#             year_dropdown = page.locator("#ContentPlaceHolder1_ddlYear")
#             print(f"⚙️ Selecting 'Year' as {year}...")
#             with page.expect_response("**/allRel.aspx**") as response_info:
#                 year_dropdown.select_option(value=str(year))
#             print(f"✅ Year selection triggered a response with status: {response_info.value.status}")
#             page.wait_for_load_state("networkidle", timeout=20000)

#             # Verify Year selection
#             selected_year = page.locator("#ContentPlaceHolder1_ddlYear").input_value()
#             if selected_year != str(year):
#                 print("⚠️ Year selection reset! Re-selecting...")
#                 with page.expect_response("**/allRel.aspx**"):
#                     year_dropdown.select_option(value=str(year))
#                 page.wait_for_load_state("networkidle", timeout=20000)

#             # Select Month
#             month_dropdown = page.locator("#ContentPlaceHolder1_ddlMonth")
#             print(f"⚙️ Selecting 'Month' as {month}...")
#             with page.expect_response("**/allRel.aspx**") as response_info:
#                 month_dropdown.select_option(value=str(month))
#             print(f"✅ Month selection triggered a response with status: {response_info.value.status}")
#             page.wait_for_load_state("networkidle", timeout=20000)

#             # Verify Month selection
#             selected_month = page.locator("#ContentPlaceHolder1_ddlMonth").input_value()
#             if selected_month != str(month):
#                 print("⚠️ Month selection reset! Re-selecting...")
#                 with page.expect_response("**/allRel.aspx**"):
#                     month_dropdown.select_option(value=str(month))
#                 page.wait_for_load_state("networkidle", timeout=20000)

#             # Select Day
#             day_dropdown = page.locator("#ContentPlaceHolder1_ddlday")
#             print(f"⚙️ Selecting 'Day' as {day}...")
#             with page.expect_response("**/allRel.aspx**") as response_info:
#                 day_dropdown.select_option(value=str(day))
#             print(f"✅ Day selection triggered a response with status: {response_info.value.status}")
#             page.wait_for_load_state("networkidle", timeout=20000)

#             # Wait for results to load
#             print("⏳ Waiting for results to load...")
#             try:
#                 page.wait_for_selector(".content-area ul li a", timeout=30000)
#                 print("✅ Results loaded.")
#             except TimeoutError:
#                 print("⚠️ No results found with '.content-area ul li a' selector. Capturing page state...")
#                 page.screenshot(path="no_results_error.png")
#                 with open("page_content.html", "w", encoding="utf-8") as f:
#                     f.write(page.content())
#                 print("📸 Saved screenshot as 'no_results_error.png' and HTML as 'page_content.html'.")
#                 return []

#             # Extract all press release links
#             print("🔍 Extracting press release links...")
#             link_elements = page.locator(".content-area ul li a").all()
#             press_releases = []
#             for link in link_elements:
#                 href = link.get_attribute("href")
#                 title = link.get_attribute("title")
#                 date_span = link.locator("xpath=following-sibling::span[@class='publishdatesmall']").first
#                 date = date_span.inner_text().strip() if date_span.is_visible() else "No date found"
#                 if href and href.startswith("/PressReleasePage.aspx"):
#                     full_url = f"https://pib.gov.in{href}"
#                     press_releases.append({"title": title, "url": full_url, "date": date})

#             # Print extracted links
#             print(f"📋 Found {len(press_releases)} press releases:")
#             for release in press_releases:
#                 print(f"Title: {release['title']}\nURL: {release['url']}\nDate: {release['date']}\n")

#             # Visit each link and check for keywords
#             keywords = ["transmission", "distribution", "hvdc", "grid"]
#             filtered_releases = []
#             print(f"🔎 Checking content of each press release for keywords: {keywords}")
#             for release in press_releases:
#                 url = release["url"]
#                 print(f"🌐 Visiting {url}...")
#                 try:
#                     page.goto(url, timeout=60000)
#                     page.wait_for_load_state("networkidle", timeout=20000)
#                     # Extract content from the body or a specific content area
#                     content = page.locator("body").inner_text().lower()
#                     # Check for each keyword and collect matches
#                     matched_keywords = [keyword for keyword in keywords if keyword.lower() in content]
#                     if matched_keywords:
#                         print(f"✅ Found keyword(s) in {url}: {matched_keywords}")
#                         release["keywords"] = matched_keywords
#                         filtered_releases.append(release)
#                     else:
#                         print(f"❌ No keywords found in {url}")
#                 except TimeoutError as e:
#                     print(f"❌ Timeout while visiting {url}: {e}")
#                     page.screenshot(path=f"timeout_{url.split('PRID=')[-1]}.png")
#                 except Exception as e:
#                     print(f"❌ Error while visiting {url}: {e}")
#                     page.screenshot(path=f"error_{url.split('PRID=')[-1]}.png")

#             # Print filtered links with matched keywords
#             print(f"\n📋 Found {len(filtered_releases)} press releases containing keywords:")
#             for release in filtered_releases:
#                 print(f"Title: {release['title']}\nURL: {release['url']}\nDate: {release['date']}\nKeywords: {release['keywords']}\n")

#             # Keep browser open for inspection
#             print("⏱️ Keeping browser open for 10 seconds to allow for inspection.")
#             time.sleep(10)

#             return filtered_releases

#         except TimeoutError as e:
#             print(f"❌ Timeout: An operation took too long to complete. Details: {e}")
#             page.screenshot(path="timeout_error.png")
#             return []
#         except Exception as e:
#             print(f"❌ Unexpected error: {e}")
#             page.screenshot(path="error_screenshot.png")
#             return []
#         finally:
#             browser.close()
#             print("🧹 Browser closed.")











# playwrightCode.py
import os, random, time
from playwright.sync_api import sync_playwright, TimeoutError

BRIGHTDATA_WS = os.getenv("BRIGHTDATA_WS", "").strip()

def _normalize_ws(ws: str) -> str:
    if not ws:
        raise RuntimeError("BRIGHTDATA_WS is not set. Paste the Playwright wss:// from Bright Data.")
    # If missing the playwright path, add it, and rotate a session to reduce blocks
    if "/playwright" not in ws:
        sep = "&" if "?" in ws else "?"
        ws = ws.rstrip("/") + "/playwright" + f"{sep}session=ses_{random.randint(10**6,10**7-1)}"
    return ws

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")

def fetch_pib_links(day: str, month: str, year: str):
    ws = _normalize_ws(BRIGHTDATA_WS)

    with sync_playwright() as p:
        # prefer connect_over_cdp if available
        connect_over_cdp = getattr(p.chromium, "connect_over_cdp", None)
        browser = connect_over_cdp(ws) if connect_over_cdp else p.chromium.connect(ws)

        context = browser.contexts[0] if browser.contexts else browser.new_context(
            user_agent=UA,
            viewport={"width": 1366, "height": 768},
            locale="en-US",
            timezone_id="Asia/Kolkata",
            extra_http_headers={
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
                "Upgrade-Insecure-Requests": "1",
            },
        )
        page = context.new_page()
        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
            Object.defineProperty(navigator, 'languages', { get: () => ['en-US','en'] });
            Object.defineProperty(navigator, 'plugins', { get: () => [1,2,3] });
            window.chrome = { runtime: {} };
        """)

        try:
            # landing
            page.goto("https://pib.gov.in/allRel.aspx?reg=3&lang=1", wait_until="networkidle", timeout=120000)

            # ministry
            min_dd = page.locator("#ContentPlaceHolder1_ddlMinistry")
            min_dd.wait_for(state="visible", timeout=60000)
            with page.expect_response("**/allRel.aspx**"):
                min_dd.select_option(value="52")
            page.wait_for_load_state("networkidle", timeout=30000)

            # year
            y_dd = page.locator("#ContentPlaceHolder1_ddlYear")
            with page.expect_response("**/allRel.aspx**"):
                y_dd.select_option(value=str(year))
            page.wait_for_load_state("networkidle", timeout=30000)

            # month
            m_dd = page.locator("#ContentPlaceHolder1_ddlMonth")
            with page.expect_response("**/allRel.aspx**"):
                m_dd.select_option(value=str(month))
            page.wait_for_load_state("networkidle", timeout=30000)

            # day
            d_dd = page.locator("#ContentPlaceHolder1_ddlday")
            with page.expect_response("**/allRel.aspx**"):
                d_dd.select_option(value=str(day))
            page.wait_for_load_state("networkidle", timeout=30000)

            # results
            page.wait_for_selector(".content-area ul li a", timeout=45000)
            results = []
            for a in page.locator(".content-area ul li a").all():
                href = a.get_attribute("href")
                title = (a.get_attribute("title") or "No title").strip()
                if href and href.startswith("/PressReleasePage.aspx"):
                    span = a.locator("xpath=following-sibling::span[@class='publishdatesmall']").first
                    date_txt = span.inner_text().strip() if span.is_visible() else ""
                    results.append({"title": title, "url": f"https://pib.gov.in{href}", "date": date_txt})

            # optional keyword filter (same as your local)
            KEYWORDS = {"transmission", "distribution", "hvdc", "grid"}
            filtered = []
            for item in results:
                try:
                    page.goto(item["url"], wait_until="domcontentloaded", timeout=60000)
                    page.wait_for_load_state("networkidle", timeout=20000)
                    text = page.locator("body").inner_text().lower()
                    k = [w for w in KEYWORDS if w in text]
                    if k:
                        item["keywords"] = k
                        filtered.append(item)
                except TimeoutError:
                    continue

            return filtered or results
        finally:
            try:
                browser.close()
            except:
                pass
