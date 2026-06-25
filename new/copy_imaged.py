import os
import shutil

SOURCE_DIR = "/home/seigyo/llm-wiki/mineru"
TARGET_DIR = "/home/seigyo/llm-wiki/input"

def main():
    os.makedirs(TARGET_DIR, exist_ok=True)

    for root, _, files in os.walk(SOURCE_DIR):
        for file in files:
            if file.endswith(".described.md"):
                source_path = os.path.join(root, file)

                # remove ".described"
                new_name = file.replace(".described", "")
                target_path = os.path.join(TARGET_DIR, new_name)

                # avoid overwriting if duplicate names exist
                if os.path.exists(target_path):
                    base, ext = os.path.splitext(new_name)
                    i = 1
                    while os.path.exists(target_path):
                        target_path = os.path.join(TARGET_DIR, f"{base}_{i}{ext}")
                        i += 1

                shutil.copy2(source_path, target_path)
                print(f"Copied: {source_path} -> {target_path}")

if __name__ == "__main__":
    main()