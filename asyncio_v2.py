import asyncio


async def func1():
    print("Начало функции func1")
    await asyncio.sleep(0)
    print("Окончание функции func1")


async def func2():
    print("Начало функции func2")
    await asyncio.sleep(0)
    print("Окончание функции func2")


def main():
    ioloop = asyncio.get_event_loop()
    tasks = [ioloop.create_task(func1()), ioloop.create_task(func2())]
    wait_tasks = asyncio.wait(tasks)
    ioloop.run_until_complete(wait_tasks)
    ioloop.close()


if __name__ == '__main__':
    main()
