"""
gui.py - Tkinter GUI for the Library Management System
Provides a modern, polished interface with all library operations.
"""

import tkinter as tk
from tkinter import ttk, messagebox, font as tkfont
import sys
import os

# Ensure the project root is on the path so we can import sibling modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models import Library
from auth import authenticate


# ════════════════════════════════════════════════════════════════════════
#  Color Palette & Style Constants
# ════════════════════════════════════════════════════════════════════════
class Theme:
    # --- background layers ---
    BG_DARK      = "#0f172a"   # slate-900
    BG_CARD      = "#1e293b"   # slate-800
    BG_INPUT     = "#334155"   # slate-700
    BG_HOVER     = "#475569"   # slate-600

    # --- accent colors ---
    PRIMARY      = "#6366f1"   # indigo-500
    PRIMARY_DARK = "#4f46e5"   # indigo-600
    SUCCESS      = "#22c55e"   # green-500
    WARNING      = "#f59e0b"   # amber-500
    DANGER       = "#ef4444"   # red-500
    INFO         = "#06b6d4"   # cyan-500

    # --- text ---
    TEXT         = "#f1f5f9"   # slate-100
    TEXT_DIM     = "#94a3b8"   # slate-400
    TEXT_MUTED   = "#64748b"   # slate-500

    # --- table ---
    ROW_EVEN     = "#1e293b"
    ROW_ODD      = "#263248"
    ROW_SELECT   = "#3730a3"   # indigo-800

    # --- fonts ---
    FONT_FAMILY  = "Segoe UI"
    FONT_SIZE    = 10


