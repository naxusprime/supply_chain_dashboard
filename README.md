# 🚚 Supply Chain Network & Route Cost Analytics

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![SQLite](https://img.shields.io/badge/Database-SQLite3-lightgrey.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

An enterprise-grade analytical engine and interactive Streamlit dashboard for multi-echelon supply chain optimization, warehouse unit-cost auditing, capacity constraint monitoring, and freight carrier spend evaluation.

---

## 📌 Executive Summary

This system bridges relational supply chain databases with interactive business intelligence to audit production, warehouse handling, and freight transport costs. It identifies major network bottlenecks, cost anomalies, single-source carrier dependencies, and throughput imbalances across global logistics operations.

### Key Business Insights Discovered
* **Extreme Volume Skew**: `PLANT03` handles **96.9%** of total unit volume (28.61M out of 29.51M units) and accounts for **$14.8M** of total warehouse handling costs.
* **Unit Cost Anomaly**: `PLANT16` exhibits a handling cost of **$1.9198/unit**, nearly **4x higher** than the network average (~$0.50/unit).
* **Cost Driver Imbalance**: Facility handling costs ($15.63M) represent over **99.5%** of overall network spend, whereas linehaul freight costs ($73.6K) represent less than **0.5%**.
* **Carrier Risk Concentration**: Carrier `V444_0` captures **92.4%** of freight expenditure, creating critical single-vendor exposure.

---

### Install Dependencies
* **pip install -r requirements.txt**

### Initialize Database & Run Dashboard
* **streamlit run app.py**
