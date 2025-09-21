from datetime import datetime, timedelta
import google.genai as genai
from google.genai import Client
from google.genai import types
import uuid
from pydantic import BaseModel
import os
import json

# Class to represent a task in the gamified task management system
# Class invariants: title is non-empty, start_time < end_time, 

class XPScore(BaseModel):
    xp_reward: int

class Task:
    def __init__(self, title: str, xp_reward: float = 10, durationMin: int = 25):
        self.id = str(uuid.uuid4())
        self.title = title
        self.xp_reward = xp_reward
        self.completed = False

        # Gamification attributes
        self.assign_xp()

    # -------------------------
    # Methods
    # -------------------------

    # Use Gemini model to assign XP based on task similarity to a dictionary of reference tasks
    # Params: self - instance of Task


    def assign_xp(self):

        reference_tasks = [
            {"title": "Do the Laundry", "xp_reward": 20},
            {"title": "Attend team meeting", "xp_reward": 10},
            {"title": "Code review", "xp_reward": 15},
            {"title": "Design mockups", "xp_reward": 25},
            {"title": "Fix bugs", "xp_reward": 30},
            {"title": "Write documentation", "xp_reward": 40},
            {"title": "Plan sprint", "xp_reward": 35},
            {"title": "User testing", "xp_reward": 45},
            {"title": "Deploy to production", "xp_reward": 100}
        ]


        # Call the Gemini model
        client = Client(api_key=os.getenv('GOOGLE_API_KEY'))
        response = client.models.generate_content(
            model="gemini-2.5-flash",

            contents=f"Given {reference_tasks}, Assign XP to {self.title} based on similarity of task importance and effort.",
            config=types.GenerateContentConfig(
                temperature=0,
                response_mime_type="application/json",
                response_schema=XPScore,
                thinking_config=types.ThinkingConfig(thinking_budget=0)
        )
        )
        self.xp_reward = json.loads(response.text)['xp_reward']
        

        # Extract the assigned XP value from the response
        # if response.candidates:
        #     self.xp_reward = int((response.candidates[0].content.parts[0]).text.strip().split()[0])  # Assuming the model returns a string with the XP value
        # else:
        #     print("No response from Gemini model.")

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
        return self.durationMin


if __name__ == "__main__":
    task  = Task("Brushed teeth")