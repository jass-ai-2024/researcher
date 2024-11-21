from runner import get_res


while True:
    # Here we search for files in volume from architects
    # If find one, Parse their file as PROMPT
    # Save_dit = Path to volume + research_<current_task_id>
    # Current task id???
    PROMPT = "Some Prompt"
    save_dir = "volume/research_1.txt"
    get_res(PROMPT, save_dir)
