import asyncio
import os
import time

programs_names = ['steam', 'bottles']

static = "hyprpaper"
video = "mpvpaper -o \"no-audio --loop-playlist shuffle\" '*' ~/.wallpapers/video.mp4"

async def check_and_kill_processes(process_name):
    while True:
        process_list = os.popen('ps -A').readlines()
        found_process = False
        for process in process_list:
            if process_name in process:
                found_process = True
                break

        if not found_process:
            break

        try:
            subprocess.run(['killall', process_name], check=True)
        except subprocess.CalledProcessError:
            pass
            
# Check if program is running
async def check_program_running(name):
    process_list = os.popen('ps -A').readlines()
    for process in process_list:
        if name in process:
            return True
    return False
    
async def check():
    for name in programs_names:
        if await check_program_running(name):
            return True
    return False
    
# Start hyprpaper and kill mpvpaper
async def start_hyprpaper():
    try:
        # Kill mpvpaper
        await check_and_kill_processes("mpvpaper")
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
        await check_and_kill_processes("hyprpaper")
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
        is_running = await check()
        if is_running:
            # If game is running, start hyprpaper and kill mpvpaper
            await start_hyprpaper()
            while is_running == True:
                time.sleep(1)
                is_running = await check()
        else:
            # If game is not running, start mpvpaper and kill hyprpaper
            await start_mpvpaper()
            while is_running == False:
                time.sleep(1)
                is_running = await check()
        await asyncio.sleep(1)

asyncio.run(main())
