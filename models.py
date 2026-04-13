"""
models.py - Data Models for Library Management System
Contains Book and Library classes with all business logic.
Handles JSON-based persistence and validation.
"""

import json
import os
from datetime import datetime


class Book:
    """Represents a single book in the library."""

    def __init__(self, book_id: str, title: str, author: str,
                 status: str = "Available", issued_to: str = "",
                 issue_date: str = ""):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.status = status          # "Available" or "Issued"
        self.issued_to = issued_to    # Student name (empty if available)
        self.issue_date = issue_date  # Date when book was issued

    # ---------- serialization ----------
    def to_dict(self) -> dict:
        """Convert book to dictionary for JSON storage."""
        return {
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author,
            "status": self.status,
            "issued_to": self.issued_to,
            "issue_date": self.issue_date,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Book":
        """Create a Book instance from a dictionary."""
        return cls(
            book_id=data["book_id"],
            title=data["title"],
            author=data["author"],
            status=data.get("status", "Available"),
            issued_to=data.get("issued_to", ""),
            issue_date=data.get("issue_date", ""),
        )

    # ---------- display ----------
    def __str__(self) -> str:
        base = f"[{self.book_id}] {self.title} by {self.author}"
        if self.status == "Issued":
            return f"{base}  ⟶  Issued to {self.issued_to}"
        return f"{base}  ✓ Available"


class Library:
    """
    Core library logic – manages a collection of Book objects.
    All data is persisted to a JSON file automatically.
    """

    DATA_DIR = "data"
    DATA_FILE = os.path.join(DATA_DIR, "books.json")

    def __init__(self):
        self.books: dict[str, Book] = {}   # book_id → Book
        self._ensure_data_dir()
        self._load()

    # ================================================================
    #  Persistence helpers
    # ================================================================
    def _ensure_data_dir(self):
        """Create the data directory if it doesn't exist."""
        if not os.path.exists(self.DATA_DIR):
            os.makedirs(self.DATA_DIR)

    def _load(self):
        """Load books from JSON file into memory."""
        if os.path.exists(self.DATA_FILE):
            try:
                with open(self.DATA_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for item in data:
                    book = Book.from_dict(item)
                    self.books[book.book_id] = book
            except (json.JSONDecodeError, KeyError):
                self.books = {}

    def _save(self):
        """Persist current book collection to JSON file."""
        data = [book.to_dict() for book in self.books.values()]
        with open(self.DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    # ================================================================
    #  CRUD operations
    # ================================================================
    def add_book(self, book_id: str, title: str, author: str) -> str:
        """
        Add a new book.
        Returns a success/error message string.
        """
        # --- validation ---
        if not book_id.strip():
            return "ERROR: Book ID cannot be empty."
        if not title.strip():
            return "ERROR: Title cannot be empty."
        if not author.strip():
            return "ERROR: Author cannot be empty."
        if book_id in self.books:
            return f"ERROR: Book ID '{book_id}' already exists."

        book = Book(book_id.strip(), title.strip(), author.strip())
        self.books[book_id.strip()] = book
        self._save()
        return f"SUCCESS: Book '{title}' added successfully."

    def delete_book(self, book_id: str) -> str:
        """Delete a book by its ID."""
        if book_id not in self.books:
            return f"ERROR: Book ID '{book_id}' not found."
        if self.books[book_id].status == "Issued":
            return "ERROR: Cannot delete a book that is currently issued."
        title = self.books[book_id].title
        del self.books[book_id]
        self._save()
        return f"SUCCESS: Book '{title}' deleted successfully."

    def issue_book(self, book_id: str, student_name: str) -> str:
        """Issue a book to a student."""
        if not student_name.strip():
            return "ERROR: Student name cannot be empty."
        if book_id not in self.books:
            return f"ERROR: Book ID '{book_id}' not found."
        book = self.books[book_id]
        if book.status == "Issued":
            return f"ERROR: Book is already issued to '{book.issued_to}'."
        book.status = "Issued"
        book.issued_to = student_name.strip()
        book.issue_date = datetime.now().strftime("%Y-%m-%d %H:%M")
        self._save()
        return f"SUCCESS: Book '{book.title}' issued to {student_name}."

    def return_book(self, book_id: str) -> str:
        """Return a previously issued book."""
        if book_id not in self.books:
            return f"ERROR: Book ID '{book_id}' not found."
        book = self.books[book_id]
        if book.status == "Available":
            return "ERROR: This book is not currently issued."
        student = book.issued_to
        book.status = "Available"
        book.issued_to = ""
        book.issue_date = ""
        self._save()
        return f"SUCCESS: Book '{book.title}' returned by {student}."

    # ================================================================
    #  Query operations
    # ================================================================
    def get_all_books(self) -> list[Book]:
        """Return all books sorted by ID."""
        return sorted(self.books.values(), key=lambda b: b.book_id)

    def search_books(self, query: str) -> list[Book]:
        """Search books by ID, title, or author (case-insensitive)."""
        q = query.lower().strip()
        results = []
        for book in self.books.values():
            if (q in book.book_id.lower()
                    or q in book.title.lower()
                    or q in book.author.lower()):
                results.append(book)
        return sorted(results, key=lambda b: b.book_id)

    def get_book(self, book_id: str):
        """Return a single Book or None."""
        return self.books.get(book_id)

    @property
    def total_books(self) -> int:
        return len(self.books)

    @property
    def available_count(self) -> int:
        return sum(1 for b in self.books.values() if b.status == "Available")

    @property
    def issued_count(self) -> int:
        return sum(1 for b in self.books.values() if b.status == "Issued")
