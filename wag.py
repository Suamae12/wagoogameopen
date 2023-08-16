import json
import requests
import webbrowser
import pygame
import time
import pyperclip

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

def print_colored_message(message, color_code):
    print(f"\033[{color_code}m{message}\033[0m")

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
    open_links = True  # Control whether to open Roblox links
    last_clipboard = ""  # Store the last clipboard content to prevent repeated actions
    try:
        while True:
            latest_message = retrieve_latest_message(channel_id, bot_token)
            if latest_message and latest_message['id'] not in processed_message_ids:
                processed_message_ids.append(latest_message['id'])

                author = f"Author: \033[36m{latest_message['author']['username']}#{latest_message['author']['discriminator']}\033[0m"
                content = f"Content: \033[35m{latest_message.get('content', '')}\033[0m"

                print_colored_message(author, 36)  # Cyan color
                print_colored_message(content, 35)  # Purple color

                if open_links:
                    game_found = False
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
                                game_found = True
                                break

                    if not game_found:
                        default_url = "roblox://placeID=975820487"  # Default Roblox game URL
                        print(f"No game mentioned, opening default URL: {default_url}")
                        webbrowser.open_new_tab(default_url)

                    sound.play()

            clipboard_content = pyperclip.paste().lower()
            if clipboard_content != last_clipboard:
                if "stop" in clipboard_content:
                    open_links = False
                    print_colored_message("Script: Roblox links will not be opened", 32)  # Green color
                elif "start" in clipboard_content:
                    open_links = True
                    print_colored_message("Script: Roblox links will be opened", 32)  # Green color
                last_clipboard = clipboard_content

            time.sleep(0.5)  # Wait for 0.5 seconds before checking again

    except KeyboardInterrupt:
        print_colored_message("\nStopping...", 31)  # Red color

    pygame.mixer.quit()

if __name__ == "__main__":
    main()
