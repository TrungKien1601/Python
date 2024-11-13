import tkinter as tk
from tkinter import messagebox, font

# Hàm xác minh đăng nhập
def login():
    username = entry_username.get()
    password = entry_password.get()
    
    # Kiểm tra tên đăng nhập và mật khẩu
    if username == "admin" and password == "password":  # Thay bằng tài khoản thực tế
        login_window.destroy()  # Đóng cửa sổ đăng nhập nếu đăng nhập thành công
        open_calculator()  # Mở giao diện máy tính
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

# Hàm mở giao diện máy tính
def open_calculator():
    # Tạo cửa sổ chính cho máy tính
    calculator = tk.Tk()
    calculator.title("Calculator")
    calculator.geometry("400x400")
    calculator.config(bg="#2C3E50")

    # Hàm tính toán
    def calculate(operation):
        try:
            num1 = float(entry_num1.get())
            num2 = float(entry_num2.get())
            if operation == 'add':
                result = num1 + num2
            elif operation == 'subtract':
                result = num1 - num2
            elif operation == 'multiply':
                result = num1 * num2
            elif operation == 'divide':
                if num2 == 0:
                    result = "Error (division by zero)"
                else:
                    result = num1 / num2
            label_result.config(text=f"Result: {result}")
        except ValueError:
            label_result.config(text="Invalid input")

    # Hàm thay đổi màu nền và màu nút
    def change_theme(bg_color, btn_color):
        calculator.config(bg=bg_color)
        label_num1.config(bg=bg_color)
        label_num2.config(bg=bg_color)
        label_result.config(bg=bg_color)
        button_add.config(bg=btn_color)
        button_subtract.config(bg=btn_color)
        button_multiply.config(bg=btn_color)
        button_divide.config(bg=btn_color)
        exit_button.config(bg=btn_color)
        clear_button.config(bg=btn_color)

    # Hàm thoát ứng dụng
    def exit_app():
        calculator.destroy()

    # Hàm thay đổi font chữ
    def change_font(new_font):
        label_num1.config(font=(new_font, 14))
        label_num2.config(font=(new_font, 14))
        label_result.config(font=(new_font, 16, "bold"))
        button_add.config(font=(new_font, 14))
        button_subtract.config(font=(new_font, 14))
        button_multiply.config(font=(new_font, 14))
        button_divide.config(font=(new_font, 14))
        exit_button.config(font=(new_font, 14))
        clear_button.config(font=(new_font, 14))

    # Hàm xóa dữ liệu
    def clear_fields():
        entry_num1.delete(0, tk.END)
        entry_num2.delete(0, tk.END)
        label_result.config(text="Result:")

    # Tạo các widget
    label_num1 = tk.Label(calculator, text="Number 1:", bg="#2C3E50", fg="#ECF0F1", font=("Arial", 14))
    label_num1.grid(row=0, column=0, padx=20, pady=10, sticky="w")

    entry_num1 = tk.Entry(calculator, font=("Arial", 14), width=15, bd=5, relief="solid")
    entry_num1.grid(row=0, column=1, padx=20, pady=10)

    label_num2 = tk.Label(calculator, text="Number 2:", bg="#2C3E50", fg="#ECF0F1", font=("Arial", 14))
    label_num2.grid(row=1, column=0, padx=20, pady=10, sticky="w")

    entry_num2 = tk.Entry(calculator, font=("Arial", 14), width=15, bd=5, relief="solid")
    entry_num2.grid(row=1, column=1, padx=20, pady=10)

    # Các nút bấm cho các phép toán, căn giữa
    button_frame = tk.Frame(calculator, bg="#2C3E50")
    button_frame.grid(row=2, column=0, columnspan=2, pady=20)

    button_add = tk.Button(button_frame, text="+", command=lambda: calculate('add'), font=("Arial", 14), width=5, height=2, bg="#2980B9", fg="white", relief="flat")
    button_add.grid(row=0, column=0, padx=5)

    button_subtract = tk.Button(button_frame, text="-", command=lambda: calculate('subtract'), font=("Arial", 14), width=5, height=2, bg="#2980B9", fg="white", relief="flat")
    button_subtract.grid(row=0, column=1, padx=5)

    button_multiply = tk.Button(button_frame, text="*", command=lambda: calculate('multiply'), font=("Arial", 14), width=5, height=2, bg="#2980B9", fg="white", relief="flat")
    button_multiply.grid(row=0, column=2, padx=5)

    button_divide = tk.Button(button_frame, text="/", command=lambda: calculate('divide'), font=("Arial", 14), width=5, height=2, bg="#2980B9", fg="white", relief="flat")
    button_divide.grid(row=0, column=3, padx=5)

    # Label hiển thị kết quả
    label_result = tk.Label(calculator, text="Result:", bg="#2C3E50", fg="#ECF0F1", font=("Arial", 16, "bold"))
    label_result.grid(row=3, columnspan=2, padx=20, pady=20)

    # Tạo menu để đổi màu, đổi font và thoát ứng dụng
    menu_bar = tk.Menu(calculator)
    theme_menu = tk.Menu(menu_bar, tearoff=0)
    font_menu = tk.Menu(menu_bar, tearoff=0)
    
    menu_bar.add_cascade(label="Theme", menu=theme_menu)
    menu_bar.add_cascade(label="Font", menu=font_menu)
    menu_bar.add_command(label="Exit", command=exit_app)  # Thêm tùy chọn Exit vào menu

    # Các tùy chọn màu sắc
    theme_menu.add_command(label="Dark Blue", command=lambda: change_theme("#2C3E50", "#2980B9"))
    theme_menu.add_command(label="Light Blue", command=lambda: change_theme("#D6EAF8", "#5DADE2"))
    theme_menu.add_command(label="Green", command=lambda: change_theme("#27AE60", "#2ECC71"))
    theme_menu.add_command(label="Gray", command=lambda: change_theme("#BDC3C7", "#7F8C8D"))
    theme_menu.add_command(label="Orange", command=lambda: change_theme("#E67E22", "#D35400"))

    # Các tùy chọn font chữ
    font_menu.add_command(label="Arial", command=lambda: change_font("Arial"))
    font_menu.add_command(label="Courier", command=lambda: change_font("Courier"))
    font_menu.add_command(label="Times New Roman", command=lambda: change_font("Times New Roman"))
    font_menu.add_command(label="Helvetica", command=lambda: change_font("Helvetica"))
    font_menu.add_command(label="Verdana", command=lambda: change_font("Verdana"))

    # Gắn menu vào cửa sổ
    calculator.config(menu=menu_bar)

    # Nút Clear
    clear_button = tk.Button(calculator, text="Clear", command=clear_fields, font=("Arial", 14), bg="#F39C12", fg="white")
    clear_button.grid(row=4, column=0, pady=10)

    # Nút Exit
    exit_button = tk.Button(calculator, text="Exit", command=exit_app, font=("Arial", 14), bg="#E74C3C", fg="white")
    exit_button.grid(row=4, column=1, pady=10)

# Tạo cửa sổ đăng nhập
login_window = tk.Tk()
login_window.title("Login")
login_window.geometry("300x250")
login_window.config(bg="#34495E")

# Giao diện đăng nhập
label_username = tk.Label(login_window, text="Username:", bg="#34495E", fg="#ECF0F1", font=("Arial", 12))
label_username.pack(pady=10)
entry_username = tk.Entry(login_window, font=("Arial", 12))
entry_username.pack()

label_password = tk.Label(login_window, text="Password:", bg="#34495E", fg="#ECF0F1", font=("Arial", 12))
label_password.pack(pady=10)
entry_password = tk.Entry(login_window, font=("Arial", 12), show="*")
entry_password.pack()

login_button = tk.Button(login_window, text="Login", command=login, font=("Arial", 12), bg="#2980B9", fg="white")
login_button.pack(pady=10)

# Nút thoát trong cửa sổ đăng nhập
exit_button = tk.Button(login_window, text="Exit", command=login_window.quit, font=("Arial", 12), bg="#E74C3C", fg="white")
exit_button.pack(pady=5)

login_window.mainloop()
