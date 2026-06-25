import telebot
import asyncio
from playwright.async_api import async_playwright


# ==========================
# توکن ربات را اینجا قرار بده
# ==========================

BOT_TOKEN = "8942028679:AAFDCbBJhVioczUtlgD3B9gJbSVM2YVLz9o"


bot = telebot.TeleBot(BOT_TOKEN)


playwright = None
browser = None
page = None



async def start_browser():

    global playwright, browser, page


    if browser is None:

        playwright = await async_playwright().start()


        browser = await playwright.chromium.launch(

            headless=True,

            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage"
            ]

        )


        page = await browser.new_page()



async def run_command(text):

    try:

        await start_browser()


        text = text.strip()


        if text.startswith("باز کن"):


            url = text.replace(
                "باز کن",
                ""
            ).strip()


            if not url.startswith("http"):

                url = "https://" + url


            await page.goto(

                url,

                wait_until="domcontentloaded",

                timeout=60000

            )


            return "✅ سایت باز شد\n" + url



        elif text.startswith("کلیک"):


            button = text.replace(
                "کلیک",
                ""
            ).strip()


            await page.get_by_text(
                button
            ).first.click(
                timeout=10000
            )


            return "✅ کلیک انجام شد"



        elif text.startswith("تایپ"):


            value = text.replace(
                "تایپ",
                ""
            ).strip()


            await page.keyboard.type(
                value
            )


            return "✅ تایپ شد"



        elif text == "اسکرول":


            await page.mouse.wheel(
                0,
                1000
            )


            return "✅ اسکرول شد"



        elif text == "عکس":


            await page.screenshot(
                path="screen.png"
            )


            return "✅ عکس گرفته شد"



        else:


            return """
دستورها:

باز کن example.com

کلیک ورود

تایپ متن

اسکرول

عکس
"""



    except Exception as e:


        return "❌ خطا:\n" + str(e)




@bot.message_handler(
    func=lambda message: True
)

def handle(message):


    result = asyncio.run(
        run_command(
            message.text
        )
    )


    bot.reply_to(
        message,
        result
    )



print("Robot Started")


bot.infinity_polling(
    skip_pending=True
)