from datetime import datetime, timedelta
import google.generativeai as genai
from google.generativeai import types

# Class to represent a task in the gamified task management system
# Class invariants: title is non-empty, start_time < end_time, 
class Task:

    # Constructor for task
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
        self.assign_xp(self)

    # -------------------------
    # Methods
    # -------------------------

    # Use Gemini model to assign XP based on task similarity to a dictionary of reference tasks
    # Params: self - instance of Task
    def assign_xp(self):
        # Prepare the function arguments
        function_args = {
            "task_title": self.title,
            "task_description": self.description,
            "reference_tasks": {
                {"title": "Do the Laundry", "description": "Wash, dry, and fold the laundry", "xp_reward": 20},
                {"title": "Attend team meeting", "description": "Participate in the weekly team sync-up meeting.", "xp_reward": 10},
                {"title": "Code review", "description": "Review code submissions from team members.", "xp_reward": 15},
                {"title": "Design mockups", "description": "Create design mockups for the new feature.", "xp_reward": 25},
                {"title": "Fix bugs", "description": "Identify and fix bugs in the application.", "xp_reward": 30},
                {"title": "Write documentation", "description": "Document the new API endpoints.", "xp_reward": 40},
                {"title": "Plan sprint", "description": "Plan tasks and goals for the next sprint.", "xp_reward": 35},
                {"title": "User testing", "description": "Conduct user testing sessions for feedback.", "xp_reward": 45},
                {"title": "Deploy to production", "description": "Deploy the latest version to the production environment.", "xp_reward": 100}
            }
        }
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
                            "xp_reward": {"type": "integer"}
                        },
                        "required": ["title", "description", "xp_reward"]
                    },
                    "description": "A list of reference tasks with their XP values."
                }
            },
            "required": ["task_title", "task_description", "reference_tasks"]
        }
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
            self.xp_reward = response.candidates[0].content.parts[0].function_call.args.get("assigned_xp", 0)
        else:
            print("No response from Gemini model.")

    # Mark task as completed
    # Params: self - instance of Task
    def complete_task(self):
        """Mark task as completed"""
        self.completed = True
        print(f"Task '{self.title}' completed! +{self.xp_reward} XP")

    # Calculate and return the duration of the task in minutes
    # Params: self - instance of Task
    def duration(self):
        """Return duration of the task in minutes"""
        return int((self.end_time - self.start_time).total_seconds() / 60)

    # Add an attendee to the task
    # Params: self - instance of Task, email - email of the attendee to add
    def add_attendee(self, email: str):
        if email not in self.attendees:
            self.attendees.append(email)

    # Add a reminder to the task
    # Params: self - instance of Task, method - method of reminder (e.g.,
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
# if __name__ == "__main__":
#     from datetime import datetime

#     task1 = Task(
#         title="Finish Python Hackathon MVP",
#         start_time=datetime(2025, 9, 20, 14, 0),
#         end_time=datetime(2025, 9, 20, 16, 0),
#         description="Implement user + task MongoDB integration",
#         location="Home Office",
#         xp_reward=50,
#         task_type="coding",
#     )

#     task1.add_attendee("maxwell@example.com")
#     task1.add_reminder(method="popup", minutes=10)
#     print(task1.to_dict())
#     task1.complete_task()
