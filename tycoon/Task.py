from datetime import datetime, timedelta
import google.generativeai as genai
from google.generativeai import types

class Task:
    def __init__(
        self,
        title: str,
        start_time: datetime,
        end_time: datetime = None,
        description: str = "",
        location: str = "",
        attendees: list = None,
        reminders: list = None,
        all_day: bool = False,
        color_id: str = "1",  # optional color for calendar
        calendar_id: str = "primary",
        xp_reward: int = 10,  # default xp points
        task_type: str = "general",  # optional categorization
    ):
        self.title = title
        self.start_time = start_time
        self.end_time = end_time or (start_time + timedelta(hours=1))
        self.description = description
        self.location = location
        self.attendees = attendees if attendees else []
        self.reminders = reminders if reminders else []  # e.g., [{"method": "popup", "minutes": 10}]
        self.all_day = all_day
        self.color_id = color_id
        self.calendar_id = calendar_id

        # Gamification attributes
        self.xp_reward = xp_reward
        self.task_type = task_type
        self.completed = False

    # -------------------------
    # Methods
    # -------------------------
    # Define the function declaration
    assign_xp_declaration = {
        "name": "assign_xp_based_on_similarity",
        "description": "Assigns an XP value to a task based on its similarity to a list of reference tasks.",
        "parameters": {
            "type": "object",
            "properties": {
                "task_title": {"type": "string", "description": "The title of the task."},
                "task_description": {"type": "string", "description": "The description of the task."},
                "reference_tasks": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string"},
                            "description": {"type": "string"},
                            "xp_value": {"type": "integer"}
                        },
                        "required": ["title", "description", "xp_value"]
                    },
                    "description": "A list of reference tasks with their XP values."
                }
            },
            "required": ["task_title", "task_description", "reference_tasks"]
        }
    }

    def assign_xp(self):
        # Prepare the function arguments
        function_args = {
            "task_title": self.title,
            "task_description": self.description,
            "reference_tasks": self.reference_tasks
        }

        # Call the Gemini model
        response = genai.models.generate_content(
            model="gemini-2.5-flash",
            contents=[types.Content(role="user", parts=[types.Part(text="Assign XP based on task similarity")])],
            function_declarations=[assign_xp_declaration],
            function_args=function_args
        )

        # Extract the assigned XP value from the response
        if response.candidates:
            self.xp_value = response.candidates[0].content.parts[0].function_call.args.get("assigned_xp", 0)
        else:
            print("No response from Gemini model.")

    def complete_task(self):
        """Mark task as completed"""
        self.completed = True
        print(f"Task '{self.title}' completed! +{self.xp_reward} XP")

    def duration(self):
        """Return duration of the task in minutes"""
        return int((self.end_time - self.start_time).total_seconds() / 60)

    def add_attendee(self, email: str):
        if email not in self.attendees:
            self.attendees.append(email)

    def add_reminder(self, method: str, minutes: int):
        self.reminders.append({"method": method, "minutes": minutes})

    def to_dict(self):
        """Convert to dictionary, useful for MongoDB or Google Calendar API"""
        return {
            "title": self.title,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "description": self.description,
            "location": self.location,
            "attendees": self.attendees,
            "reminders": self.reminders,
            "all_day": self.all_day,
            "color_id": self.color_id,
            "calendar_id": self.calendar_id,
            "xp_reward": self.xp_reward,
            "task_type": self.task_type,
            "completed": self.completed,
        }


# -------------------------
# Example Usage
# -------------------------
if __name__ == "__main__":
    from datetime import datetime

    task1 = Task(
        title="Finish Python Hackathon MVP",
        start_time=datetime(2025, 9, 20, 14, 0),
        end_time=datetime(2025, 9, 20, 16, 0),
        description="Implement user + task MongoDB integration",
        location="Home Office",
        xp_reward=50,
        task_type="coding",
    )

    task1.add_attendee("maxwell@example.com")
    task1.add_reminder(method="popup", minutes=10)
    print(task1.to_dict())
    task1.complete_task()
