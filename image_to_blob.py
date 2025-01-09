import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import sqlite3
from PIL import Image
import io
import os

class ImageToBlobApp:
    def __init__(self, master):
        self.master = master
        master.title("محول الصورة إلى BLOB (تحديث مجمع بمرونة)")

        # متغيرات لتخزين الاختيارات (يجب تعريفها هنا)
        self.db_path = tk.StringVar()
        self.name_table = tk.StringVar()
        self.name_column = tk.StringVar()
        self.image_table = tk.StringVar()
        self.image_column = tk.StringVar()
        self.image_folder_path = tk.StringVar()

        # إطار اختيار قاعدة البيانات (كما هو)
        db_frame = ttk.LabelFrame(master, text="قاعدة البيانات")
        db_frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(db_frame, text="ملف قاعدة البيانات:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(db_frame, textvariable=self.db_path, width=50).grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ttk.Button(db_frame, text="تصفح", command=self.browse_database).grid(row=0, column=2, padx=5, pady=5)

        # إطار اختيار جدول وأعمدة أسماء الحيوانات
        names_frame = ttk.LabelFrame(master, text="جدول وأعمدة أسماء الحيوانات")
        names_frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(names_frame, text="الجدول:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.name_table_combo = ttk.Combobox(names_frame, textvariable=self.name_table, state="readonly")
        self.name_table_combo.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.name_table_combo.bind("<<ComboboxSelected>>", lambda event: self.update_columns(self.name_table.get(), self.name_column_combo))

        ttk.Label(names_frame, text="العمود (الاسم):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.name_column_combo = ttk.Combobox(names_frame, textvariable=self.name_column, state="readonly")
        self.name_column_combo.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # إطار اختيار الوجهة (الصورة) - معاد استخدامه
        dest_frame = ttk.LabelFrame(master, text="الوجهة (الصورة)")
        dest_frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(dest_frame, text="الجدول:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.image_table_combo = ttk.Combobox(dest_frame, textvariable=self.image_table, state="readonly")
        self.image_table_combo.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.image_table_combo.bind("<<ComboboxSelected>>", lambda event: self.update_columns(self.image_table.get(), self.image_column_combo))

        ttk.Label(dest_frame, text="العمود (الصورة):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.image_column_combo = ttk.Combobox(dest_frame, textvariable=self.image_column, state="readonly")
        self.image_column_combo.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # إطار اختيار الصورة (كما هو)
        image_frame = ttk.LabelFrame(master, text="الصور")
        image_frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(image_frame, text="مجلد الصور:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(image_frame, textvariable=self.image_folder_path, width=50).grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ttk.Button(image_frame, text="تصفح المجلد", command=self.browse_images_folder).grid(row=0, column=2, padx=5, pady=5)

        # زر المعالجة (كما هو)
        ttk.Button(master, text="معالجة صور المجلد", command=self.process_images_folder).pack(pady=20)

        # شريط التقدم (كما هو)
        self.progress = ttk.Progressbar(master, orient=tk.HORIZONTAL, length=400, mode='determinate')
        self.progress.pack(padx=10, pady=5)

    def browse_database(self):
        file_path = filedialog.askopenfilename(defaultextension=".db", filetypes=[("SQLite Database", "*.db")])
        if file_path:
            self.db_path.set(file_path)
            self.update_table_lists()

    def update_table_lists(self):
        db_path = self.db_path.get()
        if db_path:
            try:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = [row[0] for row in cursor.fetchall()]
                self.name_table_combo['values'] = tables
                self.image_table_combo['values'] = tables
                conn.close()
            except sqlite3.Error as e:
                messagebox.showerror("خطأ", f"خطأ في فتح قاعدة البيانات: {e}")

    def update_columns(self, table_name, combo_box):
        db_path = self.db_path.get()
        if db_path and table_name:
            try:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute(f"PRAGMA table_info('{table_name}')")
                columns = [col[1] for col in cursor.fetchall()]
                combo_box['values'] = columns
                conn.close()
            except sqlite3.Error as e:
                messagebox.showerror("خطأ", f"خطأ في جلب أعمدة الجدول: {e}")

    def browse_images_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.image_folder_path.set(folder_path)

    def convert_image_to_blob(self, image_path):
        try:
            img = Image.open(image_path)
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format="WEBP")  # تحديث هنا لضمان حفظها كـ WEBP إذا لزم الأمر
            return img_byte_arr.getvalue()
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ أثناء تحويل الصورة إلى BLOB: {e}")
            return None

    def process_images_folder(self):
        db_path = self.db_path.get()
        image_folder = self.image_folder_path.get()
        name_table = self.name_table.get()
        name_column = self.name_column.get()
        image_table = self.image_table.get()
        image_column = self.image_column.get()

        if not all([db_path, image_folder, name_table, name_column, image_table, image_column]):
            messagebox.showerror("خطأ", "الرجاء تحديد قاعدة البيانات، والجداول والأعمدة المطلوبة، ومجلد الصور.")
            return

        print(f"قاعدة البيانات المختارة: {db_path}")
        print(f"مجلد الصور المختار: {image_folder}")
        print(f"جدول أسماء الحيوانات: {name_table}, عمود الاسم: {name_column}")
        print(f"جدول الصور: {image_table}, عمود الصورة: {image_column}")

        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # استرداد أسماء الحيوانات من الجدول المحدد
            print(f"تنفيذ الاستعلام لاسترداد أسماء الحيوانات: SELECT `{name_column}` FROM `{name_table}`")
            cursor.execute(f"SELECT `{name_column}` FROM `{name_table}`")
            results = cursor.fetchall()
            animal_names = []
            if results:
                for row in results:
                    animal_names.append(row[0])
            print(f"تم استرداد أسماء الحيوانات: {animal_names}")

            processed_count = 0
            not_found_count = 0
            skipped_count = 0

            print(f"محتويات مجلد الصور: {os.listdir(image_folder)}")

            for filename in os.listdir(image_folder):
                print(f"تم العثور على ملف في المجلد: {filename}")
                if filename.lower().endswith('.webp'):  # تم التعديل هنا لدعم امتداد WEBP
                    animal_name = os.path.splitext(filename)[0]
                    print(f"جاري معالجة الملف: {filename}, اسم الحيوان المستخرج: {animal_name}")
                    if animal_name in animal_names:
                        print(f"تم العثور على تطابق لـ {animal_name} في قائمة أسماء الحيوانات.")
                        # التحقق مما إذا كان حقل الصورة فارغًا
                        cursor.execute(f"SELECT `{image_column}` FROM `{image_table}` WHERE `{name_column}` = ?", (animal_name,))
                        existing_image = cursor.fetchone()[0]

                        if existing_image is None:
                            print(f"حقل الصورة لـ {animal_name} فارغ. سيتم تحديثه.")
                            image_path = os.path.join(image_folder, filename)
                            print(f"مسار الصورة الكامل: {image_path}")
                            image_blob = self.convert_image_to_blob(image_path)
                            if image_blob:
                                # تحديث جدول الصور المحدد
                                print(f"جاري تنفيذ تحديث قاعدة البيانات لـ {animal_name}.")
                                cursor.execute(f"UPDATE `{image_table}` SET `{image_column}` = ? WHERE `{name_column}` = ?", (image_blob, animal_name))
                                processed_count += 1
                                print(f"تم تحديث صورة {animal_name} بنجاح.")
                            else:
                                print(f"فشل تحويل الصورة {filename} إلى BLOB.")
                        else:
                            skipped_count += 1
                            print(f"تم تخطي {animal_name} لأن حقل الصورة لم يكن فارغًا.")
                    else:
                        not_found_count += 1
                        print(f"لم يتم العثور على تطابق لـ {animal_name} في قاعدة البيانات.")

            conn.commit()
            conn.close()

            message = f"تمت معالجة {processed_count} صورة بنجاح.\n"
            if not_found_count > 0:
                message += f"لم يتم العثور على تطابق لـ {not_found_count} صورة في قاعدة البيانات.\n"
            if skipped_count > 0:
                message += f"تم تخطي {skipped_count} صورة لأن حقل الصورة لم يكن فارغًا."
            messagebox.showinfo("اكتمل", message)

        except sqlite3.Error as e:
            messagebox.showerror("خطأ في قاعدة البيانات", f"حدث خطأ أثناء معالجة قاعدة البيانات: {e}")
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ غير متوقع: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageToBlobApp(root)
    root.mainloop()