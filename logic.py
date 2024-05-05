import os
import asyncio
from pyrogram import Client, errors, enums

SESSION_DIR = "sessions"


async def get_channels(client):
    all_channels = []
    async for dialog in client.get_dialogs():
        if dialog.chat.type in [enums.ChatType.CHANNEL, enums.ChatType.SUPERGROUP] and dialog.chat.title is not None:
            all_channels.append((dialog.chat.id, dialog.chat.title))
    return all_channels


async def send_message(client, channel_id, channel_name, message):
    try:
        await client.send_message(channel_id, message)
        print(f"Message sent successfully to channel {channel_name}")
        return True
    except errors.FloodWait as e:
        print(f"Error: Flood wait of {e.value} seconds for channel {channel_name}.")
    except errors.UserBannedInChannel:
        print(f"Error: User is banned in channel {channel_name}.")
    except Exception as e:
        print(f"Error sending message to channel {channel_name}: {e}")
    return False


async def send_to_all_channels(user, message):
    client = Client(os.path.join(SESSION_DIR, user['name']), user['api_id'], user['api_hash'], phone_number=user['phone_number'])
    async with client:
        if not client.is_connected:
            await client.start()
        channels = await get_channels(client)
        successful_channels = []
        unsuccessful_channels = []

        for channel_id, channel_name in channels:
            success = await send_message(client, channel_id, channel_name, message)
            if success:
                successful_channels.append(channel_name)
            else:
                unsuccessful_channels.append(channel_name)

        print("\nSummary:")
        print("Found Channels:")
        for _, channel_name in channels:
            print(f" - {channel_name}")

        print("\nSuccessfully Sent Messages to:")
        for channel_name in successful_channels:
            print(f" - {channel_name}")

        print("\nUnsuccessful Attempts:")
        for channel_name in unsuccessful_channels:
            print(f" - {channel_name}")
