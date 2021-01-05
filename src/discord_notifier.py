import asyncio
import discord
import os

token = "DISCORD_TOKEN"
def send_scrape_result_messages(scrape_results, delete_screenshots=True):
    client = discord.Client()
    @client.event
    async def on_ready():
        print('Logged in as {0.user}'.format(client))
        await send_messages()

    async def send_messages():
        text_channel = [c for c in client.get_all_channels() if c.name == 'general'][0]
        for scrape_result in scrape_results:
            await text_channel.send(content=f'{scrape_result.name}:')
            for url, screenshots in scrape_result.url_to_screenshots_map.items():
                screenshot_files = [discord.File(open(s, 'rb')) for s in screenshots]
                # Discord limits 10 pictures per message.
                if len(screenshot_files) > 10:
                    screenshot_files = screenshot_files[:10]
                await text_channel.send(content=f'{len(screenshots)} results from {url} :', files=screenshot_files)
                for f in screenshot_files:
                    f.close()
                if delete_screenshots:
                    for sf in screenshots:
                        os.remove(sf)
        await client.close()

    client.run(os.getenv(token))
