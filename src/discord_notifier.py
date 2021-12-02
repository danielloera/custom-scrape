import asyncio
import discord
import os

token = "DISCORD_TOKEN"
max_files_per_message = 10


def discord_name(name):
    return name.replace(' ', '_').replace('/', '_')


def convert_to_filenames(paths):
    return {discord_name(p): p for p in paths}


def send_scrape_result_messages(scrape_results, channel_name):
    client = discord.Client()

    @client.event
    async def on_ready():
        print('Logged in as {0.user}'.format(client))
        text_channel = [c for c in client.get_all_channels()
                        if c.name == channel_name][0]
        print('Scanning for new items...')
        await send_messages(text_channel, client.user)

    async def send_messages(text_channel, bot):
        current_screenshots_map = (
            await get_current_screenshots(text_channel, bot))
        for scrape_result in scrape_results:
            result_items = scrape_result.url_to_screenshots_map.items()
            if result_items:
                for url, screenshots in result_items:
                    filenames_map = convert_to_filenames(screenshots)
                    all_current = set(current_screenshots_map.keys())
                    new_pics = [filenames_map[f]
                                for f in set(filenames_map.keys()).difference(
                                all_current)]
                    print('{0.name}: {1} new items found.'.format(
                        scrape_result, len(new_pics)))
                    if new_pics:
                        for message in (current_screenshots_map[f]
                                        for f in all_current
                                        if discord_name(scrape_result.name)
                                        in f):
                            try:
                                await message.delete()
                            except discord.NotFound:
                                pass
                        screenshot_files = [
                            discord.File(open(s, 'rb'))
                            for s in new_pics]
                        # Discord only allows 10 files per message.
                        chunked_files = [screenshot_files[i:i + 10]
                                         for i in
                                         range(0, len(screenshot_files), 10)]
                        await text_channel.send(
                            content='{} {} results from: \n{}'.format(
                                len(new_pics), scrape_result.name, url),
                            files=chunked_files[0])
                        # Send the rest of the chunks, if present.
                        if len(chunked_files) > 1:
                            for chunk in chunked_files[1:]:
                                await text_channel.send(files=chunk)
                        for f in screenshot_files:
                            f.close()
                        print('Discord messages sent.')
            else:
                await delete_all_bot_messages(text_channel)
                await text_channel.send('Nothing found :(')
        await client.close()

    async def get_current_screenshots(text_channel, bot):
        print('Fetching current screenshots...')
        screenshots = {}
        async for message in text_channel.history(limit=100):
            if message.author == bot and message.attachments:
                for att in message.attachments:
                    screenshots[att.filename] = message
        print(f'Found {len(screenshots)} existing screenshots.')
        return screenshots

    async def delete_all_bot_messages(text_channel):
        print('Purging all bot messages')
        await text_channel.purge(
            limit=1000, check=lambda m: m.author == client.user)

    discord_token = os.getenv(token)
    if discord_token is None:
        raise ValueError(
            ('No Discord token found. '
             'Please set the "DISCORD_TOKEN" environment variable.'))

    client.run(discord_token)
