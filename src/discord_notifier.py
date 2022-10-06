import asyncio
import discord
import os
from src.scraper import ScrapeResult

token = "DISCORD_TOKEN"
max_files_per_message = 10
scrape_results_log = "scrape_results.log"
no_changes_message = "No new results were found."

def send_scrape_result_messages(scrape_results: list[ScrapeResult],
                                channel_name: str,
                                notify_on_changes: bool):
  client = discord.Client(intents=discord.Intents.default())

  @client.event
  async def on_ready():
    print('Logged in as {0.user}'.format(client))
    text_channel = [c for c in client.get_all_channels()
                    if c.name == channel_name][0]
    changes_detected = new_changes_detected()
    if not notify_on_changes or changes_detected:
      print('Purging all bot messages')
      await delete_all_bot_messages(text_channel)
      print('Sending new messages')
      await send_messages(text_channel)

    if notify_on_changes and not changes_detected:
      print('No changes found.')
      async for msg in text_channel.history(limit=1000):
        if msg.content == no_changes_message:
          await msg.delete()
      await text_channel.send(content=no_changes_message)

    await client.close()

  def new_changes_detected():
    current_changes_key = str(sorted(scrape_results))
    if not os.path.isfile(scrape_results_log):
      with open(scrape_results_log, 'w') as log:
        print("Creating results log.")
        log.write(current_changes_key)
      return True

    with open(scrape_results_log, 'r+') as log:
      existing_key = log.read()
      if existing_key != current_changes_key:
        print('New changes found.')
        log.write(current_changes_key)
        return True
      return False

  async def delete_all_bot_messages(text_channel):
    await text_channel.purge(
        limit=1000, check=lambda m: m.author == client.user)

  async def send_messages(text_channel):
    for scrape_result in scrape_results:
      await text_channel.send(content=f'{scrape_result.name}:')
      result_items = scrape_result.url_to_scrape_data_map.items()
      if result_items:
        for url, scrape_data in result_items:
          if scrape_data:
            await text_channel.send(
                content=f'{len(scrape_data)} results from:\n{url}')
            for data in scrape_data:
              with open(data.screenshot, 'rb') as screenshot_file:
                discord_file = discord.File(screenshot_file)
                message_url = f'{url}{data.href}' if data.href.startswith('/') else data.href
                await text_channel.send(content=message_url, files=[discord_file])
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
