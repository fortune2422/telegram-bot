# autoreg_browser.py
import random, string, asyncio
from playwright.async_api import async_playwright

REGISTER_URL = "https://jili707.co/register"

def generate_random_account():
    username = "user" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    return username, password

async def auto_register():
    username, password = generate_random_account()
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        try:
            await page.goto(REGISTER_URL, timeout=20000)
            await page.fill('input[name="username"]', username)
            await page.fill('input[name="password"]', password)
            await page.fill('input[name="checkPass"]', password)
            await page.click("button:has-text('Register')")

            # 等待成功标志或跳转（你可以根据实际情况调整）
            await page.wait_for_timeout(2000)  # 等待页面反应

            content = await page.content()
            if "login" in content.lower() or "成功" in content.lower():
                return True, username, password
            else:
                return False, None, None
        except Exception as e:
            print("注册失败:", e)
            return False, None, None
        finally:
            await browser.close()
