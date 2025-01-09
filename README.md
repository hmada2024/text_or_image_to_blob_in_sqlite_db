                Text to Speech Converter

Welcome to the Text to Speech Converter app! This application allows you to convert text in a SQLite database to audio files using the gTTS (Google Text-to-Speech) library.

Steps to use the application:
Choose the database file.

Select the table and column containing the text.

Select the table and column to store the audio.

Click the 'Convert Text to Speech' button to start the conversion.

Requirements:
Python 3

gTTS library

tkinter library

sqlite3 library

Installation:
sh
pip install gtts

                 Image to BLOB Converter
Welcome to the Image to BLOB Converter app! This application allows you to convert images from your computer to BLOB data and insert them into a column in a SQLite database table.

Steps to use the application:
Choose the database file.

Select the table and column to store the image.

Click the 'Browse' button to choose an image.

Click the 'Convert Image to BLOB' button to start the conversion.

Requirements:
Python 3

Pillow library

tkinter library

sqlite3 library

Installation:
sh
pip 


تطبيق محول الصور إلى BLOB (تحديث مجمع بمرونة)
وصف التطبيق
هذا التطبيق هو أداة رسومية (GUI) مبنية باستخدام مكتبة tkinter في Python، تتيح لك تحويل مجموعة من الصور الموجودة على جهاز الكمبيوتر إلى بيانات BLOB (Binary Large Object) وتحديث سجلات موجودة في قاعدة بيانات SQLite بناءً على تطابق أسماء الملفات مع قيم في عمود محدد. يتميز التطبيق بالمرونة حيث يمكنك تحديد الجدول والعمود الذي يحتوي على أسماء العناصر (مثل أسماء الحيوانات) والجدول والعمود الذي سيتم تخزين بيانات BLOB للصور فيه.

المميزات الرئيسية
واجهة مستخدم رسومية سهلة الاستخدام: تعتمد على مكتبة tkinter لتوفير تجربة مستخدم بسيطة وواضحة.

تحديث مجمع للصور: يمكنك معالجة مجلد كامل من الصور دفعة واحدة، مما يوفر الوقت والجهد.

ربط الصور بالأسماء: يتم ربط الصور بالسجلات الموجودة في قاعدة البيانات بناءً على تطابق اسم ملف الصورة (بدون الامتداد) مع قيمة في عمود محدد.

تحديد الجداول والأعمدة ديناميكيًا: يمكنك اختيار الجدول الذي يحتوي على أسماء العناصر والعمود الخاص بالاسم، بالإضافة إلى الجدول والعمود المخصص لتخزين الصور.

دعم صيغ الصور الشائعة: يدعم التطبيق صيغ الصور الشائعة مثل JPG، PNG، JPEG، BMP، و GIF.

تخزين الصور بصيغة BLOB: يتم تحويل الصور إلى بيانات BLOB وتخزينها في قاعدة بيانات SQLite.

خطوات الاستخدام
تشغيل التطبيق: قم بتشغيل ملف Python الخاص بالتطبيق (image_to_blob.py).

تحديد قاعدة البيانات:

اضغط على زر "تصفح" في إطار "قاعدة البيانات".

اختر ملف قاعدة بيانات SQLite (.db).

تحديد جدول وأعمدة أسماء العناصر:

في إطار "جدول وأعمدة أسماء الحيوانات":

اختر الجدول الذي يحتوي على أسماء العناصر من القائمة المنسدلة "الجدول".

اختر العمود الذي يحتوي على أسماء العناصر من القائمة المنسدلة "العمود (الاسم)".

تحديد جدول وأعمدة الصور:

في إطار "الوجهة (الصورة)":

اختر الجدول الذي سيتم تخزين الصور فيه من القائمة المنسدلة "الجدول".

اختر العمود الذي سيتم تخزين بيانات BLOB للصور فيه من القائمة المنسدلة "العمود (الصورة)".

تحديد مجلد الصور:

اضغط على زر "تصفح المجلد" في إطار "الصور".

اختر المجلد الذي يحتوي على صور العناصر. تأكد من أن أسماء ملفات الصور تطابق أسماء العناصر في العمود المحدد (مع تجاهل الامتداد).

معالجة الصور:

اضغط على زر "معالجة صور المجلد".

سيقوم التطبيق بمعالجة الصور الموجودة في المجلد ومحاولة مطابقتها مع الأسماء الموجودة في قاعدة البيانات وتحديث سجلاتها بالصور.

عرض النتائج: ستظهر رسالة توضح عدد الصور التي تمت معالجتها بنجاح وعدد الصور التي لم يتم العثور على تطابق لها.

المتطلبات
Python 3.6 أو أحدث: يجب أن يكون لديك Python مثبتًا على جهازك.

مكتبات Python التالية:

tkinter: تأتي مثبتة بشكل افتراضي مع معظم توزيعات Python.

sqlite3: تأتي مثبتة بشكل افتراضي مع Python.

Pillow (PIL): مكتبة لمعالجة الصور. يمكنك تثبيتها باستخدام pip: pip install Pillow.

ملاحظات
تسمية ملفات الصور: يجب أن تكون أسماء ملفات الصور مطابقة تمامًا لأسماء العناصر الموجودة في العمود المحدد في قاعدة البيانات (مع تجاهل امتداد الملف).

المرونة: يتيح لك هذا التطبيق التعامل مع هياكل قواعد بيانات مختلفة دون الحاجة إلى تعديل الكود، طالما أن لديك جدولًا يحتوي على أسماء العناصر وجدولًا آخر (قد يكون هو نفسه) يحتوي على عمود لتخزين الصور.

ملفات المشروع
image_to_blob.py: ملف كود Python الرئيسي للتطبيق.

كيفية التشغيل
تأكد من تثبيت جميع المتطلبات المذكورة أعلاه.

افتح موجه الأوامر أو الطرفية (Terminal).

انتقل إلى المجلد الذي يحتوي على ملف image_to_blob.py.

قم بتشغيل التطبيق باستخدام الأمر: python image_to_blob.py.

ترخيص
[أضف هنا نوع الترخيص الخاص بمشروعك إذا كنت ترغب في ذلك، مثل MIT License أو Apache License 2.0]

يمكنك نسخ هذا الشرح ووضعه في ملف README.md في مجلد مشروعك. يمكنك أيضًا تعديله ليناسب احتياجاتك بشكل أفضل.