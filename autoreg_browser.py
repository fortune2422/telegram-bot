# autoreg_browser.py
import random, string, asyncio
from playwright.async_api import async_playwright

REGISTER_URL = "https://jili707.co/register"

# 生成随机账号
def generate_random_account():
    username = "user" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    return username, password

# 注册主函数
async def auto_register():
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
            await page.click("button[type='submit']")

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
