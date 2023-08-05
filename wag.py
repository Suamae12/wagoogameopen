import json
import requests
import webbrowser
import pygame
import time

def load_config():
    with open("config.json", "r") as config_file:
        return json.load(config_file)

def retrieve_latest_message(channel_id, bot_token):
    headers = {
        'authorization': bot_token
    }
    params = {
        'limit': 1
    }
    r = requests.get(f'https://discord.com/api/v8/channels/{channel_id}/messages', headers=headers, params=params)
    try:
        message = r.json()[0]  # Only retrieve the latest message
    except json.JSONDecodeError as e:
        print("JSON decode error:", e)
        return None

    return message

def main():
    config = load_config()
    bot_token = config.get('bot_token')
    channel_id = config.get('channel_id')

    if not bot_token or not channel_id:
        print("Error: bot_token or channel_id not found in config.json")
        return

    pygame.init()
    pygame.mixer.init()
    sound = pygame.mixer.Sound("t.mp3")

    processed_message_ids = []
    try:
        while True:
            latest_message = retrieve_latest_message(channel_id, bot_token)
            if latest_message and latest_message['id'] not in processed_message_ids:
                processed_message_ids.append(latest_message['id'])

                print(f"Author: {latest_message['author']['username']}#{latest_message['author']['discriminator']}")
                print(f"Content: {latest_message.get('content', '')}")

                for embed in latest_message.get('embeds', []):
                    print("Embed:")
                    print(f"  Title: {embed.get('title', '')}")
                    print(f"  Description: {embed.get('description', '')}")
                    print(f"  URL: {embed.get('url', '')}")
                    for field in embed.get('fields', []):
                        field_name = field['name']
                        field_value = field['value']

                        if field_name.lower() == 'game':
                            game_id = field_value.split('/')[-1]
                            print(f"  Game ID: {game_id}")
                            url = f"roblox://placeID={game_id}"
                            print(f"Opening URL: {url}")
                            webbrowser.open_new_tab(url)

                sound.play()

            time.sleep(0.5)  # Wait for 0.5 seconds before checking again

    except KeyboardInterrupt:
        print("\nStopping...")

    pygame.mixer.quit()

if __name__ == "__main__":
    main()
