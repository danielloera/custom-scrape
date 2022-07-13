printf "Pulling latest changes...\n"

git -C custom-scrape pull

printf "\n"

python3 custom-scrape/custom_scrape.py --discord_notification_channel general --config_file "custom-scrape/daniel_configs.json"

