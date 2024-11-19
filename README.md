# JASS
### Overview
Our main goal is to create a tool for researchers which will make the process easier and simplify the way for getting up-to-date information.

###  Problem Statement (technology perspective)
It takes long time to find relevant and up-to-date information daily. Good to have brief overview of new tecnologies.

### Objectives
- Objective 1: Simplify the process of recieving up-to-date information on daily basis
- Objective 2: Asistance for the researcher on filtering the information
- Objective 3: Guidance for the person to advice next steps

### Features
- Feature 1: Summary of all papers that were released today.
- Feature 2: Search of the code bases that suit the papers for the selected topics of research (to give code examples).
- Feature 3: Filtering of the main papers by topic or by tecnical parametrs (limitations)
- Feature 4: Customers feedback that can affect the answer to give more relevant results
- Feature 5: Predict next steps of research, suggestions for the new topics and spheres that will help to solve current problem

### Timeline
- 18.11: Deliverables:
	- Parsing of the papers from huggingface (daily updates)
 	- Getting summary of these papers
  	- Search of code bases for the reserches found on previous steps
- 19.11: Deliverables:
	- Adding search conditions: filter by the topic
	- Adding search conditions: filter by tecnical limitations
- 20.11: Deliverables:
	- Communication with the found paper/article
 	- Customers feedback that can affect the answer to give more relevant results
- 21.11: Deliverables:
	- Reseearch forecast: predict next steps, interesting domains
### Team
- Evgenii
- Dmitry
- Alexei
- Ekaterina

### Risks and Mitigation Strategies

At least two!

| Risk   | Impact          | Probability     | Mitigation Strategy  |
| ------ | --------------- | --------------- | -------------------- |
| Risk 1 | High/Medium/Low | High/Medium/Low | Strategy description |
| Risk 2 | High/Medium/Low | High/Medium/Low | Strategy description |
### Success Criteria
- Criterion 1
- Criterion 2
- Criterion 3

### Appendix
Any additional information, references, or documents relevant to the project.


# Setting Up Python Environment with `pip` and Running Code

## 1. Creating a Virtual Environment

1. Navigate to the project directory:
   ```bash
   cd /path/to/your/project
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv jass_researcher
   ```

3. Activate the virtual environment:
   ```bash
   source jass_researcher/bin/activate
   ```

## 2. Installing Dependencies

Install dependencies:
```bash
pip install <package_name>
```

## 3. Freezing Dependencies

Create `requirements.txt`:
```bash
pip freeze > requirements.txt
```

## 4. Installing Dependencies from `requirements.txt`

Install all dependencies:
```bash
pip install -r requirements.txt
```

## 5. Running Python Code

Activate the virtual environment:
```bash
source jass_researcher/bin/activate
```

Run a Python script:
```bash
python main.py
```




