import json
import pytest_asyncio
from playwright.async_api import async_playwright
from supporting_files import support_api_methods  # where GLOBAL_BEARER_TOKEN is defined

# 🔐 Fixture 1: Login and return context + browser
@pytest_asyncio.fixture(scope="session")
async def login_context():
    print("🔐 Logging in to get browser context...")
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=False)
    context = await browser.new_context()
    page = await context.new_page()

    await page.goto("https://now3.amagi.tv/signin")
    #await page.goto("https://integration.amaginow.tv/signin")
    #await page.fill('input[id="domainName"]', 'prod_push')
    await page.fill('input[id="domainName"]', 'lgusa')
    await page.click('button[type="submit"]')
    #await page.fill('input[name="username"]', 'veeresh.pn+prod_push@amagi.com')
    #await page.fill('input[name="password"]', 'Amagi@1234')
    await page.fill('input[name="username"]', 'harsha.patil@amagi.com')
    await page.fill('input[name="password"]', 'H@rsha2001')
    await page.click('button[type="submit"]')
    await page.wait_for_load_state("networkidle")

    # yield context so next fixture can use it
    yield context

    print("🔒 Closing browser...")
    await browser.close()
    await playwright.stop()

# 🔑 Fixture 2: Extract token from cookies and set global variable
@pytest_asyncio.fixture(scope="session", autouse=True)
async def bearer_token(login_context):
    print("📥 Extracting token from cookies...")
    cookies = await login_context.cookies()
    token_parts = {}

    for cookie in cookies:
        if cookie["name"].startswith("access_token_part_"):
            try:
                data = json.loads(cookie["value"])
                token_parts.update(data)
            except json.JSONDecodeError:
                print(f"⚠️ Failed to parse token part: {cookie['name']}")

    token = ''.join([token_parts[k] for k in sorted(token_parts.keys())])
    print(f"✅ Bearer token set: {token[:10]}...")  # truncate for safety
    return token

