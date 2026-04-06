# DataClean RL Environment
---
title: DataClean RL
emoji: 🤖
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
pinned: false
---
## Overview
A reinforcement learning environment simulating real-world data cleaning tasks.

## Tasks
- Easy: missing + duplicates
- Medium: type + normalization
- Hard: mixed complex errors

## Actions
- fix_missing
- remove_duplicates
- convert_type
- normalize_text
- drop_row
- fill_default
- rename_column

## Reward Design
- Positive reward for correct cleaning
- Penalty for wrong actions
- Cost per action
- Final grading score (0–1)

## Setup

```bash
pip install -r requirements.txt
uvicorn api.main:app --reload