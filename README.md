# 💸 Crowdfunding Console App

A terminal-based crowdfunding application written in Python. Users can register, log in, and manage their fundraising campaigns directly from the command line.

---

## 📌 Features

### 🔐 Authentication System
- User Registration with:
  - First Name & Last Name
  - Valid Email (format checked)
  - Secure Password (with confirmation)
  - Egyptian Mobile Phone (validated)
- Login with email & password
- Account activation (simulated)

### 🗂️ Project Management
- Create crowdfunding campaigns:
  - Title, Details, Target Amount, Start Date, End Date
- View all or personal projects
- Edit or Delete owned projects
- Search for projects by specific date (bonus feature)

---

## 🛠 Technologies Used

- **Python 3**
- **Rich**: for colorful console UI (tables, prompts, panels)
- Data stored in CSV files (`users.csv`, `projects.csv`)

---

## 📁 Folder Structure

```

CROWDFUNDING-CONSOLE-APP/
├── Data-storage/
│   ├── users.csv
│   └── projects.csv
├── main.py
└── README.md

```

---

## ▶️ How to Run the App

1. **Clone the repo**:
   ```bash
   git clone https://github.com/Mohamedelwali/crowdfunding-console-app.git
   cd crowdfunding-console-app

2. **Install required packages**:

   ```bash
   pip install rich
   ```

3. **Run the app**:

   ```bash
   python main.py
   ```

---

## 🔍 Future Improvements

* Switch to SQLite or PostgreSQL for more secure storage
* Add a donation feature per user
* Add email confirmation functionality
* Build a web interface (Flask or Django frontend)

---

## 📚 References

* [GoFundMe](https://www.gofundme.com)
* [Kickstarter](https://www.kickstarter.com)
* [Wikipedia - Crowdfunding](https://en.wikipedia.org/wiki/Crowdfunding)
* [`rich` Python Library](https://github.com/Textualize/rich)

---

## 👤 Author

**Mohamed Elwaly**
Fullstack Developer – Python | Django | React
[GitHub](https://github.com/) | [LinkedIn](https://linkedin.com/) | [Portfolio](https://your-portfolio.com)

---
