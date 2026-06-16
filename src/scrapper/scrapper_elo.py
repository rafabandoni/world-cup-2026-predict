import pandas as pd

def main():
    dfs = []

    columns = [
        "local_rank", "global_rank", "team_code", "rating",
        "rank_max", "rating_max",
        "rank_avg", "rating_avg",
        "rank_min", "rating_min",
        "rank_3m_change", "rating_3m_change",
        "rank_6m_change", "rating_6m_change",
        "rank_1y_change", "rating_1y_change",
        "rank_2y_change", "rating_2y_change",
        "rank_5y_change", "rating_5y_change",
        "rank_10y_change", "rating_10y_change",
        "matches_total", "matches_home", "matches_away", "matches_neutral",
        "wins", "losses", "draws",
        "goals_for", "goals_against",
        "rank_change", "rating_change"
    ]

    for year in range(1901, 2026):
        try:
            url = f"https://www.eloratings.net/{year}.tsv"

            df = pd.read_csv(url, sep="\t", header=None, names=columns)
            df["year"] = year

            dfs.append(df)
            print(f"{year}: {len(df)} linhas")

        except Exception as e:
            print(f"Erro em {year}: {e}")

    historico = pd.concat(dfs, ignore_index=True)
    cols = []
    for col in historico.columns:
        if 'change' in col:
            cols.append(col)

    for col in cols:
        historico[col] = (
            historico[col]
            .str.replace('−', '-', regex=False)  # U+2212 -> hífen normal
            .str.replace('+', '', regex=False)   # opcional
        )
        historico[col] = pd.to_numeric(
            historico[col],
            errors='coerce'
        )

    historico.to_parquet("data/elo_historico.parquet")

if __name__ == "__main__":
    main()