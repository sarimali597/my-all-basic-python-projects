import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import barcode
from barcode.writer import ImageWriter
from PIL import Image, ImageTk, ImageDraw, ImageFont
import io
import datetime
import os
from pathlib import Path
import json

class InventoryDatabase:
    def __init__(self):
        self.conn = sqlite3.connect('garments_inventory.db')
        self.create_tables()
    
    def create_tables(self):
        cursor = self.conn.cursor()
        
        # Products table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                barcode TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                category TEXT,
                size TEXT,
                color TEXT,
                cost_price REAL,
                selling_price REAL,
                stock_quantity INTEGER DEFAULT 0,
                min_stock_level INTEGER DEFAULT 5,
                date_added TEXT,
                last_updated TEXT
            )
        ''')
        
        # Sales table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                barcode TEXT,
                product_name TEXT,
                quantity INTEGER,
                original_price REAL,
                discount_price REAL,
                final_price REAL,
                sale_date TEXT,
                FOREIGN KEY (barcode) REFERENCES products (barcode)
            )
        ''')
        
        # Returns table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS returns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                barcode TEXT,
                product_name TEXT,
                quantity INTEGER,
                reason TEXT,
                return_date TEXT,
                sale_id INTEGER,
                FOREIGN KEY (barcode) REFERENCES products (barcode)
            )
        ''')
        
        # Exchanges table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS exchanges (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                old_barcode TEXT,
                new_barcode TEXT,
                old_product TEXT,
                new_product TEXT,
                exchange_date TEXT
            )
        ''')
        
        self.conn.commit()
    
    def get_next_barcode(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT MAX(CAST(barcode AS INTEGER)) FROM products WHERE LENGTH(barcode) = 4')
        result = cursor.fetchone()[0]
        if result:
            return str(int(result) + 1).zfill(4)
        return '1001'
    
    def add_product(self, data):
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO products (barcode, name, category, size, color, cost_price, 
                                    selling_price, stock_quantity, min_stock_level, 
                                    date_added, last_updated)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', data)
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def update_product(self, barcode, data):
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE products 
            SET name=?, category=?, size=?, color=?, cost_price=?, 
                selling_price=?, stock_quantity=?, min_stock_level=?, last_updated=?
            WHERE barcode=?
        ''', (*data, barcode))
        self.conn.commit()
    
    def delete_product(self, barcode):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM products WHERE barcode=?', (barcode,))
        self.conn.commit()
    
    def get_product(self, barcode):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM products WHERE barcode=?', (barcode,))
        return cursor.fetchone()
    
    def get_all_products(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM products ORDER BY last_updated DESC')
        return cursor.fetchall()
    
    def search_products(self, query):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM products 
            WHERE name LIKE ? OR barcode LIKE ? OR category LIKE ?
        ''', (f'%{query}%', f'%{query}%', f'%{query}%'))
        return cursor.fetchall()
    
    def add_sale(self, data):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO sales (barcode, product_name, quantity, original_price, 
                             discount_price, final_price, sale_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', data)
        
        # Update stock
        cursor.execute('''
            UPDATE products SET stock_quantity = stock_quantity - ? 
            WHERE barcode = ?
        ''', (data[2], data[0]))
        self.conn.commit()
    
    def add_return(self, data):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO returns (barcode, product_name, quantity, reason, return_date, sale_id)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', data)
        
        # Update stock
        cursor.execute('''
            UPDATE products SET stock_quantity = stock_quantity + ? 
            WHERE barcode = ?
        ''', (data[2], data[0]))
        self.conn.commit()
    
    def add_exchange(self, data):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO exchanges (old_barcode, new_barcode, old_product, new_product, exchange_date)
            VALUES (?, ?, ?, ?, ?)
        ''', data)
        
        # Update stocks
        cursor.execute('UPDATE products SET stock_quantity = stock_quantity + 1 WHERE barcode = ?', (data[0],))
        cursor.execute('UPDATE products SET stock_quantity = stock_quantity - 1 WHERE barcode = ?', (data[1],))
        self.conn.commit()

class BarcodeGenerator:
    @staticmethod
    def generate_barcode(code, product_name, price):
        # Generate barcode image
        EAN = barcode.get_barcode_class('code128')
        ean = EAN(code, writer=ImageWriter())
        buffer = io.BytesIO()
        ean.write(buffer, options={'write_text': False, 'module_height': 8, 'module_width': 0.2})
        barcode_img = Image.open(buffer)
        
        # Create label for thermal printer (32mm x 23mm = ~121px x 87px at 96 DPI)
        # Using 3 columns: barcode center, product left, price right
        label_width = 380
        label_height = 280
        label = Image.new('RGB', (label_width, label_height), 'white')
        draw = ImageDraw.Draw(label)
        
        # Resize barcode
        barcode_img = barcode_img.resize((label_width - 40, 100))
        label.paste(barcode_img, (20, 20))
        
        # Try to load font, fallback to default
        try:
            font_large = ImageFont.truetype("arial.ttf", 24)
            font_medium = ImageFont.truetype("arial.ttf", 20)
            font_small = ImageFont.truetype("arial.ttf", 16)
        except:
            font_large = ImageFont.load_default()
            font_medium = ImageFont.load_default()
            font_small = ImageFont.load_default()
        
        # Product name (left column)
        product_short = product_name[:20] + '...' if len(product_name) > 20 else product_name
        draw.text((20, 130), product_short, fill='black', font=font_medium)
        
        # Barcode number (center)
        draw.text((label_width//2 - 30, 170), code, fill='black', font=font_large)
        
        # Price (right column, large)
        price_text = f"Rs. {price:.0f}"
        draw.text((label_width - 150, 220), price_text, fill='black', font=font_large)
        
        return label

class InventoryManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Garments Retail Inventory Management System")
        self.root.geometry("1400x800")
        self.root.configure(bg='#1a1a2e')
        
        self.db = InventoryDatabase()
        self.current_scan = ""
        
        # Style configuration
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_styles()
        
        self.create_widgets()
        self.load_products()
        
        # Bind barcode scanner input
        self.root.bind('<Key>', self.on_barcode_scan)
    
    def configure_styles(self):
        # Configure custom styles
        self.style.configure('TNotebook', background='#1a1a2e', borderwidth=0)
        self.style.configure('TNotebook.Tab', background='#16213e', foreground='white', 
                           padding=[20, 10], font=('Arial', 11, 'bold'))
        self.style.map('TNotebook.Tab', background=[('selected', '#0f3460')], 
                      foreground=[('selected', '#00d4ff')])
        
        self.style.configure('Treeview', background='#16213e', foreground='white', 
                           fieldbackground='#16213e', borderwidth=0, font=('Arial', 10))
        self.style.configure('Treeview.Heading', background='#0f3460', foreground='white', 
                           font=('Arial', 11, 'bold'))
        self.style.map('Treeview', background=[('selected', '#00d4ff')], 
                      foreground=[('selected', 'black')])
    
    def create_widgets(self):
        # Main container
        main_container = tk.Frame(self.root, bg='#1a1a2e')
        main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Header
        header = tk.Frame(main_container, bg='#0f3460', height=80)
        header.pack(fill='x', pady=(0, 10))
        header.pack_propagate(False)
        
        tk.Label(header, text="🏪 GARMENTS INVENTORY SYSTEM", 
                font=('Arial', 24, 'bold'), bg='#0f3460', fg='#00d4ff').pack(pady=20)
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill='both', expand=True)
        
        # Create tabs
        self.create_inventory_tab()
        self.create_pos_tab()
        self.create_returns_tab()
        self.create_exchange_tab()
        self.create_reports_tab()
    
    def create_inventory_tab(self):
        tab = tk.Frame(self.notebook, bg='#1a1a2e')
        self.notebook.add(tab, text='📦 Inventory')
        
        # Top controls
        controls = tk.Frame(tab, bg='#1a1a2e')
        controls.pack(fill='x', padx=10, pady=10)
        
        # Search
        tk.Label(controls, text="Search:", bg='#1a1a2e', fg='white', 
                font=('Arial', 11)).pack(side='left', padx=5)
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(controls, textvariable=self.search_var, width=30, 
                               font=('Arial', 11), bg='#16213e', fg='white', 
                               insertbackground='white')
        search_entry.pack(side='left', padx=5)
        self.search_var.trace('w', lambda *args: self.search_products())
        
        # Buttons
        btn_style = {'font': ('Arial', 10, 'bold'), 'bg': '#0f3460', 'fg': 'white', 
                    'activebackground': '#00d4ff', 'activeforeground': 'black', 
                    'relief': 'flat', 'cursor': 'hand2', 'padx': 15, 'pady': 8}
        
        tk.Button(controls, text="➕ Add Product", command=self.add_product_dialog, 
                 **btn_style).pack(side='left', padx=5)
        tk.Button(controls, text="✏️ Edit Product", command=self.edit_product_dialog, 
                 **btn_style).pack(side='left', padx=5)
        tk.Button(controls, text="🗑️ Delete Product", command=self.delete_product, 
                 **btn_style).pack(side='left', padx=5)
        tk.Button(controls, text="🖨️ Print Barcode", command=self.print_barcode, 
                 **btn_style).pack(side='left', padx=5)
        tk.Button(controls, text="🔄 Refresh", command=self.load_products, 
                 **btn_style).pack(side='left', padx=5)
        
        # Products table
        table_frame = tk.Frame(tab, bg='#1a1a2e')
        table_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        scrollbar_y = ttk.Scrollbar(table_frame, orient='vertical')
        scrollbar_x = ttk.Scrollbar(table_frame, orient='horizontal')
        
        self.products_tree = ttk.Treeview(table_frame, columns=(
            'Barcode', 'Name', 'Category', 'Size', 'Color', 'Cost', 'Price', 'Stock', 'Min Stock'
        ), show='headings', yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        scrollbar_y.config(command=self.products_tree.yview)
        scrollbar_x.config(command=self.products_tree.xview)
        
        # Configure columns
        columns = {
            'Barcode': 100, 'Name': 200, 'Category': 120, 'Size': 80, 
            'Color': 100, 'Cost': 100, 'Price': 100, 'Stock': 80, 'Min Stock': 100
        }
        
        for col, width in columns.items():
            self.products_tree.heading(col, text=col)
            self.products_tree.column(col, width=width)
        
        self.products_tree.pack(side='left', fill='both', expand=True)
        scrollbar_y.pack(side='right', fill='y')
        scrollbar_x.pack(side='bottom', fill='x')
        
        self.products_tree.bind('<Double-1>', lambda e: self.edit_product_dialog())
    
    def create_pos_tab(self):
        tab = tk.Frame(self.notebook, bg='#1a1a2e')
        self.notebook.add(tab, text='💰 Point of Sale')
        
        # Left panel - Cart
        left_panel = tk.Frame(tab, bg='#1a1a2e')
        left_panel.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        
        tk.Label(left_panel, text="Shopping Cart", font=('Arial', 16, 'bold'), 
                bg='#1a1a2e', fg='#00d4ff').pack(pady=10)
        
        # Cart table
        cart_frame = tk.Frame(left_panel, bg='#1a1a2e')
        cart_frame.pack(fill='both', expand=True)
        
        self.cart_tree = ttk.Treeview(cart_frame, columns=(
            'Barcode', 'Product', 'Qty', 'Price', 'Discount', 'Total'
        ), show='headings', height=15)
        
        for col in ['Barcode', 'Product', 'Qty', 'Price', 'Discount', 'Total']:
            self.cart_tree.heading(col, text=col)
            self.cart_tree.column(col, width=120)
        
        scrollbar = ttk.Scrollbar(cart_frame, orient='vertical', command=self.cart_tree.yview)
        self.cart_tree.configure(yscrollcommand=scrollbar.set)
        
        self.cart_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Right panel - Controls
        right_panel = tk.Frame(tab, bg='#16213e', width=400)
        right_panel.pack(side='right', fill='y', padx=10, pady=10)
        right_panel.pack_propagate(False)
        
        tk.Label(right_panel, text="Scan/Enter Barcode", font=('Arial', 12, 'bold'), 
                bg='#16213e', fg='white').pack(pady=10)
        
        self.barcode_entry = tk.Entry(right_panel, font=('Arial', 16), bg='#0f3460', 
                                      fg='white', insertbackground='white', justify='center')
        self.barcode_entry.pack(pady=10, padx=20, fill='x')
        self.barcode_entry.bind('<Return>', self.add_to_cart)
        self.barcode_entry.focus()
        
        btn_style = {'font': ('Arial', 11, 'bold'), 'bg': '#0f3460', 'fg': 'white', 
                    'activebackground': '#00d4ff', 'activeforeground': 'black', 
                    'relief': 'flat', 'cursor': 'hand2', 'pady': 10}
        
        tk.Button(right_panel, text="➕ Add to Cart", command=self.add_to_cart, 
                 **btn_style).pack(pady=5, padx=20, fill='x')
        tk.Button(right_panel, text="➖ Remove Item", command=self.remove_from_cart, 
                 **btn_style).pack(pady=5, padx=20, fill='x')
        
        # Bargaining section
        tk.Label(right_panel, text="💬 Bargaining", font=('Arial', 12, 'bold'), 
                bg='#16213e', fg='#00d4ff').pack(pady=15)
        
        discount_frame = tk.Frame(right_panel, bg='#16213e')
        discount_frame.pack(pady=5, padx=20, fill='x')
        
        tk.Label(discount_frame, text="Discount %:", bg='#16213e', 
                fg='white', font=('Arial', 10)).pack(side='left')
        self.discount_var = tk.StringVar(value="0")
        tk.Entry(discount_frame, textvariable=self.discount_var, width=10, 
                font=('Arial', 10), bg='#0f3460', fg='white').pack(side='right')
        
        tk.Button(right_panel, text="Apply Discount", command=self.apply_discount, 
                 **btn_style).pack(pady=5, padx=20, fill='x')
        
        # Totals
        totals_frame = tk.Frame(right_panel, bg='#0f3460')
        totals_frame.pack(pady=20, padx=20, fill='x')
        
        self.subtotal_label = tk.Label(totals_frame, text="Subtotal: Rs. 0", 
                                       font=('Arial', 12), bg='#0f3460', fg='white')
        self.subtotal_label.pack(pady=5)
        
        self.discount_label = tk.Label(totals_frame, text="Discount: Rs. 0", 
                                       font=('Arial', 12), bg='#0f3460', fg='white')
        self.discount_label.pack(pady=5)
        
        self.total_label = tk.Label(totals_frame, text="TOTAL: Rs. 0", 
                                    font=('Arial', 16, 'bold'), bg='#0f3460', fg='#00d4ff')
        self.total_label.pack(pady=10)
        
        # Checkout button
        tk.Button(right_panel, text="💳 CHECKOUT", command=self.checkout, 
                 font=('Arial', 14, 'bold'), bg='#00d4ff', fg='black', 
                 activebackground='#00ff88', relief='flat', cursor='hand2', 
                 pady=15).pack(pady=10, padx=20, fill='x')
        
        tk.Button(right_panel, text="🗑️ Clear Cart", command=self.clear_cart, 
                 **btn_style).pack(pady=5, padx=20, fill='x')
    
    def create_returns_tab(self):
        tab = tk.Frame(self.notebook, bg='#1a1a2e')
        self.notebook.add(tab, text='↩️ Returns')
        
        # Controls
        controls = tk.Frame(tab, bg='#16213e')
        controls.pack(fill='x', padx=10, pady=10)
        
        tk.Label(controls, text="Return Product", font=('Arial', 14, 'bold'), 
                bg='#16213e', fg='#00d4ff').pack(pady=10)
        
        form = tk.Frame(controls, bg='#16213e')
        form.pack(pady=10)
        
        fields = ['Barcode:', 'Quantity:', 'Reason:']
        self.return_vars = {}
        
        for i, field in enumerate(fields):
            tk.Label(form, text=field, bg='#16213e', fg='white', 
                    font=('Arial', 11)).grid(row=i, column=0, padx=10, pady=5, sticky='e')
            
            var = tk.StringVar()
            self.return_vars[field] = var
            
            if field == 'Reason:':
                entry = tk.Entry(form, textvariable=var, width=40, font=('Arial', 11), 
                               bg='#0f3460', fg='white')
            else:
                entry = tk.Entry(form, textvariable=var, width=20, font=('Arial', 11), 
                               bg='#0f3460', fg='white')
            entry.grid(row=i, column=1, padx=10, pady=5)
        
        btn_style = {'font': ('Arial', 11, 'bold'), 'bg': '#0f3460', 'fg': 'white', 
                    'activebackground': '#00d4ff', 'activeforeground': 'black', 
                    'relief': 'flat', 'cursor': 'hand2', 'padx': 20, 'pady': 10}
        
        tk.Button(controls, text="Process Return", command=self.process_return, 
                 **btn_style).pack(pady=10)
        
        # Returns history
        tk.Label(tab, text="Returns History", font=('Arial', 14, 'bold'), 
                bg='#1a1a2e', fg='#00d4ff').pack(pady=10)
        
        table_frame = tk.Frame(tab, bg='#1a1a2e')
        table_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.returns_tree = ttk.Treeview(table_frame, columns=(
            'ID', 'Barcode', 'Product', 'Quantity', 'Reason', 'Date'
        ), show='headings')
        
        for col in ['ID', 'Barcode', 'Product', 'Quantity', 'Reason', 'Date']:
            self.returns_tree.heading(col, text=col)
            self.returns_tree.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.returns_tree.yview)
        self.returns_tree.configure(yscrollcommand=scrollbar.set)
        
        self.returns_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        self.load_returns()
    
    def create_exchange_tab(self):
        tab = tk.Frame(self.notebook, bg='#1a1a2e')
        self.notebook.add(tab, text='🔄 Exchange')
        
        # Controls
        controls = tk.Frame(tab, bg='#16213e')
        controls.pack(fill='x', padx=10, pady=10)
        
        tk.Label(controls, text="Exchange Product", font=('Arial', 14, 'bold'), 
                bg='#16213e', fg='#00d4ff').pack(pady=10)
        
        form = tk.Frame(controls, bg='#16213e')
        form.pack(pady=10)
        
        fields = ['Old Barcode:', 'New Barcode:']
        self.exchange_vars = {}
        
        for i, field in enumerate(fields):
            tk.Label(form, text=field, bg='#16213e', fg='white', 
                    font=('Arial', 11)).grid(row=i, column=0, padx=10, pady=5, sticky='e')
            
            var = tk.StringVar()
            self.exchange_vars[field] = var
            
            entry = tk.Entry(form, textvariable=var, width=20, font=('Arial', 11), 
                           bg='#0f3460', fg='white')
            entry.grid(row=i, column=1, padx=10, pady=5)
        
        # Product info display
        info_frame = tk.Frame(form, bg='#16213e')
        info_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        self.old_product_label = tk.Label(info_frame, text="", bg='#16213e', 
                                          fg='white', font=('Arial', 10))
        self.old_product_label.pack(pady=5)
        
        self.new_product_label = tk.Label(info_frame, text="", bg='#16213e', 
                                          fg='white', font=('Arial', 10))
        self.new_product_label.pack(pady=5)
        
        self.exchange_vars['Old Barcode:'].trace('w', self.update_exchange_info)
        self.exchange_vars['New Barcode:'].trace('w', self.update_exchange_info)
        
        btn_style = {'font': ('Arial', 11, 'bold'), 'bg': '#0f3460', 'fg': 'white', 
                    'activebackground': '#00d4ff', 'activeforeground': 'black', 
                    'relief': 'flat', 'cursor': 'hand2', 'padx': 20, 'pady': 10}
        
        tk.Button(controls, text="Process Exchange", command=self.process_exchange, 
                 **btn_style).pack(pady=10)
        
        # Exchange history
        tk.Label(tab, text="Exchange History", font=('Arial', 14, 'bold'), 
                bg='#1a1a2e', fg='#00d4ff').pack(pady=10)
        
        table_frame = tk.Frame(tab, bg='#1a1a2e')
        table_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.exchange_tree = ttk.Treeview(table_frame, columns=(
            'ID', 'Old Barcode', 'New Barcode', 'Old Product', 'New Product', 'Date'
        ), show='headings')
        
        for col in ['ID', 'Old Barcode', 'New Barcode', 'Old Product', 'New Product', 'Date']:
            self.exchange_tree.heading(col, text=col)
            self.exchange_tree.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.exchange_tree.yview)
        self.exchange_tree.configure(yscrollcommand=scrollbar.set)
        
        self.exchange_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        self.load_exchanges()
    
    def create_reports_tab(self):
        tab = tk.Frame(self.notebook, bg='#1a1a2e')
        self.notebook.add(tab, text='📊 Reports')
        
        # Report buttons
        btn_frame = tk.Frame(tab, bg='#1a1a2e')
        btn_frame.pack(pady=20)
        
        btn_style = {'font': ('Arial', 12, 'bold'), 'bg': '#0f3460', 'fg': 'white', 
                    'activebackground': '#00d4ff', 'activeforeground': 'black', 
                    'relief': 'flat', 'cursor': 'hand2', 'padx': 30, 'pady': 15}
        
        tk.Button(btn_frame, text="📦 Stock Report", command=self.show_stock_report, 
                 **btn_style).pack(pady=10, fill='x', padx=50)
        tk.Button(btn_frame, text="⚠️ Low Stock Alert", command=self.show_low_stock, 
                 **btn_style).pack(pady=10, fill='x', padx=50)
        tk.Button(btn_frame, text="💰 Sales Report", command=self.show_sales_report, 
                 **btn_style).pack(pady=10, fill='x', padx=50)
        tk.Button(btn_frame, text="📈 Revenue Analysis", command=self.show_revenue_analysis, 
                 **btn_style).pack(pady=10, fill='x', padx=50)
        
        # Report display area
        self.report_text = tk.Text(tab, font=('Courier', 10), bg='#16213e', 
                                  fg='white', insertbackground='white', wrap='word')
        self.report_text.pack(fill='both', expand=True, padx=20, pady=20)
    
    def add_product_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Product")
        dialog.geometry("500x600")
        dialog.configure(bg='#16213e')
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="Add New Product", font=('Arial', 16, 'bold'), 
                bg='#16213e', fg='#00d4ff').pack(pady=20)
        
        form = tk.Frame(dialog, bg='#16213e')
        form.pack(pady=10, padx=30, fill='both', expand=True)
        
        fields = {
            'Barcode (4 digits):': tk.StringVar(value=self.db.get_next_barcode()),
            'Product Name:': tk.StringVar(),
            'Category:': tk.StringVar(),
            'Size:': tk.StringVar(),
            'Color:': tk.StringVar(),
            'Cost Price:': tk.StringVar(),
            'Selling Price:': tk.StringVar(),
            'Stock Quantity:': tk.StringVar(value='0'),
            'Min Stock Level:': tk.StringVar(value='5')
        }
        
        entries = {}
        for i, (label, var) in enumerate(fields.items()):
            tk.Label(form, text=label, bg='#16213e', fg='white', 
                    font=('Arial', 11)).grid(row=i, column=0, sticky='e', padx=10, pady=8)
            entry = tk.Entry(form, textvariable=var, font=('Arial', 11), 
                           bg='#0f3460', fg='white', insertbackground='white')
            entry.grid(row=i, column=1, sticky='ew', padx=10, pady=8)
            entries[label] = var
        
        form.columnconfigure(1, weight=1)
        
        def save_product():
            try:
                barcode = entries['Barcode (4 digits):'].get().strip()
                if len(barcode) != 4 or not barcode.isdigit():
                    messagebox.showerror("Error", "Barcode must be exactly 4 digits!")
                    return
                
                name = entries['Product Name:'].get().strip()
                if not name:
                    messagebox.showerror("Error", "Product name is required!")
                    return
                
                data = (
                    barcode,
                    name,
                    entries['Category:'].get().strip(),
                    entries['Size:'].get().strip(),
                    entries['Color:'].get().strip(),
                    float(entries['Cost Price:'].get() or 0),
                    float(entries['Selling Price:'].get() or 0),
                    int(entries['Stock Quantity:'].get() or 0),
                    int(entries['Min Stock Level:'].get() or 5),
                    datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                )
                
                if self.db.add_product(data):
                    messagebox.showinfo("Success", "Product added successfully!")
                    self.load_products()
                    dialog.destroy()
                else:
                    messagebox.showerror("Error", "Barcode already exists!")
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numeric values!")
        
        btn_frame = tk.Frame(dialog, bg='#16213e')
        btn_frame.pack(pady=20)
        
        btn_style = {'font': ('Arial', 11, 'bold'), 'relief': 'flat', 
                    'cursor': 'hand2', 'padx': 30, 'pady': 10}
        
        tk.Button(btn_frame, text="💾 Save", command=save_product, 
                 bg='#00d4ff', fg='black', activebackground='#00ff88', 
                 **btn_style).pack(side='left', padx=10)
        tk.Button(btn_frame, text="❌ Cancel", command=dialog.destroy, 
                 bg='#0f3460', fg='white', activebackground='#ff4757', 
                 **btn_style).pack(side='left', padx=10)
    
    def edit_product_dialog(self):
        selected = self.products_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a product to edit!")
            return
        
        values = self.products_tree.item(selected[0])['values']
        barcode = values[0]
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Product")
        dialog.geometry("500x600")
        dialog.configure(bg='#16213e')
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="Edit Product", font=('Arial', 16, 'bold'), 
                bg='#16213e', fg='#00d4ff').pack(pady=20)
        
        form = tk.Frame(dialog, bg='#16213e')
        form.pack(pady=10, padx=30, fill='both', expand=True)
        
        tk.Label(form, text=f"Barcode: {barcode}", font=('Arial', 12, 'bold'), 
                bg='#16213e', fg='white').grid(row=0, column=0, columnspan=2, pady=10)
        
        fields = {
            'Product Name:': tk.StringVar(value=values[1]),
            'Category:': tk.StringVar(value=values[2]),
            'Size:': tk.StringVar(value=values[3]),
            'Color:': tk.StringVar(value=values[4]),
            'Cost Price:': tk.StringVar(value=values[5]),
            'Selling Price:': tk.StringVar(value=values[6]),
            'Stock Quantity:': tk.StringVar(value=values[7]),
            'Min Stock Level:': tk.StringVar(value=values[8])
        }
        
        entries = {}
        for i, (label, var) in enumerate(fields.items(), start=1):
            tk.Label(form, text=label, bg='#16213e', fg='white', 
                    font=('Arial', 11)).grid(row=i, column=0, sticky='e', padx=10, pady=8)
            entry = tk.Entry(form, textvariable=var, font=('Arial', 11), 
                           bg='#0f3460', fg='white', insertbackground='white')
            entry.grid(row=i, column=1, sticky='ew', padx=10, pady=8)
            entries[label] = var
        
        form.columnconfigure(1, weight=1)
        
        def update_product():
            try:
                data = (
                    entries['Product Name:'].get().strip(),
                    entries['Category:'].get().strip(),
                    entries['Size:'].get().strip(),
                    entries['Color:'].get().strip(),
                    float(entries['Cost Price:'].get() or 0),
                    float(entries['Selling Price:'].get() or 0),
                    int(entries['Stock Quantity:'].get() or 0),
                    int(entries['Min Stock Level:'].get() or 5),
                    datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                )
                
                self.db.update_product(barcode, data)
                messagebox.showinfo("Success", "Product updated successfully!")
                self.load_products()
                dialog.destroy()
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numeric values!")
        
        btn_frame = tk.Frame(dialog, bg='#16213e')
        btn_frame.pack(pady=20)
        
        btn_style = {'font': ('Arial', 11, 'bold'), 'relief': 'flat', 
                    'cursor': 'hand2', 'padx': 30, 'pady': 10}
        
        tk.Button(btn_frame, text="💾 Update", command=update_product, 
                 bg='#00d4ff', fg='black', activebackground='#00ff88', 
                 **btn_style).pack(side='left', padx=10)
        tk.Button(btn_frame, text="❌ Cancel", command=dialog.destroy, 
                 bg='#0f3460', fg='white', activebackground='#ff4757', 
                 **btn_style).pack(side='left', padx=10)
    
    def delete_product(self):
        selected = self.products_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a product to delete!")
            return
        
        values = self.products_tree.item(selected[0])['values']
        barcode = values[0]
        name = values[1]
        
        if messagebox.askyesno("Confirm Delete", 
                               f"Are you sure you want to delete:\n{name} (Barcode: {barcode})?"):
            self.db.delete_product(barcode)
            messagebox.showinfo("Success", "Product deleted successfully!")
            self.load_products()
    
    def load_products(self):
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)
        
        products = self.db.get_all_products()
        for product in products:
            values = product[1:10]  # Exclude id and dates
            self.products_tree.insert('', 'end', values=values)
    
    def search_products(self):
        query = self.search_var.get().strip()
        
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)
        
        if query:
            products = self.db.search_products(query)
        else:
            products = self.db.get_all_products()
        
        for product in products:
            values = product[1:10]
            self.products_tree.insert('', 'end', values=values)
    
    def print_barcode(self):
        selected = self.products_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a product to print barcode!")
            return
        
        values = self.products_tree.item(selected[0])['values']
        barcode = values[0]
        name = values[1]
        price = values[6]
        
        try:
            label = BarcodeGenerator.generate_barcode(barcode, name, price)
            
            # Save to temp file
            temp_dir = Path("barcodes")
            temp_dir.mkdir(exist_ok=True)
            
            filename = temp_dir / f"barcode_{barcode}.png"
            label.save(filename)
            
            # Show preview
            preview = tk.Toplevel(self.root)
            preview.title(f"Barcode Preview - {barcode}")
            preview.configure(bg='white')
            
            img = ImageTk.PhotoImage(label)
            label_widget = tk.Label(preview, image=img, bg='white')
            label_widget.image = img
            label_widget.pack(padx=20, pady=20)
            
            btn_frame = tk.Frame(preview, bg='white')
            btn_frame.pack(pady=10)
            
            btn_style = {'font': ('Arial', 10, 'bold'), 'relief': 'flat', 
                        'cursor': 'hand2', 'padx': 20, 'pady': 8}
            
            def print_label():
                # For thermal printer, you would use a library like python-escpos
                # This example saves the file for manual printing
                messagebox.showinfo("Print", 
                                   f"Barcode saved to:\n{filename}\n\n"
                                   f"Send this file to your thermal printer.\n"
                                   f"Configure printer for 32mm x 23mm labels.")
            
            tk.Button(btn_frame, text="🖨️ Print", command=print_label, 
                     bg='#00d4ff', fg='black', **btn_style).pack(side='left', padx=5)
            tk.Button(btn_frame, text="❌ Close", command=preview.destroy, 
                     bg='#ff4757', fg='white', **btn_style).pack(side='left', padx=5)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate barcode: {str(e)}")
    
    def on_barcode_scan(self, event):
        # Handle barcode scanner input
        if event.char and event.char.isprintable():
            self.current_scan += event.char
        elif event.keysym == 'Return' and self.current_scan:
            if self.notebook.tab(self.notebook.select(), "text") == '💰 Point of Sale':
                self.barcode_entry.delete(0, tk.END)
                self.barcode_entry.insert(0, self.current_scan)
                self.add_to_cart()
            self.current_scan = ""
    
    def add_to_cart(self, event=None):
        barcode = self.barcode_entry.get().strip()
        if not barcode:
            return
        
        product = self.db.get_product(barcode)
        if not product:
            messagebox.showerror("Error", f"Product with barcode {barcode} not found!")
            self.barcode_entry.delete(0, tk.END)
            return
        
        if product[8] <= 0:  # stock_quantity
            messagebox.showerror("Error", "Product out of stock!")
            self.barcode_entry.delete(0, tk.END)
            return
        
        # Check if already in cart
        for item in self.cart_tree.get_children():
            if self.cart_tree.item(item)['values'][0] == barcode:
                # Increase quantity
                values = list(self.cart_tree.item(item)['values'])
                values[2] += 1
                values[5] = values[2] * values[3]
                self.cart_tree.item(item, values=values)
                self.update_cart_totals()
                self.barcode_entry.delete(0, tk.END)
                return
        
        # Add new item
        self.cart_tree.insert('', 'end', values=(
            barcode,
            product[2],  # name
            1,  # quantity
            product[7],  # selling_price
            0,  # discount
            product[7]  # total
        ))
        
        self.update_cart_totals()
        self.barcode_entry.delete(0, tk.END)
        self.barcode_entry.focus()
    
    def remove_from_cart(self):
        selected = self.cart_tree.selection()
        if selected:
            self.cart_tree.delete(selected)
            self.update_cart_totals()
    
    def apply_discount(self):
        try:
            discount_percent = float(self.discount_var.get() or 0)
            if discount_percent < 0 or discount_percent > 100:
                messagebox.showerror("Error", "Discount must be between 0 and 100!")
                return
            
            for item in self.cart_tree.get_children():
                values = list(self.cart_tree.item(item)['values'])
                original_price = values[3]
                quantity = values[2]
                discount_amount = (original_price * discount_percent / 100)
                values[4] = discount_amount
                values[5] = (original_price - discount_amount) * quantity
                self.cart_tree.item(item, values=values)
            
            self.update_cart_totals()
            messagebox.showinfo("Success", f"{discount_percent}% discount applied!")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid discount percentage!")
    
    def update_cart_totals(self):
        subtotal = 0
        total_discount = 0
        
        for item in self.cart_tree.get_children():
            values = self.cart_tree.item(item)['values']
            subtotal += values[2] * values[3]
            total_discount += values[4] * values[2]
        
        total = subtotal - total_discount
        
        self.subtotal_label.config(text=f"Subtotal: Rs. {subtotal:.2f}")
        self.discount_label.config(text=f"Discount: Rs. {total_discount:.2f}")
        self.total_label.config(text=f"TOTAL: Rs. {total:.2f}")
    
    def checkout(self):
        if not self.cart_tree.get_children():
            messagebox.showwarning("Warning", "Cart is empty!")
            return
        
        try:
            for item in self.cart_tree.get_children():
                values = self.cart_tree.item(item)['values']
                sale_data = (
                    values[0],  # barcode
                    values[1],  # product_name
                    values[2],  # quantity
                    values[3],  # original_price
                    values[4],  # discount_price
                    values[5],  # final_price
                    datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                )
                self.db.add_sale(sale_data)
            
            total = float(self.total_label.cget("text").split("Rs. ")[1])
            
            messagebox.showinfo("Success", 
                               f"Sale completed!\n\nTotal: Rs. {total:.2f}\n\nThank you!")
            
            self.clear_cart()
            self.load_products()
            
        except Exception as e:
            messagebox.showerror("Error", f"Checkout failed: {str(e)}")
    
    def clear_cart(self):
        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)
        self.discount_var.set("0")
        self.update_cart_totals()
    
    def process_return(self):
        try:
            barcode = self.return_vars['Barcode:'].get().strip()
            quantity = int(self.return_vars['Quantity:'].get())
            reason = self.return_vars['Reason:'].get().strip()
            
            if not barcode or quantity <= 0 or not reason:
                messagebox.showerror("Error", "Please fill all fields correctly!")
                return
            
            product = self.db.get_product(barcode)
            if not product:
                messagebox.showerror("Error", "Product not found!")
                return
            
            return_data = (
                barcode,
                product[2],  # name
                quantity,
                reason,
                datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                None  # sale_id
            )
            
            self.db.add_return(return_data)
            messagebox.showinfo("Success", "Return processed successfully!")
            
            for var in self.return_vars.values():
                var.set("")
            
            self.load_returns()
            self.load_products()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid quantity!")
    
    def load_returns(self):
        for item in self.returns_tree.get_children():
            self.returns_tree.delete(item)
        
        cursor = self.db.conn.cursor()
        cursor.execute('SELECT * FROM returns ORDER BY return_date DESC')
        returns = cursor.fetchall()
        
        for ret in returns:
            self.returns_tree.insert('', 'end', values=ret[:6])
    
    def update_exchange_info(self, *args):
        old_barcode = self.exchange_vars['Old Barcode:'].get().strip()
        new_barcode = self.exchange_vars['New Barcode:'].get().strip()
        
        if old_barcode:
            product = self.db.get_product(old_barcode)
            if product:
                self.old_product_label.config(
                    text=f"Old: {product[2]} - Rs. {product[7]}"
                )
            else:
                self.old_product_label.config(text="Old: Product not found")
        
        if new_barcode:
            product = self.db.get_product(new_barcode)
            if product:
                self.new_product_label.config(
                    text=f"New: {product[2]} - Rs. {product[7]}"
                )
            else:
                self.new_product_label.config(text="New: Product not found")
    
    def process_exchange(self):
        old_barcode = self.exchange_vars['Old Barcode:'].get().strip()
        new_barcode = self.exchange_vars['New Barcode:'].get().strip()
        
        if not old_barcode or not new_barcode:
            messagebox.showerror("Error", "Please enter both barcodes!")
            return
        
        old_product = self.db.get_product(old_barcode)
        new_product = self.db.get_product(new_barcode)
        
        if not old_product or not new_product:
            messagebox.showerror("Error", "One or both products not found!")
            return
        
        if new_product[8] <= 0:  # stock_quantity
            messagebox.showerror("Error", "New product out of stock!")
            return
        
        exchange_data = (
            old_barcode,
            new_barcode,
            old_product[2],  # old name
            new_product[2],  # new name
            datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        
        self.db.add_exchange(exchange_data)
        messagebox.showinfo("Success", "Exchange processed successfully!")
        
        for var in self.exchange_vars.values():
            var.set("")
        
        self.old_product_label.config(text="")
        self.new_product_label.config(text="")
        
        self.load_exchanges()
        self.load_products()
    
    def load_exchanges(self):
        for item in self.exchange_tree.get_children():
            self.exchange_tree.delete(item)
        
        cursor = self.db.conn.cursor()
        cursor.execute('SELECT * FROM exchanges ORDER BY exchange_date DESC')
        exchanges = cursor.fetchall()
        
        for exc in exchanges:
            self.exchange_tree.insert('', 'end', values=exc)
    
    def show_stock_report(self):
        self.report_text.delete(1.0, tk.END)
        
        products = self.db.get_all_products()
        
        report = "=" * 80 + "\n"
        report += "STOCK REPORT\n"
        report += "=" * 80 + "\n\n"
        report += f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        report += f"Total Products: {len(products)}\n\n"
        
        report += f"{'Barcode':<10} {'Product Name':<30} {'Stock':<10} {'Value (Rs.)':<15}\n"
        report += "-" * 80 + "\n"
        
        total_value = 0
        for product in products:
            value = product[7] * product[8]  # price * quantity
            total_value += value
            report += f"{product[1]:<10} {product[2]:<30} {product[8]:<10} {value:<15.2f}\n"
        
        report += "-" * 80 + "\n"
        report += f"{'TOTAL INVENTORY VALUE:':<51} Rs. {total_value:.2f}\n"
        report += "=" * 80 + "\n"
        
        self.report_text.insert(1.0, report)
    
    def show_low_stock(self):
        self.report_text.delete(1.0, tk.END)
        
        cursor = self.db.conn.cursor()
        cursor.execute('''
            SELECT * FROM products 
            WHERE stock_quantity <= min_stock_level 
            ORDER BY stock_quantity ASC
        ''')
        products = cursor.fetchall()
        
        report = "=" * 80 + "\n"
        report += "LOW STOCK ALERT\n"
        report += "=" * 80 + "\n\n"
        report += f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        report += f"Products Below Minimum Stock: {len(products)}\n\n"
        
        if products:
            report += f"{'Barcode':<10} {'Product':<30} {'Stock':<10} {'Min Level':<10}\n"
            report += "-" * 80 + "\n"
            
            for product in products:
                report += f"{product[1]:<10} {product[2]:<30} {product[8]:<10} {product[9]:<10}\n"
        else:
            report += "All products are adequately stocked!\n"
        
        report += "=" * 80 + "\n"
        
        self.report_text.insert(1.0, report)
    
    def show_sales_report(self):
        self.report_text.delete(1.0, tk.END)
        
        cursor = self.db.conn.cursor()
        cursor.execute('SELECT * FROM sales ORDER BY sale_date DESC LIMIT 50')
        sales = cursor.fetchall()
        
        report = "=" * 80 + "\n"
        report += "RECENT SALES REPORT (Last 50 Transactions)\n"
        report += "=" * 80 + "\n\n"
        report += f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        report += f"Total Transactions: {len(sales)}\n\n"
        
        report += f"{'Date':<20} {'Product':<25} {'Qty':<5} {'Total':<15}\n"
        report += "-" * 80 + "\n"
        
        total_revenue = 0
        for sale in sales:
            total_revenue += sale[6]  # final_price
            report += f"{sale[7]:<20} {sale[2]:<25} {sale[3]:<5} Rs. {sale[6]:<12.2f}\n"
        
        report += "-" * 80 + "\n"
        report += f"{'TOTAL REVENUE:':<46} Rs. {total_revenue:.2f}\n"
        report += "=" * 80 + "\n"
        
        self.report_text.insert(1.0, report)
    
    def show_revenue_analysis(self):
        self.report_text.delete(1.0, tk.END)
        
        cursor = self.db.conn.cursor()
        
        # Today's sales
        cursor.execute('''
            SELECT SUM(final_price) FROM sales 
            WHERE DATE(sale_date) = DATE('now')
        ''')
        today_revenue = cursor.fetchone()[0] or 0
        
        # This month's sales
        cursor.execute('''
            SELECT SUM(final_price) FROM sales 
            WHERE strftime('%Y-%m', sale_date) = strftime('%Y-%m', 'now')
        ''')
        month_revenue = cursor.fetchone()[0] or 0
        
        # Total sales
        cursor.execute('SELECT SUM(final_price) FROM sales')
        total_revenue = cursor.fetchone()[0] or 0
        
        # Total products sold
        cursor.execute('SELECT SUM(quantity) FROM sales')
        total_items = cursor.fetchone()[0] or 0
        
        # Top selling products
        cursor.execute('''
            SELECT product_name, SUM(quantity) as total_qty, SUM(final_price) as revenue
            FROM sales
            GROUP BY product_name
            ORDER BY total_qty DESC
            LIMIT 10
        ''')
        top_products = cursor.fetchall()
        
        report = "=" * 80 + "\n"
        report += "REVENUE ANALYSIS\n"
        report += "=" * 80 + "\n\n"
        report += f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        report += "REVENUE SUMMARY:\n"
        report += f"Today's Revenue:      Rs. {today_revenue:.2f}\n"
        report += f"This Month's Revenue: Rs. {month_revenue:.2f}\n"
        report += f"Total Revenue:        Rs. {total_revenue:.2f}\n"
        report += f"Total Items Sold:     {total_items}\n\n"
        
        report += "TOP 10 SELLING PRODUCTS:\n"
        report += "-" * 80 + "\n"
        report += f"{'Product':<40} {'Qty Sold':<15} {'Revenue':<15}\n"
        report += "-" * 80 + "\n"
        
        for product in top_products:
            report += f"{product[0]:<40} {product[1]:<15} Rs. {product[2]:<12.2f}\n"
        
        report += "=" * 80 + "\n"
        
        self.report_text.insert(1.0, report)

if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryManagementSystem(root)
    root.mainloop()