# 💰 Expense Tracker

A simple and interactive **Expense Tracker** web app built with **Python & Streamlit**. Track your daily expenses, upload existing data, visualize spending by category, and download your data — all from a clean browser interface.

---

## 📋 Features

- ➕ **Add Expenses** — Enter date, category, amount, and description
- 📂 **Upload Files** — Supports CSV, JSON, and Excel (`.xlsx`) formats
- 💾 **Download Data** — Export your expense data as a CSV file
- 📊 **Visualizations** — Bar chart showing spending by category
- 🧹 **Auto Data Cleaning** — Handles missing values & format issues automatically

---

## 🛠️ Requirements

Make sure you have **Python** installed. Then install the required libraries:

```bash
pip install streamlit pandas matplotlib seaborn openpyxl
```

| Library      | Purpose                          |
|--------------|----------------------------------|
| `streamlit`  | Web app framework                |
| `pandas`     | Data handling & manipulation     |
| `matplotlib` | Plotting graphs                  |
| `seaborn`    | Styled visualizations            |
| `openpyxl`   | Reading Excel (`.xlsx`) files    |

---

## 🚀 How to Run

**Step 1:** Open your terminal / PowerShell

**Step 2:** Navigate to the project folder:
```bash
cd c:\Users\91750\Desktop\projects\expensetracker
```

**Step 3:** Run the app:
```bash
streamlit run expense.py
```

**Step 4:** Your browser will automatically open at:
```
http://localhost:8501
```

---

## 📁 Project Structure

```
expensetracker/
│
├── expense.py      # Main application file
└── README.md       # Project documentation (this file)
```

---

## 📖 How to Use

### ➕ Adding an Expense
1. Look at the **left sidebar**
2. Fill in:
   - **Date** — Select the date of the expense
   - **Category** — Choose from Food, Transport, Entertainment, Utilities, Shopping, or Other
   - **Amount** — Enter the amount spent
   - **Description** — Optional note about the expense
3. Click **"Add Expense"**

### 📂 Uploading a File
1. In the sidebar under **File Operations**, click **"Upload File"**
2. Select a `.csv`, `.json`, or `.xlsx` file
3. The data will be automatically loaded and merged with existing entries

### 💾 Downloading Data
1. Click **"Download Data as CSV"** in the sidebar
2. Your current expense data will be saved as `my_expenses.csv`

### 📊 Viewing Charts
- After adding expenses, scroll down on the main page
- A **bar chart** showing total spending per category will be displayed

---

## ⚠️ Notes

- Data is stored **temporarily in session** — it will reset if you refresh or close the browser
- To keep your data, always **download it as CSV** before closing
- When uploading, duplicate entries are automatically removed
