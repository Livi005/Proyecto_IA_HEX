# HEX AI - Jugador Inteligente para el Juego HEX

Implementación de un jugador de HEX usando **búsqueda adversarial** (Minimax con poda alfa-beta) y **Monte Carlo Tree Search (MCTS)**, con heurísticas específicas del dominio.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📌 Descripción

HEX es un juego de tablero PSPACE-completo donde dos jugadores intentan conectar sus lados opuestos. Este proyecto implementa y compara cuatro estrategias de IA, demostrando que **MCTS supera a Minimax** en tableros 7×7.

### Hallazgos principales

- **MCTS gana 62.2%** del total de partidas, superando a Minimax (46.7%).
- **MCTS vs Minimax: 16-4** (p=0.012) — estadísticamente significativo.
- **Greedy no mejora sobre Random** — la heurística local es insuficiente.
- **Sin ventaja del primer jugador** con IAs adversariales (49.2% vs 50.8%).

---

## 🎯 Características

- ✅ Representación eficiente con NumPy.
- ✅ 4 jugadores: Random, Greedy, Minimax, MCTS.
- ✅ Heurísticas de puentes, puentes rotos y caminos.
- ✅ Interfaz web con Flask (tablero hexagonal).
- ✅ Torneos automatizados con análisis estadístico.
- ✅ Tests unitarios con pytest.
- ✅ Notebook exploratorio con Jupyter.

---

## 📦 Instalación

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## 🚀 Uso

```bash
# Jugar en consola
python -m src.hex_ai.game

# Interfaz web
python -m src.web.app
# Abrir http://127.0.0.1:5000

# Torneo y análisis
python -m experiments.run_tournament
python -m experiments.analyze_results

# Tests
pytest tests/ -v
```

## 📊 Resultados

| Jugador | Victorias | Win rate |
|---|---:|---:|
| **MCTS** | **56** | **62.2%** |
| Minimax | 42 | 46.7% |
| Random | 11 | 12.2% |
| Greedy | 11 | 12.2% |

## 📁 Estructura

```
hex-ai/
├── src/hex_ai/         # Motor del juego y jugadores
├── src/web/            # Interfaz Flask
├── experiments/        # Torneos y análisis
├── tests/              # Tests unitarios
├── docs/               # Memoria PDF
└── notebooks/          # Análisis exploratorio
```

## 📚 Referencias

- Browne et al. (2012). *A Survey of Monte Carlo Tree Search Methods*.
- Hayward et al. (2007). *The Game of Hex: A Survey*.

## 📄 Licencia

MIT