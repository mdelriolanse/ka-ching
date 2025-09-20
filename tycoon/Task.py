from datetime import datetime, timedelta
import google.generativeai as genai
from google.generativeai import types
import uuid
from typing import Optional


class Task:
    """Minimal Task model used by the tycoon Flask backend.

    Attributes:
        id: uuid string
        title: non-empty string
        description: optional string
        duration_min: int estimated duration in minutes (default 25)
        xp_reward: float XP awarded on completion
        completed: bool
        created_at: timestamp
        completed_at: optional timestamp
    """
    def __init__(self, title: str, duration_min: int = 25, xp_reward: float = None):
        if not title.strip():
            raise ValueError("Title cannot be empty")
        self.id = str(uuid.uuid4())
        self.title = title.strip()
        self.duration_min = duration_min
        self.xp_reward = xp_reward if xp_reward is not None else float(duration_min)
        self.completed = False

        self.assign_xp()

    # -------------------------
    # Methods
    # -------------------------

    # Use Gemini model to assign XP based on task similarity to a dictionary of reference tasks
    # Params: self - instance of Task
    def assign_xp(self):
        try:
            # Prepare the function arguments
            function_args = {
                "task_title": self.title,
                "reference_tasks": {
                    {"title": "Do the Laundry. Wash, dry, and fold the laundry", "xp_reward": 20},
                    {"title": "Attend team meeting. Participate in the weekly team sync-up meeting.", "xp_reward": 10},
                    {"title": "Code review. Review code submissions from team members.", "xp_reward": 15},
                    {"title": "Design mockups. Create design mockups for the new feature.", "xp_reward": 25},
                    {"title": "Fix bugs. Identify and fix bugs in the application.", "xp_reward": 30},
                    {"title": "Write documentation. Document the new API endpoints.", "xp_reward": 40},
                    {"title": "Plan sprint. Plan tasks and goals for the next sprint.", "xp_reward": 35},
                    {"title": "User testing. Conduct user testing sessions for feedback.", "xp_reward": 45},
                    {"title": "Deploy to production. Deploy the latest version to the production environment.", "xp_reward": 100}
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
        except Exception as e:
            print(f"Error assigning XP using Gemini model: {e}")
            self.xp_reward = float(self.duration_min / 5)  # Fallback to duration as XP

    # Mark task as completed
    # Params: self - instance of Task
    def complete_task(self):
        """Mark task as completed"""
        self.completed = True
        print(f"Task '{self.title}' completed! +{self.xp_reward} XP")
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "durationMin": self.duration_min,
            "xp_reward": self.xp_reward,
            "completed": self.completed
        }
