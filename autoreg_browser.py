# autoreg_browser.py
import random, string, asyncio
from playwright.async_api import async_playwright

REGISTER_URL = "https://jili707.co/register"
LOGIN_URL = "https://jili707.co/login"

# 生成随机账号
def generate_random_account():
    username = "user" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    return username, password

async def playwright_register():
    username, password = generate_random_account()

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-gpu"]
            )
            context = await browser.new_context()
            page = await context.new_page()

            await page.goto(REGISTER_URL, timeout=20000)

            await page.fill('input[name="username"]', username)
            await page.fill('input[name="password"]', password)
            await page.fill('input[name="checkPass"]', password)

            await page.wait_for_selector("button.submit_btn", timeout=5000)
            await page.click("button.submit_btn")

            # 等待注册结果页加载
            await page.wait_for_timeout(3000)
            content = await page.content()

            # ✅ 检查页面内容是否有注册成功标志
            if "login" in content.lower() or "success" in content.lower() or "成功" in content:
                return True, username, password
            else:
                print("⚠️ 注册提交后返回页面未包含成功标志")
                return False, None, None

    except Exception as e:
        print("❌ 注册失败:", e)
        return False, None, None

async def playwright_check_info(username: str, password: str):
    print(f"🔐 正在使用 {username}/{password} 登录查询余额...")

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()

            await page.goto(LOGIN_URL, timeout=30000)

            await page.wait_for_selector('input[name="username"]', timeout=10000)
            await page.wait_for_selector('input[name="password"]', timeout=10000)

            await page.fill('input[name="username"]', username)
            await page.fill('input[name="password"]', password)
            await page.click('button[type="submit"]')

            await page.wait_for_timeout(3000)

            if "login" in page.url:
                print("❌ 登录失败：仍然停留在登录页面")
                return None

            content = await page.content()
            print("🔍 登录后页面内容部分：")
            print(content[:1000])

            # 读取余额
            try:
                await page.wait_for_selector("span.balance", timeout=5000)
                balance = await page.text_content("span.balance")
            except:
                print("❌ 未找到 balance 元素")
                balance = "N/A"

            # 读取邀请链接
            try:
                await page.wait_for_selector("input#address", timeout=5000)
                invite_url = await page.get_attribute("input#address", "value")
            except:
                print("❌ 未找到 invite_url 元素")
                invite_url = "N/A"

            return {
                "balance": (balance or "N/A").strip(),
                "invite_url": (invite_url or "N/A").strip()
            }

    except Exception as e:
        print("❌ playwright_check_info 报错:", e)
        return None


