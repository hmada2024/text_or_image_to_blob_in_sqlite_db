import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import sqlite3
from gtts import gTTS
import os

class AudioConverterApp:
    def __init__(self, master):
        self.master = master
        master.title("محول النص إلى صوت")

        # إضافة وصف التطبيق
        description_frame = ttk.LabelFrame(master, text="وصف التطبيق")
        description_frame.pack(padx=10, pady=10, fill="x")

        description_label = tk.Label(description_frame, text=(
            "أهلاً بك في تطبيق محول النص إلى صوت!\n"
            "يتيح لك هذا التطبيق تحويل النصوص الموجودة في قاعدة بيانات SQLite إلى ملفات صوتية\n"
            "بالاعتماد على مكتبة gTTS (Google Text-to-Speech).\n\n"
            "الخطوات:\n"
            "1. اختر ملف قاعدة البيانات.\n"
            "2. اختر الجدول والعمود الذي يحتوي على النص.\n"
            "3. اختر الجدول والعمود الذي سيتم تخزين الصوت فيه.\n"
            "4. اضغط على زر 'تحويل النص إلى صوت' للبدء في التحويل.\n\n"
            "تمتع باستخدام التطبيق!"
        ), anchor="center", justify="center", wraplength=400)
        description_label.pack(padx=10, pady=10)

        # متغيرات لتخزين الاختيارات
        self.db_path = tk.StringVar()
        self.source_table = tk.StringVar()
        self.source_column = tk.StringVar()
        self.destination_table = tk.StringVar()
        self.destination_column = tk.StringVar()

        # إطار اختيار قاعدة البيانات
        db_frame = ttk.LabelFrame(master, text="قاعدة البيانات")
        db_frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(db_frame, text="ملف قاعدة البيانات:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(db_frame, textvariable=self.db_path, width=50).grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ttk.Button(db_frame, text="تصفح", command=self.browse_database).grid(row=0, column=2, padx=5, pady=5)

        # إطار اختيار المصدر
        source_frame = ttk.LabelFrame(master, text="المصدر (النص)")
        source_frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(source_frame, text="الجدول:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.source_table_combo = ttk.Combobox(source_frame, textvariable=self.source_table, state="readonly")
        self.source_table_combo.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.source_table_combo.bind("<<ComboboxSelected>>", self.update_source_columns)

        ttk.Label(source_frame, text="العمود:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.source_column_combo = ttk.Combobox(source_frame, textvariable=self.source_column, state="readonly")
        self.source_column_combo.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # إطار اختيار الوجهة
        dest_frame = ttk.LabelFrame(master, text="الوجهة (الصوت)")
        dest_frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(dest_frame, text="الجدول:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.dest_table_combo = ttk.Combobox(dest_frame, textvariable=self.destination_table, state="readonly")
        self.dest_table_combo.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.dest_table_combo.bind("<<ComboboxSelected>>", self.update_dest_columns)

        ttk.Label(dest_frame, text="العمود:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.dest_column_combo = ttk.Combobox(dest_frame, textvariable=self.destination_column, state="readonly")
        self.dest_column_combo.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # زر المعالجة
        ttk.Button(master, text="تحويل النص إلى صوت", command=self.process_data).pack(pady=20)

        # شريط التقدم
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
                self.source_table_combo['values'] = tables
                self.dest_table_combo['values'] = tables
                conn.close()
            except sqlite3.Error as e:
                messagebox.showerror("خطأ", f"خطأ في فتح قاعدة البيانات: {e}")

    def update_source_columns(self, event=None):
        self._update_columns(self.source_table.get(), self.source_column_combo)

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

    def convert_text_to_blob(self, text):
        tts = gTTS(text=text, lang='en')
        temp_file = "temp_audio.mp3"
        tts.save(temp_file)
        with open(temp_file, "rb") as audio_file:
            audio_blob = audio_file.read()
        os.remove(temp_file)
        return audio_blob

    def process_data(self):
        db_path = self.db_path.get()
        source_table = self.source_table.get()
        source_column = self.source_column.get()
        destination_table = self.destination_table.get()
        destination_column = self.destination_column.get()

        if not all([db_path, source_table, source_column, destination_table, destination_column]):
            messagebox.showerror("خطأ", "الرجاء ملء جميع الحقول.")
            return

        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # جلب البيانات من جدول المصدر
            cursor.execute(f"SELECT id, {source_column} FROM {source_table}")
            rows = cursor.fetchall()

            # إعداد شريط التقدم
            self.progress["maximum"] = len(rows)
            self.progress["value"] = 0

            for row in rows:
                item_id, text_to_convert = row
                try:
                    audio_blob = self.convert_text_to_blob(text_to_convert)
                    # تحديث جدول الوجهة
                    cursor.execute(f"UPDATE {destination_table} SET {destination_column} = ? WHERE id = ?", (audio_blob, item_id))
                    conn.commit()
                    self.progress["value"] += 1
                    self.master.update_idletasks()
                    print(f"تم تحويل النص من {source_table}.{source_column} (ID: {item_id}) إلى صوت وحفظه في {destination_table}.{destination_column}.")
                except Exception as e:
                    print(f"فشل تحويل النص (ID: {item_id}): {e}")

            messagebox.showinfo("اكتمل", "تمت معالجة البيانات بنجاح.")
            conn.close()

        except sqlite3.Error as e:
            messagebox.showerror("خطأ في قاعدة البيانات", f"حدث خطأ أثناء معالجة قاعدة البيانات: {e}")
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ غير متوقع: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AudioConverterApp(root)
    root.mainloop()
