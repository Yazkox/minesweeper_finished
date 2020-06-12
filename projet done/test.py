import asyncio
import time
#import pygame
timer = 0
async def timer_loop():
    global timer
    while True :
        timer += 1
        await asyncio.sleep(1)
    #
    # async def check_cancel():
    #     while True :
    #         for event in pygame.event.get():
    #             if event.type == pygame.QUIT:
    #                 timer_task.cancel()
    #                 pygame.quit()

async def main():
    task = asyncio.create_task(timer_loop())
    task.run()
    while True :
        print(timer)
asyncio.run(main())