# 📚 Library Management System

A fully functional Library Management System built with **Python** and **Tkinter**, featuring a modern dark-themed GUI, persistent JSON storage, and a simple login system.

---

## 🚀 How to Run

```bash
cd LibraryManagementSystem
python main.py
```

> **No external dependencies required** — uses only Python standard library (`tkinter`, `json`, `hashlib`, `os`, `datetime`).

---

## 🔐 Login Credentials

| Username    | Password   |
|-------------|------------|
| `admin`     | `admin123` |
| `librarian` | `lib2024`  |

---

## ✨ Features

### Core Operations
| Feature        | Description                                                |
|----------------|------------------------------------------------------------|
| **Add Book**   | Add new books with ID, Title, and Author                   |
| **Issue Book** | Issue a book to a student — tracks student name & date     |
| **Return Book**| Return a previously issued book                            |
| **View All**   | Browse all books in a sortable table with scrollbar        |
| **Search**     | Search by Book ID, Title, or Author (case-insensitive)     |
| **Delete Book**| Delete a book (with confirmation; cannot delete if issued) |

### Extra Features
- 🔒 **Login System** — SHA-256 hashed password authentication
- 🏠 **Dashboard** — Live stats (total / available / issued books)
- 📄 **Persistent Storage** — Data saved to `data/books.json`
- ✅ **Status Indicators** — Available / Issued shown in table
- 🔍 **Live Preview** — See book details as you type the ID
- 🧹 **Clear/Reset** — Every form has a clear button
- 📜 **Scrollbar** — Built into all book tables
- ⚠️ **Validation** — Prevents duplicates, empty fields, invalid operations
- 🎨 **Modern Dark Theme** — Slate/Indigo color palette with hover effects

---

## 📁 Project Structure

```
LibraryManagementSystem/
├── main.py          # Entry point
├── gui.py           # Tkinter GUI (views, layout, theme)
├── models.py        # Book & Library classes (business logic)
├── auth.py          # Simple login authentication
├── data/
│   ├── books.json   # Book records (auto-created)
│   └── users.json   # User credentials (auto-created)
└── README.md        # This file
```

---

## 🏗️ Architecture

The project follows a clean **MVC-inspired** pattern:

- **Model** (`models.py`) — `Book` and `Library` classes handle all data operations, validation, and JSON persistence.
- **View / Controller** (`gui.py`) — Tkinter GUI handles user interaction and calls model methods.
- **Auth** (`auth.py`) — Separate authentication module with hashed password storage.

---

## 🖥️ Screenshots

> Run the application to see the modern dark-themed interface with:
> - Sidebar navigation
> - Dashboard with stat cards
> - Data tables with alternating row colors
> - Status messages with color-coded feedback

---

## 📝 Notes

- The `data/` folder and JSON files are **auto-created** on first run.
- Default login credentials are created automatically.
- All data persists between sessions.
- Tested on **Python 3.10+** (any Python 3.7+ should work).
