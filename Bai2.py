import tkinter as tk
from tkinter import messagebox
import psycopg2
from psycopg2 import sql

class DatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Database App")

        # Login Screen
        self.username = tk.StringVar()
        self.password = tk.StringVar()

        self.create_login_widgets()

    def create_login_widgets(self):
        # Create login frame
        login_frame = tk.Frame(self.root)
        login_frame.pack(padx=20, pady=20)

        tk.Label(login_frame, text="Username:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        tk.Entry(login_frame, textvariable=self.username).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(login_frame, text="Password:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        tk.Entry(login_frame, textvariable=self.password, show="*").grid(row=1, column=1, padx=5, pady=5)

        tk.Button(login_frame, text="Login", command=self.login).grid(row=2, columnspan=2, pady=10)

    def login(self):
        # Hardcoded credentials for simplicity
        if self.username.get() == "admin" and self.password.get() == "password":
            messagebox.showinfo("Login Success", "Welcome!")
            self.create_main_interface()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password!")

    def create_main_interface(self):
        # Remove login screen
        for widget in self.root.winfo_children():
            widget.destroy()

        # Database connection fields
        self.db_name = tk.StringVar(value='dbtest')
        self.user = tk.StringVar(value='postgres')
        self.password = tk.StringVar(value='1234')
        self.host = tk.StringVar(value='localhost')
        self.port = tk.StringVar(value='5432')
        self.table_name = tk.StringVar(value='sinhvien')

        # Create the main GUI elements
        self.create_widgets()

    def create_widgets(self):
        # Connection section
        connection_frame = tk.Frame(self.root)
        connection_frame.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        tk.Label(connection_frame, text="DB Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        tk.Entry(connection_frame, textvariable=self.db_name).grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(connection_frame, text="User:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        tk.Entry(connection_frame, textvariable=self.user).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(connection_frame, text="Password:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        tk.Entry(connection_frame, textvariable=self.password, show="*").grid(row=2, column=1, padx=5, pady=5)

        tk.Label(connection_frame, text="Host:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        tk.Entry(connection_frame, textvariable=self.host).grid(row=3, column=1, padx=5, pady=5)

        tk.Label(connection_frame, text="Port:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        tk.Entry(connection_frame, textvariable=self.port).grid(row=4, column=1, padx=5, pady=5)

        tk.Button(connection_frame, text="Connect", command=self.connect_db).grid(row=5, columnspan=2, pady=10)

        # Query section
        query_frame = tk.Frame(self.root)
        query_frame.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        tk.Label(query_frame, text="Table Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        tk.Entry(query_frame, textvariable=self.table_name).grid(row=0, column=1, padx=5, pady=5)

        tk.Button(query_frame, text="Load Data", command=self.load_data).grid(row=1, columnspan=2, pady=10)

        # Insert section (remove "Ngày sinh" and "CCCD")
        insert_frame = tk.Frame(self.root)
        insert_frame.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.column1 = tk.StringVar()
        self.column2 = tk.StringVar()

        tk.Label(insert_frame, text="Ho ten:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        tk.Entry(insert_frame, textvariable=self.column1).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(insert_frame, text="MSSV:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        tk.Entry(insert_frame, textvariable=self.column2).grid(row=1, column=1, padx=5, pady=5)

        tk.Button(insert_frame, text="Insert Data", command=self.insert_data).grid(row=2, columnspan=2, pady=10)

        # Data display section on the right
        self.data_display = tk.Text(self.root, height=20, width=60)
        self.data_display.grid(row=0, column=1, rowspan=3, padx=10, pady=10, sticky="nsew")

    def connect_db(self):
        try:
            self.conn = psycopg2.connect(
                dbname=self.db_name.get(),
                user=self.user.get(),
                password=self.password.get(),
                host=self.host.get(),
                port=self.port.get()
            )
            self.cur = self.conn.cursor()
            messagebox.showinfo("Success", "Connected to the database successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error connecting to the database: {e}")

    def load_data(self):
        try:
            query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(self.table_name.get()))
            self.cur.execute(query)
            rows = self.cur.fetchall()
            self.data_display.delete(1.0, tk.END)
            for row in rows:
                self.data_display.insert(tk.END, f"{row}\n")
        except Exception as e:
            messagebox.showerror("Error", f"Error loading data: {e}")

    def insert_data(self):
        try:
            insert_query = sql.SQL("INSERT INTO {} (MSSV, HoTen) VALUES (%s, %s)").format(sql.Identifier(self.table_name.get()))
            data_to_insert = (self.column1.get(), self.column2.get())
            self.cur.execute(insert_query, data_to_insert)
            self.conn.commit()
            messagebox.showinfo("Success", "Data inserted successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error inserting data: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1000x600")  # Increase window size for better layout
    app = DatabaseApp(root)
    root.mainloop()
