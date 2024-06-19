import json
import os
import tkinter
from notopenai import NotOpenAI
from graphics import Canvas

# Constants for the canvas size
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600

# Initialize the NotOpenAI client with your API key
CLIENT = NotOpenAI(api_key="your_api_key_here")

def load_story(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def print_scene(scene_data):
    print(scene_data["text"])
    for index, choice in enumerate(scene_data["choices"], start=1):
        print(f"{index}. {choice['text']}")

def valid_choice(scene_data):
    while True:
        try:
            chosen_integer = int(input("What do you choose? "))
            if 1 <= chosen_integer <= len(scene_data["choices"]):
                return chosen_integer - 1  # Convert to 0-based index
        except ValueError:
            pass
        print("Please enter a valid choice: ")

def create_new_scene(client, story_data, scene_key):
    print("[Suspenseful music plays as the story continues...]")
    example_scene = json.dumps(story_data["scenes"]["start"], indent=2)
    plot = story_data["plot"]
    
    prompt = f"Return the next scene of a story for key {scene_key}. An example scene should be formatted in json like this: {example_scene}. The main plot line of the story is {plot}."
    
    chat_completion = client.chat.completions.create(
        messages=[{
            "role": "user",
            "content": prompt,
        }],
        model="gpt-3.5-turbo",
        response_format={"type": "json_object"}
    )
    
    response_str = chat_completion.choices[0].message.content
    new_scene_data = json.loads(response_str)
    story_data["scenes"][scene_key] = new_scene_data
    return new_scene_data

def main():
    story_data = load_story('data/original_big.json')
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT, "Infinite Story")
    current_scene_key = "start"

    while True:
        if current_scene_key not in story_data["scenes"]:
            new_scene_data = create_new_scene(CLIENT, story_data, current_scene_key)
            story_data["scenes"][current_scene_key] = new_scene_data
        
        current_scene_data = story_data["scenes"][current_scene_key]
        print("\n")
        print_scene(current_scene_data)
        
        user_choice_index = valid_choice(current_scene_data)
        current_scene_key = current_scene_data["choices"][user_choice_index]["scene_key"]
        
        image_path = f"img/{current_scene_key}.jpg"
        if os.path.exists(image_path):
            photo = tkinter.PhotoImage(file=image_path)
            canvas.create_image(0, 0, image=photo, anchor=tkinter.NW)
        else:
            canvas.create_rectangle(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, fill="black")

        canvas.mainloop()

if __name__ == "__main__":
    main()