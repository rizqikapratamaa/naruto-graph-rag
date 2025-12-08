# Naruto Graph RAG 🍥

> **IF4070 Knowledge Representation and Reasoning Project**  
> A Retrieval-Augmented Generation (RAG) system based on the Naruto Universe, powered by **Neo4j** (Knowledge Graph) and **Qwen-1.5B** (LLM).

This project allows users to query information about Shinobi, Jutsu, Villages, and Clans naturally. The system retrieves accurate facts from the graph database and generates human-like responses using a local Large Language Model.

---

## 📋 Table of Contents
- [Prerequisites](#-prerequisites)
- [Database Setup](#-1-database-setup-neo4j)
- [Environment Setup](#-2-environment-setup)
- [How to Run](#-3-how-to-run)
- [Project Structure](#-project-structure)
- [Testing & Validation](#-testing--validation)
- [Authors](#-authors)

---

## 🛠️ Prerequisites

Before running the code, ensure you have the following installed:

1. **Python 3.10+**
2. **Neo4j Desktop** (Download from https://neo4j.com/download/)
3. **Git**

---

## 💾 1. Database Setup (Neo4j)

You need to load the pre-built knowledge graph data (`.dump` file) into your Neo4j instance using Neo4j Desktop.

### Step 1: Locate the Dump File
The database dump file is located in this repository at:  
`data/naruto.dump`

### Step 2: Import into Neo4j Desktop
1. Open **Neo4j Desktop**.
2. Select your Project (e.g., "Project 1").
3. Click **Add** (Top right corner) → **File** → Select `data/naruto.dump` from this repository.
4. The file will appear in the "File" tab. Click the **three dots (...)** next to `naruto.dump`.
5. Select **Create new DBMS from dump**.
6. Set the password (or match it with your `.env` later).
7. Click **Create**.
8. Once created, click **Start** on the new database card.

> **Note:** Ensure the database status is **Active** (Green) and running on port `7687` before running the Python code.

---

## ⚙️ 2. Environment Setup

### Step 1: Clone Repository
```bash
git clone https://github.com/your-username/naruto-graph-rag.git
cd naruto-graph-rag
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# MacOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Credentials

Create a file named `.env` in the root directory and add your Neo4j configuration:

```ini
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=yourneo4juser
NEO4J_PASSWORD=yourneo4jpassword
```

---

## 🚀 3. How to Run

You can interact with the system in two ways: via a Web Interface (Streamlit) or the Terminal (CLI).

### Option A: Web Interface (Streamlit) - **Recommended**

This provides a chat-like interface with streaming responses.

```bash
streamlit run src/app.py
```

*The app will open automatically in your browser at `http://localhost:8501`.*

### Option B: Terminal (CLI)

Simple text-based interaction for quick testing.

```bash
python -m src.main
```

---

## 📂 Project Structure

```text
naruto-graph-rag/
├── data/
│   ├── naruto.dump           # Neo4j Database Backup (The Knowledge Graph)
│   └── naruto.rdf            # Original Ontology Source
├── src/
│   ├── database/             # Database Logic
│   │   ├── connection.py     # Neo4j Connection Handler
│   │   └── repository.py     # Cypher Queries implementation
│   ├── rag/                  # RAG Logic
│   │   ├── context_builder.py # Logic to map user input to graph data
│   │   ├── llm_engine.py     # Qwen LLM Handler (HuggingFace)
│   │   └── formatters.py     # String formatters
│   ├── app.py                # Streamlit UI Entry point
│   └── main.py               # CLI Entry point
├── .env                      # Configuration file
├── requirements.txt          # Python dependencies
└── README.md
```

---

## 🧪 Testing & Validation

To ensure the RAG system is actually reading from the Graph (and not hallucinating), try these specific queries:

1. **"Siapa pengguna Rinnegan?"** → Should list Madara, Sasuke.  
2. **"Siapa guru Naruto?"** → Should retrieve info about Kakashi/Jiraiya.  
3. **"Apa elemen Kakashi Hatake?"** → Should return Raiton.  
4. **"Siapa Goku?"** → Should return "Data not found" (proving it relies on the DB).

---

## 👥 Authors

- **Rizqika Mulia Pratama (13522126)** - Ontology Design, RAG Logic & System Architecture.
- **Samy Muhammad Haikal (13522151)** - Ontology Design, Documentation & Testing.
- **Rafif Ardhinto Ichwantoro (13522159)** - Ontology Design, Graph Engineering & Database.

---

*Disclaimer: Naruto is a trademark of Masashi Kishimoto/Shueisha. This project is for educational purposes.*