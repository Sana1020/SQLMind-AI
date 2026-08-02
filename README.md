#  SQLMind AI
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![PyTorch](https://img.shields.io/badge/PyTorch-2.x-red)
![Transformers](https://img.shields.io/badge/HuggingFace-Transformers-yellow)
![Streamlit](https://img.shields.io/badge/Streamlit-App-ff4b4b)
![License](https://img.shields.io/badge/License-MIT-green)

<p align="center">
  <b>Generate SQL Queries from Natural Language using a Fine-Tuned Qwen2.5 Model</b>
</p>

---

## 📖 Overview

SQLMind AI is an AI-powered application that converts natural language into SQL queries using a fine-tuned **Qwen2.5 Instruct** language model. The project combines a modern Streamlit web interface with a complete QLoRA fine-tuning pipeline for efficient SQL generation.

Whether you're learning SQL or building database applications, SQLMind AI allows users to describe database requests in plain English and instantly receive accurate SQL queries.

---

## ✨ Features

| Feature | Description |
|----------|-------------|
|  Natural Language to SQL | Converts English prompts into SQL queries |
|  Fine-Tuned Qwen2.5 | Uses a QLoRA fine-tuned language model |
|  Streamlit Interface | Clean and interactive web application |
|  SQL Export | Download generated SQL queries |
|  Efficient Inference | 4-bit quantized model for lower memory usage |
|  Training Pipeline | Dataset preparation, tokenization, and fine-tuning |

---

## 🏗️ Project Architecture

```text
                User
                  │
                  ▼
          Streamlit Web App
                  │
                  ▼
          Inference Engine
                  │
                  ▼
     Fine-Tuned Qwen2.5 Model
                  │
                  ▼
          Generated SQL Query
```

---

## 📂 Project Structure

```
SQLMind-AI/
│
├── app/
│   ├── app.py
│   └── inference.py
│
├── training/
│   ├── prepare_dataset.py
│   ├── tokenize_dataset.py
│   └── train.py
│
├── configs/
│   └── training_config.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🛠️ Tech Stack

- Python
- PyTorch
- Hugging Face Transformers
- PEFT (QLoRA)
- BitsAndBytes
- Streamlit
- Datasets
- Accelerate

---

## ⚙️ Requirements

- Python 3.10+
- CUDA-enabled GPU (recommended)
- pip

Install all dependencies:

```bash
pip install -r requirements.txt
```

---

##  Installation

Clone the repository:

```bash
git clone https://github.com/Sana1020/SQLMind-AI.git
```

Navigate to the project:

```bash
cd SQLMind-AI
```

Create a virtual environment:

```bash
python -m venv .venv
```

### Windows

```powershell
.venv\Scripts\Activate.ps1
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

##  Running the Application

Launch the Streamlit application:

```bash
streamlit run app/app.py
```

Then open your browser and start generating SQL queries from natural language.

---

## 🧠 Training Workflow

### 1. Prepare the dataset

```bash
python training/prepare_dataset.py
```

### 2. Tokenize the dataset

```bash
python training/tokenize_dataset.py
```

### 3. Fine-tune the model

```bash
python training/train.py
```

Training parameters are defined in:

```
configs/training_config.py
```

The model is fine-tuned using **QLoRA** with **4-bit quantization** for efficient memory usage.

---

##  Example

### Input

```text
Show all employees earning more than 7000.
```

### Generated SQL

```sql
SELECT *
FROM employees
WHERE salary > 7000;
```

---

## 📌 Example Prompts

- Show all employees earning more than 7000
- List the names of all students
- Show total sales by month
- List customers from Cairo

---

##  Future Improvements

- Database schema-aware prompting
- Multi-table query generation
- Support for multiple SQL dialects (MySQL, PostgreSQL, SQLite)
- SQL explanation and debugging mode
- Query optimization suggestions
- Docker deployment
---

##  Author

**Sana Elbakry**

Faculty of Computers and Artificial Intelligence

Artificial Intelligence Student

---
