# autoreg_browser.py
import concurrent.futures
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

executor = concurrent.futures.ThreadPoolExecutor()

def run_in_thread(coro):
    return asyncio.get_event_loop().run_in_executor(executor, lambda: asyncio.run(coro))
