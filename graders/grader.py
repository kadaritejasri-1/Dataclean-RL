import pandas as pd


def grade(df: pd.DataFrame) -> float:
    score = 0.0
    total = 5

    # 1. No missing values
    if df.isnull().sum().sum() == 0:
        score += 1

    # 2. No duplicate rows
    if df.duplicated().sum() == 0:
        score += 1

    # 3. Age column type check
    type_ok = True
    if "age" in df.columns:
        try:
            # convert safely
            df["age"] = pd.to_numeric(df["age"], errors="coerce")

            # check no NaN introduced & all integers
            if df["age"].isnull().any() or not (df["age"] % 1 == 0).all():
                type_ok = False
        except:
            type_ok = False

    if type_ok:
        score += 1

    # 4. Name column normalization check
    text_ok = True
    if "name" in df.columns:
        for v in df["name"]:
            if pd.isna(v) or not isinstance(v, str):
                text_ok = False
                break

            v_clean = v.strip()
            if v_clean != v_clean.capitalize():
                text_ok = False
                break

    if text_ok:
        score += 1

    # 5. Minimum row check
    if len(df) >= 2:
        score += 1

    # Final normalized score
    return round(score / total, 3)