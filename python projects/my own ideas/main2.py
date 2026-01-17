import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
from datetime import datetime
import json
import os
from typing import Dict, List
import barcode
from barcode.writer import ImageWriter
from PIL import Image, ImageTk, ImageDraw, ImageFont
import io

class GarmentShopManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Retail Garments Shop Management System")
        self.root.geometry("1400x800")
        self.root.configure(bg='#2c3e50')
        
        # Data storage
        self.products = {}
        self.sales = []
        self.stock_history = []
        self.barcode_counter = 1
        
        # Load existing data
        self.load_data()
        
        # Create main interface
        self.create_menu()
        self.create_main_frame()
        
    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File Menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Backup Data", command=self.backup_data)
        file_menu.add_command(label="Restore Data", command=self.restore_data)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Inventory Menu
        inventory_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Inventory", menu=inventory_menu)
        inventory_menu.add_command(label="Add Stock", command=self.show_add_stock)
        inventory_menu.add_command(label="Edit Stock", command=self.show_edit_stock)
        inventory_menu.add_command(label="Remove Stock", command=self.show_remove_stock)
        
        # Sales Menu
        sales_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Sales", menu=sales_menu)
        sales_menu.add_command(label="New Sale", command=self.show_sale_window)
        sales_menu.add_command(label="Return/Exchange", command=self.show_return_exchange)
        
        # Reports Menu
        reports_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Reports", menu=reports_menu)
        reports_menu.add_command(label="Sales Report", command=self.show_sales_report)
        reports_menu.add_command(label="Stock Report", command=self.show_stock_report)
        reports_menu.add_command(label="Low Stock Alert", command=self.show_low_stock_alert)
        
    def create_main_frame(self):
        # Main container
        main_container = tk.Frame(self.root, bg='#34495e')
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title = tk.Label(main_container, text="Garments Shop Management System", 
                        font=('Arial', 24, 'bold'), bg='#34495e', fg='white')
        title.pack(pady=20)
        
        # Dashboard Frame
        dashboard = tk.Frame(main_container, bg='#34495e')
        dashboard.pack(fill=tk.BOTH, expand=True, padx=20)
        
        # Quick Stats
        stats_frame = tk.Frame(dashboard, bg='#34495e')
        stats_frame.pack(fill=tk.X, pady=20)
        
        self.create_stat_card(stats_frame, "Total Products", len(self.products), '#3498db', 0)
        self.create_stat_card(stats_frame, "Total Stock Value", f"Rs. {self.calculate_total_stock_value()}", '#2ecc71', 1)
        self.create_stat_card(stats_frame, "Low Stock Items", self.count_low_stock(), '#e74c3c', 2)
        self.create_stat_card(stats_frame, "Today's Sales", f"Rs. {self.calculate_today_sales()}", '#f39c12', 3)
        
        # Quick Actions
        actions_frame = tk.LabelFrame(dashboard, text="Quick Actions", font=('Arial', 14, 'bold'),
                                     bg='#34495e', fg='white', padx=20, pady=20)
        actions_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        buttons = [
            ("Add New Product", self.show_add_stock, '#3498db'),
            ("Make Sale", self.show_sale_window, '#2ecc71'),
            ("Generate Barcodes", self.show_barcode_generator, '#9b59b6'),
            ("View Stock", self.show_stock_report, '#e67e22'),
            ("Return/Exchange", self.show_return_exchange, '#e74c3c'),
            ("Sales Report", self.show_sales_report, '#1abc9c')
        ]
        
        for i, (text, command, color) in enumerate(buttons):
            btn = tk.Button(actions_frame, text=text, command=command,
                          font=('Arial', 12, 'bold'), bg=color, fg='white',
                          width=20, height=2, cursor='hand2')
            btn.grid(row=i//3, column=i%3, padx=10, pady=10)
        
    def create_stat_card(self, parent, title, value, color, col):
        card = tk.Frame(parent, bg=color, relief=tk.RAISED, borderwidth=2)
        card.grid(row=0, column=col, padx=10, sticky='ew')
        parent.grid_columnconfigure(col, weight=1)
        
        tk.Label(card, text=title, font=('Arial', 12), bg=color, fg='white').pack(pady=(10, 5))
        tk.Label(card, text=str(value), font=('Arial', 20, 'bold'), bg=color, fg='white').pack(pady=(0, 10))
    
    def show_add_stock(self):
        window = tk.Toplevel(self.root)
        window.title("Add New Product")
        window.geometry("600x700")
        window.configure(bg='#ecf0f1')
        
        # Form
        form_frame = tk.Frame(window, bg='#ecf0f1', padx=30, pady=30)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(form_frame, text="Add New Product", font=('Arial', 18, 'bold'), 
                bg='#ecf0f1').grid(row=0, column=0, columnspan=2, pady=20)
        
        fields = {}
        labels = [
            ("Product Name:", "name"),
            ("Category:", "category"),
            ("Size:", "size"),
            ("Color:", "color"),
            ("Purchase Price:", "purchase_price"),
            ("Selling Price:", "selling_price"),
            ("Quantity:", "quantity"),
            ("Secret Code:", "secret_code"),
            ("Min Stock Level:", "min_stock")
        ]
        
        for i, (label, key) in enumerate(labels, start=1):
            tk.Label(form_frame, text=label, font=('Arial', 11), bg='#ecf0f1').grid(
                row=i, column=0, sticky='w', pady=8)
            entry = tk.Entry(form_frame, font=('Arial', 11), width=30)
            entry.grid(row=i, column=1, pady=8, padx=10)
            fields[key] = entry
        
        def save_product():
            try:
                barcode_num = str(self.barcode_counter).zfill(4)
                product_id = f"{fields['secret_code'].get().upper()}{barcode_num}"
                
                if not fields['secret_code'].get():
                    messagebox.showerror("Error", "Secret code is required!")
                    return
                
                product = {
                    'id': product_id,
                    'barcode': barcode_num,
                    'secret_code': fields['secret_code'].get().upper(),
                    'name': fields['name'].get(),
                    'category': fields['category'].get(),
                    'size': fields['size'].get(),
                    'color': fields['color'].get(),
                    'purchase_price': float(fields['purchase_price'].get()),
                    'selling_price': float(fields['selling_price'].get()),
                    'quantity': int(fields['quantity'].get()),
                    'min_stock': int(fields['min_stock'].get()),
                    'added_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                self.products[product_id] = product
                self.barcode_counter += 1
                self.stock_history.append({
                    'product_id': product_id,
                    'action': 'Added',
                    'quantity': product['quantity'],
                    'date': product['added_date']
                })
                
                self.save_data()
                messagebox.showinfo("Success", f"Product added successfully!\nProduct ID: {product_id}")
                window.destroy()
                self.refresh_dashboard()
                
            except ValueError as e:
                messagebox.showerror("Error", "Please enter valid numeric values!")
        
        tk.Button(form_frame, text="Save Product", command=save_product,
                 bg='#2ecc71', fg='white', font=('Arial', 12, 'bold'),
                 width=20, height=2).grid(row=len(labels)+1, column=0, columnspan=2, pady=20)
    
    def show_edit_stock(self):
        window = tk.Toplevel(self.root)
        window.title("Edit Stock")
        window.geometry("900x600")
        window.configure(bg='#ecf0f1')
        
        # Search frame
        search_frame = tk.Frame(window, bg='#ecf0f1', padx=20, pady=10)
        search_frame.pack(fill=tk.X)
        
        tk.Label(search_frame, text="Search Product:", font=('Arial', 11), bg='#ecf0f1').pack(side=tk.LEFT, padx=5)
        search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=search_var, font=('Arial', 11), width=40)
        search_entry.pack(side=tk.LEFT, padx=5)
        
        # Product list
        list_frame = tk.Frame(window, bg='#ecf0f1', padx=20)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ('ID', 'Name', 'Category', 'Size', 'Color', 'Price', 'Qty')
        tree = ttk.Treeview(list_frame, columns=columns, show='tree headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill=tk.BOTH, expand=True)
        
        def populate_tree(search_term=""):
            tree.delete(*tree.get_children())
            for pid, prod in self.products.items():
                if search_term.lower() in prod['name'].lower() or search_term.lower() in pid.lower():
                    tree.insert('', tk.END, values=(
                        prod['id'], prod['name'], prod['category'], 
                        prod['size'], prod['color'], prod['selling_price'], prod['quantity']
                    ))
        
        populate_tree()
        search_var.trace('w', lambda *args: populate_tree(search_var.get()))
        
        def edit_selected():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Warning", "Please select a product to edit!")
                return
            
            values = tree.item(selected[0])['values']
            product_id = values[0]
            
            edit_win = tk.Toplevel(window)
            edit_win.title(f"Edit Product - {product_id}")
            edit_win.geometry("500x600")
            edit_win.configure(bg='#ecf0f1')
            
            form = tk.Frame(edit_win, bg='#ecf0f1', padx=30, pady=20)
            form.pack(fill=tk.BOTH, expand=True)
            
            product = self.products[product_id]
            fields = {}
            
            edit_labels = [
                ("Product Name:", "name"),
                ("Category:", "category"),
                ("Size:", "size"),
                ("Color:", "color"),
                ("Purchase Price:", "purchase_price"),
                ("Selling Price:", "selling_price"),
                ("Quantity:", "quantity"),
                ("Secret Code:", "secret_code"),
                ("Min Stock Level:", "min_stock")
            ]
            
            for i, (label, key) in enumerate(edit_labels):
                tk.Label(form, text=label, font=('Arial', 10), bg='#ecf0f1').grid(
                    row=i, column=0, sticky='w', pady=5)
                entry = tk.Entry(form, font=('Arial', 10), width=30)
                entry.insert(0, product[key])
                entry.grid(row=i, column=1, pady=5)
                fields[key] = entry
            
            def update_product():
                try:
                    old_qty = product['quantity']
                    new_qty = int(fields['quantity'].get())
                    
                    product['name'] = fields['name'].get()
                    product['category'] = fields['category'].get()
                    product['size'] = fields['size'].get()
                    product['color'] = fields['color'].get()
                    product['purchase_price'] = float(fields['purchase_price'].get())
                    product['selling_price'] = float(fields['selling_price'].get())
                    product['quantity'] = new_qty
                    product['secret_code'] = fields['secret_code'].get().upper()
                    product['min_stock'] = int(fields['min_stock'].get())
                    
                    if old_qty != new_qty:
                        self.stock_history.append({
                            'product_id': product_id,
                            'action': 'Updated',
                            'old_quantity': old_qty,
                            'new_quantity': new_qty,
                            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        })
                    
                    self.save_data()
                    messagebox.showinfo("Success", "Product updated successfully!")
                    edit_win.destroy()
                    populate_tree()
                    self.refresh_dashboard()
                except ValueError:
                    messagebox.showerror("Error", "Please enter valid values!")
            
            tk.Button(form, text="Update Product", command=update_product,
                     bg='#3498db', fg='white', font=('Arial', 11, 'bold'),
                     width=20, height=2).grid(row=len(edit_labels), column=0, columnspan=2, pady=20)
        
        tk.Button(window, text="Edit Selected Product", command=edit_selected,
                 bg='#3498db', fg='white', font=('Arial', 11, 'bold'),
                 width=20, height=2).pack(pady=10)
    
    def show_remove_stock(self):
        window = tk.Toplevel(self.root)
        window.title("Remove Stock")
        window.geometry("900x600")
        window.configure(bg='#ecf0f1')
        
        # Search frame
        search_frame = tk.Frame(window, bg='#ecf0f1', padx=20, pady=10)
        search_frame.pack(fill=tk.X)
        
        tk.Label(search_frame, text="Search Product:", font=('Arial', 11), bg='#ecf0f1').pack(side=tk.LEFT, padx=5)
        search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=search_var, font=('Arial', 11), width=40)
        search_entry.pack(side=tk.LEFT, padx=5)
        
        # Product list
        list_frame = tk.Frame(window, bg='#ecf0f1', padx=20)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ('ID', 'Name', 'Category', 'Size', 'Color', 'Price', 'Qty')
        tree = ttk.Treeview(list_frame, columns=columns, show='tree headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill=tk.BOTH, expand=True)
        
        def populate_tree(search_term=""):
            tree.delete(*tree.get_children())
            for pid, prod in self.products.items():
                if search_term.lower() in prod['name'].lower() or search_term.lower() in pid.lower():
                    tree.insert('', tk.END, values=(
                        prod['id'], prod['name'], prod['category'], 
                        prod['size'], prod['color'], prod['selling_price'], prod['quantity']
                    ))
        
        populate_tree()
        search_var.trace('w', lambda *args: populate_tree(search_var.get()))
        
        def remove_selected():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Warning", "Please select a product to remove!")
                return
            
            values = tree.item(selected[0])['values']
            product_id = values[0]
            
            confirm = messagebox.askyesno("Confirm", f"Are you sure you want to remove product {product_id}?")
            if confirm:
                self.stock_history.append({
                    'product_id': product_id,
                    'action': 'Removed',
                    'product_data': self.products[product_id],
                    'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                del self.products[product_id]
                self.save_data()
                messagebox.showinfo("Success", "Product removed successfully!")
                populate_tree()
                self.refresh_dashboard()
        
        tk.Button(window, text="Remove Selected Product", command=remove_selected,
                 bg='#e74c3c', fg='white', font=('Arial', 11, 'bold'),
                 width=20, height=2).pack(pady=10)
    
    def show_barcode_generator(self):
        window = tk.Toplevel(self.root)
        window.title("Barcode Generator")
        window.geometry("1000x700")
        window.configure(bg='#ecf0f1')
        
        # Product selection
        select_frame = tk.Frame(window, bg='#ecf0f1', padx=20, pady=20)
        select_frame.pack(fill=tk.X)
        
        tk.Label(select_frame, text="Select Products for Barcode Generation", 
                font=('Arial', 14, 'bold'), bg='#ecf0f1').pack(pady=10)
        
        # Product list with checkboxes
        list_frame = tk.Frame(window, bg='#ecf0f1', padx=20)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ('Select', 'ID', 'Name', 'Size', 'Color', 'Price', 'Qty')
        tree = ttk.Treeview(list_frame, columns=columns, show='tree headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=130)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill=tk.BOTH, expand=True)
        
        selected_products = {}
        
        for pid, prod in self.products.items():
            item = tree.insert('', tk.END, values=(
                '☐', prod['id'], prod['name'], 
                prod['size'], prod['color'], prod['selling_price'], prod['quantity']
            ))
            selected_products[item] = {'selected': False, 'product': prod}
        
        def toggle_selection(event):
            item = tree.identify_row(event.y)
            if item:
                selected_products[item]['selected'] = not selected_products[item]['selected']
                current_values = list(tree.item(item)['values'])
                current_values[0] = '☑' if selected_products[item]['selected'] else '☐'
                tree.item(item, values=current_values)
        
        tree.bind('<Button-1>', toggle_selection)
        
        def generate_barcodes():
            selected = [data['product'] for data in selected_products.values() if data['selected']]
            
            if not selected:
                messagebox.showwarning("Warning", "Please select at least one product!")
                return
            
            preview_win = tk.Toplevel(window)
            preview_win.title("Barcode Preview")
            preview_win.geometry("900x700")
            preview_win.configure(bg='white')
            
            canvas = tk.Canvas(preview_win, bg='white')
            scrollbar = ttk.Scrollbar(preview_win, orient=tk.VERTICAL, command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg='white')
            
            scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            # Generate barcode stickers (3 per row)
            row = 0
            col = 0
            for product in selected:
                sticker = self.create_barcode_sticker(product)
                label = tk.Label(scrollable_frame, image=sticker, bg='white')
                label.image = sticker
                label.grid(row=row, column=col, padx=5, pady=5)
                
                col += 1
                if col >= 3:
                    col = 0
                    row += 1
            
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            def print_barcodes():
                # Save barcodes for printing
                save_path = filedialog.asksaveasfilename(
                    defaultextension=".png",
                    filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
                )
                if save_path:
                    # Create a combined image
                    sticker_width = 250
                    sticker_height = 150
                    rows = (len(selected) + 2) // 3
                    combined = Image.new('RGB', (sticker_width * 3, sticker_height * rows), 'white')
                    
                    row = 0
                    col = 0
                    for product in selected:
                        sticker_img = self.create_barcode_image(product)
                        combined.paste(sticker_img, (col * sticker_width, row * sticker_height))
                        col += 1
                        if col >= 3:
                            col = 0
                            row += 1
                    
                    combined.save(save_path)
                    messagebox.showinfo("Success", f"Barcodes saved to {save_path}")
            
            tk.Button(preview_win, text="Save for Printing", command=print_barcodes,
                     bg='#2ecc71', fg='white', font=('Arial', 12, 'bold'),
                     width=20, height=2).pack(pady=10)
        
        tk.Button(window, text="Generate Barcodes", command=generate_barcodes,
                 bg='#9b59b6', fg='white', font=('Arial', 12, 'bold'),
                 width=20, height=2).pack(pady=10)
    
    def create_barcode_sticker(self, product):
        img = self.create_barcode_image(product)
        return ImageTk.PhotoImage(img)
    
    def create_barcode_image(self, product):
        # Create barcode sticker image
        width, height = 250, 150
        img = Image.new('RGB', (width, height), 'white')
        draw = ImageDraw.Draw(img)
        
        try:
            font_large = ImageFont.truetype("arial.ttf", 14)
            font_small = ImageFont.truetype("arial.ttf", 10)
            font_code = ImageFont.truetype("arial.ttf", 12)
        except:
            font_large = ImageFont.load_default()
            font_small = ImageFont.load_default()
            font_code = ImageFont.load_default()
        
        # Product name
        draw.text((10, 10), product['name'][:25], fill='black', font=font_large)
        
        # Size and Color
        draw.text((10, 30), f"Size: {product['size']} | Color: {product['color']}", 
                 fill='black', font=font_small)
        
        # Secret Code
        draw.text((10, 50), f"Code: {product['secret_code']}", fill='red', font=font_code)
        
        # Price
        draw.text((10, 70), f"Rs. {product['selling_price']}", fill='black', font=font_large)
        
        # Generate barcode
        try:
            from barcode import Code128
            barcode_data = product['barcode']
            code128 = Code128(barcode_data, writer=ImageWriter())
            
            # Generate barcode to bytes
            buffer = io.BytesIO()
            code128.write(buffer)
            buffer.seek(0)
            barcode_img = Image.open(buffer)
            
            # Resize and paste barcode
            barcode_img = barcode_img.resize((230, 50))
            img.paste(barcode_img, (10, 90))
        except Exception as e:
            # Fallback: draw barcode number
            draw.text((10, 100), product['barcode'], fill='black', font=font_large)
        
        # Border
        draw.rectangle([(0, 0), (width-1, height-1)], outline='black', width=2)
        
        return img
    
    def show_sale_window(self):
        window = tk.Toplevel(self.root)
        window.title("Make Sale")
        window.geometry("1100x700")
        window.configure(bg='#ecf0f1')
        
        # Main container
        main_frame = tk.Frame(window, bg='#ecf0f1')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Left side - Product selection
        left_frame = tk.Frame(main_frame, bg='#ecf0f1')
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        tk.Label(left_frame, text="Scan Barcode or Search Product", 
                font=('Arial', 12, 'bold'), bg='#ecf0f1').pack(pady=5)
        
        search_frame = tk.Frame(left_frame, bg='#ecf0f1')
        search_frame.pack(fill=tk.X, pady=5)
        
        search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=search_var, font=('Arial', 11), width=40)
        search_entry.pack(side=tk.LEFT, padx=5)
        search_entry.focus()
        
        # Product list
        columns = ('ID', 'Name', 'Size', 'Color', 'Price', 'Stock')
        tree = ttk.Treeview(left_frame, columns=columns, show='tree headings', height=20)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        
        scrollbar = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill=tk.BOTH, expand=True, pady=5)
        
        def populate_products(search_term=""):
            tree.delete(*tree.get_children())
            for pid, prod in self.products.items():
                if (search_term.lower() in prod['name'].lower() or 
                    search_term.lower() in pid.lower() or
                    search_term in prod['barcode']):
                    tree.insert('', tk.END, values=(
                        prod['id'], prod['name'], prod['size'], 
                        prod['color'], prod['selling_price'], prod['quantity']
                    ))
        
        populate_products()
        search_var.trace('w', lambda *args: populate_products(search_var.get()))
        
        # Right side - Cart
        right_frame = tk.Frame(main_frame, bg='white', relief=tk.RAISED, borderwidth=2)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0))
        
        tk.Label(right_frame, text="Shopping Cart", font=('Arial', 14, 'bold'), 
                bg='white').pack(pady=10)
        
        # Cart items
        cart_frame = tk.Frame(right_frame, bg='white')
        cart_frame.pack(fill=tk.BOTH, expand=True, padx=10)
        
        cart_columns = ('Item', 'Price', 'Qty', 'Total')
        cart_tree = ttk.Treeview(cart_frame, columns=cart_columns, show='tree headings', height=15)
        
        for col in cart_columns:
            cart_tree.heading(col, text=col)
            cart_tree.column(col, width=100)
        
        cart_scrollbar = ttk.Scrollbar(cart_frame, orient=tk.VERTICAL, command=cart_tree.yview)
        cart_tree.configure(yscroll=cart_scrollbar.set)
        cart_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        cart_tree.pack(fill=tk.BOTH, expand=True)
        
        cart_items = {}
        
        def add_to_cart():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Warning", "Please select a product!")
                return
            
            values = tree.item(selected[0])['values']
            product_id = values[0]
            product = self.products[product_id]
            
            if product['quantity'] <= 0:
                messagebox.showerror("Error", "Product out of stock!")
                return
            
            qty = simpledialog.askinteger("Quantity", f"Enter quantity for {product['name']}:",
                                         minvalue=1, maxvalue=product['quantity'])
            if qty:
                if product_id in cart_items:
                    cart_items[product_id]['qty'] += qty
                else:
                    cart_items[product_id] = {
                        'product': product,
                        'qty': qty
                    }
                update_cart()
        
        def update_cart():
            cart_tree.delete(*cart_tree.get_children())
            total = 0
            for pid, item in cart_items.items():
                prod = item['product']
                qty = item['qty']
                item_total = prod['selling_price'] * qty
                total += item_total
                cart_tree.insert('', tk.END, values=(
                    prod['name'][:15], prod['selling_price'], qty, item_total
                ))
            
            subtotal_label.config(text=f"Rs. {total:.2f}")
            discount_amount = total * (discount_var.get() / 100)
            discount_label.config(text=f"Rs. {discount_amount:.2f}")
            total_label.config(text=f"Rs. {total - discount_amount:.2f}")
        
        def remove_from_cart():
            selected = cart_tree.selection()
            if selected:
                idx = cart_tree.index(selected[0])
                product_id = list(cart_items.keys())[idx]
                del cart_items[product_id]
                update_cart()
        
        tree.bind('<Double-1>', lambda e: add_to_cart())
        
        # Buttons
        btn_frame = tk.Frame(right_frame, bg='white')
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Button(btn_frame, text="Add to Cart", command=add_to_cart,
                 bg='#3498db', fg='white', font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Remove Item", command=remove_from_cart,
                 bg='#e74c3c', fg='white', font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)
        
        # Discount and Total
        totals_frame = tk.Frame(right_frame, bg='white', padx=10, pady=10)
        totals_frame.pack(fill=tk.X)
        
        tk.Label(totals_frame, text="Discount %:", bg='white', font=('Arial', 11)).grid(row=0, column=0, sticky='w', pady=5)
        discount_var = tk.DoubleVar(value=0)
        discount_entry = tk.Entry(totals_frame, textvariable=discount_var, font=('Arial', 11), width=10)
        discount_entry.grid(row=0, column=1, pady=5)
        discount_var.trace('w', lambda *args: update_cart())
        
        tk.Label(totals_frame, text="Subtotal:", bg='white', font=('Arial', 11, 'bold')).grid(row=1, column=0, sticky='w', pady=5)
        subtotal_label = tk.Label(totals_frame, text="Rs. 0.00", bg='white', font=('Arial', 11))
        subtotal_label.grid(row=1, column=1, pady=5)
        
        tk.Label(totals_frame, text="Discount:", bg='white', font=('Arial', 11, 'bold')).grid(row=2, column=0, sticky='w', pady=5)
        discount_label = tk.Label(totals_frame, text="Rs. 0.00", bg='white', font=('Arial', 11))
        discount_label.grid(row=2, column=1, pady=5)
        
        tk.Label(totals_frame, text="Total:", bg='white', font=('Arial', 14, 'bold')).grid(row=3, column=0, sticky='w', pady=5)
        total_label = tk.Label(totals_frame, text="Rs. 0.00", bg='white', font=('Arial', 14, 'bold'), fg='#2ecc71')
        total_label.grid(row=3, column=1, pady=5)
        
        def complete_sale():
            if not cart_items:
                messagebox.showwarning("Warning", "Cart is empty!")
                return
            
            # Update stock
            for pid, item in cart_items.items():
                self.products[pid]['quantity'] -= item['qty']
                self.stock_history.append({
                    'product_id': pid,
                    'action': 'Sold',
                    'quantity': item['qty'],
                    'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
            
            # Record sale
            subtotal = sum(item['product']['selling_price'] * item['qty'] for item in cart_items.values())
            discount_amount = subtotal * (discount_var.get() / 100)
            total = subtotal - discount_amount
            
            sale = {
                'sale_id': f"SALE{len(self.sales) + 1:04d}",
                'items': [{
                    'product_id': pid,
                    'name': item['product']['name'],
                    'price': item['product']['selling_price'],
                    'quantity': item['qty']
                } for pid, item in cart_items.items()],
                'subtotal': subtotal,
                'discount_percent': discount_var.get(),
                'discount_amount': discount_amount,
                'total': total,
                'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            self.sales.append(sale)
            self.save_data()
            
            messagebox.showinfo("Success", f"Sale completed!\nTotal: Rs. {total:.2f}\nSale ID: {sale['sale_id']}")
            window.destroy()
            self.refresh_dashboard()
        
        tk.Button(right_frame, text="Complete Sale", command=complete_sale,
                 bg='#2ecc71', fg='white', font=('Arial', 12, 'bold'),
                 width=20, height=2).pack(pady=10)
    
    def show_return_exchange(self):
        window = tk.Toplevel(self.root)
        window.title("Return/Exchange")
        window.geometry("900x700")
        window.configure(bg='#ecf0f1')
        
        notebook = ttk.Notebook(window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Return Tab
        return_frame = tk.Frame(notebook, bg='#ecf0f1')
        notebook.add(return_frame, text="Return Product")
        
        tk.Label(return_frame, text="Enter Sale ID or Scan Product Barcode", 
                font=('Arial', 12, 'bold'), bg='#ecf0f1').pack(pady=20)
        
        search_frame = tk.Frame(return_frame, bg='#ecf0f1')
        search_frame.pack(pady=10)
        
        tk.Label(search_frame, text="Sale ID / Barcode:", bg='#ecf0f1', font=('Arial', 11)).pack(side=tk.LEFT, padx=5)
        search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=search_var, font=('Arial', 11), width=30)
        search_entry.pack(side=tk.LEFT, padx=5)
        
        # Sales list
        columns = ('Sale ID', 'Date', 'Items', 'Total')
        tree = ttk.Treeview(return_frame, columns=columns, show='tree headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=200)
        
        scrollbar = ttk.Scrollbar(return_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        def populate_sales(search_term=""):
            tree.delete(*tree.get_children())
            for sale in reversed(self.sales):
                if search_term.lower() in sale['sale_id'].lower():
                    items_str = ", ".join([f"{item['name']} x{item['quantity']}" for item in sale['items']])
                    tree.insert('', tk.END, values=(
                        sale['sale_id'], sale['date'], items_str, f"Rs. {sale['total']:.2f}"
                    ))
        
        populate_sales()
        search_var.trace('w', lambda *args: populate_sales(search_var.get()))
        
        def process_return():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Warning", "Please select a sale!")
                return
            
            values = tree.item(selected[0])['values']
            sale_id = values[0]
            
            # Find the sale
            sale = next((s for s in self.sales if s['sale_id'] == sale_id), None)
            if not sale:
                return
            
            # Show items for return
            return_win = tk.Toplevel(window)
            return_win.title(f"Return Items - {sale_id}")
            return_win.geometry("600x500")
            return_win.configure(bg='#ecf0f1')
            
            tk.Label(return_win, text="Select Items to Return", 
                    font=('Arial', 14, 'bold'), bg='#ecf0f1').pack(pady=20)
            
            items_frame = tk.Frame(return_win, bg='#ecf0f1')
            items_frame.pack(fill=tk.BOTH, expand=True, padx=20)
            
            return_items = {}
            
            for item in sale['items']:
                item_frame = tk.Frame(items_frame, bg='white', relief=tk.RAISED, borderwidth=1)
                item_frame.pack(fill=tk.X, pady=5, padx=10)
                
                var = tk.BooleanVar()
                chk = tk.Checkbutton(item_frame, variable=var, bg='white')
                chk.pack(side=tk.LEFT, padx=10)
                
                tk.Label(item_frame, text=f"{item['name']} - Qty: {item['quantity']} - Rs. {item['price']}", 
                        bg='white', font=('Arial', 10)).pack(side=tk.LEFT, padx=10)
                
                return_items[item['product_id']] = {'var': var, 'item': item}
            
            def confirm_return():
                returned = [pid for pid, data in return_items.items() if data['var'].get()]
                
                if not returned:
                    messagebox.showwarning("Warning", "Please select items to return!")
                    return
                
                # Update stock
                for pid in returned:
                    item = return_items[pid]['item']
                    if pid in self.products:
                        self.products[pid]['quantity'] += item['quantity']
                        self.stock_history.append({
                            'product_id': pid,
                            'action': 'Returned',
                            'quantity': item['quantity'],
                            'sale_id': sale_id,
                            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        })
                
                self.save_data()
                messagebox.showinfo("Success", "Return processed successfully!")
                return_win.destroy()
                self.refresh_dashboard()
            
            tk.Button(return_win, text="Process Return", command=confirm_return,
                     bg='#e74c3c', fg='white', font=('Arial', 12, 'bold'),
                     width=20, height=2).pack(pady=20)
        
        tk.Button(return_frame, text="Process Return", command=process_return,
                 bg='#e74c3c', fg='white', font=('Arial', 11, 'bold'),
                 width=20, height=2).pack(pady=10)
        
        # Exchange Tab
        exchange_frame = tk.Frame(notebook, bg='#ecf0f1')
        notebook.add(exchange_frame, text="Exchange Product")
        
        tk.Label(exchange_frame, text="Product Exchange Feature", 
                font=('Arial', 14, 'bold'), bg='#ecf0f1').pack(pady=20)
        tk.Label(exchange_frame, text="Select product to exchange and new product", 
                font=('Arial', 11), bg='#ecf0f1').pack(pady=10)
    
    def show_sales_report(self):
        window = tk.Toplevel(self.root)
        window.title("Sales Report")
        window.geometry("1000x700")
        window.configure(bg='#ecf0f1')
        
        # Filter frame
        filter_frame = tk.Frame(window, bg='#ecf0f1', padx=20, pady=10)
        filter_frame.pack(fill=tk.X)
        
        tk.Label(filter_frame, text="Filter by Date:", font=('Arial', 11, 'bold'), bg='#ecf0f1').pack(side=tk.LEFT, padx=5)
        
        date_options = ['Today', 'This Week', 'This Month', 'All Time']
        date_var = tk.StringVar(value='All Time')
        date_dropdown = ttk.Combobox(filter_frame, textvariable=date_var, values=date_options, width=15)
        date_dropdown.pack(side=tk.LEFT, padx=5)
        
        # Stats frame
        stats_frame = tk.Frame(window, bg='#ecf0f1', padx=20, pady=10)
        stats_frame.pack(fill=tk.X)
        
        total_sales_label = tk.Label(stats_frame, text="Total Sales: Rs. 0", 
                                     font=('Arial', 12, 'bold'), bg='#2ecc71', fg='white', padx=20, pady=10)
        total_sales_label.pack(side=tk.LEFT, padx=10)
        
        total_items_label = tk.Label(stats_frame, text="Items Sold: 0", 
                                     font=('Arial', 12, 'bold'), bg='#3498db', fg='white', padx=20, pady=10)
        total_items_label.pack(side=tk.LEFT, padx=10)
        
        avg_sale_label = tk.Label(stats_frame, text="Avg Sale: Rs. 0", 
                                  font=('Arial', 12, 'bold'), bg='#9b59b6', fg='white', padx=20, pady=10)
        avg_sale_label.pack(side=tk.LEFT, padx=10)
        
        # Sales list
        list_frame = tk.Frame(window, bg='#ecf0f1', padx=20)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ('Sale ID', 'Date', 'Items', 'Subtotal', 'Discount', 'Total')
        tree = ttk.Treeview(list_frame, columns=columns, show='tree headings', height=20)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill=tk.BOTH, expand=True, pady=10)
        
        def update_report():
            tree.delete(*tree.get_children())
            total = 0
            items_count = 0
            
            for sale in reversed(self.sales):
                items_str = ", ".join([f"{item['name']} x{item['quantity']}" for item in sale['items']])
                tree.insert('', tk.END, values=(
                    sale['sale_id'], sale['date'], items_str, 
                    f"Rs. {sale['subtotal']:.2f}", 
                    f"{sale['discount_percent']}%",
                    f"Rs. {sale['total']:.2f}"
                ))
                total += sale['total']
                items_count += sum(item['quantity'] for item in sale['items'])
            
            total_sales_label.config(text=f"Total Sales: Rs. {total:.2f}")
            total_items_label.config(text=f"Items Sold: {items_count}")
            avg_sale = total / len(self.sales) if self.sales else 0
            avg_sale_label.config(text=f"Avg Sale: Rs. {avg_sale:.2f}")
        
        update_report()
        
        def export_report():
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            if filename:
                with open(filename, 'w') as f:
                    f.write("SALES REPORT\n")
                    f.write("=" * 80 + "\n\n")
                    for sale in self.sales:
                        f.write(f"Sale ID: {sale['sale_id']}\n")
                        f.write(f"Date: {sale['date']}\n")
                        f.write(f"Items:\n")
                        for item in sale['items']:
                            f.write(f"  - {item['name']} x{item['quantity']} @ Rs. {item['price']}\n")
                        f.write(f"Subtotal: Rs. {sale['subtotal']:.2f}\n")
                        f.write(f"Discount: {sale['discount_percent']}%\n")
                        f.write(f"Total: Rs. {sale['total']:.2f}\n")
                        f.write("-" * 80 + "\n")
                messagebox.showinfo("Success", f"Report exported to {filename}")
        
        tk.Button(window, text="Export Report", command=export_report,
                 bg='#2ecc71', fg='white', font=('Arial', 11, 'bold'),
                 width=20, height=2).pack(pady=10)
    
    def show_stock_report(self):
        window = tk.Toplevel(self.root)
        window.title("Stock Report")
        window.geometry("1000x700")
        window.configure(bg='#ecf0f1')
        
        # Search frame
        search_frame = tk.Frame(window, bg='#ecf0f1', padx=20, pady=10)
        search_frame.pack(fill=tk.X)
        
        tk.Label(search_frame, text="Search:", font=('Arial', 11), bg='#ecf0f1').pack(side=tk.LEFT, padx=5)
        search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=search_var, font=('Arial', 11), width=40)
        search_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Label(search_frame, text="Category:", font=('Arial', 11), bg='#ecf0f1').pack(side=tk.LEFT, padx=20)
        categories = ['All'] + list(set(p['category'] for p in self.products.values()))
        category_var = tk.StringVar(value='All')
        category_dropdown = ttk.Combobox(search_frame, textvariable=category_var, values=categories, width=15)
        category_dropdown.pack(side=tk.LEFT, padx=5)
        
        # Stock list
        list_frame = tk.Frame(window, bg='#ecf0f1', padx=20)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ('ID', 'Name', 'Category', 'Size', 'Color', 'Purchase', 'Selling', 'Qty', 'Value')
        tree = ttk.Treeview(list_frame, columns=columns, show='tree headings', height=20)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill=tk.BOTH, expand=True, pady=10)
        
        def update_stock_list():
            tree.delete(*tree.get_children())
            search_term = search_var.get().lower()
            category = category_var.get()
            
            for pid, prod in self.products.items():
                if (search_term in prod['name'].lower() or search_term in pid.lower()) and \
                   (category == 'All' or prod['category'] == category):
                    value = prod['purchase_price'] * prod['quantity']
                    
                    # Color code low stock items
                    tags = ()
                    if prod['quantity'] <= prod['min_stock']:
                        tags = ('low_stock',)
                    
                    tree.insert('', tk.END, values=(
                        prod['id'], prod['name'], prod['category'], 
                        prod['size'], prod['color'], 
                        f"Rs. {prod['purchase_price']}", 
                        f"Rs. {prod['selling_price']}", 
                        prod['quantity'],
                        f"Rs. {value:.2f}"
                    ), tags=tags)
            
            tree.tag_configure('low_stock', background='#ffcccc')
        
        update_stock_list()
        search_var.trace('w', lambda *args: update_stock_list())
        category_var.trace('w', lambda *args: update_stock_list())
        
        def export_stock():
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv"), ("All files", "*.*")]
            )
            if filename:
                with open(filename, 'w') as f:
                    if filename.endswith('.csv'):
                        f.write("ID,Name,Category,Size,Color,Purchase Price,Selling Price,Quantity,Value\n")
                        for pid, prod in self.products.items():
                            value = prod['purchase_price'] * prod['quantity']
                            f.write(f"{prod['id']},{prod['name']},{prod['category']},{prod['size']},{prod['color']},"
                                  f"{prod['purchase_price']},{prod['selling_price']},{prod['quantity']},{value}\n")
                    else:
                        f.write("STOCK REPORT\n")
                        f.write("=" * 100 + "\n\n")
                        for pid, prod in self.products.items():
                            value = prod['purchase_price'] * prod['quantity']
                            f.write(f"ID: {prod['id']}\n")
                            f.write(f"Name: {prod['name']}\n")
                            f.write(f"Category: {prod['category']} | Size: {prod['size']} | Color: {prod['color']}\n")
                            f.write(f"Purchase Price: Rs. {prod['purchase_price']} | Selling Price: Rs. {prod['selling_price']}\n")
                            f.write(f"Quantity: {prod['quantity']} | Stock Value: Rs. {value:.2f}\n")
                            f.write("-" * 100 + "\n")
                messagebox.showinfo("Success", f"Stock report exported to {filename}")
        
        tk.Button(window, text="Export Stock Report", command=export_stock,
                 bg='#3498db', fg='white', font=('Arial', 11, 'bold'),
                 width=20, height=2).pack(pady=10)
    
    def show_low_stock_alert(self):
        window = tk.Toplevel(self.root)
        window.title("Low Stock Alert")
        window.geometry("900x600")
        window.configure(bg='#ecf0f1')
        
        tk.Label(window, text="⚠ Low Stock Items", font=('Arial', 18, 'bold'), 
                bg='#ecf0f1', fg='#e74c3c').pack(pady=20)
        
        # Low stock list
        list_frame = tk.Frame(window, bg='#ecf0f1', padx=20)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ('ID', 'Name', 'Category', 'Size', 'Current Qty', 'Min Level', 'Status')
        tree = ttk.Treeview(list_frame, columns=columns, show='tree headings', height=20)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill=tk.BOTH, expand=True, pady=10)
        
        low_stock_count = 0
        out_of_stock_count = 0
        
        for pid, prod in self.products.items():
            if prod['quantity'] <= prod['min_stock']:
                status = "OUT OF STOCK" if prod['quantity'] == 0 else "LOW STOCK"
                tags = ('out_stock',) if prod['quantity'] == 0 else ('low_stock',)
                
                tree.insert('', tk.END, values=(
                    prod['id'], prod['name'], prod['category'], 
                    prod['size'], prod['quantity'], prod['min_stock'], status
                ), tags=tags)
                
                if prod['quantity'] == 0:
                    out_of_stock_count += 1
                else:
                    low_stock_count += 1
        
        tree.tag_configure('low_stock', background='#fff3cd')
        tree.tag_configure('out_stock', background='#ffcccc')
        
        # Summary
        summary_frame = tk.Frame(window, bg='#ecf0f1', padx=20, pady=10)
        summary_frame.pack(fill=tk.X)
        
        tk.Label(summary_frame, text=f"Low Stock Items: {low_stock_count}", 
                font=('Arial', 12, 'bold'), bg='#fff3cd', padx=20, pady=10).pack(side=tk.LEFT, padx=10)
        tk.Label(summary_frame, text=f"Out of Stock Items: {out_of_stock_count}", 
                font=('Arial', 12, 'bold'), bg='#ffcccc', padx=20, pady=10).pack(side=tk.LEFT, padx=10)
    
    def calculate_total_stock_value(self):
        return sum(prod['purchase_price'] * prod['quantity'] for prod in self.products.values())
    
    def count_low_stock(self):
        return sum(1 for prod in self.products.values() if prod['quantity'] <= prod['min_stock'])
    
    def calculate_today_sales(self):
        today = datetime.now().strftime("%Y-%m-%d")
        return sum(sale['total'] for sale in self.sales if sale['date'].startswith(today))
    
    def refresh_dashboard(self):
        self.root.destroy()
        root = tk.Tk()
        app = GarmentShopManager(root)
        root.mainloop()
    
    def save_data(self):
        data = {
            'products': self.products,
            'sales': self.sales,
            'stock_history': self.stock_history,
            'barcode_counter': self.barcode_counter
        }
        with open('shop_data.json', 'w') as f:
            json.dump(data, f, indent=4)
    
    def load_data(self):
        if os.path.exists('shop_data.json'):
            try:
                with open('shop_data.json', 'r') as f:
                    data = json.load(f)
                    self.products = data.get('products', {})
                    self.sales = data.get('sales', [])
                    self.stock_history = data.get('stock_history', [])
                    self.barcode_counter = data.get('barcode_counter', 1)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load data: {str(e)}")
    
    def backup_data(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialfile=f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        if filename:
            self.save_data()
            import shutil
            shutil.copy('shop_data.json', filename)
            messagebox.showinfo("Success", f"Data backed up to {filename}")
    
    def restore_data(self):
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'r') as f:
                    data = json.load(f)
                    self.products = data.get('products', {})
                    self.sales = data.get('sales', [])
                    self.stock_history = data.get('stock_history', [])
                    self.barcode_counter = data.get('barcode_counter', 1)
                    self.save_data()
                messagebox.showinfo("Success", "Data restored successfully!")
                self.refresh_dashboard()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to restore data: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = GarmentShopManager(root)
    root.mainloop()