# ════════════════════════════════════════════════════════════════════════
#  Login Window
# ════════════════════════════════════════════════════════════════════════
class LoginWindow:
    """Simple login dialog that must succeed before launching the main app."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Library Management System — Login")
        self.root.configure(bg=Theme.BG_DARK)
        self.root.resizable(False, False)

        # Center window
        w, h = 420, 380
        sx = (self.root.winfo_screenwidth() - w) // 2
        sy = (self.root.winfo_screenheight() - h) // 2
        self.root.geometry(f"{w}x{h}+{sx}+{sy}")

        self.authenticated = False
        self._build_ui()

    # ---------- UI construction ----------
    def _build_ui(self):
        outer = tk.Frame(self.root, bg=Theme.BG_DARK)
        outer.pack(expand=True, fill="both", padx=30, pady=30)

        # Icon / branding
        icon_label = tk.Label(outer, text="📚", font=(Theme.FONT_FAMILY, 42),
                              bg=Theme.BG_DARK, fg=Theme.PRIMARY)
        icon_label.pack(pady=(0, 5))

        title = tk.Label(outer, text="Library Management System",
                         font=(Theme.FONT_FAMILY, 16, "bold"),
                         bg=Theme.BG_DARK, fg=Theme.TEXT)
        title.pack()

        subtitle = tk.Label(outer, text="Sign in to continue",
                            font=(Theme.FONT_FAMILY, 10),
                            bg=Theme.BG_DARK, fg=Theme.TEXT_DIM)
        subtitle.pack(pady=(2, 20))

        # Username
        self._label(outer, "Username")
        self.username_var = tk.StringVar()
        self.ent_user = self._entry(outer, self.username_var)

        # Password
        self._label(outer, "Password")
        self.password_var = tk.StringVar()
        self.ent_pass = self._entry(outer, self.password_var, show="●")
        self.ent_pass.bind("<Return>", lambda e: self._login())

        # Login button
        btn = tk.Button(outer, text="Sign In", font=(Theme.FONT_FAMILY, 11, "bold"),
                        bg=Theme.PRIMARY, fg="white", activebackground=Theme.PRIMARY_DARK,
                        activeforeground="white", relief="flat", cursor="hand2",
                        bd=0, padx=20, pady=8, command=self._login)
        btn.pack(fill="x", pady=(18, 6))

        hint = tk.Label(outer, text="Default — admin / admin123",
                        font=(Theme.FONT_FAMILY, 8), bg=Theme.BG_DARK,
                        fg=Theme.TEXT_MUTED)
        hint.pack()

    # ---------- helpers ----------
    def _label(self, parent, text):
        lbl = tk.Label(parent, text=text, font=(Theme.FONT_FAMILY, 10),
                       bg=Theme.BG_DARK, fg=Theme.TEXT_DIM, anchor="w")
        lbl.pack(fill="x", pady=(6, 2))

    def _entry(self, parent, var, show=""):
        ent = tk.Entry(parent, textvariable=var, font=(Theme.FONT_FAMILY, 11),
                       bg=Theme.BG_INPUT, fg=Theme.TEXT, insertbackground=Theme.TEXT,
                       relief="flat", bd=0, show=show)
        # Add internal padding via a frame trick
        frame = tk.Frame(parent, bg=Theme.BG_INPUT, bd=1,
                         highlightbackground=Theme.TEXT_MUTED,
                         highlightthickness=1)
        frame.pack(fill="x")
        ent = tk.Entry(frame, textvariable=var, font=(Theme.FONT_FAMILY, 11),
                       bg=Theme.BG_INPUT, fg=Theme.TEXT, insertbackground=Theme.TEXT,
                       relief="flat", bd=0, show=show)
        ent.pack(fill="x", padx=8, pady=6)
        return ent

    def _login(self):
        user = self.username_var.get().strip()
        pwd = self.password_var.get().strip()
        if not user or not pwd:
            messagebox.showwarning("Validation", "Please enter both username and password.",
                                   parent=self.root)
            return
        if authenticate(user, pwd):
            self.authenticated = True
            self.logged_in_user = user
            self.root.destroy()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.",
                                 parent=self.root)


# ════════════════════════════════════════════════════════════════════════
#  Main Application Window
# ════════════════════════════════════════════════════════════════════════
class LibraryApp:
    """Main application window with sidebar navigation and content panels."""

    SIDEBAR_WIDTH = 200

    def __init__(self, root: tk.Tk, username: str = "admin"):
        self.root = root
        self.username = username
        self.library = Library()

        self.root.title("📚 Library Management System")
        self.root.configure(bg=Theme.BG_DARK)

        # Window sizing
        w, h = 1060, 640
        sx = (self.root.winfo_screenwidth() - w) // 2
        sy = (self.root.winfo_screenheight() - h) // 2
        self.root.geometry(f"{w}x{h}+{sx}+{sy}")
        self.root.minsize(900, 560)

        # Configure ttk styles
        self._configure_styles()

        # Build layout
        self._build_sidebar()
        self._build_content_area()

        # Show default view
        self._show_dashboard()

    # ================================================================
    #  TTK Style Configuration
    # ================================================================
    def _configure_styles(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Treeview (table)
        self.style.configure("Custom.Treeview",
                             background=Theme.BG_CARD,
                             foreground=Theme.TEXT,
                             fieldbackground=Theme.BG_CARD,
                             borderwidth=0,
                             font=(Theme.FONT_FAMILY, 10),
                             rowheight=32)
        self.style.configure("Custom.Treeview.Heading",
                             background=Theme.BG_INPUT,
                             foreground=Theme.TEXT,
                             font=(Theme.FONT_FAMILY, 10, "bold"),
                             borderwidth=0,
                             relief="flat")
        self.style.map("Custom.Treeview",
                       background=[("selected", Theme.ROW_SELECT)],
                       foreground=[("selected", "white")])

        # Scrollbar
        self.style.configure("Custom.Vertical.TScrollbar",
                             background=Theme.BG_INPUT,
                             troughcolor=Theme.BG_CARD,
                             borderwidth=0,
                             arrowcolor=Theme.TEXT_DIM)

    # ================================================================
    #  Sidebar
    # ================================================================
    def _build_sidebar(self):
        self.sidebar = tk.Frame(self.root, bg=Theme.BG_CARD,
                                width=self.SIDEBAR_WIDTH)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Branding
        brand = tk.Frame(self.sidebar, bg=Theme.BG_CARD)
        brand.pack(fill="x", pady=(20, 10), padx=16)
        tk.Label(brand, text="📚", font=(Theme.FONT_FAMILY, 24),
                 bg=Theme.BG_CARD, fg=Theme.PRIMARY).pack()
        tk.Label(brand, text="LibraryMS",
                 font=(Theme.FONT_FAMILY, 14, "bold"),
                 bg=Theme.BG_CARD, fg=Theme.TEXT).pack()

        sep = tk.Frame(self.sidebar, bg=Theme.BG_INPUT, height=1)
        sep.pack(fill="x", padx=16, pady=8)

        # Navigation buttons
        self.nav_buttons: list[tk.Button] = []
        nav_items = [
            ("🏠  Dashboard",   self._show_dashboard),
            ("➕  Add Book",     self._show_add_book),
            ("📤  Issue Book",   self._show_issue_book),
            ("📥  Return Book",  self._show_return_book),
            ("🔍  Search",       self._show_search),
            ("📋  All Books",    self._show_all_books),
            ("🗑️  Delete Book",  self._show_delete_book),
        ]
        for text, cmd in nav_items:
            btn = tk.Button(self.sidebar, text=text, anchor="w",
                            font=(Theme.FONT_FAMILY, 11),
                            bg=Theme.BG_CARD, fg=Theme.TEXT_DIM,
                            activebackground=Theme.BG_INPUT,
                            activeforeground=Theme.TEXT,
                            relief="flat", bd=0, padx=20, pady=8,
                            cursor="hand2",
                            command=lambda c=cmd, b=None: self._nav(c))
            btn.pack(fill="x")
            # Hover effect
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=Theme.BG_INPUT, fg=Theme.TEXT))
            btn.bind("<Leave>", lambda e, b=btn: (
                b.config(bg=Theme.PRIMARY_DARK, fg="white")
                if b == self._active_btn
                else b.config(bg=Theme.BG_CARD, fg=Theme.TEXT_DIM)))
            self.nav_buttons.append(btn)

        # Footer – logged-in user
        footer = tk.Frame(self.sidebar, bg=Theme.BG_CARD)
        footer.pack(side="bottom", fill="x", padx=16, pady=16)
        tk.Label(footer, text=f"👤 {self.username}",
                 font=(Theme.FONT_FAMILY, 9),
                 bg=Theme.BG_CARD, fg=Theme.TEXT_MUTED).pack(anchor="w")

        self._active_btn = None

    def _nav(self, command):
        """Handle sidebar navigation click."""
        # Determine which button was clicked by matching command
        for btn in self.nav_buttons:
            btn.config(bg=Theme.BG_CARD, fg=Theme.TEXT_DIM)
        # Find the button that triggered this command
        idx = [
            self._show_dashboard, self._show_add_book, self._show_issue_book,
            self._show_return_book, self._show_search, self._show_all_books,
            self._show_delete_book
        ].index(command)
        self._active_btn = self.nav_buttons[idx]
        self._active_btn.config(bg=Theme.PRIMARY_DARK, fg="white")
        command()

    # ================================================================
    #  Content Area
    # ================================================================
    def _build_content_area(self):
        self.content = tk.Frame(self.root, bg=Theme.BG_DARK)
        self.content.pack(side="left", fill="both", expand=True)

    def _clear_content(self):
        """Remove all widgets from the content area."""
        for w in self.content.winfo_children():
            w.destroy()

    # ---------- section helpers ----------
    def _section_title(self, parent, text, icon=""):
        frame = tk.Frame(parent, bg=Theme.BG_DARK)
        frame.pack(fill="x", padx=30, pady=(24, 4))
        tk.Label(frame, text=f"{icon}  {text}" if icon else text,
                 font=(Theme.FONT_FAMILY, 18, "bold"),
                 bg=Theme.BG_DARK, fg=Theme.TEXT).pack(anchor="w")
        # Underline accent
        bar = tk.Frame(frame, bg=Theme.PRIMARY, height=3, width=60)
        bar.pack(anchor="w", pady=(6, 0))
        return frame

    def _card(self, parent, **pack_kw) -> tk.Frame:
        """Return a rounded-look card frame."""
        card = tk.Frame(parent, bg=Theme.BG_CARD, bd=0,
                        highlightbackground=Theme.BG_INPUT,
                        highlightthickness=1)
        card.pack(fill="x", padx=30, pady=10, **pack_kw)
        return card

    def _form_label(self, parent, text, row, col=0):
        lbl = tk.Label(parent, text=text, font=(Theme.FONT_FAMILY, 10),
                       bg=Theme.BG_CARD, fg=Theme.TEXT_DIM, anchor="w")
        lbl.grid(row=row, column=col, sticky="w", padx=(20, 8), pady=(12, 2))
        return lbl

    def _form_entry(self, parent, var, row, col=1, width=32):
        frame = tk.Frame(parent, bg=Theme.BG_INPUT, bd=0,
                         highlightbackground=Theme.TEXT_MUTED,
                         highlightthickness=1)
        frame.grid(row=row, column=col, sticky="ew", padx=(0, 20), pady=(12, 2))
        ent = tk.Entry(frame, textvariable=var, font=(Theme.FONT_FAMILY, 10),
                       bg=Theme.BG_INPUT, fg=Theme.TEXT,
                       insertbackground=Theme.TEXT, relief="flat",
                       bd=0, width=width)
        ent.pack(padx=8, pady=5)
        return ent

    def _action_button(self, parent, text, command, color=None, **pack_kw):
        color = color or Theme.PRIMARY
        btn = tk.Button(parent, text=text, font=(Theme.FONT_FAMILY, 10, "bold"),
                        bg=color, fg="white",
                        activebackground=Theme.PRIMARY_DARK,
                        activeforeground="white",
                        relief="flat", bd=0, padx=18, pady=7,
                        cursor="hand2", command=command)
        btn.pack(padx=20, pady=10, **pack_kw)

        # Darken on hover
        def on_enter(e):
            # Simple darken by blending toward black
            btn.config(bg=Theme.PRIMARY_DARK)
        def on_leave(e):
            btn.config(bg=color)
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        return btn

    def _status_label(self, parent):
        """Create a label for status messages and return it."""
        lbl = tk.Label(parent, text="", font=(Theme.FONT_FAMILY, 10),
                       bg=Theme.BG_DARK, fg=Theme.SUCCESS, anchor="w")
        lbl.pack(fill="x", padx=30, pady=(2, 0))
        return lbl

    def _show_status(self, label: tk.Label, message: str):
        """Display a success or error message on the given label."""
        if message.startswith("ERROR"):
            label.config(fg=Theme.DANGER, text=f"✖  {message[7:]}")
        elif message.startswith("SUCCESS"):
            label.config(fg=Theme.SUCCESS, text=f"✔  {message[9:]}")
        else:
            label.config(fg=Theme.INFO, text=message)

    # ================================================================
    #  Views
    # ================================================================

    # ---- Dashboard ----
    def _show_dashboard(self):
        self._clear_content()
        if self._active_btn is None:
            self._active_btn = self.nav_buttons[0]
            self._active_btn.config(bg=Theme.PRIMARY_DARK, fg="white")

        self._section_title(self.content, "Dashboard", "🏠")

        stats_frame = tk.Frame(self.content, bg=Theme.BG_DARK)
        stats_frame.pack(fill="x", padx=30, pady=16)

        stats = [
            ("Total Books", str(self.library.total_books), Theme.PRIMARY, "📚"),
            ("Available", str(self.library.available_count), Theme.SUCCESS, "✅"),
            ("Issued", str(self.library.issued_count), Theme.WARNING, "📤"),
        ]

        for i, (label, value, color, icon) in enumerate(stats):
            card = tk.Frame(stats_frame, bg=Theme.BG_CARD, bd=0,
                            highlightbackground=color, highlightthickness=2)
            card.grid(row=0, column=i, padx=(0, 16), sticky="nsew")
            stats_frame.columnconfigure(i, weight=1)

            inner = tk.Frame(card, bg=Theme.BG_CARD)
            inner.pack(padx=20, pady=18)

            tk.Label(inner, text=icon, font=(Theme.FONT_FAMILY, 22),
                     bg=Theme.BG_CARD, fg=color).pack()
            tk.Label(inner, text=value, font=(Theme.FONT_FAMILY, 28, "bold"),
                     bg=Theme.BG_CARD, fg=Theme.TEXT).pack()
            tk.Label(inner, text=label, font=(Theme.FONT_FAMILY, 10),
                     bg=Theme.BG_CARD, fg=Theme.TEXT_DIM).pack()

        # Recent books table
        self._section_title(self.content, "Recent Books", "📋")
        books = self.library.get_all_books()[-10:]   # last 10
        if books:
            self._build_book_table(self.content, books)
        else:
            tk.Label(self.content, text="No books in the library yet. Add one!",
                     font=(Theme.FONT_FAMILY, 11), bg=Theme.BG_DARK,
                     fg=Theme.TEXT_DIM).pack(padx=30, pady=20, anchor="w")

    # ---- Add Book ----
    def _show_add_book(self):
        self._clear_content()
        self._section_title(self.content, "Add New Book", "➕")

        card = self._card(self.content)
        card.columnconfigure(1, weight=1)

        id_var = tk.StringVar()
        title_var = tk.StringVar()
        author_var = tk.StringVar()

        self._form_label(card, "Book ID", 0)
        ent_id = self._form_entry(card, id_var, 0)
        self._form_label(card, "Title", 1)
        self._form_entry(card, title_var, 1)
        self._form_label(card, "Author", 2)
        self._form_entry(card, author_var, 2)

        btn_frame = tk.Frame(card, bg=Theme.BG_CARD)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=(10, 0))

        status_lbl = self._status_label(self.content)

        def add():
            msg = self.library.add_book(id_var.get(), title_var.get(), author_var.get())
            self._show_status(status_lbl, msg)
            if msg.startswith("SUCCESS"):
                id_var.set("")
                title_var.set("")
                author_var.set("")

        def clear():
            id_var.set("")
            title_var.set("")
            author_var.set("")
            status_lbl.config(text="")

        self._action_button(btn_frame, "Add Book", add, Theme.SUCCESS, side="left")
        self._action_button(btn_frame, "Clear", clear, Theme.TEXT_MUTED, side="left")

        ent_id.focus_set()

    # ---- Issue Book ----
    def _show_issue_book(self):
        self._clear_content()
        self._section_title(self.content, "Issue Book", "📤")

        card = self._card(self.content)
        card.columnconfigure(1, weight=1)

        id_var = tk.StringVar()
        student_var = tk.StringVar()

        self._form_label(card, "Book ID", 0)
        ent_id = self._form_entry(card, id_var, 0)
        self._form_label(card, "Student Name", 1)
        self._form_entry(card, student_var, 1)

        btn_frame = tk.Frame(card, bg=Theme.BG_CARD)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=(10, 0))

        status_lbl = self._status_label(self.content)

        # Preview area
        preview_lbl = tk.Label(self.content, text="",
                               font=(Theme.FONT_FAMILY, 10),
                               bg=Theme.BG_DARK, fg=Theme.TEXT_DIM,
                               anchor="w", justify="left")
        preview_lbl.pack(fill="x", padx=30, pady=(6, 0))

        def preview(*_):
            book = self.library.get_book(id_var.get().strip())
            if book:
                status_color = Theme.SUCCESS if book.status == "Available" else Theme.WARNING
                preview_lbl.config(
                    text=f"📖  {book.title}  by {book.author}    —    Status: {book.status}",
                    fg=status_color)
            else:
                preview_lbl.config(text="", fg=Theme.TEXT_DIM)

        id_var.trace_add("write", preview)

        def issue():
            msg = self.library.issue_book(id_var.get().strip(), student_var.get())
            self._show_status(status_lbl, msg)
            if msg.startswith("SUCCESS"):
                id_var.set("")
                student_var.set("")
                preview_lbl.config(text="")

        def clear():
            id_var.set("")
            student_var.set("")
            status_lbl.config(text="")
            preview_lbl.config(text="")

        self._action_button(btn_frame, "Issue Book", issue, Theme.WARNING, side="left")
        self._action_button(btn_frame, "Clear", clear, Theme.TEXT_MUTED, side="left")

        ent_id.focus_set()

    # ---- Return Book ----
    def _show_return_book(self):
        self._clear_content()
        self._section_title(self.content, "Return Book", "📥")

        card = self._card(self.content)
        card.columnconfigure(1, weight=1)

        id_var = tk.StringVar()

        self._form_label(card, "Book ID", 0)
        ent_id = self._form_entry(card, id_var, 0)

        btn_frame = tk.Frame(card, bg=Theme.BG_CARD)
        btn_frame.grid(row=1, column=0, columnspan=2, pady=(10, 0))

        status_lbl = self._status_label(self.content)

        # Preview
        preview_lbl = tk.Label(self.content, text="",
                               font=(Theme.FONT_FAMILY, 10),
                               bg=Theme.BG_DARK, fg=Theme.TEXT_DIM,
                               anchor="w", justify="left")
        preview_lbl.pack(fill="x", padx=30, pady=(6, 0))

        def preview(*_):
            book = self.library.get_book(id_var.get().strip())
            if book and book.status == "Issued":
                preview_lbl.config(
                    text=f"📖  {book.title}  —  Issued to: {book.issued_to}  on {book.issue_date}",
                    fg=Theme.WARNING)
            elif book:
                preview_lbl.config(
                    text=f"📖  {book.title}  —  Already available",
                    fg=Theme.SUCCESS)
            else:
                preview_lbl.config(text="")

        id_var.trace_add("write", preview)

        def return_book():
            msg = self.library.return_book(id_var.get().strip())
            self._show_status(status_lbl, msg)
            if msg.startswith("SUCCESS"):
                id_var.set("")
                preview_lbl.config(text="")

        def clear():
            id_var.set("")
            status_lbl.config(text="")
            preview_lbl.config(text="")

        self._action_button(btn_frame, "Return Book", return_book, Theme.SUCCESS, side="left")
        self._action_button(btn_frame, "Clear", clear, Theme.TEXT_MUTED, side="left")

        ent_id.focus_set()

    # ---- Search ----
    def _show_search(self):
        self._clear_content()
        self._section_title(self.content, "Search Books", "🔍")

        card = self._card(self.content)
        card.columnconfigure(1, weight=1)

        query_var = tk.StringVar()
        self._form_label(card, "Search", 0)
        ent = self._form_entry(card, query_var, 0, width=40)

        btn_frame = tk.Frame(card, bg=Theme.BG_CARD)
        btn_frame.grid(row=1, column=0, columnspan=2, pady=(10, 0))

        result_frame = tk.Frame(self.content, bg=Theme.BG_DARK)
        result_frame.pack(fill="both", expand=True, padx=0, pady=0)

        info_lbl = tk.Label(self.content, text="",
                            font=(Theme.FONT_FAMILY, 10),
                            bg=Theme.BG_DARK, fg=Theme.TEXT_DIM)
        info_lbl.pack(padx=30, anchor="w")

        def search():
            # Clear previous results
            for w in result_frame.winfo_children():
                w.destroy()
            q = query_var.get().strip()
            if not q:
                info_lbl.config(text="Please enter a search term.", fg=Theme.WARNING)
                return
            results = self.library.search_books(q)
            info_lbl.config(text=f"Found {len(results)} result(s)", fg=Theme.INFO)
            if results:
                self._build_book_table(result_frame, results)

        ent.bind("<Return>", lambda e: search())

        self._action_button(btn_frame, "Search", search, Theme.INFO, side="left")
        self._action_button(btn_frame, "Clear", lambda: (
            query_var.set(""),
            info_lbl.config(text=""),
            [w.destroy() for w in result_frame.winfo_children()]
        ), Theme.TEXT_MUTED, side="left")

        ent.focus_set()

    # ---- All Books ----
    def _show_all_books(self):
        self._clear_content()
        self._section_title(self.content, "All Books", "📋")

        books = self.library.get_all_books()

        info = tk.Label(self.content,
                        text=f"{len(books)} book(s)  •  "
                             f"{self.library.available_count} available  •  "
                             f"{self.library.issued_count} issued",
                        font=(Theme.FONT_FAMILY, 10),
                        bg=Theme.BG_DARK, fg=Theme.TEXT_DIM)
        info.pack(padx=30, anchor="w", pady=(8, 0))

        if books:
            self._build_book_table(self.content, books, expand=True)
        else:
            tk.Label(self.content, text="The library is empty.",
                     font=(Theme.FONT_FAMILY, 12),
                     bg=Theme.BG_DARK, fg=Theme.TEXT_DIM).pack(padx=30, pady=30)

        btn_frame = tk.Frame(self.content, bg=Theme.BG_DARK)
        btn_frame.pack(padx=30, pady=6, anchor="w")
        self._action_button(btn_frame, "↻  Refresh", self._show_all_books,
                            Theme.INFO, side="left")

    # ---- Delete Book ----
    def _show_delete_book(self):
        self._clear_content()
        self._section_title(self.content, "Delete Book", "🗑️")

        card = self._card(self.content)
        card.columnconfigure(1, weight=1)

        id_var = tk.StringVar()
        self._form_label(card, "Book ID", 0)
        ent_id = self._form_entry(card, id_var, 0)

        btn_frame = tk.Frame(card, bg=Theme.BG_CARD)
        btn_frame.grid(row=1, column=0, columnspan=2, pady=(10, 0))

        status_lbl = self._status_label(self.content)

        # Preview
        preview_lbl = tk.Label(self.content, text="",
                               font=(Theme.FONT_FAMILY, 10),
                               bg=Theme.BG_DARK, fg=Theme.TEXT_DIM,
                               anchor="w")
        preview_lbl.pack(fill="x", padx=30, pady=(6, 0))

        def preview(*_):
            book = self.library.get_book(id_var.get().strip())
            if book:
                preview_lbl.config(
                    text=f"📖  {book.title}  by {book.author}  —  {book.status}",
                    fg=Theme.DANGER)
            else:
                preview_lbl.config(text="")

        id_var.trace_add("write", preview)

        def delete():
            bid = id_var.get().strip()
            book = self.library.get_book(bid)
            if not book:
                self._show_status(status_lbl, f"ERROR: Book ID '{bid}' not found.")
                return
            confirm = messagebox.askyesno(
                "Confirm Deletion",
                f"Are you sure you want to delete:\n\n"
                f"  {book.title} by {book.author}?",
                parent=self.root)
            if confirm:
                msg = self.library.delete_book(bid)
                self._show_status(status_lbl, msg)
                if msg.startswith("SUCCESS"):
                    id_var.set("")
                    preview_lbl.config(text="")

        def clear():
            id_var.set("")
            status_lbl.config(text="")
            preview_lbl.config(text="")

        self._action_button(btn_frame, "Delete Book", delete, Theme.DANGER, side="left")
        self._action_button(btn_frame, "Clear", clear, Theme.TEXT_MUTED, side="left")

        ent_id.focus_set()

    # ================================================================
    #  Shared Table Builder
    # ================================================================
    def _build_book_table(self, parent, books, expand=False):
        """Build a Treeview table of books with a scrollbar."""
        container = tk.Frame(parent, bg=Theme.BG_DARK)
        container.pack(fill="both", expand=expand, padx=30, pady=(10, 6))

        columns = ("id", "title", "author", "status", "issued_to", "issue_date")
        tree = ttk.Treeview(container, columns=columns, show="headings",
                            style="Custom.Treeview", selectmode="browse")

        headings = {
            "id": ("Book ID", 90),
            "title": ("Title", 200),
            "author": ("Author", 160),
            "status": ("Status", 90),
            "issued_to": ("Issued To", 140),
            "issue_date": ("Issue Date", 120),
        }
        for col, (text, width) in headings.items():
            tree.heading(col, text=text, anchor="w")
            tree.column(col, width=width, minwidth=60, anchor="w")

        # Scrollbar
        scrollbar = ttk.Scrollbar(container, orient="vertical",
                                  command=tree.yview,
                                  style="Custom.Vertical.TScrollbar")
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Insert rows with alternating colors
        for i, book in enumerate(books):
            tag = "even" if i % 2 == 0 else "odd"
            status_display = "✅ Available" if book.status == "Available" else "📤 Issued"
            tree.insert("", "end", values=(
                book.book_id, book.title, book.author,
                status_display,
                book.issued_to if book.issued_to else "—",
                book.issue_date if book.issue_date else "—",
            ), tags=(tag,))

        tree.tag_configure("even", background=Theme.ROW_EVEN)
        tree.tag_configure("odd", background=Theme.ROW_ODD)

        return tree


# ════════════════════════════════════════════════════════════════════════
#  Entry point (can also be used by main.py)
# ════════════════════════════════════════════════════════════════════════
def launch():
    """Run login window, then launch main app on success."""
    # --- Login ---
    login_root = tk.Tk()
    login_win = LoginWindow(login_root)
    login_root.mainloop()

    if not login_win.authenticated:
        return   # user closed the login window

    # --- Main App ---
    app_root = tk.Tk()
    app = LibraryApp(app_root, username=login_win.logged_in_user)
    app_root.mainloop()


if __name__ == "__main__":
    launch()
