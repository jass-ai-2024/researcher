import time
import os
from runner import get_res

VOLUME = os.getenv("VOLUME", "/tmp/jass/research")
processed_ids = set()

while True:
    for filename in os.listdir(VOLUME):
        if filename.startswith("research_task_") and filename.endswith(".txt"):
            task_id = filename[len("research_task_"):-len(".txt")]
            if task_id in processed_ids:
                continue
            file_path = os.path.join(VOLUME, filename)
            with open(file_path, 'r') as file:
                prompt_content = file.read()
            result_filename = f"research_result_{task_id}.txt"
            result_path = os.path.join(VOLUME, result_filename)
            get_res(prompt_content, result_path, task_id)
            processed_ids.add(task_id)
    time.sleep(10)
