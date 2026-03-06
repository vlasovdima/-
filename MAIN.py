import numpy as np
import logging

# Настройка логгера
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("decision_log.log", encoding='utf-8'), logging.StreamHandler()]
)

def solve_decision_task():
    # Матрица выигрышей со слайда 16
    A = np.array([
        [15, 12, 18, 13],
        [13, 15, 23, 10],
        [14, 20, 12, 11],
        [11, 12, 13, 14]
    ])
    
    strategies = ["A1", "A2", "A3", "A4"]
    logging.info("Матрица выигрышей загружена успешно.")

    # 1. Критерий Вальда (Максимин)
    mins = np.min(A, axis=1)
    wald_idx = np.argmax(mins)
    logging.info(f"Критерий Вальда: минимумы строк {mins}. Оптимально: {strategies[wald_idx]}")

    # 2. Критерий Сэвиджа (Минимаксный риск)
    # Построение матрицы рисков: R_ij = max(столбца) - A_ij
    max_cols = np.max(A, axis=0)
    R = max_cols - A
    max_risks = np.max(R, axis=1)
    savage_idx = np.argmin(max_risks)
    logging.info(f"Матрица рисков R:\n{R}")
    logging.info(f"Критерий Сэвиджа: макс. риски {max_risks}. Оптимально: {strategies[savage_idx]}")

    # 3. Критерий Гурвица (p = 0.4)
    p = 0.4
    maxs = np.max(A, axis=1)
    hurwitz_vals = p * mins + (1 - p) * maxs
    hurwitz_idx = np.argmax(hurwitz_vals)
    logging.info(f"Критерий Гурвица (p={p}): значения {hurwitz_vals}. Оптимально: {strategies[hurwitz_idx]}")

    return {
        "Wald": strategies[wald_idx],
        "Savage": strategies[savage_idx],
        "Hurwitz": strategies[hurwitz_idx]
    }

if __name__ == "__main__":
    results = solve_decision_task()
    print("\nИтоговые результаты:")
    for k, v in results.items():
        print(f"{k}: Лучшая стратегия - {v}")
