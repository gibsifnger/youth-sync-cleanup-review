import pandas as pd

df = pd.read_csv("A_policy/policy_master_20260421.csv")

print("행 수:", len(df))
print("컬럼:", df.columns.tolist())

for col in ["_category", "lclsfNm", "rgtrHghrkInstCdNm", "rgtrInstCdNm", "bizPrdBgngYmd", "bizPrdEndYmd"]:
    if col in df.columns:
        print(f"\n[{col}] 상위 분포")
        print(df[col].astype(str).value_counts().head(10))

print("\n결측치 비율")
print((df.isna().mean() * 100).sort_values(ascending=False).head(20))