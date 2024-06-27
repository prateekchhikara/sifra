from langchain_core.pydantic_v1 import BaseModel, Field
from enum import Enum


class Personality(BaseModel):
    name: str = Field(
        description="The full name of the person. This should include their first name, middle name (if any), and last name.",
        default="",
        required=True
    )

    likes: list[str] = Field(
        description="Topics, or experiences that the person enjoys or finds particularly engaging. This can include interests, or general preferences. Examples: 'exploring new cuisines', 'travelling to new places', 'learning new languages'.",
        default=[],
        required=True
    )

    dislikes: list[str] = Field(
        description="A list of activities, topics, or experiences that the person prefers to avoid or has a negative attitude towards. This can include specific dislikes, aversions, or things they find unpleasant. Examples: 'spicy food', 'horror movies', 'loud environments', 'crowded places', 'public speaking'.",
        default=[],
        required=True
    )

    hobbies: list[str] = Field(
        description="A list of regular activities that the person engages in for pleasure, relaxation, or personal fulfillment. These are typically activities done in their free time and can range from creative to physical to intellectual pursuits. Examples: 'playing guitar', 'painting landscapes', 'gardening', 'hiking', 'writing poetry', 'cooking gourmet meals'.",
        default=[],
        required=True
    )

    personality_traits: list[str] = Field(
        description="A list of inherent qualities or characteristics that define the person's typical behaviors, attitudes, and mindset. These traits help to describe how the person generally thinks and acts. Examples: 'optimistic', 'introverted', 'empathetic', 'decisive', 'adventurous', 'detail-oriented'.",
        default=[],
        required=True
    )

    values: list[str] = Field(
        description="A list of core beliefs or principles that are deeply important to the person and guide their behavior, decisions, and interactions with others. These values reflect what the person stands for and prioritizes in life. Examples: 'honesty', 'loyalty', 'integrity', 'respect', 'kindness', 'ambition'.",
        default=[],
        required=True
    )

    about_me: str = Field(
        description="A comprehensive narrative detailing the person's history, experiences, and cultural background. This can include information about their upbringing, education, career, significant life events, personal achievements, and other aspects of their life story. It provides a holistic view of who they are and what has shaped them.",
        default="",
        required=True
    )

    relationships: list[str] = Field(
        description="A description of the person's various connections and interactions with others, including family, friends, and colleagues. This can detail the nature and quality of these relationships, such as close family bonds, friendships, professional networks, and social circles. Examples: 'has a close relationship with siblings', 'maintains a large circle of friends', 'is well-regarded by colleagues', 'enjoys networking with professionals'.",
        default=[],
        required=True
    )

    to_do_list: list[str] = Field(
        description="A list of tasks, goals, or activities that the person plans to accomplish or engage in. This can include short-term objectives, long-term aspirations, or ongoing projects. Examples: 'complete a certification course', 'travel to Europe next summer', 'organize a charity event', 'learn to play the piano'.",
        default=[],
        required=True
    )

    reminders: list[str] = Field(
        description="A set of important dates, events, or commitments that the person needs to remember or prepare for. This can include birthdays, anniversaries, deadlines, appointments, or other significant occasions. Examples: 'mother's birthday on May 12th', 'project deadline on Friday', 'dentist appointment next week', 'annual company meeting on June 30th'. The user can also explicitly ask the AI to remind them about specific events.",
        default=[],
        required=True
    )


class Action(str, Enum):
    """
        Enum class to define the type of action to be performed on the memory.
    """
    Add = "Add"
    Update = "Update"
    Delete = "Delete"
    Nothing = "Nothing"


class PersonalityUpdate(Personality, BaseModel):
    action: Action = Field(
        default=Action.Nothing,
        description="""Specifies the type of update operation to be performed:
        - Add: Created a new personality record 
        - Update: Modified an existing personality record"
        - Delete: Removed an existing personality record"
        - Nothing: No changes required (default)"""
    )


if __name__ == "__main__":
    obj = PersonalityUpdate()
    print(obj)