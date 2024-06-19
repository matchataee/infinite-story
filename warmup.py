import json
story_data = json.load(open('data/original_small.json'))

STORY_NAME = "original_small"

def main():
    print("Warmup.py")
    # TODO: your code here
    for scene_key, scene_value in story_data["scenes"].items():
        for choice in scene_value.get("choices", []):
            if choice["scene_key"] not in story_data["scenes"]:
                print(choice["scene_key"])



if __name__ == "__main__":
    main()
