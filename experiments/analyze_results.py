"""
Genera gráficos y análisis a partir del CSV del torneo.
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from scipy import stats


def main():
    csv_path = "experiments/results/tournament.csv"
    if not os.path.exists(csv_path):
        print("No existe el CSV. Ejecuta primero run_tournament.py")
        return

    df = pd.read_csv(csv_path)

    # ===== Victorias por clase de jugador =====
    wins = {}
    for _, row in df.iterrows():
        wins[row["player1"]] = wins.get(row["player1"], 0) + row["p1_class_wins"]
        wins[row["player2"]] = wins.get(row["player2"], 0) + row["p2_class_wins"]

    plt.figure(figsize=(8, 5))
    sns.barplot(x=list(wins.keys()), y=list(wins.values()),
                hue=list(wins.keys()), palette="viridis", legend=False)
    plt.title("Victorias totales por jugador")
    plt.ylabel("Victorias")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("experiments/results/wins.png")
    plt.close()

    # ===== Ventaja estructural del primer jugador =====
    total_first = df["wins_first"].sum()
    total_second = df["wins_second"].sum()
    total_games = total_first + total_second + df["draws"].sum()

    plt.figure(figsize=(6, 5))
    plt.bar(["Primer jugador", "Segundo jugador"],
            [total_first, total_second],
            color=["#4C72B0", "#DD8452"])
    plt.title(f"Ventaja estructural (n={total_games})")
    plt.ylabel("Victorias")
    plt.tight_layout()
    plt.savefig("experiments/results/first_player_advantage.png")
    plt.close()

    # ===== Tiempos =====
    plt.figure(figsize=(8, 5))
    sns.barplot(data=df, x="player1", y="avg_time",
                hue="player1", palette="magma", legend=False)
    plt.title("Tiempo medio por partida (jugador 1)")
    plt.ylabel("Segundos")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("experiments/results/times.png")
    plt.close()

    # ===== Análisis por enfrentamiento =====
    print("\n--- Análisis por enfrentamiento ---")
    for _, row in df.iterrows():
        total = row["p1_class_wins"] + row["p2_class_wins"]
        if total > 0:
            p_value = stats.binomtest(int(row["p1_class_wins"]), int(total), 0.5).pvalue
            sig = "✅ significativo" if p_value < 0.05 else "❌ no significativo"
            print(f"{row['player1']:12s} vs {row['player2']:12s}: "
                  f"{row['p1_class_wins']:2d}-{row['p2_class_wins']:2d}  "
                  f"p={p_value:.4f}  {sig}")

    # ===== Ventaja del primer jugador =====
    print(f"\n--- Ventaja estructural del primer jugador ---")
    print(f"Total partidas: {total_games}")
    print(f"Primer jugador ganó: {total_first} ({100*total_first/total_games:.1f}%)")
    print(f"Segundo jugador ganó: {total_second} ({100*total_second/total_games:.1f}%)")
    p_adv = stats.binomtest(int(total_first), int(total_first + total_second), 0.5).pvalue
    print(f"Test binomial (H0: 50/50): p={p_adv:.4f}")
    if p_adv < 0.05:
        print("→ Hay ventaja significativa del primer jugador (considera implementar swap)")
    else:
        print("→ No hay ventaja significativa del primer jugador")

    # ===== Resumen =====
    print("\n--- Resumen de victorias por jugador ---")
    for name, w in sorted(wins.items(), key=lambda x: -x[1]):
        print(f"{name:15s}: {w} victorias")

    print("\n✅ Gráficos guardados en experiments/results/")


if __name__ == "__main__":
    main()