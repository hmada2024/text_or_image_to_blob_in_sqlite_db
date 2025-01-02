import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import sqlite3
from PIL import Image  # لضمان تحويل الصورة إلى BLOB
import io
import os

class ImageToBlobApp:
    def __init__(self, master):
        self.master = master
        master.title("محول الصورة إلى BLOB")

        # إضافة وصف التطبيق
        description_frame = ttk.LabelFrame(master, text="وصف التطبيق")
        description_frame.pack(padx=10, pady=10, fill="x")

        description_label = tk.Label(description_frame, text=(
            "أهلاً بك في تطبيق محول الصورة إلى BLOB!\n"
            "يتيح لك هذا التطبيق تحويل الصور الموجودة على جهاز الكمبيوتر إلى بيانات BLOB\n"
            "وإدخالها في أحد الأعمدة في أحد الجداول داخل قاعدة بيانات SQLite.\n\n"
            "الخطوات:\n"
            "1. اختر ملف قاعدة البيانات.\n"
            "2. اختر الجدول والعمود الذي سيتم تخزين الصورة فيه.\n"
            "3. اضغط على زر 'تصفح' لاختيار الصورة.\n"
            "4. اضغط على زر 'تحويل الصورة إلى BLOB' للبدء في التحويل.\n\n"
            "تمتع باستخدام التطبيق!"
        ), anchor="center", justify="center", wraplength=400)
        description_label.pack(padx=10, pady=10)

        # متغيرات لتخزين الاختيارات
        self.db_path = tk.StringVar()
        self.destination_table = tk.StringVar()
        self.destination_column = tk.StringVar()
        self.image_path = tk.StringVar()

        # إطار اختيار قاعدة البيانات
        db_frame = ttk.LabelFrame(master, text="قاعدة البيانات")
        db_frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(db_frame, text="ملف قاعدة البيانات:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(db_frame, textvariable=self.db_path, width=50).grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ttk.Button(db_frame, text="تصفح", command=self.browse_database).grid(row=0, column=2, padx=5, pady=5)

        # إطار اختيار الوجهة
        dest_frame = ttk.LabelFrame(master, text="الوجهة (الصورة)")
        dest_frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(dest_frame, text="الجدول:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.dest_table_combo = ttk.Combobox(dest_frame, textvariable=self.destination_table, state="readonly")
        self.dest_table_combo.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.dest_table_combo.bind("<<ComboboxSelected>>", self.update_dest_columns)

        ttk.Label(dest_frame, text="العمود:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.dest_column_combo = ttk.Combobox(dest_frame, textvariable=self.destination_column, state="readonly")
        self.dest_column_combo.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # إطار اختيار الصورة
        image_frame = ttk.LabelFrame(master, text="الصورة")
        image_frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(image_frame, text="ملف الصورة:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(image_frame, textvariable=self.image_path, width=50).grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ttk.Button(image_frame, text="تصفح", command=self.browse_image).grid(row=0, column=2, padx=5, pady=5)

        # زر المعالجة
        ttk.Button(master, text="تحويل الصورة إلى BLOB", command=self.process_data).pack(pady=20)

        # شريط التقدم
        self.progress = ttk.Progressbar(master, orient=tk.HORIZONTAL, length=400, mode='determinate')
        self.progress.pack(padx=10, pady=5)

    def browse_database(self):
        file_path = filedialog.askopenfilename(defaultextension=".db", filetypes=[("SQLite Database", "*.db")])
        if file_path:
            self.db_path.set(file_path)
            self.update_table_lists()

    def browse_image(self):
        file_path = filedialog.askopenfilename(defaultextension=".jpg", filetypes=[("Image files", "*.jpg;*.png")])
        if file_path:
            self.image_path.set(file_path)

    def update_table_lists(self):
        db_path = self.db_path.get()
        if db_path:
            try:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = [row[0] for row in cursor.fetchall()]
                self.dest_table_combo['values'] = tables
                conn.close()
            except sqlite3.Error as e:
                messagebox.showerror("خطأ", f"خطأ في فتح قاعدة البيانات: {e}")

    def update_dest_columns(self, event=None):
        self._update_columns(self.destination_table.get(), self.dest_column_combo)

    def _update_columns(self, table_name, combo_box):
        db_path = self.db_path.get()
        if db_path and table_name:
            try:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute(f"PRAGMA table_info({table_name});")
                columns = [row[1] for row in cursor.fetchall()]
                combo_box['values'] = columns
                conn.close()
            except sqlite3.Error as e:
                messagebox.showerror("خطأ", f"خطأ في جلب أعمدة الجدول: {e}")

    def convert_image_to_blob(self, image_path):
        with open(image_path, "rb") as image_file:
            blob = image_file.read()
        return blob

    def process_data(self):
        db_path = self.db_path.get()
        destination_table = self.destination_table.get()
        destination_column = self.destination_column.get()
        image_path = self.image_path.get()

        if not all([db_path, destination_table, destination_column, image_path]):
            messagebox.showerror("خطأ", "الرجاء ملء جميع الحقول.")
            return

        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # تحويل الصورة إلى BLOB
            image_blob = self.convert_image_to_blob(image_path)

            # إضافة البيانات إلى جدول الوجهة
            cursor.execute(f"INSERT INTO {destination_table} ({destination_column}) VALUES (?)", (image_blob,))
            conn.commit()

            messagebox.showinfo("اكتمل", "تمت معالجة البيانات بنجاح.")
            conn.close()

        except sqlite3.Error as e:
            messagebox.showerror("خطأ في قاعدة البيانات", f"حدث خطأ أثناء معالجة قاعدة البيانات: {e}")
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ غير متوقع: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageToBlobApp(root)
    root.mainloop()
