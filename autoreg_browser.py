# autoreg_browser.py
import random, string, asyncio
from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright

REGISTER_URL = "https://jili707.co/register"

# 生成随机账号
def generate_random_account():
    username = "user" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    return username, password

# Playwright 注册函数，不再接收 update/context，只负责返回结果
async def playwright_register():
    username, password = generate_random_account()

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()

            # 打开注册页面
            await page.goto(REGISTER_URL, timeout=20000)

            # 填写表单
            await page.fill('input[name="username"]', username)
            await page.fill('input[name="password"]', password)
            await page.fill('input[name="checkPass"]', password)

            # 提交注册（建议用按钮类型选择器更稳）
            await page.wait_for_selector("button.submit_btn", timeout=5000)
            await page.click("button.submit_btn")


            # 等待页面响应（可视情况改为 wait_for_selector）
            await page.wait_for_timeout(2000)

            # 页面内容判断是否成功
            content = await page.content()
            if "login" in content.lower() or "success" in content.lower() or "成功" in content:
                return True, username, password
            else:
                return False, None, None

    except Exception as e:
        print("❌ 注册失败:", e)
        return False, None, None

    finally:
        await browser.close()

def playwright_check_info(username: str, password: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            page = browser.new_page()

            # 打开登录页面
            page.goto("https://jili707.co/login")

            # 输入用户名与密码
            page.fill('input[name="username"]', username)
            page.fill('input[name="password"]', password)

            # 点击登录按钮
            page.click('button[type="submit"]')

            # 等待登录后余额元素出现
            page.wait_for_selector("span.balance", timeout=5000)

            # 获取余额
            balance = page.text_content("span.balance") or "N/A"

            # 获取邀请码链接
            try:
                invite_url = page.get_attribute("input#address", "value") or "N/A"
            except:
                invite_url = "N/A"

            return {
                "balance": balance.strip(),
                "invite_url": invite_url.strip()
            }

        finally:
            browser.close()

