# 💰 Personal Budget Tracker CLI

![Python](https://img.shields.io/badge/Python-3.7%2B-blue?logo=python)
![Interface](https://img.shields.io/badge/Interface-CLI-lightgrey?logo=terminal)
![Visualization](https://img.shields.io/badge/Visualization-Matplotlib-orange?logo=plotly)

A **command-line interface (CLI) application** built with **Python** to help you manage your **personal finances**.  
This tool allows you to create spending categories, set budgets, log transactions, and generate insightful reports to better understand your **spending habits**.

---

## 🚀 Features

- **📂 Category Management**  
  Create custom spending categories (e.g., Groceries, Transport, Entertainment) with **monthly budget limits**.

- **💸 Transaction Logging**  
  Add new expenses with an **amount** and an optional **description** for any category.

- **📊 Budget Tracking**  
  Instantly view how much you’ve spent in a category and how much of your budget remains.

- **💾 Data Persistence**  
  Automatically saves all budgets and transactions in a **JSON file**, so your financial data is **never lost**.

- **📈 Visual Reports**
  - Generate **weekly bar charts** to visualize daily spending.
  - Generate **monthly bar charts** to compare spending across different months of the year.

- **🧾 Text-Based Summaries**
  - View clear, concise reports directly in your **terminal** for quick overviews.

---

<details>
<summary>🧩 <b>How to Run</b></summary>

### ✅ Prerequisites

- **Python 3.7+**
- Required Python Libraries:

```bash
pip install matplotlib
```

---

### ▶️ Execution Steps

1. **Clone or Download** this repository to your local machine.  
2. **Install** the required library:  
   ```bash
   pip install matplotlib
   ```
3. **Navigate** to the project directory in your terminal.  
4. **Run** the application:  
   ```bash
   python budget_tracker.py
   ```

</details>

---

## 🧱 How It Works

When you run the script, it presents an **interactive text-based menu** with the following options:

1. **Add Category:** Create a new category and set its monthly budget limit.  
2. **Add Transaction:** Log a new expense by specifying the category, amount, and an optional description.  
3. **Generate Report:** View a detailed summary for a specific category, including:
   - Total budget  
   - Total spent  
   - Remaining balance  
   - List of transactions  
4. **Generate Weekly/Monthly Report:** Create **visual bar charts** comparing your spending patterns.  
5. **Save to File:** Save all current data to a `.json` file for future sessions.  
6. **Load from File:** Load previously saved data to continue where you left off.

---

## ⚙️ Design Overview

This project follows **object-oriented programming principles** with three main classes:

| Class | Purpose |
|-------|----------|
| **Transaction** | Represents an individual spending entry (amount, description, date). |
| **Category** | Manages transactions within a specific spending category. |
| **BudgetTracker** | The main controller that ties everything together — manages categories, storage, and reports. |

---

## 📊 Example Usage

```bash
Welcome to Personal Budget Tracker!
----------------------------------
1. Add Category
2. Add Transaction
3. Generate Report
4. Generate Weekly/Monthly Report
5. Save to File
6. Load from File
7. Exit
Enter your choice: 1
```

---

## 🧰 Tech Stack

| Component | Technology |
|------------|-------------|
| Programming Language | Python 3.7+ |
| Interface | Command-Line (CLI) |
| Data Storage | JSON |
| Visualization | Matplotlib |

---

## 🧠 Future Improvements

- Add **interactive terminal UI** with `rich` or `textual`.  
- Integrate **CSV export/import** functionality.  
- Implement **spending insights** (e.g., highest category, average weekly expense).  
- Add **password-protected data storage** for privacy.  

---

## 👨‍💻 Author & License

**Author:** [Aditya Raj Gaur](https://github.com/)  

> 💡 *Open for contributions and suggestions!*  
