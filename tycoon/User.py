from datetime import datetime
from Task import Task

class User:
    def __init__(self, username: str):
        self.username = username
        self.level = 1
        self.xp = 0
        self.xp_to_next_level = 100
        self.streak = 1
        self.completed_tasks = []
        self.to_do_tasks = []
        self.events = []
        self.last_completed_task_time = None
        self.boost = 1
        self.permanent_boost = 1
        self.rebirths = 0
        self.upgrades = {
            "Focus Lamp": (0, 8),
            "Coffee Mug": (0, 8),
            "Ergonomic Chair": (0, 8),
            "Standing Desk": (0, 8),
            "Noise-Cancelling Headphones": (0, 8),
            "Motivational Poster": (0, 8),
            "Time Management Book": (0, 8),
            "Productivity App Subscription": (0, 8)
        }

    def add_xp(self, amount: float):
        self.xp += amount * self.boost * self.permanent_boost
        while self.xp >= self.xp_to_next_level:
            self.xp -= self.xp_to_next_level
            self.level_up()

    def level_up(self):
        self.level += 1
        self.xp_to_next_level += 100

    def add_task(self, task: Task):
        self.to_do_tasks.append(task)

    def finish_task(self, task: Task):
        if task in self.to_do_tasks:
            task.complete_task()
            self.add_xp(task.xp_reward)
            self.to_do_tasks.remove(task)
            self.completed_tasks.append(task)
            self.update_streak()

    def update_streak(self):
        now = datetime.now()
        if self.last_completed_task_time != None:
            delta = (now.date() - self.last_completed_task_time.date()).days
            self.streak = self.streak + 1 if delta <= 2 else 1
        else:
            self.streak = 1
        self.last_completed_task_time = now

    def purchase_upgrade(self, upgrade_name: str) -> bool:
        if upgrade_name not in self.upgrades:
            return False
        count, cost = self.upgrades[upgrade_name]
        if self.xp >= cost:
            self.xp -= cost
            self.upgrades[upgrade_name] = (count + 1, cost * 2)
            return True
        return False

    def rebirth(self):
        if self.level < 10:
            return False
        self.rebirths += 1
        self.level = 1
        self.xp = 0
        self.xp_to_next_level = 100
        self.streak = 1
        self.permanent_boost += self.xp / 1000
        self.boost = 1
        self.to_do_tasks = []
        self.completed_tasks = []
        self.upgrades = {k: (0, v[1]) for k, v in self.upgrades.items()}
        return True
    
    def add_event(self, event):
        self.events.append(event)

    def get_events(self):
        return [e.summary() for e in self.events]

    def summary(self):
        return {
            username: self.username,
            level: self.level,
            xp: self.xp,
            xp_to_next_level: self.xp_to_next_level,
            streak: self.streak,
            completed_tasks: len(self.completed_tasks),
            to_do_tasks: len(self.to_do_tasks),
            events: len(self.events),
            last_completed_task_time: self.last_completed_task_time.isoformat() if self.last_completed_task_time else None,
            boost: self.boost,
            permanent_boost: self.permanent_boost,
            rebirths: self.rebirths,
            upgrades: self.upgrades
            tasks: [t.summary() for t in self.to_do_tasks]
            events: [e.summary() for e in self.events]
        }

        
    # Handle income from upgrades
    # Params: self - instance of User
    def constant_income(self):
        income = 0
        for upgrade in self.upgrades:
            income += self.upgrades[upgrade][0] * 0.0001  # Each second gives 0.0001 XP per upgrade level
        self.add_xp(income)
        print(f"{self.username} received constant income of {income} XP.")
    
    