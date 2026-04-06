# DataClean RL Environment

## Overview
DataClean RL is a reinforcement learning environment designed for real-world data cleaning tasks. Agents interact with messy datasets and learn to clean them efficiently using structured actions under budget constraints.

## Tasks
The environment includes three levels of difficulty:

- **Easy:** Missing values and duplicate rows  
- **Medium:** Data type issues and text normalization  
- **Hard:** Complex datasets with multiple overlapping errors  

## Action Space
Agents can perform the following actions:

- fix_missing  
- remove_duplicates  
- convert_type  
- normalize_text  
- drop_row  
- fill_default  
- rename_column  

## Reward Design
- Positive reward for correct cleaning actions  
- Penalty for incorrect or unnecessary actions  
- Cost associated with each action  
- Final score (0.0–1.0) based on data quality  

## API Endpoints
- `/reset` – Initialize environment  
- `/step` – Apply an action  
- `/state` – Get current dataset  
- `/tasks` – List available tasks  
- `/grader` – Get final score  
- `/baseline` – Run baseline agent  

## Setup

```bash
pip install -r requirements.txt
uvicorn api.main:app --reload

Live Demo

Hugging Face Space:
https://tejasri-kadari-dataclean-rl.hf.space/docs
