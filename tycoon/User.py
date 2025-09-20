from Task import Task
from datetime import datetime, timedelta

# Class to represent a user in the gamified task management system
# Class invariants: username is unique, inventory, completed_tasks, and to_do_tasks contain valid entries
class User:

    # -------------------------
    # Initialization and incremental methods
    # ------------------------- 

    # Constructor for user
    # Params: self - instance of User, username - unique identifier for the user 
    def __init__(self, username):
        self.username = username
        self.level = 1
        self.xp = 0.0
        self.xp_to_next_level = 100  # starting threshold

        self.completed_tasks = []
        self.to_do_tasks = []
        self.last_completed_task_time = None
        self.upgrades = {}        
        
        self.streak = 1
        self.boost = 1 # multiplicative boost to xp gain
        self.permanent_boost = 1 # permanent boost to xp gain
        self.inventory = {
            "Focus Lamp": (0,8),
            "Coffee Mug": (0,8),
            "Ergonomic Chair": (0,8),
            "Standing Desk": (0,8),
            "Noise-Cancelling Headphones": (0,8),
            "Motivational Poster": (0,8),
            "Time Management Book": (0,8),
            "Productivity App Subscription": (0,8)
            }  # e.g., {"Time Management Book": (2,32)} means 2 owned, cost 32 xp
        self.rebirths = 0

    # Handle adding xp to user total
    # Params: self - instance of User, amount - xp to add
    def add_xp(self, amount):
        # Apply boost if available
        self.xp += amount * self.boost * self.permanent_boost
        print(f"{self.username} gained {amount} XP!")

        # Check level up
        while self.xp >= self.xp_to_next_level:
            self.xp -= self.xp_to_next_level
            self.level_up()

    # Handle leveling up the user
    # Params: self - instance of User
    def level_up(self):
        self.level += 1
        self.xp_to_next_level = self.xp_to_next_level + 100  # scale XP needed
        print(f"{self.username} leveled up! Now at level {self.level}.")

    # -------------------------
    # Streak Methods
    # -------------------------

    # Increment the user's streak
    # Params: self - instance of User
    def increment_streak(self):
        self.streak += 1
        print(f"{self.username}'s streak is now {self.streak}!")

    # Update the user's streak based on task completion timing
    # Params: self - instance of User, task_time - datetime of the completed task
    def _update_streak(self, task_time: datetime):
        """Update the user's streak based on task completion timing"""
        if self.last_completed_task_time is None:
            # First task ever completed
            self.streak = 1
        else:
            delta = task_time.date() - self.last_completed_task_time.date()

            if delta.days <= 2:
                self.streak += 1
            else:
                self.streak = 1

    # -------------------------
    # Task Management
    # -------------------------

    # Add a task to the user's to-do list
    # Params: self - instance of User, task - Task object to add
    def add_task(self, task):
        self.to_do_tasks.append(task)

    # Finish a task from the user's to-do list
    # Params: self - instance of User, task - Task object to finish
    def finish_task(self, task):
        if task in self.to_do_tasks:
            task.complete_task()
            self.add_xp(task.xp_reward)
            self.to_do_tasks.remove(task)
            self.completed_tasks.append(task)
            self._update_streak()
        else:
            print(f"Task '{task.title}' not found in {self.username}'s to-do list.")

    # -------------------------
    # Inventory / Boost Methods
    # -------------------------

    # Add an item to the user's inventory
    # Params: self - instance of User, item_name - name of the item to add
    # Returns: True if item was already in inventory and incremented, False if new item added
    def add_item(self, item_name):
        if item_name in self.inventory:
            self.inventory[item_name] += 1
            print(f"{self.username} gained item: {item_name}.")
            return True
        self.inventory.append(item_name)
        print(f"{self.username} received item: {item_name}.")
        return False

    # Use an item from the user's inventory
    # Params: self - instance of User, item_name - name of the item to use
    # Returns: True if item was used, False if item not found or none left
    def use_item(self, item_name):
        if item_name in self.inventory and self.inventory[item_name] > 0:
            self.inventory[item_name] -= 1
            if item_name == "Double XP Boost":
                self.boost = 2
            elif item_name == "Triple XP Boost":
                self.boost = 3
            elif item_name == "Quadruple XP Boost":
                self.boost = 4
            print(f"{self.username} used boost: {item_name}.")
            return True
        print(f"No boosts left for {item_name}.")
        return False
    
    # -----------------------------
    # Upgrade / Rebirth Methods
    # -----------------------------

    # Purchase an upgrade for the user
    # Params: self - instance of User, upgrade_name - name of the upgrade,
    # Returns: True if upgrade purchased, False if not enough xp
    def purchase_upgrade(self, upgrade_name):
        if upgrade_name in self.upgrades:
            if self.upgrades[upgrade_name][1] <= self.xp:
                self.xp -= self.upgrades[upgrade_name][1]
                self.upgrades[upgrade_name] = (self.upgrades[upgrade_name][0] + 1, self.upgrades[upgrade_name][1] * 2)
                print(f"{self.username} purchased upgrade: {upgrade_name}.")
                return True
            else:
                print(f"Not enough XP to purchase {upgrade_name}. Needed: {self.upgrades[upgrade_name][1]}, Available: {self.xp}.")
                return False
        else:
            print(f"Invalid upgrade.")
            return False
        
    # Handle income from upgrades
    # Params: self - instance of User
    def constant_income(self):
        income = 0
        for upgrade in self.upgrades:
            income += self.upgrades[upgrade][0] * 0.0001  # Each second gives 0.0001 XP per upgrade level
        self.add_xp(income)
        print(f"{self.username} received constant income of {income} XP.")
    
    def rebirth(self):
        if self.level >= 10:  # Minimum level to rebirth
            self.rebirths += 1
            self.level = 1
            self.xp = 0
            self.xp_to_next_level = 100
            self.streak = 1
            self.boost = 1
            self.permanent_boost += self.xp/1000  # Increase permanent boost by 1x per 1000 xp
            self.inventory = {item: (0, cost) for item, cost in self.inventory.items()}  # Reset inventory counts
            self.upgrades = {}  # Reset upgrades
            print(f"{self.username} has rebirthed! Permanent boost is now {self.permanent_boost}x.")
        else:
            print(f"{self.username} needs to be at least level 10 to rebirth. Current level: {self.level}.")

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
