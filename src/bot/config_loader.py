import os
import yaml
from typing import Callable, Dict
import asyncio

class ConfigLoader:
    def __init__(self):
        self.configs = {}
        self.last_modified_times = {}
        self.subscribers = []
        self.loading_configs = set()

    def is_config_updated(self, config_name: str) -> bool:
        path = os.path.join("config", f"{config_name}.yml") if config_name != "config" else "config.yml"
        if os.path.exists(path):
            mtime = os.path.getmtime(path)
            return config_name not in self.last_modified_times or mtime > self.last_modified_times[config_name]
        else:
            return False

    async def load_config(self, config_name: str) -> Dict:
        if config_name in self.loading_configs:
            return self.configs.get(config_name, {})
        self.loading_configs.add(config_name)
        try:
            print(f"Checking for updates to {config_name}")
            path = f"config/{config_name}.yml" if config_name != "config" else "config.yml"
            with open(path, 'r', encoding='utf-8') as file:
                self.configs[config_name] = yaml.safe_load(file)
            self.last_modified_times[config_name] = os.path.getmtime(path)
            await self.notify_subscribers(config_name)
            return self.configs.get(config_name, {})
        except Exception as e:
            print(f"Failed to reload {config_name}: {e}")
        finally:
            self.loading_configs.remove(config_name)

    def subscribe(self, subscriber: Callable):
        self.subscribers.append(subscriber)

    async def notify_subscribers(self, config_name: str):
        print(f"Notifying subscribers of update to {config_name}")
        tasks = []
        for subscriber in self.subscribers:
            if asyncio.iscoroutinefunction(subscriber):
                task = asyncio.create_task(subscriber(config_name))
                tasks.append(task)
            else:
                print(f"Subscriber {subscriber} is not awaitable. Ensure all subscribers are coroutines.")
        if tasks:
            await asyncio.gather(*tasks)

config_loader = ConfigLoader()