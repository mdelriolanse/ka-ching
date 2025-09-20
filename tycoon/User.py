class User:
    def __init__(self, username):
        self.username = username
        self.level = 1
        self.xp = 0
        self.xp_to_next_level = 100  # starting threshold
        self.streak = 0
        self.boosts = {}  # e.g., {"double_xp": 2} means 2 uses left
        self.inventory = []  # list of items
        self.completed_tasks = []
        self.to_do_tasks = []

    # Handle adding xp to user total
    def add_xp(self, amount):
        # Apply boost if available
        if "double_xp" in self.boosts and self.boosts["double_xp"] > 0:
            amount *= 2
            self.boosts["double_xp"] -= 1
            print(f"{self.username} used a Double XP boost!")

        self.xp += amount
        print(f"{self.username} gained {amount} XP!")

        # Check level up
        while self.xp >= self.xp_to_next_level:
            self.xp -= self.xp_to_next_level
            self.level_up()

    def level_up(self):
        self.level += 1
        self.xp_to_next_level = self.xp_to_next_level + 100  # scale XP needed
        print(f"{self.username} leveled up! Now at level {self.level}.")

    def increment_streak(self):
        self.streak += 1
        print(f"{self.username}'s streak is now {self.streak}!")

    def reset_streak(self):
        self.streak = 0
        print(f"{self.username}'s streak has been reset.")
    
    def add_task(self, task):
        self.to_do_tasks.append(task)

    # -------------------------
    # Inventory / Boost Methods
    # -------------------------
    def add_item(self, item_name):
        self.inventory.append(item_name)
        print(f"{self.username} received item: {item_name}.")

    def use_boost(self, boost_name):
        if boost_name in self.boosts and self.boosts[boost_name] > 0:
            self.boosts[boost_name] -= 1
            print(f"{self.username} used boost: {boost_name}.")
            return True
        print(f"No boosts left for {boost_name}.")
        return False

    def add_boost(self, boost_name, count=1):
        self.boosts[boost_name] = self.boosts.get(boost_name, 0) + count
        print(f"{self.username} got {count} {boost_name} boost(s).")

    # -------------------------
    # Task Tracking
    # -------------------------
    def complete_task(self, task_name, xp_reward=10):
        self.completed_tasks.append(task_name)
        print(f"{self.username} completed task: {task_name}")
        self.add_xp(xp_reward)
        self.increment_streak()

    # -------------------------
    # Display / Summary
    # -------------------------
    def summary(self):
        return {
            "username": self.username,
            "level": self.level,
            "xp": self.xp,
            "xp_to_next_level": self.xp_to_next_level,
            "streak": self.streak,
            "inventory": self.inventory,
            "boosts": self.boosts,
            "completed_tasks": self.completed_tasks,
        }
