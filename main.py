import asyncio
import os
import time

STEAM_PROGRAM_NAME = 'steam'

static = "hyprpaper"
video = "mpvpaper -o \"no-audio --loop-playlist shuffle\" '*' ~/.wallpapers/video.mp4"

# Check if Steam is running
async def check_steam_running():
    process_list = os.popen('ps -A').readlines()
    for process in process_list:
        if STEAM_PROGRAM_NAME in process:
            return True
    return False

# Start hyprpaper and kill mpvpaper
async def start_hyprpaper():
    try:
        # Kill mpvpaper
        await asyncio.create_subprocess_shell('pkill mpvpaper')
        print('mpvpaper killed.')
    except Exception as e:
        print(f"Error killing mpvpaper: {e}")
        
    try:
        # Start hyprpaper
        await asyncio.create_subprocess_shell(static)
        print('hyprpaper started.')
    except Exception as e:
        print(f"Error starting hyprpaper: {e}")

# Start mpvpaper and kill hyprpaper
async def start_mpvpaper():
    try:
        # Kill hyprpaper
        await asyncio.create_subprocess_shell('pkill hyprpaper')
        print('hyprpaper killed.')
    except Exception as e:
        print(f"Error killing hyprpaper: {e}")
        
    try:
        # Start mpvpaper
        await asyncio.create_subprocess_shell(video)
        print('mpvpaper started.')
    except Exception as e:
        print(f"Error starting mpvpaper: {e}")
        
async def main():
    # Check if Steam is running
    while True:
        is_running = await check_steam_running()
        if is_running:
            # If Steam is running, start hyprpaper and kill mpvpaper
            await start_hyprpaper()
            while is_running == True:
            	time.sleep(1)
            	is_running = await check_steam_running()
        else:
            # If Steam is not running, start mpvpaper and kill hyprpaper
            await start_mpvpaper()
            while is_running == False:
            	time.sleep(1)
            	is_running = await check_steam_running()
        await asyncio.sleep(1)

asyncio.run(main())
