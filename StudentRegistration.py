import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os

class Student:
    def __init__(self, student_id, name, age, course,email, photo_path=None):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.course = course
        self.email = email
        self.photo_path = photo_path

class StudentRegistrationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Registration with Photos")
        self.root.geometry("750x500")
        self.students = {}

        # Variables for form input
        self.var_id = tk.StringVar()
        self.var_name = tk.StringVar()
        self.var_age = tk.StringVar()
        self.var_course = tk.StringVar()
        self.var_email= tk.StringVar()
        self.var_photo_path = None

        # Left frame (Form)
        form_frame = ttk.Frame(root, padding=20)
        form_frame.pack(side=tk.LEFT, fill=tk.Y)

        ttk.Label(form_frame, text="Student Registration", font=("Arial", 16, "bold")).pack(pady=10)

        ttk.Label(form_frame, text="Student ID:").pack(anchor=tk.W)
        ttk.Entry(form_frame, textvariable=self.var_id, width=30).pack()

        ttk.Label(form_frame, text="Name:").pack(anchor=tk.W, pady=(10, 0))
        ttk.Entry(form_frame, textvariable=self.var_name, width=30).pack()

        ttk.Label(form_frame, text="Age:").pack(anchor=tk.W, pady=(10, 0))
        ttk.Entry(form_frame, textvariable=self.var_age, width=30).pack()

        ttk.Label(form_frame, text="Course:").pack(anchor=tk.W, pady=(10, 0))
        ttk.Entry(form_frame, textvariable=self.var_course, width=30).pack()

        ttk.Label(form_frame, text="email:").pack(anchor=tk.W, pady=(10, 0))
        ttk.Entry(form_frame, textvariable=self.var_email, width=30).pack()

        photo_button = ttk.Button(form_frame, text="Upload Photo", command=self.upload_photo)
        photo_button.pack(pady=(15,0))

        self.photo_label = ttk.Label(form_frame, text="No photo selected", relief=tk.SUNKEN, width=30, anchor='center')
        self.photo_label.pack(pady=10)

        ttk.Button(form_frame, text="Register Student", command=self.register_student).pack(pady=10)

        # Right frame (Student list)
        list_frame = ttk.Frame(root, padding=20)
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        ttk.Label(list_frame, text="Registered Students", font=("Arial", 16, "bold")).pack(pady=10)

        columns = ("id", "name", "age", "course","email")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", selectmode="browse")
        for col in columns:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, anchor=tk.CENTER, width=100)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_student_select)

        # Image display
        self.img_canvas = tk.Canvas(list_frame, width=180, height=180, bg="white", bd=2, relief=tk.SUNKEN)
        self.img_canvas.pack(pady=10)

        self.current_img = None

        # Buttons for update and delete
        btn_frame = ttk.Frame(list_frame)
        btn_frame.pack(pady=5, fill=tk.X)

        ttk.Button(btn_frame, text="Update Selected", command=self.update_student).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Delete Selected", command=self.delete_student).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Clear Fields", command=self.clear_form).pack(side=tk.RIGHT, padx=2)

    def upload_photo(self):
        filetypes = [("Image files", "*.png *.jpg *.jpeg *.bmp *.gif"), ("All files", "*.*")]
        filepath = filedialog.askopenfilename(title="Select Student Photo", filetypes=filetypes)
        if filepath:
            self.var_photo_path = filepath
            self.photo_label.config(text=os.path.basename(filepath))
        else:
            self.var_photo_path = None
            self.photo_label.config(text="No photo selected")

    def register_student(self):
        sid = self.var_id.get().strip()
        name = self.var_name.get().strip()
        age = self.var_age.get().strip()
        course = self.var_course.get().strip()
        email = self.var_email.get().strip()

        if not sid or not name or not age or not course:
            messagebox.showerror("Input Error", "Please fill all fields.")
            return
        if not age.isdigit() or not (1 <= int(age) <= 130):
            messagebox.showerror("Input Error", "Age must be a valid number between 1 and 130.")
            return
        if sid in self.students:
            messagebox.showerror("Duplicate ID", "Student ID already exists.")
            return

        student = Student(sid, name, int(age), course,email, self.var_photo_path)
        self.students[sid] = student
        self.tree.insert("", tk.END, iid=sid, values=(sid, name, age, course,email))
        messagebox.showinfo("Success", f"Student '{name}' registered successfully.")
        self.clear_form()

    def on_student_select(self, event):
        selected = self.tree.focus()
        if not selected:
            return
        student = self.students.get(selected)
        if student:
            self.var_id.set(student.student_id)
            self.var_name.set(student.name)
            self.var_age.set(str(student.age))
            self.var_course.set(student.course)
            self.var_email.set(student.email)
            self.var_photo_path = student.photo_path
            self.photo_label.config(text=os.path.basename(student.photo_path) if student.photo_path else "No photo selected")
            self.show_photo(student.photo_path)
        else:
            self.clear_form()

    def show_photo(self, photo_path):
        self.img_canvas.delete("all")
        if photo_path and os.path.exists(photo_path):
            try:
                img = Image.open(photo_path)
                img.thumbnail((180, 180))
                self.current_img = ImageTk.PhotoImage(img)
                self.img_canvas.create_image(90, 90, image=self.current_img)
            except Exception as e:
                self.img_canvas.create_text(90, 90, text="Cannot load image", fill="red")
        else:
            self.img_canvas.create_text(90, 90, text="No Image", fill="gray")

    def update_student(self):
        sid = self.var_id.get().strip()
        if sid not in self.students:
            messagebox.showerror("Error", "Select a valid student from the list to update.")
            return
        name = self.var_name.get().strip()
        age = self.var_age.get().strip()
        course = self.var_course.get().strip()
        email = self.var_email.get().strip()


        if not sid or not name or not age or not course:
            messagebox.showerror("Input Error", "Please fill all fields.")
            return
        if not age.isdigit() or not (1 <= int(age) <= 130):
            messagebox.showerror("Input Error", "Age must be a valid number between 1 and 130.")
            return

        student = self.students[sid]
        student.name = name
        student.age = int(age)
        student.course = course
        student.email = email
        student.photo_path = self.var_photo_path

        self.tree.item(sid, values=(sid, name, age, course,email
                                    ))
        messagebox.showinfo("Success", f"Student '{name}' updated successfully.")
        self.clear_form()

    def delete_student(self):
        sid = self.var_id.get().strip()
        if sid not in self.students:
            messagebox.showerror("Error", "Select a valid student from the list to delete.")
            return
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete student '{self.students[sid].name}'?")
        if confirm:
            del self.students[sid]
            self.tree.delete(sid)
            self.clear_form()
            messagebox.showinfo("Deleted", "Student deleted successfully.")

    def clear_form(self):
        self.var_id.set("")
        self.var_name.set("")
        self.var_age.set("")
        self.var_course.set("")
        self.var_email.set("")
        self.var_photo_path = None
        self.photo_label.config(text="No photo selected")
        self.img_canvas.delete("all")
        self.current_img = None
        self.tree.selection_remove(self.tree.selection())

if __name__ == "__main__":
    try:
        from PIL import Image, ImageTk
    except ImportError:
        import sys
        sys.exit("Pillow module required. Please install it with 'pip install Pillow' and run again.")

    root = tk.Tk()
    app = StudentRegistrationApp(root)
    root.mainloop()

