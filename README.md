# Level5Project
My Level 5 Project at University of Glasgow - The Complexity of Linear Programming - Theory vs. Practice
This project explores the **practical behavior of the Simplex method** compared to the **Interior Point Method (IPM)**, focusing on how various pivot rules and problem structures affect performance.

## Overview

Despite Simplex having exponential worst-case complexity and IPM having polynomial guarantees, in practice Simplex often performs exceptionally well. This project investigates **why**, through controlled experiments and custom-built implementations.

---

## Experiments

### 1. **Pivot Rule Comparison**

Using a custom-built Simplex implementation, this experiment evaluates the impact of different pivot rules:

- **Pivot Rules Tested:**
  - Dantzig’s Rule
  - Bland’s Rule
  - Steepest Edge
  - Random Edge

- **Problem Types:**
  - **Balanced:** same number of constraints and variables
  - **Tall:** constraints = 2*variables
  - **Wide:** variables = 2*constraints

- **Phases:**
  - **One-phase Simplex:** problems where the origin point is a valid initial starting feasible solutoin
  - **Two-phase Simplex:** problems where an initial basic feasible solution has to be computed

Each problem size within each category includes **250 randomly generated dense LPs**.

---

### 2. **Simplex vs. Interior Point Method (GLPK)**

This experiment compares:
- **GLPK Simplex** vs. **GLPK Primal-Dual Interior Point Method**

Using the same problem categories as above, plus an extra experiment containing **sparse LPs**:
- We only consider **balanced sparse LPs** as they already influence problem status.
- **Balanced, Tall, Wide** forms — for **one-phase** and **two-phase** as for the previous experiment.

Each problem size within each category includes **250 randomly generated LPs**.
---

## Custom Simplex Implementation Highlights

- Custom **Simplex algorithm** written from scratch (supports all pivot rules)
- **Two-phase support**: detects feasibility and transitions cleanly into optimization
- Problem generator with:
  - Dense and sparse matrix generation
  - Full control over problem shape
  - Outputs the LP into the .lp format (one of the standard formats).
- Benchmarking framework to track:
  - **Pivot steps**
  - **Execution time**
  - **Problem status** (Optimal, Infeasible, Unbounded)
---

