# Benny's Pool Time System – Code Repository

📂 **Path:** `Bennys-Project/code/`  

This folder contains all source files, scripts, and application code for **Benny's CueTime System**, developed as part of the MIS 4173 Capstone Project.

---

## 📜 Contents

- **`.gitkeep`** – Placeholder file to preserve the folder in version control.
- **`Bennys.sql`** – SQL script that defines the database schema for the CueTime system, including all necessary tables, keys, and constraints.
- **`Bennys_clean.zip`** – Working version of the **web-based manager interface**, built with HTML, CSS, and JavaScript. This code provides access to reporting, customer management, rental rate editing, and more.
- **`Test App.py`** – Updated **Python version of the bartender-facing app**, now supporting:
  - Table selection and rental rate application
  - Customer lookup and creation
  - Waitlist functionality with real-time assignment to tables

---

## 🚀 Current Architecture & Future Development

- ✅ **Manager Interface**: Web-based front end using standard web technologies (inside `Bennys_clean.zip`)
- ✅ **Bartender App**: Python-based local interface for tracking rentals and managing the waitlist
- ✅ **SQL Server**: Backend hosted on SQL Server Express; communicates with both front-end apps
- 🔒 **Data Security**: BitLocker encryption and regular OneDrive backups recommended per technical documentation

---

## 🗂 Repository Structure
```bash
Bennys-Project/
 ├── 📂 code/                  
 │   ├── .gitkeep                 
 │   ├── Bennys.sql              # SQL schema
 │   ├── Bennys_clean.zip        # Manager web app (HTML/JS)
 │   ├── Test App.py             # Bartender Python app
 ├── 📂 documents/
 │   ├── sprint 1/
 │   ├── sprint 2/
 │   ├── sprint 3/
 │   ├── sprint 4/
 │   ├── sprint 5/
 │   └── sprint 6/
 ├── README.md                   # Main project overview
