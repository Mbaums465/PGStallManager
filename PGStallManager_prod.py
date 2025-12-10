#!/usr/bin/env python3
"""
Sales Summary GUI - Python/Tkinter Version
Analyzes Project Gorgon Player Shop Log files
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import re
from datetime import datetime
from pathlib import Path
from collections import defaultdict


class SalesViewerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sales Viewer")
        self.root.geometry("480x570")
        
        # Center window on screen
        self.center_window()
        
        # Create GUI elements
        self.create_widgets()
        
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def create_widgets(self):
        """Create all GUI widgets"""
        
        # --- Folder Selection ---
        folder_frame = tk.Frame(self.root)
        folder_frame.pack(pady=5, padx=15, fill='x')
        
        tk.Label(folder_frame, text="Folder:").pack(side='left', padx=(0, 10))
        
        self.txt_folder = tk.Entry(folder_frame, width=35)
        # Set default folder path
        default_path = os.path.join(
            os.path.expanduser("~"),
            "AppData", "LocalLow", "Elder Game", "Project Gorgon", "Books"
        )
        self.txt_folder.insert(0, default_path)
        self.txt_folder.pack(side='left', padx=(0, 10))
        
        btn_browse = tk.Button(folder_frame, text="Browse...", command=self.browse_folder)
        btn_browse.pack(side='left')
        
        # --- Group By ---
        group_frame = tk.Frame(self.root)
        group_frame.pack(pady=3, padx=15, fill='x')
        
        tk.Label(group_frame, text="Group By:").pack(side='left', padx=(0, 10))
        
        self.cmb_group = ttk.Combobox(group_frame, width=20, state='readonly')
        self.cmb_group['values'] = ("Buyer", "Item", "Year", "Month", "Week", "Day")
        self.cmb_group.current(1)  # Default to Item
        self.cmb_group.pack(side='left')
        
        # --- Buyer Filter ---
        buyer_frame = tk.Frame(self.root)
        buyer_frame.pack(pady=3, padx=15, fill='x')
        
        tk.Label(buyer_frame, text="Buyer Filter:").pack(side='left', padx=(0, 10))
        
        self.txt_buyer = tk.Entry(buyer_frame, width=20)
        self.txt_buyer.pack(side='left')
        
        # --- Item Filter ---
        item_frame = tk.Frame(self.root)
        item_frame.pack(pady=3, padx=15, fill='x')
        
        tk.Label(item_frame, text="Item Filter:").pack(side='left', padx=(0, 10))
        
        self.txt_item = tk.Entry(item_frame, width=20)
        self.txt_item.pack(side='left', padx=(0, 10))
        
        self.chk_exact_var = tk.BooleanVar()
        self.chk_exact = tk.Checkbutton(item_frame, text="Exact", variable=self.chk_exact_var)
        self.chk_exact.pack(side='left')
        
        # --- Date Filters ---
        start_frame = tk.Frame(self.root)
        start_frame.pack(pady=3, padx=15, fill='x')
        
        tk.Label(start_frame, text="Start Date (MM/DD/YYYY):").pack(side='left', padx=(0, 10))
        
        self.txt_start = tk.Entry(start_frame, width=15)
        # Default to January 1st of current year
        self.txt_start.insert(0, datetime.now().strftime("01/01/%Y"))
        self.txt_start.pack(side='left')
        
        end_frame = tk.Frame(self.root)
        end_frame.pack(pady=3, padx=15, fill='x')
        
        tk.Label(end_frame, text="End Date (MM/DD/YYYY):").pack(side='left', padx=(0, 10))
        
        self.txt_end = tk.Entry(end_frame, width=15)
        # Default to today
        self.txt_end.insert(0, datetime.now().strftime("%m/%d/%Y"))
        self.txt_end.pack(side='left')
        
        # --- Top N ---
        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=3, padx=15, fill='x')
        
        tk.Label(top_frame, text="Top N Results:").pack(side='left', padx=(0, 10))
        
        self.txt_top = tk.Entry(top_frame, width=10)
        self.txt_top.insert(0, "100")
        self.txt_top.pack(side='left')
        
        # --- Sort By ---
        sort_frame = tk.Frame(self.root)
        sort_frame.pack(pady=3, padx=15, fill='x')
        
        tk.Label(sort_frame, text="Sort By:").pack(side='left', padx=(0, 10))
        
        self.cmb_sort = ttk.Combobox(sort_frame, width=20, state='readonly')
        self.cmb_sort['values'] = ("Group", "TotalSold", "TotalEarned", "AvgPrice")
        self.cmb_sort.current(2)  # Default to TotalEarned
        self.cmb_sort.pack(side='left')
        
        # --- Run Button ---
        btn_run = tk.Button(self.root, text="Run", command=self.run_analysis, 
                           width=10, height=1)
        btn_run.pack(pady=8)
        
        # --- Summary Label ---
        self.lbl_summary = tk.Label(self.root, text="", anchor='w', justify='left')
        self.lbl_summary.pack(pady=(3, 1), padx=15, fill='x')
        
        # --- Total Earned Label (pack FIRST with side='bottom' so it stays at bottom) ---
        self.lbl_total = tk.Label(self.root, text="Total Earned: 0", 
                                 font=('TkDefaultFont', 10, 'bold'), anchor='e')
        self.lbl_total.pack(side='bottom', pady=(3, 5), padx=15, fill='x')
        
        # --- Output Treeview (pack AFTER total label, fills remaining space) ---
        output_frame = tk.Frame(self.root)
        output_frame.pack(pady=(3, 0), padx=(15, 5), fill='both', expand=True)
        
        # Create Treeview with columns
        self.tree = ttk.Treeview(output_frame, columns=('Group', 'TotalSold', 'TotalEarned', 'AvgPrice'), 
                                 show='headings')
        
        # Define column headings and make them clickable for sorting
        self.tree.heading('Group', text='Group', command=lambda: self.sort_treeview('Group', False))
        self.tree.heading('TotalSold', text='TotalSold', command=lambda: self.sort_treeview('TotalSold', True))
        self.tree.heading('TotalEarned', text='TotalEarned', command=lambda: self.sort_treeview('TotalEarned', True))
        self.tree.heading('AvgPrice', text='AvgPrice', command=lambda: self.sort_treeview('AvgPrice', True))
        
        # Configure column widths and alignment
        self.tree.column('Group', width=90, anchor='w')
        self.tree.column('TotalSold', width=100, anchor='e')
        self.tree.column('TotalEarned', width=120, anchor='e')
        self.tree.column('AvgPrice', width=100, anchor='e')
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(output_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Store current results for sorting
        self.current_results = []
        self.sort_column = None
        self.sort_reverse = False
        
    def browse_folder(self):
        """Open folder browser dialog"""
        folder = filedialog.askdirectory(initialdir=self.txt_folder.get())
        if folder:
            self.txt_folder.delete(0, tk.END)
            self.txt_folder.insert(0, folder)
    
    def sort_treeview(self, column, is_numeric):
        """Sort treeview by column when header is clicked"""
        # Toggle sort direction if clicking same column
        if self.sort_column == column:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_column = column
            self.sort_reverse = False if column == 'Group' else True  # Group ascending by default, others descending
        
        # Map column names to result dict keys
        col_map = {
            'Group': 'Group',
            'TotalSold': 'TotalSold',
            'TotalEarned': 'TotalEarned',
            'AvgPrice': 'AvgPrice'
        }
        
        # Sort the current results
        sort_key = col_map[column]
        self.current_results.sort(key=lambda x: x[sort_key], reverse=self.sort_reverse)
        
        # Refresh display
        self.display_results(self.current_results)
    
    def display_results(self, results):
        """Display results in the treeview"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Insert new items
        total_earned_sum = 0
        for r in results:
            self.tree.insert('', 'end', values=(
                r['Group'],
                f"{r['TotalSold']:,}",
                f"{r['TotalEarned']:,}",
                f"{int(r['AvgPrice']):,}"
            ))
            total_earned_sum += r['TotalEarned']
        
        # Update total earned label
        self.lbl_total.config(text=f"Total Earned: {total_earned_sum:,}")
            
    def parse_file_date(self, filename):
        """
        Extract date from filename in format PlayerShopLog_YYMMDD_HHMMSS.txt
        Returns tuple: (date_string, timestamp_string, datetime_obj)
        """
        match = re.match(r'^PlayerShopLog_(\d{6})_(\d+)$', filename)
        if not match:
            return None
            
        date_str = match.group(1)
        time_str = match.group(2)
        
        yy = int(date_str[0:2])
        mm = int(date_str[2:4])
        dd = int(date_str[4:6])
        
        try:
            date_obj = datetime(2000 + yy, mm, dd)
            return (date_str, time_str, date_obj)
        except ValueError:
            return None
            
    def get_latest_files_by_date(self, folder, start_date, end_date):
        """
        Get the latest file for each date within the date range.
        
        This is the complex logic from the PowerShell script:
        1. Find all files matching PlayerShopLog_*.txt
        2. Filter by date range
        3. Group by date (YYMMDD part)
        4. For each date, select the file with the highest timestamp
        
        Returns: dict mapping date_obj to file_path
        """
        files_by_date = defaultdict(list)
        
        # Find all matching files
        pattern = re.compile(r'^PlayerShopLog_(\d{6})_(\d+)\.txt$')
        
        try:
            for filename in os.listdir(folder):
                match = pattern.match(filename)
                if not match:
                    continue
                    
                basename = filename[:-4]  # Remove .txt extension
                parsed = self.parse_file_date(basename)
                
                if parsed is None:
                    continue
                    
                date_str, time_str, date_obj = parsed
                
                # Filter by date range
                if date_obj < start_date or date_obj > end_date:
                    continue
                    
                # Group by date
                file_path = os.path.join(folder, filename)
                files_by_date[date_obj].append((int(time_str), file_path))
                
        except Exception as e:
            messagebox.showerror("Error", f"Error reading folder: {str(e)}")
            return {}
            
        # For each date, select the file with the highest timestamp
        latest_files = {}
        for date_obj, file_list in files_by_date.items():
            # Sort by timestamp (descending) and take the first (latest)
            file_list.sort(reverse=True)
            latest_files[date_obj] = file_list[0][1]  # Get the file path
            
        return latest_files
        
    def parse_sales_data(self, file_path, date_obj):
        """
        Parse sales data from a log file.
        Returns list of sales dictionaries.
        """
        sales = []
        
        # Regex pattern to match purchase lines
        pattern = re.compile(
            r"- (?P<buyer>\S+) bought\s+(?P<item>.+?)(?:\s*x(?P<qty>\d+))?\s+at a cost.*=\s*(?P<earned>\d+)$"
        )
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if 'bought' not in line:
                        continue
                        
                    match = pattern.search(line)
                    if match:
                        sales.append({
                            'Buyer': match.group('buyer'),
                            'Item': match.group('item').strip(),
                            'Quantity': int(match.group('qty')) if match.group('qty') else 1,
                            'Earned': int(match.group('earned')),
                            'SaleDate': date_obj
                        })
        except Exception as e:
            # Skip files that can't be read
            pass
            
        return sales
        
    def apply_filters(self, sales_data, buyer_filter, item_filter, item_exact):
        """Apply buyer and item filters to sales data"""
        filtered = sales_data
        
        if buyer_filter:
            filtered = [s for s in filtered if s['Buyer'] == buyer_filter]
            
        if item_filter:
            if item_exact:
                filtered = [s for s in filtered if s['Item'] == item_filter]
            else:
                item_lower = item_filter.lower()
                filtered = [s for s in filtered if item_lower in s['Item'].lower()]
                
        return filtered
        
    def get_group_key(self, sale, group_by):
        """Get the grouping key for a sale based on group_by option"""
        if group_by == "Buyer":
            return sale['Buyer']
        elif group_by == "Item":
            return sale['Item']
        elif group_by == "Year":
            return str(sale['SaleDate'].year)
        elif group_by == "Month":
            return sale['SaleDate'].strftime("%Y-%m")
        elif group_by == "Week":
            # Python's strftime %U for week number (Sunday as first day)
            return sale['SaleDate'].strftime("%Y-%U")
        elif group_by == "Day":
            return sale['SaleDate'].strftime("%Y-%m-%d")
        else:
            return sale['Item']
            
    def group_and_aggregate(self, sales_data, group_by):
        """Group sales data and calculate aggregates"""
        groups = defaultdict(list)
        
        for sale in sales_data:
            key = self.get_group_key(sale, group_by)
            groups[key].append(sale)
            
        results = []
        for group_name, group_sales in groups.items():
            total_sold = sum(s['Quantity'] for s in group_sales)
            total_earned = sum(s['Earned'] for s in group_sales)
            avg_price = round(total_earned / total_sold, 0) if total_sold > 0 else 0
            
            results.append({
                'Group': group_name,
                'TotalSold': total_sold,
                'TotalEarned': total_earned,
                'AvgPrice': avg_price
            })
            
        return results
        
    def run_analysis(self):
        """Main analysis function - triggered by Run button"""
        try:
            # Get parameters from GUI
            folder = self.txt_folder.get()
            
            if not os.path.exists(folder):
                messagebox.showerror("Error", "Please select a valid folder.")
                return
                
            group_by = self.cmb_group.get()
            buyer_filter = self.txt_buyer.get().strip()
            item_filter = self.txt_item.get().strip()
            item_exact = self.chk_exact_var.get()
            sort_by = self.cmb_sort.get()
            
            try:
                top_n = int(self.txt_top.get())
            except ValueError:
                top_n = 0
                
            try:
                start_date = datetime.strptime(self.txt_start.get(), "%m/%d/%Y")
                end_date = datetime.strptime(self.txt_end.get(), "%m/%d/%Y")
            except ValueError:
                messagebox.showerror("Error", "Invalid date format. Use MM/DD/YYYY")
                return
                
            # Get latest files by date
            latest_files = self.get_latest_files_by_date(folder, start_date, end_date)
            
            if not latest_files:
                self.lbl_summary.config(text="No files found in the specified date range.")
                self.current_results = []
                self.display_results([])
                return
                
            # Parse sales data from all files
            all_sales = []
            for date_obj, file_path in latest_files.items():
                sales = self.parse_sales_data(file_path, date_obj)
                all_sales.extend(sales)
                
            if not all_sales:
                self.lbl_summary.config(text="No sales data found in the files.")
                self.current_results = []
                self.display_results([])
                return
                
            # Apply filters
            filtered_sales = self.apply_filters(all_sales, buyer_filter, item_filter, item_exact)
            
            if not filtered_sales:
                self.lbl_summary.config(text="No sales found for the applied filters.")
                self.current_results = []
                self.display_results([])
                return
                
            # Group and aggregate
            results = self.group_and_aggregate(filtered_sales, group_by)
            
            # Sort results
            sort_descending = True
            if sort_by == "Group":
                sort_descending = False
                
            results.sort(key=lambda x: x[sort_by], reverse=sort_descending)
            
            # Apply top N filter
            if top_n > 0:
                results = results[:top_n]
            
            # Store results and display
            self.current_results = results
            self.sort_column = sort_by
            self.sort_reverse = sort_descending
            
            # Update summary label
            summary_text = f"Showing totals grouped by {group_by} (sorted by {sort_by})"
            if top_n > 0:
                summary_text += f" - Top {top_n} results"
            self.lbl_summary.config(text=summary_text)
            
            # Display results in treeview
            self.display_results(results)
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")


def main():
    root = tk.Tk()
    app = SalesViewerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()