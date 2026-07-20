# 🚢 Cruise Trip Tracker

A database-backed desktop application built with Python and MySQL for tracking cruises, passengers, ports, products, and onboard purchases. Built as a final project for Advanced Database Development at Valencia College.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Features](#features)
- [Project Structure](#project-structure)
- [Database Schema](#database-schema)
- [Setup Instructions](#setup-instructions)
- [How to Use](#how-to-use)
- [File Upload Format](#file-upload-format)
- [Sample Data](#sample-data)
- [CRUD Operations](#crud-operations)
- [Analytics Dashboard](#analytics-dashboard)

---

## Overview

Cruise Trip Tracker is a full-stack desktop application that simulates how a real cruise line might manage its operational data. The idea came from how cruise lines are designed to maximize onboard spending — tracking which drinks passengers buy, which excursions they book, which entertainment they attend, and analyzing what generates the most revenue.

The app enforces a logical data flow: **a cruise must exist before passengers can board, passengers must exist before purchases can be logged.** This mirrors real-world database integrity constraints.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.14 |
| GUI Framework | CustomTkinter |
| Database | MySQL 9.7 |
| DB Connector | mysql-connector-python |
| Charts | Matplotlib |
| File Uploads | csv (built-in) + openpyxl |
| IDE | IntelliJ IDEA |

---

## Features

### Core
- ✅ Full CRUD operations on 5 database tables
- ✅ Object-oriented design — each table has its own class
- ✅ Real-time connection to MySQL database
- ✅ Input validation on every field with specific error messages
- ✅ Foreign key enforcement (can't delete a cruise that has passengers)
- ✅ Duplicate cabin detection per cruise

### UI
- ✅ Dark navy/ocean blue theme — cruise inspired
- ✅ Sidebar navigation with icons
- ✅ Scrollable data tables for all entities
- ✅ Pop-up forms for Add and Edit operations
- ✅ Confirmation dialogs before any delete

### Gate Screen
- ✅ On first launch, the app requires you to add a cruise before accessing anything else
- ✅ Once a cruise exists, the full app unlocks automatically on future launches

### File Upload
- ✅ Upload CSV or Excel (.xlsx) files to bulk-import data
- ✅ Download CSV templates for each table
- ✅ Upload result dialog shows exactly how many rows succeeded and which rows failed with reasons

### Analytics Dashboard
- ✅ Total revenue, items sold, active spenders, top item stat cards
- ✅ Bar chart: top 10 most purchased items
- ✅ Pie chart: revenue breakdown by category
- ✅ Category filter (All, Drinks, Dining, Excursions, Entertainment, Spa)

---

## Project Structure

```
CruiseTripTracker/
│
├── App.py                          # Main application file
├── main.py                         # Console version (backup)
│
├── sample_data/
│   ├── cruises.csv                 # 5 sample cruises
│   ├── ports.csv                   # 15 sample ports
│   ├── passengers.xlsx             # 20 sample passengers
│   ├── products.csv                # 25 products/activities
│   └── purchases.xlsx              # 50 purchase records
│
└── README.md
```

---

## Database Schema

The application uses a MySQL database called `CruiseDB` with 5 tables:

```
Cruises
├── cruise_id       INT  PK AUTO_INCREMENT
├── cruise_line     VARCHAR(100)
├── ship_name       VARCHAR(100)
├── destination     VARCHAR(100)
├── departure_date  DATE
└── duration_days   INT

Passengers
├── passenger_id    INT  PK AUTO_INCREMENT
├── first_name      VARCHAR(100)
├── last_name       VARCHAR(100)
├── age             INT
├── cabin_number    VARCHAR(20)
└── cruise_id       INT  FK → Cruises

Ports
├── port_id         INT  PK AUTO_INCREMENT
├── port_name       VARCHAR(100)
├── country         VARCHAR(100)
├── arrival_date    DATE
└── cruise_id       INT  FK → Cruises

Products
├── product_id      INT  PK AUTO_INCREMENT
├── name            VARCHAR(150)
├── category        VARCHAR(50)
└── price           DECIMAL(10,2)

Purchases
├── purchase_id     INT  PK AUTO_INCREMENT
├── passenger_id    INT  FK → Passengers
├── product_id      INT  FK → Products
├── quantity        INT
└── purchase_date   DATE
```

### Relationships

```
Cruises ──< Passengers
Cruises ──< Ports
Passengers ──< Purchases
Products   ──< Purchases
```

---

## Setup Instructions

### Prerequisites
- Python 3.10 or higher
- MySQL Server running locally
- MySQL Workbench (optional but recommended)

### Step 1 — Clone or download the project

Place all files in your IntelliJ project folder.

### Step 2 — Install dependencies

```bash
pip install customtkinter mysql-connector-python matplotlib openpyxl
```

### Step 3 — Create the database in MySQL

Open MySQL Workbench and run:

```sql
CREATE DATABASE CruiseDB;
USE CruiseDB;

CREATE TABLE Cruises (
    cruise_id      INT AUTO_INCREMENT PRIMARY KEY,
    cruise_line    VARCHAR(100) NOT NULL,
    ship_name      VARCHAR(100) NOT NULL,
    destination    VARCHAR(100) NOT NULL,
    departure_date DATE NOT NULL,
    duration_days  INT NOT NULL
);

CREATE TABLE Passengers (
    passenger_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name   VARCHAR(100) NOT NULL,
    last_name    VARCHAR(100) NOT NULL,
    age          INT NOT NULL,
    cabin_number VARCHAR(20) NOT NULL,
    cruise_id    INT,
    FOREIGN KEY (cruise_id) REFERENCES Cruises(cruise_id)
);

CREATE TABLE Ports (
    port_id      INT AUTO_INCREMENT PRIMARY KEY,
    port_name    VARCHAR(100) NOT NULL,
    country      VARCHAR(100) NOT NULL,
    arrival_date DATE NOT NULL,
    cruise_id    INT,
    FOREIGN KEY (cruise_id) REFERENCES Cruises(cruise_id)
);
```

> The `Products` and `Purchases` tables are created automatically when the app first launches.

### Step 4 — Update your database password

Open `App.py` and find the `get_connection()` function near the top:

```python
def get_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",       # ← put your MySQL root password here
        database="CruiseDB"
    )
```

### Step 5 — Run the app

```bash
python App.py
```

---

## How to Use

### First Launch
When you open the app for the first time with an empty database, you'll see a **gate screen** asking you to add your first cruise. Fill in the form and click **Launch App** to unlock the full application.

### Navigation
Use the sidebar on the left to switch between tabs:
- **🚢 Cruises** — manage cruise records
- **👤 Passengers** — add and manage passengers per cruise
- **⚓ Ports** — track which ports each cruise visits
- **📦 Products** — manage the onboard product and activity catalog
- **🛒 Purchases** — log what each passenger buys onboard
- **📊 Analytics** — view revenue charts and top-selling items

### Adding Records
1. Click **➕ Add** on any tab
2. Fill in the form fields
3. Click **💾 Save**

Validation errors appear in red directly in the form — you won't be able to save until all fields pass.

### Editing Records
1. Click on a row in the table to select it
2. Click **✏️ Edit**
3. The form opens pre-filled with current values
4. Make changes and click **💾 Save**

### Deleting Records
1. Select a row
2. Click **🗑️ Delete**
3. Confirm the deletion

> Note: You cannot delete a cruise that still has passengers or ports linked to it. Delete the linked records first.

---

## File Upload Format

Each tab has a **📂 Upload CSV/Excel** button and a **📋 Download Template** button. Download the template first to get the exact column names, then fill it in.

### cruises.csv
```
cruise_line, ship_name, destination, departure_date, duration_days
Royal Caribbean, Wonder of the Seas, Caribbean, 2025-06-01, 7
```

### passengers.xlsx / passengers.csv
```
first_name, last_name, age, cabin_number, cruise_id
LeBron, James, 39, A101, 1
```

### ports.csv
```
port_name, country, arrival_date, cruise_id
Nassau, Bahamas, 2025-06-03, 1
```

### products.csv
```
name, category, price
Margarita, Drinks, 12.99
```
> Valid categories: `Drinks`, `Dining`, `Excursions`, `Entertainment`, `Spa`

### purchases.xlsx / purchases.csv
```
passenger_id, product_id, quantity, purchase_date
1, 3, 2, 2025-06-02
```

### Upload order
Always upload in this order to avoid foreign key errors:
1. Cruises
2. Ports
3. Passengers
4. Products
5. Purchases

---

## Sample Data

The `sample_data/` folder includes ready-to-use files that import cleanly with zero errors:

| File | Rows | Contents |
|---|---|---|
| cruises.csv | 5 | Royal Caribbean, Norwegian, Carnival, MSC, Disney |
| ports.csv | 15 | 3 ports per cruise across Caribbean, Alaska, Mediterranean |
| passengers.xlsx | 20 | 4 passengers per cruise including a Disney family with kids |
| products.csv | 25 | 5 products per category — drinks, dining, excursions, entertainment, spa |
| purchases.xlsx | 50 | Realistic purchases spread across all passengers |

---

## CRUD Operations

Every table supports full Create, Read, Update, Delete:

| Operation | How |
|---|---|
| **Create** | Click ➕ Add → fill form → 💾 Save |
| **Read** | Data displays automatically in the table on each tab |
| **Update** | Select row → ✏️ Edit → change fields → 💾 Save |
| **Delete** | Select row → 🗑️ Delete → confirm |
| **Bulk Create** | 📂 Upload CSV/Excel |

---

## Analytics Dashboard

The Analytics tab gives a real-time view of onboard revenue and purchasing patterns.

**Stat Cards:**
- 💰 Total Revenue — total dollars spent across all purchases
- 📦 Items Sold — total quantity of all items purchased
- 👤 Active Spenders — number of unique passengers who made at least one purchase
- 🏆 Top Item — the single most purchased product by quantity

**Charts:**
- **Most Purchased Items** — horizontal bar chart of the top 10 products by quantity sold
- **Revenue by Category** — pie chart showing revenue split across Drinks, Dining, Excursions, Entertainment, and Spa

**Category Filter:**
Use the dropdown at the top to filter all stats and the bar chart by a specific category. For example, selecting "Drinks" shows only drink-related revenue and top drinks purchased. The pie chart always shows the full category breakdown for context.

---


