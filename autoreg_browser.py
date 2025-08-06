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
    browser = None

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False, slow_mo=100)  # 开启可视模式调试
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                viewport={'width': 1280, 'height': 800}
            )
            page = await context.new_page()

            await page.goto(REGISTER_URL, timeout=20000)
            await page.wait_for_selector('input[name="username"]')

            # 模拟人工输入
            await page.click('input[name="username"]')
            await page.keyboard.type(username)
            await asyncio.sleep(0.5)

            await page.click('input[name="password"]')
            await page.keyboard.type(password)
            await asyncio.sleep(0.5)

            await page.click('input[name="checkPass"]')
            await page.keyboard.type(password)
            await asyncio.sleep(0.5)

            await page.click("button.submit_btn")
            await page.wait_for_timeout(3000)

            content = await page.content()
            print(content[:800])  # 打印前 800 字，看看注册失败提示

            if "login" in content.lower() or "success" in content.lower() or "成功" in content:
                return True, username, password
            else:
                return False, None, None

    except Exception as e:
        print("❌ 注册失败:", e)
        return False, None, None

    finally:
        if browser:
            await browser.close()

async def playwright_check_info(username: str, password: str):
    browser = None

    try:
        print(f"🔐 正在使用 {username}/{password} 登录查询余额...")

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()

            await page.goto(LOGIN_URL, timeout=30000)

            # 等待页面的输入框加载完成再操作
            await page.wait_for_selector('input[name="username"]', timeout=10000)
            await page.wait_for_selector('input[name="password"]', timeout=10000)

            await page.fill('input[name="username"]', username)
            await page.fill('input[name="password"]', password)
            await page.click('button[type="submit"]')

            await page.wait_for_timeout(3000)  # 等待页面跳转加载

            # ✅ 登录是否成功
            if "login" in page.url:
                print("❌ 登录失败：仍然停留在登录页面")
                return None

            # 打印页面内容调试
            content = await page.content()
            print("🔍 登录后页面内容部分：")
            print(content[:1000])  # 避免日志过长

            # 查询余额
            try:
                await page.wait_for_selector("span.balance", timeout=5000)
                balance = await page.text_content("span.balance")
            except:
                print("❌ 未找到 balance 元素")
                balance = "N/A"

            # 查询邀请链接
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

    finally:
        if browser:
            await browser.close()

