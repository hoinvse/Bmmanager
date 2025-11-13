import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import csv
import json
import os
import shutil
from datetime import datetime

class BMManager:
    def __init__(self, root):
        self.root = root
        self.root.title("BM Manager - Quản lý Business Manager Facebook")
        self.root.geometry("1200x800")
        
        # Maximize window
        try:
            self.root.state('zoomed')  # Windows
        except Exception:
            try:
                self.root.attributes('-zoomed', True)  # Linux
            except Exception:
                pass
        
        # Modern color scheme
        self.colors = {
            'primary': '#2563eb',      # Blue-600
            'primary_light': '#3b82f6', # Blue-500
            'primary_dark': '#1d4ed8',  # Blue-700
            'secondary': '#10b981',     # Emerald-500
            'accent': '#f59e0b',        # Amber-500
            'danger': '#ef4444',        # Red-500
            'bg_primary': '#ffffff',    # White
            'bg_secondary': '#f8fafc',  # Slate-50
            'bg_card': '#ffffff',       # White
            'text_primary': '#1f2937',  # Gray-800
            'text_secondary': '#6b7280', # Gray-500
            'border': '#e5e7eb',        # Gray-200
            'hover': '#f3f4f6',         # Gray-100
            'success': '#22c55e',       # Green-500
        }
        
        self.root.configure(bg=self.colors['bg_secondary'])
        
        # Create modern style
        self.create_modern_style()
        
        # Initialize data
        self.bm_data = []
        self.current_file = None
        self.data_dir = os.path.join(os.path.dirname(__file__), 'bm_data')
        self.current_folder = 'default'
        self.db_path = os.path.join(self.data_dir, self.current_folder, 'bm_data.json')
        
        # Create data directory
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        if not os.path.exists(os.path.join(self.data_dir, 'default')):
            os.makedirs(os.path.join(self.data_dir, 'default'))
        
        # Create widgets
        self.create_widgets()
        self.load_json_db()
        
    def create_modern_style(self):
        """Tạo style hiện đại"""
        self.style = ttk.Style()
        
        # Configure modern theme
        self.style.theme_use('clam')
        
        # Configure modern styles
        self.style.configure('Modern.TFrame', 
                           background=self.colors['bg_card'],
                           relief='flat',
                           borderwidth=1)
        
        self.style.configure('Card.TFrame',
                           background=self.colors['bg_card'],
                           relief='solid',
                           borderwidth=1,
                           padding=20)
        
        self.style.configure('Modern.TLabel',
                           background=self.colors['bg_card'],
                           foreground=self.colors['text_primary'],
                           font=('Segoe UI', 10))
        
        self.style.configure('Title.TLabel',
                           background=self.colors['bg_secondary'],
                           foreground=self.colors['primary'],
                           font=('Segoe UI', 18, 'bold'))
        
        self.style.configure('Subtitle.TLabel',
                           background=self.colors['bg_card'],
                           foreground=self.colors['text_secondary'],
                           font=('Segoe UI', 11, 'bold'))
        
        # Modern buttons
        self.style.configure('Primary.TButton',
                           background=self.colors['primary'],
                           foreground='white',
                           font=('Segoe UI', 9, 'bold'),
                           padding=(15, 8),
                           relief='flat',
                           borderwidth=0)
        
        self.style.map('Primary.TButton',
                      background=[('active', self.colors['primary_light']),
                                ('pressed', self.colors['primary_dark'])])
        
        self.style.configure('Success.TButton',
                           background=self.colors['success'],
                           foreground='white',
                           font=('Segoe UI', 9, 'bold'),
                           padding=(12, 6),
                           relief='flat')
        
        self.style.configure('Danger.TButton',
                           background=self.colors['danger'],
                           foreground='white',
                           font=('Segoe UI', 9, 'bold'),
                           padding=(12, 6),
                           relief='flat')
        
        self.style.configure('Accent.TButton',
                           background=self.colors['accent'],
                           foreground='white',
                           font=('Segoe UI', 9, 'bold'),
                           padding=(12, 6),
                           relief='flat')
        
        # Modern notebook
        self.style.configure('Modern.TNotebook',
                           background=self.colors['bg_secondary'],
                           tabposition='n')
        
        self.style.configure('Modern.TNotebook.Tab',
                           background=self.colors['bg_card'],
                           foreground=self.colors['text_primary'],
                           padding=(20, 12),
                           font=('Segoe UI', 11, 'bold'))
        
        self.style.map('Modern.TNotebook.Tab',
                      background=[('selected', self.colors['primary']),
                                ('active', self.colors['hover'])],
                      foreground=[('selected', 'white'),
                                ('active', self.colors['text_primary'])])
        # Hide notebook tabs (we'll switch via header buttons)
        try:
            self.style.layout('Modern.TNotebook.Tab', [])
        except Exception:
            pass
        
        # Modern treeview
        self.style.configure('Modern.Treeview',
                           background='white',
                           foreground=self.colors['text_primary'],
                           fieldbackground='white',
                           borderwidth=0,
                           relief='flat',
                           font=('Segoe UI', 11),
                           rowheight=38)
        
        self.style.configure('Modern.Treeview.Heading',
                           background=self.colors['primary'],
                           foreground='white',
                           font=('Segoe UI', 10, 'bold'),
                           padding=(6, 8))
        
        self.style.map('Modern.Treeview',
                      background=[('selected', self.colors['primary_light'])],
                      foreground=[('selected', 'white')])
        
        # Modern entry
        self.style.configure('Modern.TEntry',
                           fieldbackground='white',
                           borderwidth=2,
                           relief='solid',
                           padding=(10, 8),
                           font=('Segoe UI', 10))
        
        # Modern combobox
        self.style.configure('Modern.TCombobox',
                           fieldbackground='white',
                           borderwidth=2,
                           relief='solid',
                           padding=(10, 8),
                           font=('Segoe UI', 10))
        
        # Modern radiobutton
        self.style.configure('Modern.TRadiobutton',
                           background=self.colors['bg_card'],
                           foreground=self.colors['text_primary'],
                           font=('Segoe UI', 10),
                           focuscolor='none')
        
        self.style.map('Modern.TRadiobutton',
                      background=[('active', self.colors['hover'])],
                      foreground=[('active', self.colors['text_primary'])])
        
    def create_widgets(self):
        # Main container
        main_container = ttk.Frame(self.root, style='Modern.TFrame')
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = ttk.Frame(main_container, style='Card.TFrame')
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Title with modern styling
        title_label = ttk.Label(header_frame, 
                               text="🚀 BM Manager Pro",
                               style='Title.TLabel')
        title_label.pack(pady=(0, 5))
        
        subtitle_label = ttk.Label(header_frame,
                                 text="Quản lý Business Manager Facebook một cách chuyên nghiệp",
                                 style='Subtitle.TLabel')
        subtitle_label.pack()
        
        # Tab switch buttons in header (top-left)
        tabs_switch = ttk.Frame(header_frame, style='Modern.TFrame')
        tabs_switch.pack(anchor=tk.W, pady=(10, 0))
        ttk.Button(tabs_switch, text="📊 Quản lý", style='Primary.TButton',
                  command=lambda: self.notebook.select(self.manage_tab)).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(tabs_switch, text="🔍 Lọc Link", style='Accent.TButton',
                  command=lambda: self.notebook.select(self.filter_tab)).pack(side=tk.LEFT)
        
        # Modern notebook with custom style
        self.notebook = ttk.Notebook(main_container, style='Modern.TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.create_manage_tab()
        self.create_filter_tab()
        
    def create_manage_tab(self):
        # Management tab
        manage_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.manage_tab = manage_frame
        self.notebook.add(manage_frame, text="📊 Quản lý")
        
        
        # Scrollable container (full-width)
        canvas = tk.Canvas(manage_frame, bg=self.colors['bg_secondary'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(manage_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style='Modern.TFrame')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        window_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        # Ensure inner frame stretches to canvas width
        def _resize_inner(event):
            try:
                canvas.itemconfig(window_id, width=event.width)
            except Exception:
                pass
        canvas.bind('<Configure>', _resize_inner)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Folder management card
        folder_card = ttk.Frame(scrollable_frame, style='Card.TFrame')
        folder_card.pack(fill=tk.X, pady=(0, 20))
        
        folder_title = ttk.Label(folder_card, text="📁 Quản lý thư mục", style='Subtitle.TLabel')
        folder_title.pack(anchor=tk.W, pady=(0, 15))
        
        folder_controls = ttk.Frame(folder_card, style='Modern.TFrame')
        folder_controls.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(folder_controls, text="Thư mục hiện tại:", style='Modern.TLabel').pack(side=tk.LEFT, padx=(0, 10))
        
        self.folder_var = tk.StringVar(value=self.current_folder)
        self.folder_combo = ttk.Combobox(folder_controls, textvariable=self.folder_var, 
                                       width=20, state='readonly', style='Modern.TCombobox')
        self.folder_combo.pack(side=tk.LEFT, padx=(0, 15))
        self.folder_combo.bind('<<ComboboxSelected>>', self.on_folder_change)
        
        # Modern buttons with icons
        ttk.Button(folder_controls, text="➕ Tạo", style='Success.TButton',
                  command=self.create_folder).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(folder_controls, text="🗑️ Xóa", style='Danger.TButton',
                  command=self.delete_folder).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(folder_controls, text="✏️ Đổi tên", style='Accent.TButton',
                  command=self.rename_folder).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(folder_controls, text="📦 Move", style='Primary.TButton',
                  command=self.move_selected).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(folder_controls, text="💾 Tải DB", style='Success.TButton',
                  command=self.load_json_db).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(folder_controls, text="🔄 Làm mới", style='Primary.TButton',
                  command=self.refresh_folders).pack(side=tk.LEFT)
        
        # Status label placed on the right within folder controls
        status_spacer = ttk.Frame(folder_controls, style='Modern.TFrame')
        status_spacer.pack(side=tk.RIGHT, padx=(0, 40))
        self.status_var = getattr(self, 'status_var', tk.StringVar(value="Tổng: 0 | Đã chọn: 0"))
        ttk.Label(status_spacer, textvariable=self.status_var,
                  style='Modern.TLabel', font=('Segoe UI', 10, 'bold')).pack(side=tk.RIGHT)
        
        # Folder info
        self.folder_info_var = tk.StringVar()
        info_label = ttk.Label(folder_card, textvariable=self.folder_info_var, style='Modern.TLabel')
        info_label.pack(anchor=tk.W, pady=(10, 0))
        
        # Data table card
        table_card = ttk.Frame(scrollable_frame, style='Card.TFrame')
        table_card.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        table_title = ttk.Label(table_card, text="📋 Danh sách Business Manager", style='Subtitle.TLabel')
        table_title.pack(anchor=tk.W, pady=(0, 15))
        
        # Table container with border
        table_container = ttk.Frame(table_card)
        table_container.pack(fill=tk.BOTH, expand=True)
        
        # Create modern treeview
        self.columns = ('STT', 'Chọn', 'TypeBM', 'ID', 'BmID', 'Thư mục', 'Ghi chú', 'Link1', 'Link2', 'Link3')
        self.tree = ttk.Treeview(table_container, columns=self.columns, show='headings', 
                               height=20, style='Modern.Treeview')
        # Faint Excel-like row stripes
        try:
            self.tree.tag_configure('row_even', background='#ffffff')
            self.tree.tag_configure('row_odd', background=self.colors.get('bg_secondary', '#f8fafc'))
        except Exception:
            pass
        
        # Configure columns
        column_configs = [
            ('STT', 60, 'STT'),
            ('Chọn', 80, 'Chọn'),
            ('TypeBM', 100, 'Type BM'),
            ('ID', 150, 'ID'),
            ('BmID', 150, 'BM ID'),
            ('Thư mục', 200, 'Thư mục'),
            ('Ghi chú', 220, 'Ghi chú'),
            ('Link1', 400, 'Link 1'),
            ('Link2', 400, 'Link 2'),
            ('Link3', 400, 'Link 3')
        ]
        
        for col_id, width, text in column_configs:
            # Heading alignment
            if col_id in ('STT', 'Chọn'):
                self.tree.heading(col_id, text=text, anchor=tk.CENTER, command=lambda c=col_id: self.sort_by_column(c))
            else:
                self.tree.heading(col_id, text=text, anchor=tk.W, command=lambda c=col_id: self.sort_by_column(c))

            # Cell alignment
            if col_id in ('Link1', 'Link2', 'Link3'):
                self.tree.column(col_id, width=width, minwidth=120, anchor=tk.W, stretch=True)
            elif col_id in ('STT', 'Chọn'):
                self.tree.column(col_id, width=width, minwidth=20, anchor=tk.CENTER, stretch=False)
            else:
                self.tree.column(col_id, width=width, minwidth=60, anchor=tk.W, stretch=False)
        
        # Modern scrollbars
        tree_v_scrollbar = ttk.Scrollbar(table_container, orient=tk.VERTICAL, command=self.tree.yview)
        tree_h_scrollbar = ttk.Scrollbar(table_container, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=tree_v_scrollbar.set, xscrollcommand=tree_h_scrollbar.set)
        
        # Pack treeview and scrollbars
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        tree_v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        tree_h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        table_container.columnconfigure(0, weight=1)
        table_container.rowconfigure(0, weight=1)
        
        # Bind events
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        self.tree.bind('<Button-1>', self.on_tree_click)
        self.tree.bind('<Double-1>', self.on_cell_double_click)
        self.tree.bind('<Control-c>', self.copy_cell)
        self.tree.bind('<Control-C>', self.copy_cell)
        
        self.sort_directions = {}
        self.current_cell = (None, None)
        
        # Create context menu
        self.create_context_menu()
        
        # Action buttons moved into context menu; status moved into folder controls
        
        # Initialize data
        self.rowid_to_index = {}
        self.refresh_folders()
        
    def create_filter_tab(self):
        # Filter tab
        filter_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.filter_tab = filter_frame
        self.notebook.add(filter_frame, text="🔍 Lọc Link")
        
        filter_container = ttk.Frame(filter_frame, style='Modern.TFrame')
        filter_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Filter card
        filter_card = ttk.Frame(filter_container, style='Card.TFrame')
        filter_card.pack(fill=tk.X, pady=(0, 20))
        
        filter_title = ttk.Label(filter_card, text="🎯 Lọc theo BmID", style='Subtitle.TLabel')
        filter_title.pack(anchor=tk.W, pady=(0, 15))
        
        ttk.Label(filter_card, text="Nhập danh sách BmID (mỗi dòng 1 BmID):", 
                 style='Modern.TLabel').pack(anchor=tk.W, pady=(0, 10))
        
        self.filter_bmid_text = tk.Text(filter_card, height=6, font=('Consolas', 10),
                                       relief='solid', borderwidth=2, padx=10, pady=8)
        self.filter_bmid_text.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Button(filter_card, text="🔍 Lọc ngay", style='Primary.TButton',
                  command=self.filter_links_by_bmid).pack(anchor=tk.W)
        
        # Results card
        results_card = ttk.Frame(filter_container, style='Card.TFrame')
        results_card.pack(fill=tk.BOTH, expand=True)
        
        results_title = ttk.Label(results_card, text="📋 Kết quả lọc", style='Subtitle.TLabel')
        results_title.pack(anchor=tk.W, pady=(0, 15))
        
        results_container = ttk.Frame(results_card, style='Modern.TFrame')
        results_container.pack(fill=tk.BOTH, expand=True)
        results_container.columnconfigure(0, weight=1)
        results_container.columnconfigure(1, weight=1)
        results_container.rowconfigure(1, weight=1)
        
        # Result lists
        ttk.Label(results_container, text="🔗 Link 1", style='Subtitle.TLabel').grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        ttk.Label(results_container, text="🔗 Link 2", style='Subtitle.TLabel').grid(row=0, column=1, sticky=tk.W, padx=(20, 0), pady=(0, 10))
        
        self.list_link1 = tk.Listbox(results_container, font=('Consolas', 9), 
                                    relief='solid', borderwidth=2)
        self.list_link2 = tk.Listbox(results_container, font=('Consolas', 9),
                                    relief='solid', borderwidth=2)
        
        self.list_link1.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        self.list_link2.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(10, 0))
        
        # Scrollbars for lists
        sb1 = ttk.Scrollbar(results_container, orient=tk.VERTICAL, command=self.list_link1.yview)
        self.list_link1.configure(yscrollcommand=sb1.set)
        sb1.grid(row=1, column=0, sticky=(tk.N, tk.S, tk.E))
        
        sb2 = ttk.Scrollbar(results_container, orient=tk.VERTICAL, command=self.list_link2.yview)
        self.list_link2.configure(yscrollcommand=sb2.set)
        sb2.grid(row=1, column=1, sticky=(tk.N, tk.S, tk.E))
        
        # Filter info
        self.filter_info_var = tk.StringVar(value="Chưa có kết quả lọc")
        info_label = ttk.Label(results_card, textvariable=self.filter_info_var, 
                             style='Modern.TLabel', font=('Segoe UI', 10, 'italic'))
        info_label.pack(anchor=tk.W, pady=(15, 0))
        
    # Keep all the existing methods from the original code...
    def refresh_folders(self):
        """Làm mới danh sách thư mục"""
        try:
            folders = [f for f in os.listdir(self.data_dir) if os.path.isdir(os.path.join(self.data_dir, f))]
            folders.sort()
            self.folder_combo['values'] = folders
            if self.current_folder not in folders:
                self.current_folder = 'default'
                self.folder_var.set(self.current_folder)
            self.update_folder_info()
            self.update_status_bar()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải danh sách thư mục: {str(e)}")
            
    def update_folder_info(self):
        """Cập nhật thông tin thư mục hiện tại"""
        try:
            folder_path = os.path.join(self.data_dir, self.current_folder)
            bm_count = len(self.bm_data)
            self.folder_info_var.set(f"📂 Thư mục: {self.current_folder} | 📊 Số BM: {bm_count}")
        except Exception:
            self.folder_info_var.set(f"📂 Thư mục: {self.current_folder} | 📊 Số BM: 0")

    def on_folder_change(self, event=None):
        """Xử lý khi thay đổi thư mục"""
        new_folder = self.folder_var.get()
        if new_folder != self.current_folder:
            self.save_json_db()
            self.current_folder = new_folder
            self.db_path = os.path.join(self.data_dir, self.current_folder, 'bm_data.json')
            self.load_json_db()
            self.update_folder_info()

    def create_folder(self):
        """Tạo thư mục mới"""
        folder_name = simpledialog.askstring("Tạo thư mục", "Nhập tên thư mục mới:")
        if folder_name and folder_name.strip():
            folder_name = folder_name.strip()
            folder_path = os.path.join(self.data_dir, folder_name)
            try:
                if os.path.exists(folder_path):
                    messagebox.showwarning("Cảnh báo", "Thư mục đã tồn tại!")
                    return
                os.makedirs(folder_path)
                self.refresh_folders()
                messagebox.showinfo("Thành công", f"✅ Đã tạo thư mục: {folder_name}")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể tạo thư mục: {str(e)}")

    def delete_folder(self):
        """Xóa thư mục"""
        if self.current_folder == 'default':
            messagebox.showwarning("Cảnh báo", "Không thể xóa thư mục mặc định!")
            return
            
        if messagebox.askyesno("Xác nhận", f"Bạn có chắc chắn muốn xóa thư mục '{self.current_folder}'?"):
            try:
                folder_path = os.path.join(self.data_dir, self.current_folder)
                if os.path.exists(folder_path):
                    shutil.rmtree(folder_path)
                self.current_folder = 'default'
                self.folder_var.set(self.current_folder)
                self.db_path = os.path.join(self.data_dir, self.current_folder, 'bm_data.json')
                self.refresh_folders()
                self.load_json_db()
                messagebox.showinfo("Thành công", "✅ Đã xóa thư mục!")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể xóa thư mục: {str(e)}")

    def rename_folder(self):
        """Đổi tên thư mục"""
        if self.current_folder == 'default':
            messagebox.showwarning("Cảnh báo", "Không thể đổi tên thư mục mặc định!")
            return
            
        new_name = simpledialog.askstring("Đổi tên thư mục", f"Tên mới cho thư mục '{self.current_folder}':")
        if new_name and new_name.strip():
            new_name = new_name.strip()
            if new_name == self.current_folder:
                return
            try:
                old_path = os.path.join(self.data_dir, self.current_folder)
                new_path = os.path.join(self.data_dir, new_name)
                if os.path.exists(new_path):
                    messagebox.showwarning("Cảnh báo", "Tên thư mục đã tồn tại!")
                    return
                os.rename(old_path, new_path)
                self.current_folder = new_name
                self.folder_var.set(self.current_folder)
                self.db_path = os.path.join(self.data_dir, self.current_folder, 'bm_data.json')
                self.refresh_folders()
                messagebox.showinfo("Thành công", f"✅ Đã đổi tên thư mục thành: {new_name}")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể đổi tên thư mục: {str(e)}")

    def move_selected(self):
        """Di chuyển dữ liệu đã chọn sang thư mục khác"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn dữ liệu cần di chuyển!")
            return
            
        # Lấy danh sách thư mục có sẵn (trừ thư mục hiện tại)
        try:
            folders = [f for f in os.listdir(self.data_dir) if os.path.isdir(os.path.join(self.data_dir, f))]
            folders = [f for f in folders if f != self.current_folder]
            folders.sort()
            
            if not folders:
                messagebox.showwarning("Cảnh báo", "Không có thư mục nào khác để di chuyển!")
                return
                
            # Tạo dialog chọn thư mục đích với giao diện đẹp
            move_window = tk.Toplevel(self.root)
            move_window.title("📦 Di chuyển dữ liệu")
            move_window.geometry("800x800")
            move_window.transient(self.root)
            move_window.grab_set()
            move_window.configure(bg=self.colors['bg_secondary'])
            
            # Center window
            move_window.update_idletasks()
            x = (move_window.winfo_screenwidth() // 2) - (800 // 2)
            y = (move_window.winfo_screenheight() // 2) - (800 // 2)
            move_window.geometry(f"800x800+{x}+{y}")
            
            # Main container
            main_container = ttk.Frame(move_window, style='Modern.TFrame')
            main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            
            # Header card
            header_card = ttk.Frame(main_container, style='Card.TFrame')
            header_card.pack(fill=tk.X, pady=(0, 20))
            
            # Title
            title_label = ttk.Label(header_card, text="📦 Di chuyển dữ liệu", style='Title.TLabel')
            title_label.pack(pady=(0, 10))
            
            # Info
            info_text = f"📊 Số dòng đã chọn: {len(selection)}\n📂 Từ thư mục: {self.current_folder}"
            ttk.Label(header_card, text=info_text, style='Modern.TLabel', 
                     font=('Segoe UI', 11, 'bold')).pack(anchor=tk.W, pady=(0, 10))
            
            # Destination selection card
            dest_card = ttk.Frame(main_container, style='Card.TFrame')
            dest_card.pack(fill=tk.X, pady=(0, 20))
            
            dest_title = ttk.Label(dest_card, text="🎯 Chọn thư mục đích", style='Subtitle.TLabel')
            dest_title.pack(anchor=tk.W, pady=(0, 15))
            
            dest_label = ttk.Label(dest_card, text="Thư mục đích:", style='Modern.TLabel')
            dest_label.pack(anchor=tk.W, pady=(0, 8))
            
            dest_folder_var = tk.StringVar()
            dest_combo = ttk.Combobox(dest_card, textvariable=dest_folder_var, values=folders, 
                                    width=40, state='readonly', style='Modern.TCombobox',
                                    font=('Segoe UI', 11))
            dest_combo.pack(fill=tk.X, pady=(0, 15))
            
            # Warning info
            warning_text = "⚠️ Dữ liệu sẽ được xóa khỏi thư mục hiện tại sau khi di chuyển"
            ttk.Label(dest_card, text=warning_text, style='Modern.TLabel', 
                     foreground=self.colors['danger'], font=('Segoe UI', 10, 'italic')).pack(anchor=tk.W)
            
            # Mode selection card
            mode_card = ttk.Frame(main_container, style='Card.TFrame')
            mode_card.pack(fill=tk.X, pady=(0, 20))
            
            mode_title = ttk.Label(mode_card, text="⚙️ Phạm vi di chuyển", style='Subtitle.TLabel')
            mode_title.pack(anchor=tk.W, pady=(0, 15))
            
            self.move_mode_var = tk.StringVar(value='all')
            
            # Mode options with better styling
            mode_options = [
                ('all', '📋 Toàn bộ (Link1 + Link2 + Link3)', 'Di chuyển tất cả links của mỗi record'),
                ('l1', '🔗 Chỉ Link 1', 'Chỉ di chuyển Link1, giữ lại Link2, Link3'),
                ('l2', '🔗 Chỉ Link 2', 'Chỉ di chuyển Link2, giữ lại Link1, Link3'),
                ('l3', '🔗 Chỉ Link 3', 'Chỉ di chuyển Link3, giữ lại Link1, Link2')
            ]
            
            for value, text, desc in mode_options:
                option_frame = ttk.Frame(mode_card)
                option_frame.pack(fill=tk.X, pady=5)
                
                radio = ttk.Radiobutton(option_frame, text=text, value=value, variable=self.move_mode_var,
                                      style='Modern.TRadiobutton')
                radio.pack(side=tk.LEFT)
                
                desc_label = ttk.Label(option_frame, text=desc, style='Modern.TLabel',
                                     foreground=self.colors['text_secondary'], font=('Segoe UI', 9, 'italic'))
                desc_label.pack(side=tk.LEFT, padx=(10, 0))

            # Buttons card
            button_card = ttk.Frame(main_container, style='Card.TFrame')
            button_card.pack(fill=tk.X)
            
            button_frame = ttk.Frame(button_card, style='Modern.TFrame')
            button_frame.pack(fill=tk.X)
            
            def confirm_move():
                dest_folder = dest_folder_var.get()
                if not dest_folder:
                    messagebox.showwarning("Cảnh báo", "Vui lòng chọn thư mục đích!")
                    return
                    
                if messagebox.askyesno("Xác nhận", 
                    f"Bạn có chắc chắn muốn di chuyển {len(selection)} dòng sang thư mục '{dest_folder}'?"):
                    self.perform_move(selection, dest_folder, self.move_mode_var.get())
                    move_window.destroy()
            
            # Buttons with better spacing
            ttk.Button(button_frame, text="✅ Xác nhận di chuyển", style='Primary.TButton',
                      command=confirm_move).pack(side=tk.LEFT, padx=(0, 15))
            ttk.Button(button_frame, text="❌ Hủy bỏ", style='Danger.TButton',
                      command=move_window.destroy).pack(side=tk.LEFT)
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tạo dialog di chuyển: {str(e)}")
            
    def perform_move(self, selection, dest_folder, mode='all'):
        """Thực hiện di chuyển dữ liệu với chế độ: all | l1 | l2 | l3 - Tối ưu tốc độ"""
        try:
            # Hiển thị cursor chờ
            self.tree.config(cursor="wait")
            self.root.update()
            
            # Lấy dữ liệu cần di chuyển - tối ưu với batch processing
            indices = [self.tree.index(item) for item in selection]
            indices.sort(reverse=True)  # Xóa từ cuối lên
            
            data_to_move = []
            items_to_remove = []
            
            # Xử lý batch để tăng tốc
            for idx in indices:
                rec = self.bm_data[idx]
                # Chuẩn hóa rec thành dict Link1..3
                if not isinstance(rec, dict):
                    rec = {'TypeBM': rec[0] if len(rec)>0 else '', 'ID': rec[1] if len(rec)>1 else '', 'BmID': rec[2] if len(rec)>2 else '', 'Link1': rec[3] if len(rec)>3 else '', 'Link2': '', 'Link3': '', 'Note': ''}
                
                if mode == 'all':
                    data_to_move.append({k: rec.get(k, '') for k in ['TypeBM','ID','BmID','Link1','Link2','Link3','Note']})
                    items_to_remove.append(idx)
                else:
                    # xác định index link
                    link_map = {'l1':'Link1','l2':'Link2','l3':'Link3'}
                    link_key = link_map.get(mode, 'Link1')
                    link_val = rec.get(link_key, '')
                    if link_val:
                        # record chỉ chứa 1 link được copy sang đích (ở Link1)
                        data_to_move.append({'TypeBM': rec.get('TypeBM',''), 'ID': rec.get('ID',''), 'BmID': rec.get('BmID',''), 'Link1': link_val, 'Link2': '', 'Link3': '', 'Note': rec.get('Note','')})
                        # loại bỏ link khỏi nguồn và dồn lên
                        links = [rec.get('Link1',''), rec.get('Link2',''), rec.get('Link3','')]
                        idx_map = {'l1':0,'l2':1,'l3':2}
                        rm_i = idx_map.get(mode,0)
                        # xóa vị trí rm_i và thêm '' ở cuối để giữ 3 phần tử
                        links.pop(rm_i)
                        links.append('')
                        rec['Link1'], rec['Link2'], rec['Link3'] = links[0], links[1], links[2]
                        # Nếu cả 3 link đều rỗng thì xóa bản ghi
                        if not any(links):
                            items_to_remove.append(idx)
                        else:
                            self.bm_data[idx] = rec
            
            # Xóa batch items
            for idx in items_to_remove:
                del self.bm_data[idx]
            
            # Lưu thư mục hiện tại
            self.save_json_db()
            
            # Tải dữ liệu thư mục đích - tối ưu I/O
            dest_path = os.path.join(self.data_dir, dest_folder, 'bm_data.json')
            dest_data = []
            if os.path.exists(dest_path):
                with open(dest_path, 'r', encoding='utf-8') as f:
                    dest_data = json.load(f)
            
            # Chuẩn hóa dest_data thành list[dict] - tối ưu với list comprehension
            normalized_dest = []
            for d in dest_data:
                if isinstance(d, dict):
                    normalized_dest.append({
                        'TypeBM': d.get('TypeBM',''), 'ID': d.get('ID',''), 'BmID': d.get('BmID',''),
                        'Link1': d.get('Link1', d.get('Link','')), 'Link2': d.get('Link2',''), 'Link3': d.get('Link3',''),
                        'Note': d.get('Note','')
                    })
                else:
                    if d and len(d) >= 4:
                        normalized_dest.append({'TypeBM': d[0], 'ID': d[1], 'BmID': d[2], 'Link1': d[3], 'Link2': '', 'Link3': '', 'Note': ''})
            dest_data = normalized_dest

            # Merge vào thư mục đích theo khóa và lấp slot link trống, tránh trùng - tối ưu với dict lookup
            key_to_idx = {(r['TypeBM'], r['ID'], r['BmID']): i for i, r in enumerate(dest_data)}
            for m in data_to_move:
                key = (m.get('TypeBM',''), m.get('ID',''), m.get('BmID',''))
                if key in key_to_idx:
                    base = dest_data[key_to_idx[key]]
                    for lk in ['Link1','Link2','Link3']:
                        val = m.get(lk, '')
                        if not val:
                            continue
                        if val in [base.get('Link1',''), base.get('Link2',''), base.get('Link3','')]:
                            continue
                        # nhét vào slot trống
                        if not base.get('Link1'): base['Link1'] = val; continue
                        if not base.get('Link2'): base['Link2'] = val; continue
                        if not base.get('Link3'): base['Link3'] = val; continue
                else:
                    dest_data.append({
                        'TypeBM': m.get('TypeBM',''), 'ID': m.get('ID',''), 'BmID': m.get('BmID',''),
                        'Link1': m.get('Link1',''), 'Link2': m.get('Link2',''), 'Link3': m.get('Link3',''),
                        'Note': m.get('Note','')
                    })
            
            # Lưu thư mục đích
            with open(dest_path, 'w', encoding='utf-8') as f:
                json.dump(dest_data, f, ensure_ascii=False, indent=2)
            
            # Cập nhật giao diện
            self.refresh_tree()
            self.update_folder_info()
            self.tree.config(cursor="")
            
            messagebox.showinfo("Thành công", 
                f"Đã di chuyển {len(data_to_move)} dòng sang thư mục '{dest_folder}'!")
                
        except Exception as e:
            self.tree.config(cursor="")
            messagebox.showerror("Lỗi", f"Không thể di chuyển dữ liệu: {str(e)}")

    def filter_links_by_bmid(self):
        """Lọc link theo danh sách BmID"""
        text = self.filter_bmid_text.get('1.0', tk.END).strip()
        if not text:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập danh sách BmID!")
            return
        bmid_list = [s.strip() for s in text.splitlines() if s.strip()]
        if not bmid_list:
            messagebox.showwarning("Cảnh báo", "Danh sách BmID trống!")
            return
        
        # Clear results
        self.list_link1.delete(0, tk.END)
        self.list_link2.delete(0, tk.END)
        
        # Filter logic (simplified version)
        found_links1 = []
        found_links2 = []
        
        for item in self.bm_data:
            if isinstance(item, dict):
                if item.get('BmID', '').strip() in bmid_list:
                    if item.get('Link1'):
                        found_links1.append(item.get('Link1'))
                    if item.get('Link2'):
                        found_links2.append(item.get('Link2'))
        
        # Add to lists
        for link in found_links1:
            self.list_link1.insert(tk.END, link)
        for link in found_links2:
            self.list_link2.insert(tk.END, link)
        
        self.filter_info_var.set(f"✅ Tìm thấy: Link1: {len(found_links1)} | Link2: {len(found_links2)}")

    def create_context_menu(self):
        """Tạo context menu cho Treeview"""
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="✅ Chọn tất cả", command=self.select_all)
        self.context_menu.add_command(label="🎯 Chọn theo điều kiện", command=self.show_select_menu)
        self.context_menu.add_command(label="📝 Nhập dữ liệu", command=self.open_bulk_modal)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="📋 Copy dữ liệu", command=self.open_copy_dialog)
        self.context_menu.add_command(label="📝 Thêm ghi chú", command=self.add_note_to_selected)
        self.context_menu.add_command(label="🗑️ Xóa đã chọn", command=self.delete_selected)
        self.context_menu.add_command(label="❌ Bỏ chọn tất cả", command=self.unselect_all)
        
        self.tree.bind("<Button-3>", self.show_context_menu)
        
    def show_context_menu(self, event):
        """Hiển thị context menu"""
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()

    def show_select_menu(self):
        """Hiển thị menu chọn dữ liệu với giao diện đẹp"""
        select_window = tk.Toplevel(self.root)
        select_window.title("🎯 Chọn dữ liệu theo điều kiện")
        select_window.geometry("800x800")
        select_window.transient(self.root)
        select_window.grab_set()
        select_window.configure(bg=self.colors['bg_secondary'])
        
        # Center window
        select_window.update_idletasks()
        x = (select_window.winfo_screenwidth() // 2) - (800 // 2)
        y = (select_window.winfo_screenheight() // 2) - (800 // 2)
        select_window.geometry(f"800x800+{x}+{y}")
        
        # Main container
        main_container = ttk.Frame(select_window, style='Modern.TFrame')
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header card
        header_card = ttk.Frame(main_container, style='Card.TFrame')
        header_card.pack(fill=tk.X, pady=(0, 20))
        
        # Title
        title_label = ttk.Label(header_card, text="🎯 Chọn dữ liệu theo điều kiện", style='Title.TLabel')
        title_label.pack(pady=(0, 10))
        
        # Info
        info_text = "Chọn dữ liệu theo các tiêu chí khác nhau để thao tác hàng loạt"
        ttk.Label(header_card, text=info_text, style='Modern.TLabel', 
                 font=('Segoe UI', 11, 'bold')).pack(anchor=tk.W, pady=(0, 10))
        
        # Selection options grid (2x2 layout)
        options_grid = ttk.Frame(main_container, style='Modern.TFrame')
        options_grid.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        options_grid.columnconfigure(0, weight=1)
        options_grid.columnconfigure(1, weight=1)
        options_grid.rowconfigure(0, weight=1)
        options_grid.rowconfigure(1, weight=1)
        
        # Type BM selection card (Top Left)
        type_card = ttk.Frame(options_grid, style='Card.TFrame')
        type_card.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10), pady=(0, 10))
        
        type_title = ttk.Label(type_card, text="📊 Chọn theo Type BM", style='Subtitle.TLabel')
        type_title.pack(anchor=tk.W, pady=(0, 15))
        
        type_info = ttk.Label(type_card, text="Nhập Type BM để chọn tất cả dòng có cùng loại:", 
                             style='Modern.TLabel', font=('Segoe UI', 10))
        type_info.pack(anchor=tk.W, pady=(0, 10))
        
        type_input_frame = ttk.Frame(type_card)
        type_input_frame.pack(fill=tk.X)
        
        self.type_select_var = tk.StringVar()
        type_entry = ttk.Entry(type_input_frame, textvariable=self.type_select_var, 
                              style='Modern.TEntry', width=30, font=('Segoe UI', 11))
        type_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        ttk.Button(type_input_frame, text="✅ Chọn", style='Success.TButton',
                  command=self.select_by_type).pack(side=tk.RIGHT)
        
        # ID selection card (Top Right)
        id_card = ttk.Frame(options_grid, style='Card.TFrame')
        id_card.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(10, 0), pady=(0, 10))
        
        id_title = ttk.Label(id_card, text="🆔 Chọn theo ID", style='Subtitle.TLabel')
        id_title.pack(anchor=tk.W, pady=(0, 15))
        
        id_info = ttk.Label(id_card, text="Nhập danh sách ID (mỗi ID một dòng):", 
                           style='Modern.TLabel', font=('Segoe UI', 10))
        id_info.pack(anchor=tk.W, pady=(0, 10))
        
        self.id_select_text = tk.Text(id_card, height=6, font=('Consolas', 10),
                                     relief='solid', borderwidth=2, padx=8, pady=6)
        self.id_select_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        ttk.Button(id_card, text="✅ Chọn theo ID", style='Success.TButton',
                  command=self.select_by_id).pack(anchor=tk.W)
        
        # BmID selection card (Bottom Left)
        bmid_card = ttk.Frame(options_grid, style='Card.TFrame')
        bmid_card.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10), pady=(10, 0))
        
        bmid_title = ttk.Label(bmid_card, text="🔢 Chọn theo BmID", style='Subtitle.TLabel')
        bmid_title.pack(anchor=tk.W, pady=(0, 15))
        
        bmid_info = ttk.Label(bmid_card, text="Nhập danh sách BmID (mỗi BmID một dòng):", 
                             style='Modern.TLabel', font=('Segoe UI', 10))
        bmid_info.pack(anchor=tk.W, pady=(0, 10))
        
        self.bmid_select_text = tk.Text(bmid_card, height=6, font=('Consolas', 10),
                                       relief='solid', borderwidth=2, padx=8, pady=6)
        self.bmid_select_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        ttk.Button(bmid_card, text="✅ Chọn theo BmID", style='Success.TButton',
                  command=self.select_by_bmid).pack(anchor=tk.W)
        
        # Link selection card (Bottom Right)
        link_card = ttk.Frame(options_grid, style='Card.TFrame')
        link_card.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(10, 0), pady=(10, 0))
        
        link_title = ttk.Label(link_card, text="🔗 Chọn theo Link", style='Subtitle.TLabel')
        link_title.pack(anchor=tk.W, pady=(0, 15))
        
        link_info = ttk.Label(link_card, text="Nhập danh sách Link (mỗi Link một dòng):", 
                             style='Modern.TLabel', font=('Segoe UI', 10))
        link_info.pack(anchor=tk.W, pady=(0, 10))
        
        self.link_select_text = tk.Text(link_card, height=6, font=('Consolas', 10),
                                       relief='solid', borderwidth=2, padx=8, pady=6)
        self.link_select_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        ttk.Button(link_card, text="✅ Chọn theo Link", style='Success.TButton',
                  command=self.select_by_link).pack(anchor=tk.W)
        
        # Close button card
        button_card = ttk.Frame(main_container, style='Card.TFrame')
        button_card.pack(fill=tk.X)
        
        ttk.Button(button_card, text="❌ Đóng", style='Danger.TButton',
                  command=select_window.destroy).pack()

    def select_by_type(self):
        """Chọn theo Type BM - Tối ưu tốc độ"""
        type_to_select = self.type_select_var.get().strip()
        if not type_to_select:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập Type BM!")
            return
            
        # Tắt cập nhật giao diện
        self.tree.config(cursor="wait")
        self.root.update()
        
        # Tìm tất cả items phù hợp trước
        matching_items = []
        tree_items = list(self.tree.get_children())
        
        for i, item in enumerate(self.bm_data):
            type_bm = item.get('TypeBM', '') if isinstance(item, dict) else (item[0] if len(item) > 0 else '')
            if type_bm.strip() == type_to_select and i < len(tree_items):
                matching_items.append(tree_items[i])
        
        # Chọn tất cả cùng lúc
        if matching_items:
            self.tree.selection_set(matching_items)
        
        # Cập nhật hiển thị một lần
        self.update_checkbox_display()
        self.tree.config(cursor="")
        
        messagebox.showinfo("Thành công", f"✅ Đã chọn {len(matching_items)} dòng có Type BM: {type_to_select}")

    def select_by_id(self):
        """Chọn theo danh sách ID - Tối ưu tốc độ"""
        ids_text = self.id_select_text.get('1.0', tk.END).strip()
        if not ids_text:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập danh sách ID!")
            return
            
        # Tắt cập nhật giao diện
        self.tree.config(cursor="wait")
        self.root.update()
        
        ids = set(id.strip() for id in ids_text.splitlines() if id.strip())
        matching_items = []
        tree_items = list(self.tree.get_children())
        
        for i, item in enumerate(self.bm_data):
            item_id = item.get('ID', '') if isinstance(item, dict) else (item[1] if len(item) > 1 else '')
            if item_id.strip() in ids and i < len(tree_items):
                matching_items.append(tree_items[i])
        
        # Chọn tất cả cùng lúc
        if matching_items:
            self.tree.selection_set(matching_items)
        
        # Cập nhật hiển thị một lần
        self.update_checkbox_display()
        self.tree.config(cursor="")
        
        messagebox.showinfo("Thành công", f"✅ Đã chọn {len(matching_items)} dòng theo ID")

    def select_by_bmid(self):
        """Chọn theo danh sách BmID - Tối ưu tốc độ"""
        bmids_text = self.bmid_select_text.get('1.0', tk.END).strip()
        if not bmids_text:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập danh sách BmID!")
            return
            
        # Tắt cập nhật giao diện
        self.tree.config(cursor="wait")
        self.root.update()
        
        bmids = set(bmid.strip() for bmid in bmids_text.splitlines() if bmid.strip())
        matching_items = []
        tree_items = list(self.tree.get_children())
        
        for i, item in enumerate(self.bm_data):
            bmid = item.get('BmID', '') if isinstance(item, dict) else (item[2] if len(item) > 2 else '')
            if bmid.strip() in bmids and i < len(tree_items):
                matching_items.append(tree_items[i])
        
        # Chọn tất cả cùng lúc
        if matching_items:
            self.tree.selection_set(matching_items)
        
        # Cập nhật hiển thị một lần
        self.update_checkbox_display()
        self.tree.config(cursor="")
        
        messagebox.showinfo("Thành công", f"✅ Đã chọn {len(matching_items)} dòng theo BmID")

    def select_by_link(self):
        """Chọn theo danh sách Link - Tối ưu tốc độ"""
        links_text = self.link_select_text.get('1.0', tk.END).strip()
        if not links_text:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập danh sách Link!")
            return
            
        # Tắt cập nhật giao diện
        self.tree.config(cursor="wait")
        self.root.update()
        
        links = set(link.strip() for link in links_text.splitlines() if link.strip())
        matching_items = []
        tree_items = list(self.tree.get_children())
        
        for i, item in enumerate(self.bm_data):
            if isinstance(item, dict):
                item_links = [item.get('Link1', ''), item.get('Link2', ''), item.get('Link3', '')]
            else:
                item_links = [item[3] if len(item) > 3 else '']
                
            if any(link in links for link in item_links if link) and i < len(tree_items):
                matching_items.append(tree_items[i])
        
        # Chọn tất cả cùng lúc
        if matching_items:
            self.tree.selection_set(matching_items)
        
        # Cập nhật hiển thị một lần
        self.update_checkbox_display()
        self.tree.config(cursor="")
        
        messagebox.showinfo("Thành công", f"✅ Đã chọn {len(matching_items)} dòng theo Link")

    def delete_selected(self):
        """Xóa các dòng đã chọn"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn dòng cần xóa!")
            return
            
        if messagebox.askyesno("Xác nhận", f"Bạn có chắc chắn muốn xóa {len(selection)} dòng đã chọn?"):
            indices = sorted([self.rowid_to_index.get(item, -1) for item in selection 
                            if self.rowid_to_index.get(item, -1) >= 0], reverse=True)
            
            for index in indices:
                del self.bm_data[index]
                
            self.refresh_tree()
            self.save_json_db()
            messagebox.showinfo("Thành công", f"✅ Đã xóa {len(selection)} dòng!")

    def select_all(self):
        """Chọn tất cả dòng - Tối ưu tốc độ"""
        all_items = self.tree.get_children()
        if not all_items:
            return
            
        # Tắt cập nhật giao diện trong quá trình chọn
        self.tree.config(cursor="wait")
        self.root.update()
        
        # Chọn tất cả items cùng lúc
        self.tree.selection_set(all_items)
        
        # Cập nhật hiển thị một lần
        self.update_checkbox_display()
        self.tree.config(cursor="")
        
        messagebox.showinfo("Thành công", f"✅ Đã chọn tất cả {len(all_items)} dòng!")

    def unselect_all(self):
        """Bỏ chọn tất cả"""
        self.tree.selection_remove(self.tree.selection())
        self.update_checkbox_display()

    def add_note_to_selected(self):
        """Thêm ghi chú cho các dòng đã chọn"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn ít nhất một dòng!")
            return
            
        note = simpledialog.askstring("Thêm ghi chú", "Nhập nội dung ghi chú:")
        if note is None:
            return
            
        note = note.strip()
        indices = []
        for item in selection:
            base_index = self.rowid_to_index.get(item, -1)
            if base_index >= 0:
                indices.append(base_index)
                
        for idx in indices:
            if isinstance(self.bm_data[idx], dict):
                self.bm_data[idx]['Note'] = note
            else:
                # Convert to dict format
                row = self.bm_data[idx]
                self.bm_data[idx] = {
                    'TypeBM': row[0] if len(row) > 0 else '',
                    'ID': row[1] if len(row) > 1 else '',
                    'BmID': row[2] if len(row) > 2 else '',
                    'Link1': row[3] if len(row) > 3 else '',
                    'Link2': '',
                    'Link3': '',
                    'Note': note,
                }
                
        self.refresh_tree()
        self.save_json_db()
        self.update_folder_info()
        messagebox.showinfo("Thành công", f"✅ Đã thêm ghi chú cho {len(indices)} dòng!")

    def open_copy_dialog(self):
        """Mở dialog copy với giao diện đẹp"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn ít nhất một dòng để copy!")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("📋 Copy dữ liệu")
        dialog.geometry("800x800")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.configure(bg=self.colors['bg_secondary'])
        
        # Center window
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (800 // 2)
        y = (dialog.winfo_screenheight() // 2) - (800 // 2)
        dialog.geometry(f"800x800+{x}+{y}")
        
        # Main container
        main_container = ttk.Frame(dialog, style='Modern.TFrame')
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header card
        header_card = ttk.Frame(main_container, style='Card.TFrame')
        header_card.pack(fill=tk.X, pady=(0, 20))
        
        # Title
        title_label = ttk.Label(header_card, text="📋 Cấu hình Copy", style='Title.TLabel')
        title_label.pack(pady=(0, 10))
        
        # Info
        info_text = f"📊 Số dòng đã chọn: {len(selection)}\n📋 Dữ liệu sẽ được copy vào clipboard"
        ttk.Label(header_card, text=info_text, style='Modern.TLabel', 
                 font=('Segoe UI', 11, 'bold')).pack(anchor=tk.W, pady=(0, 10))
        
        # Column mapping card
        mapping_card = ttk.Frame(main_container, style='Card.TFrame')
        mapping_card.pack(fill=tk.X, pady=(0, 20))
        
        mapping_title = ttk.Label(mapping_card, text="🔀 Ánh xạ cột → trường", style='Subtitle.TLabel')
        mapping_title.pack(anchor=tk.W, pady=(0, 15))
        
        fields = ('TypeBM', 'ID', 'BmID', 'Link1', 'Link2', 'Link3')
        self.map_vars = [tk.StringVar(value=('TypeBM','ID','BmID','Link1')[i] if i<4 else fields[i]) 
                        for i in range(4)]
        
        # Mapping grid
        mapping_grid = ttk.Frame(mapping_card)
        mapping_grid.pack(fill=tk.X)
        
        for i in range(4):
            row_frame = ttk.Frame(mapping_grid)
            row_frame.pack(fill=tk.X, pady=8)
            
            ttk.Label(row_frame, text=f"Cột {i+1}:", style='Modern.TLabel', 
                     font=('Segoe UI', 11, 'bold')).pack(side=tk.LEFT, padx=(0, 15))
            cb = ttk.Combobox(row_frame, textvariable=self.map_vars[i], values=fields, 
                            width=20, state='readonly', style='Modern.TCombobox',
                            font=('Segoe UI', 11))
            cb.pack(side=tk.LEFT, padx=(0, 20))
            
            # Description
            desc_text = f"Trường dữ liệu cho cột {i+1}"
            ttk.Label(row_frame, text=desc_text, style='Modern.TLabel',
                     foreground=self.colors['text_secondary'], font=('Segoe UI', 9, 'italic')).pack(side=tk.LEFT, padx=(10, 0))
        
        # Delimiter card
        delim_card = ttk.Frame(main_container, style='Card.TFrame')
        delim_card.pack(fill=tk.X, pady=(0, 20))
        
        delim_title = ttk.Label(delim_card, text="🔀 Dấu phân cách", style='Subtitle.TLabel')
        delim_title.pack(anchor=tk.W, pady=(0, 15))
        
        delim_info = ttk.Label(delim_card, text="Ký tự để phân tách các trường trong mỗi dòng:", 
                              style='Modern.TLabel', font=('Segoe UI', 10))
        delim_info.pack(anchor=tk.W, pady=(0, 10))
        
        self.delim_var = tk.StringVar(value='|')
        delim_entry = ttk.Entry(delim_card, textvariable=self.delim_var, 
                               style='Modern.TEntry', width=15, font=('Segoe UI', 12))
        delim_entry.pack(anchor=tk.W, pady=(0, 10))
        
        # Examples
        examples_text = "Ví dụ: | (pipe), , (comma), ; (semicolon), \\t (tab)"
        ttk.Label(delim_card, text=examples_text, style='Modern.TLabel',
                 foreground=self.colors['text_secondary'], font=('Segoe UI', 9, 'italic')).pack(anchor=tk.W)
        
        # Buttons card
        button_card = ttk.Frame(main_container, style='Card.TFrame')
        button_card.pack(fill=tk.X)
        
        button_frame = ttk.Frame(button_card, style='Modern.TFrame')
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="📋 Copy ngay", style='Primary.TButton',
                  command=lambda: self.perform_copy(dialog)).pack(side=tk.LEFT, padx=(0, 15))
        ttk.Button(button_frame, text="❌ Đóng", style='Danger.TButton',
                  command=dialog.destroy).pack(side=tk.LEFT)

    def perform_copy(self, dialog):
        """Thực hiện copy dữ liệu"""
        mapping = [v.get() for v in self.map_vars]
        if len(set(mapping)) != 4:
            messagebox.showerror("Lỗi", "Ánh xạ 4 cột phải là 4 trường khác nhau!")
            return
            
        delim = self.delim_var.get()
        if not delim:
            messagebox.showerror("Lỗi", "Vui lòng nhập dấu phân cách!")
            return
            
        selection = self.tree.selection()
        lines = []
        
        for item in selection:
            base_index = self.rowid_to_index.get(item, -1)
            if base_index >= 0 and base_index < len(self.bm_data):
                rec = self.bm_data[base_index]
                if not isinstance(rec, dict):
                    rec = {
                        'TypeBM': rec[0] if len(rec) > 0 else '',
                        'ID': rec[1] if len(rec) > 1 else '',
                        'BmID': rec[2] if len(rec) > 2 else '',
                        'Link1': rec[3] if len(rec) > 3 else '',
                        'Link2': '',
                        'Link3': '',
                    }
                parts = [str(rec.get(field, '')) for field in mapping]
                lines.append(delim.join(parts))
        
        text = "\n".join(lines)
        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
            self.root.update()
            messagebox.showinfo("Thành công", f"✅ Đã copy {len(lines)} dòng vào clipboard!")
            dialog.destroy()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể copy: {str(e)}")

    def load_json_db(self):
        """Tải dữ liệu từ JSON DB"""
        try:
            if os.path.exists(self.db_path):
                with open(self.db_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                normalized = []
                for item in data:
                    if not isinstance(item, dict):
                        continue
                    normalized.append({
                        'TypeBM': str(item.get('TypeBM', '')).strip(),
                        'ID': str(item.get('ID', '')).strip(),
                        'BmID': str(item.get('BmID', '')).strip(),
                        'Link1': str(item.get('Link1', item.get('Link', ''))).strip(),
                        'Link2': str(item.get('Link2', '')).strip(),
                        'Link3': str(item.get('Link3', '')).strip(),
                        'Note': str(item.get('Note', '')).strip()
                    })
                self.bm_data = normalized
            else:
                self.bm_data = []
                
            self.refresh_tree()
            self.update_status_bar()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải DB JSON: {str(e)}")
            self.bm_data = []
            self.refresh_tree()
            self.update_status_bar()

    def save_json_db(self):
        """Lưu dữ liệu vào JSON DB"""
        try:
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            with open(self.db_path, 'w', encoding='utf-8') as f:
                json.dump(self.bm_data, f, ensure_ascii=False, indent=2)
            self.update_status_bar()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể lưu DB JSON: {str(e)}")

    def open_bulk_modal(self):
        """Mở cửa sổ nhập dữ liệu hàng loạt với giao diện đẹp"""
        if hasattr(self, 'bulk_modal') and self.bulk_modal.winfo_exists():
            self.bulk_modal.deiconify()
            self.bulk_modal.lift()
            return
            
        self.bulk_modal = tk.Toplevel(self.root)
        self.bulk_modal.title("📝 Nhập dữ liệu hàng loạt")
        self.bulk_modal.geometry("800x600")
        self.bulk_modal.transient(self.root)
        self.bulk_modal.grab_set()
        self.bulk_modal.configure(bg=self.colors['bg_secondary'])
        
        container = ttk.Frame(self.bulk_modal, style='Card.TFrame')
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        title = ttk.Label(container, text="📝 Nhập dữ liệu hàng loạt", style='Title.TLabel')
        title.pack(pady=(0, 20))
        
        # Column mapping
        mapping_frame = ttk.LabelFrame(container, text="🔀 Ánh xạ cột → trường", padding=15)
        mapping_frame.pack(fill=tk.X, pady=(0, 15))
        
        mapping_values = ('TypeBM', 'ID', 'BmID', 'Link1')
        self.bulk_map_vars = [tk.StringVar(value=mapping_values[i]) for i in range(4)]
        
        maps_grid = ttk.Frame(mapping_frame)
        maps_grid.pack(fill=tk.X)
        
        for i in range(4):
            ttk.Label(maps_grid, text=f"Cột {i+1}:", style='Modern.TLabel').grid(
                row=0, column=i*2, sticky=tk.W, padx=(0, 5))
            cb = ttk.Combobox(maps_grid, textvariable=self.bulk_map_vars[i], 
                            values=mapping_values, width=12, state='readonly', style='Modern.TCombobox')
            cb.grid(row=0, column=i*2+1, padx=(0, 15))
        
        # Delimiter
        delim_frame = ttk.Frame(mapping_frame)
        delim_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Label(delim_frame, text="Dấu phân cách:", style='Modern.TLabel').pack(side=tk.LEFT)
        self.bulk_delim_var = tk.StringVar(value='|')
        ttk.Entry(delim_frame, textvariable=self.bulk_delim_var, width=8, 
                 style='Modern.TEntry').pack(side=tk.LEFT, padx=(10, 0))
        
        # Data input
        data_frame = ttk.LabelFrame(container, text="📋 Dữ liệu (mỗi dòng một bản ghi)", padding=15)
        data_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        self.bulk_text = tk.Text(data_frame, height=15, font=('Consolas', 10),
                               relief='solid', borderwidth=2, padx=10, pady=8)
        self.bulk_text.pack(fill=tk.BOTH, expand=True)
        
        # Buttons
        button_frame = ttk.Frame(container)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="📥 Nhập hàng loạt", style='Primary.TButton',
                  command=self.bulk_add).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="🧹 Xóa nội dung", style='Accent.TButton',
                  command=lambda: self.bulk_text.delete('1.0', tk.END)).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="❌ Đóng", style='Danger.TButton',
                  command=self.bulk_modal.destroy).pack(side=tk.LEFT)

    def bulk_add(self):
        """Nhập dữ liệu hàng loạt"""
        mapping = [v.get() for v in self.bulk_map_vars]
        if len(set(mapping)) != 4:
            messagebox.showerror("Lỗi", "Ánh xạ 4 cột phải là 4 trường khác nhau!")
            return
            
        delim = self.bulk_delim_var.get()
        if not delim:
            messagebox.showerror("Lỗi", "Vui lòng nhập dấu phân cách!")
            return
            
        text = self.bulk_text.get('1.0', tk.END).strip()
        if not text:
            messagebox.showerror("Lỗi", "Vui lòng nhập dữ liệu!")
            return
        
        # Create key index for duplicate checking
        key_to_index = {}
        for idx, it in enumerate(self.bm_data):
            if isinstance(it, dict):
                key_to_index[(it.get('TypeBM',''), it.get('ID',''), it.get('BmID',''))] = idx
            else:
                if len(it) >= 3:
                    key_to_index[(it[0], it[1], it[2])] = idx
        
        added = 0
        skipped_dup = 0
        skipped_invalid = 0
        
        for raw_line in text.splitlines():
            line = raw_line.strip()
            if not line:
                continue
                
            parts = line.split(delim)
            if len(parts) < 4:
                skipped_invalid += 1
                continue
                
            parts = [p.strip() for p in parts[:6]]  # Allow up to 6 columns
            record = {}
            
            try:
                for idx, field_name in enumerate(mapping):
                    record[field_name] = parts[idx]
                    
                # Ensure all required keys
                record = {
                    'TypeBM': record.get('TypeBM', ''),
                    'ID': record.get('ID', ''),
                    'BmID': record.get('BmID', ''),
                    'Link1': parts[3] if len(parts) > 3 else record.get('Link1',''),
                    'Link2': parts[4] if len(parts) > 4 else '',
                    'Link3': parts[5] if len(parts) > 5 else '',
                    'Note': ''
                }
            except Exception:
                skipped_invalid += 1
                continue
            
            # Check required fields
            if not record['TypeBM'] or not record['ID'] or not record['BmID'] or not record['Link1']:
                skipped_invalid += 1
                continue
            
            key = (record['TypeBM'], record['ID'], record['BmID'])
            if key in key_to_index:
                # Merge links into existing record
                i = key_to_index[key]
                if isinstance(self.bm_data[i], dict):
                    base = self.bm_data[i]
                else:
                    base = {
                        'TypeBM': self.bm_data[i][0], 
                        'ID': self.bm_data[i][1], 
                        'BmID': self.bm_data[i][2], 
                        'Link1': self.bm_data[i][3] if len(self.bm_data[i])>3 else '', 
                        'Link2': '', 
                        'Link3': '',
                        'Note': ''
                    }
                
                # Merge unique links
                for ln_key in ['Link1','Link2','Link3']:
                    new_link = record.get(ln_key, '')
                    if new_link and new_link not in [base.get('Link1',''), base.get('Link2',''), base.get('Link3','')]:
                        # Find empty slot
                        for slot in ['Link1','Link2','Link3']:
                            if not base.get(slot):
                                base[slot] = new_link
                                break
                                
                self.bm_data[i] = base
                skipped_dup += 1
            else:
                self.bm_data.append(record)
                key_to_index[key] = len(self.bm_data) - 1
                added += 1
        
        self.refresh_tree()
        self.save_json_db()
        self.update_folder_info()
        
        result_msg = f"✅ Thêm mới: {added}\n⚠️ Trùng: {skipped_dup}\n❌ Lỗi/thiếu dữ liệu: {skipped_invalid}"
        messagebox.showinfo("Kết quả nhập dữ liệu", result_msg)

    def refresh_tree(self, data=None):
        """Làm mới Treeview theo dữ liệu hiện có."""
        # Xóa cũ
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Reset mapping
        self.rowid_to_index = {}
        # Đổ dữ liệu
        data = data or self.bm_data
        for i, item in enumerate(data):
            if isinstance(item, dict):
                values = [
                    i + 1,
                    '⬜',
                    item.get('TypeBM', ''),
                    item.get('ID', ''),
                    item.get('BmID', ''),
                    self.current_folder,
                    item.get('Note', ''),
                    item.get('Link1', ''),
                    item.get('Link2', ''),
                    item.get('Link3', ''),
                ]
            else:
                link1 = item[3] if len(item) > 3 else ''
                values = [
                    i + 1, '⬜',
                    item[0] if len(item) > 0 else '',
                    item[1] if len(item) > 1 else '',
                    item[2] if len(item) > 2 else '',
                    self.current_folder,
                    '',
                    link1,
                    '',
                    ''
                ]
            tag = 'row_even' if (i % 2) == 0 else 'row_odd'
            row_id = self.tree.insert('', 'end', values=values, tags=(tag,))
            try:
                base_index = i if data is self.bm_data else self.bm_data.index(item)
            except Exception:
                base_index = i
            self.rowid_to_index[row_id] = base_index
        self.update_checkbox_display()
        self.update_status_bar()

    def update_checkbox_display(self):
        """Đồng bộ cột 'Chọn' với selection hiện tại."""
        items = self.tree.get_children()
        selected = set(self.tree.selection())
        for it in items:
            vals = list(self.tree.item(it, 'values'))
            if len(vals) >= 2:
                vals[1] = '✅' if it in selected else '⬜'
                self.tree.item(it, values=vals)
        self.update_status_bar()

    def update_status_bar(self):
        """Cập nhật thanh trạng thái Tổng | Đã chọn."""
        try:
            total = len(self.bm_data)
            selected = len(self.tree.selection())
            self.status_var.set(f"Tổng: {total} | Đã chọn: {selected}")
        except Exception:
            pass

    def on_select(self, event=None):
        """Khi selection thay đổi, cập nhật checkbox và status."""
        self.update_checkbox_display()
        self.update_status_bar()

    def on_tree_click(self, event):
        """Xử lý click: toggle checkbox ở cột 2, lưu cell hiện tại."""
        region = self.tree.identify_region(event.x, event.y)
        column = self.tree.identify_column(event.x)
        row_id = self.tree.identify_row(event.y)
        if region == 'cell' and column == '#2':
            # Toggle selection như checkbox
            if row_id:
                if row_id in self.tree.selection():
                    self.tree.selection_remove(row_id)
                else:
                    self.tree.selection_add(row_id)
                self.update_checkbox_display()
            return 'break'
        # Lưu cell để copy/sửa
        self.current_cell = (row_id, column)
        return

    def on_cell_double_click(self, event):
        """Cho phép sửa trực tiếp một số cột."""
        row_id = self.tree.identify_row(event.y)
        column = self.tree.identify_column(event.x)
        if not row_id or not column:
            return
        col_index = int(column.replace('#', '')) - 1
        # Không cho sửa các cột STT(0), Chọn(1), Thư mục(5)
        if col_index in (0, 1, 5):
            return
        bbox = self.tree.bbox(row_id, column)
        if not bbox:
            return
        x, y, w, h = bbox
        old_values = list(self.tree.item(row_id, 'values'))
        old_text = old_values[col_index]
        editor = ttk.Entry(self.tree)
        editor.insert(0, old_text)
        editor.select_range(0, tk.END)
        editor.focus_set()
        editor.place(x=x, y=y, width=w, height=h)

        def finish_edit(save):
            new_text = editor.get()
            editor.destroy()
            if not save or new_text == old_text:
                return
            # Cập nhật tree
            old_values[col_index] = new_text
            self.tree.item(row_id, values=old_values)
            # Ánh xạ về dữ liệu
            data_index = self.rowid_to_index.get(row_id, -1)
            if 0 <= data_index < len(self.bm_data):
                # Đảm bảo record là dict chuẩn
                rec = self.bm_data[data_index]
                if not isinstance(rec, dict):
                    rec = {
                        'TypeBM': rec[0] if len(rec) > 0 else '',
                        'ID': rec[1] if len(rec) > 1 else '',
                        'BmID': rec[2] if len(rec) > 2 else '',
                        'Link1': rec[3] if len(rec) > 3 else '',
                        'Link2': '',
                        'Link3': '',
                        'Note': ''
                    }
                key_map = {2: 'TypeBM', 3: 'ID', 4: 'BmID', 6: 'Note', 7: 'Link1', 8: 'Link2', 9: 'Link3'}
                field = key_map.get(col_index)
                if field:
                    rec[field] = new_text
                    self.bm_data[data_index] = rec
                    self.save_json_db()
                    self.update_folder_info()
                    self.update_status_bar()

        editor.bind('<Return>', lambda e: finish_edit(True))
        editor.bind('<Escape>', lambda e: finish_edit(False))
        editor.bind('<FocusOut>', lambda e: finish_edit(True))

    def copy_cell(self, event=None):
        """Copy nội dung ô hiện tại (Ctrl+C)."""
        row_id, column = self.current_cell
        if not row_id or not column:
            return
        col_index = int(column.replace('#', '')) - 1
        values = self.tree.item(row_id, 'values')
        if not values or col_index < 0 or col_index >= len(values):
            return
        text = str(values[col_index])
        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
            self.root.update()
        except Exception:
            pass

    def sort_by_column(self, column_id):
        """Sắp xếp tăng/giảm theo một cột; giữ lại STT mới."""
        items = self.tree.get_children('')
        if not items:
            return
        try:
            col_index = self.columns.index(column_id)
        except ValueError:
            return
        if column_id == 'Chọn':
            return
        rows = []
        for it in items:
            vals = self.tree.item(it, 'values')
            key = str(vals[col_index]) if col_index < len(vals) else ''
            rows.append((key.lower(), it))
        ascending = not self.sort_directions.get(column_id, True)
        self.sort_directions[column_id] = ascending
        rows.sort(key=lambda r: r[0])
        if not ascending:
            rows.reverse()
        for idx, (_, it) in enumerate(rows):
            self.tree.move(it, '', idx)
        for idx, it in enumerate(self.tree.get_children('')):
            vals = list(self.tree.item(it, 'values'))
            if len(vals) > 0:
                vals[0] = idx + 1
                self.tree.item(it, values=vals)
        self.update_checkbox_display()
        self.update_status_bar()

    def export_csv(self):
        """Export CSV với các cột Link1-3."""
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(['TypeBM', 'ID', 'BmID', 'Link1', 'Link2', 'Link3', 'Note'])
                    for item in self.bm_data:
                        if isinstance(item, dict):
                            writer.writerow([
                                item.get('TypeBM', ''), item.get('ID', ''), item.get('BmID', ''),
                                item.get('Link1', ''), item.get('Link2', ''), item.get('Link3', ''),
                                item.get('Note', '')
                            ])
                        else:
                            writer.writerow([
                                item[0] if len(item) > 0 else '',
                                item[1] if len(item) > 1 else '',
                                item[2] if len(item) > 2 else '',
                                item[3] if len(item) > 3 else '',
                                '', '', ''
                            ])
                messagebox.showinfo("Thành công", f"✅ Đã export file: {filename}")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể export file: {str(e)}")

    def import_csv(self):
        """Import CSV, hỗ trợ Link1-3 và Link cũ."""
        filename = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    rows = list(reader)
                imported = []
                for r in rows:
                    # Hỗ trợ header cũ 'Link'
                    link1 = r.get('Link1') or r.get('Link') or ''
                    rec = {
                        'TypeBM': r.get('TypeBM', ''),
                        'ID': r.get('ID', ''),
                        'BmID': r.get('BmID', ''),
                        'Link1': link1,
                        'Link2': r.get('Link2', ''),
                        'Link3': r.get('Link3', ''),
                        'Note': r.get('Note', ''),
                    }
                    if any([rec['TypeBM'], rec['ID'], rec['BmID'], rec['Link1'], rec['Link2'], rec['Link3']]):
                        imported.append(rec)
                if not imported:
                    messagebox.showwarning("Cảnh báo", "File CSV không có dữ liệu hợp lệ!")
                    return
                if messagebox.askyesno("Xác nhận", "Thêm vào dữ liệu hiện tại?"):
                    self.bm_data.extend(imported)
                else:
                    self.bm_data = imported
                self.refresh_tree()
                self.save_json_db()
                messagebox.showinfo("Thành công", f"✅ Đã import file: {filename}")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể import file: {str(e)}")

    def show_stats(self):
        """(Đã bỏ theo yêu cầu)"""
        messagebox.showinfo("Thông tin", "Chức năng Thống kê đã được ẩn.")


def main():
    root = tk.Tk()
    app = BMManager(root)
    root.mainloop()


if __name__ == "__main__":
    main()