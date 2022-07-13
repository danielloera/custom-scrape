import asyncio
import discord
import os

token = "DISCORD_TOKEN"
max_files_per_message = 10


def send_scrape_result_messages(scrape_results, channel_name):
    client = discord.Client()

    @client.event
    async def on_ready():
        print('Logged in as {0.user}'.format(client))
        text_channel = [c for c in client.get_all_channels()
                        if c.name == channel_name][0]
        print('Purging all bot messages')
        await delete_all_bot_messages(text_channel)
        print('Sending new messages')
        await send_messages(text_channel)
        await client.close()

    async def delete_all_bot_messages(text_channel):
        await text_channel.purge(
            limit=1000, check=lambda m: m.author == client.user)

    async def send_messages(text_channel):
        for scrape_result in scrape_results:
            await text_channel.send(content=f'{scrape_result.name}:')
            result_items = scrape_result.url_to_screenshots_map.items()
            if result_items:
                for url, screenshots in result_items:
                    if screenshots:
                        screenshot_files = [discord.File(
                            open(s, 'rb')) for s in screenshots]
                        # Discord only allows 10 files per message.
                        chunked_files = [screenshot_files[i:i + 10]
                                         for i in
                                         range(0, len(screenshot_files), 10)]
                        await text_channel.send(
                            content=f'{len(screenshots)} results from:\n{url}',
                            files=chunked_files[0])
                        # Send the rest of the chunks, if present.
                        if len(chunked_files) > 1:
                            for chunk in chunked_files[1:]:
                                await text_channel.send(files=chunk)
                        for f in screenshot_files:
                            f.close()
            else:
                await text_channel.send('Nothing found :(')

    client.run(os.getenv(token))

def send_message(text, channel_name):
    client = discord.Client()

    @client.event
    async def on_ready():        
        text_channel = [c for c in client.get_all_channels()
                        if c.name == channel_name][0]
        await text_channel.purge(limit=1000)
        await text_channel.send(content=text)
        await client.close()

    client.run(os.getenv(token))


