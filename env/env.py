import pandas as pd
from models.schemas import Observation, Action
from graders.grader import grade


class DataCleanEnv:

    def __init__(self):
        self.df = None
        self.budget = 10
        self.done = False
        self.history = []

        self.action_costs = {
            "fix_missing": 0.1,
            "remove_duplicates": 0.2,
            "convert_type": 0.15,
            "normalize_text": 0.1,
            "drop_row": 0.25,
            "fill_default": 0.1,
            "rename_column": 0.05
        }

    def reset(self, data, task_name="task"):
        self.df = pd.DataFrame(data)
        self.budget = 10
        self.done = False
        self.history = []
        return self._obs("reset")

    def _obs(self, msg):
        return Observation(
            preview_rows=self.df.head(3).to_dict(orient="records"),
            issues_summary={
                "missing": int(self.df.isnull().sum().sum()),
                "duplicates": int(self.df.duplicated().sum())
            },
            budget_remaining=self.budget,
            last_action_result=msg
        )

    def step(self, action: Action):

        if self.done:
            return self._obs("done"), 0.0, True, {}

        reward = 0.0

        try:
            if action.action_type == "fix_missing":
                if pd.isnull(self.df.iloc[action.row_id][action.column]):
                    self.df.at[action.row_id, action.column] = action.value
                    reward += 0.3
                else:
                    reward -= 0.3

            elif action.action_type == "remove_duplicates":
                before = len(self.df)
                self.df = self.df.drop_duplicates().reset_index(drop=True)
                reward += (before - len(self.df)) * 0.2

            elif action.action_type == "convert_type":
                try:
                    self.df.at[action.row_id, action.column] = int(action.value)
                    reward += 0.3
                except:
                    reward -= 0.3

            elif action.action_type == "normalize_text":
                self.df.at[action.row_id, action.column] = str(action.value).capitalize()
                reward += 0.2

            elif action.action_type == "drop_row":
                self.df = self.df.drop(index=action.row_id).reset_index(drop=True)
                reward += 0.1

            elif action.action_type == "fill_default":
                self.df[action.column] = self.df[action.column].fillna(action.value)
                reward += 0.2

            elif action.action_type == "rename_column":
                self.df = self.df.rename(columns={action.column: action.value})
                reward += 0.1

            else:
                reward -= 0.2

        except Exception:
            reward -= 0.5

        # action cost
        reward -= self.action_costs.get(action.action_type, 0.2)

        self.budget -= 1
        self.history.append(action.dict())

        if self.budget <= 0:
            self.done = True
            reward -= 0.5

        final_score = 0.0
        if self.done:
            final_score = grade(self.df)
            reward += final_score

        return self._obs("step"), round(reward, 3), self.done, {"final_score": final_score}

    def state(self):
        return self.df.to_dict(orient="records")