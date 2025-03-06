# **Django API Project**

## **🔹 Project Overview**
This is a Django-based RESTful API that provides statistical insights into student placements. The API should expose a GET endpoint at: "/statistics" returning the expected JSON Format using **SQLite** as the database.
---

## **🔹 Prerequisites**
Ensure you have the following installed:
- **Python 3.x** (Check version with `python --version`)
- **pip** (Python package manager)
- **virtualenv** (Optional but recommended)
- **Git** (For version control)

---

## **🔹 Installation Steps**

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/nidhi-005/CDC.git
```
### 2️⃣ Create a Virtual Environment (Recommended)
```bash
python -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate      # On Windows
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Apply Database Migrations (SQLite)
```bash
python manage.py migrate
```

### 5️⃣ Run the Development Server
```bash
python manage.py runserver
```
Your API will be live at **`http://127.0.0.1:8000/statistics`** 

