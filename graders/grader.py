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
            df["age"] = pd.to_numeric(df["age"], errors="coerce")
            if df["age"].isnull().any() or not (df["age"] % 1 == 0).all():
                type_ok = False
        except:
            type_ok = False

    if type_ok:
        score += 1

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

    if len(df) >= 2:
        score += 1

  
    final_score = score / total

    if final_score <= 0:
        final_score = 0.1
    elif final_score >= 1:
        final_score = 0.9

    return round(final_score, 3)
