import time
import os
from runner import get_res

while True:

    VOLUME = "tmp/jass"
    for filename in os.listdir(VOLUME):
        if filename.startswith("research_result_") and filename.endswith(".txt"):
            task_id = filename[len("research_result_"):-len(".txt")]
            file_path = os.path.join(VOLUME, filename)
            with open(file_path, 'r') as file:
                prompt_content = file.read()
            get_res(prompt_content, file_path, task_id)
    time.sleep(30)