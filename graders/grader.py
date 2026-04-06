import pandas as pd


def grade(df: pd.DataFrame) -> float:
    score = 0.0
    total = 5

    if df.isnull().sum().sum() == 0:
        score += 1

    if df.duplicated().sum() == 0:
        score += 1

    type_ok = True
    if "age" in df.columns:
        try:
            df["age"].astype(int)
        except:
            type_ok = False

    if type_ok:
        score += 1

    text_ok = True
    if "name" in df.columns:
        for v in df["name"]:
            if not isinstance(v, str) or v != v.capitalize():
                text_ok = False
                break

    if text_ok:
        score += 1

    if len(df) >= 2:
        score += 1

    return round(score / total, 3)