import hashlib
import random
from tkinter import *
from tkinter import ttk

import mysql.connector
import customtkinter

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

sys = customtkinter.CTk()
sys.title("Online Kurs Sistemi")
sys.geometry("570x520")
sys.iconbitmap("academy.ico")
sys.resizable(False, False)
sys.attributes("-alpha", 0.97)

usrMail = ""

def connectDb():
    # Veritabanına bağlanmak için gerekli bilgiler
    db_host = "localhost"
    db_user = "root"
    db_password = ""
    db_name = "online_kurs_sistemi"

    # Bağlantı nesnesi oluşturuluyor
    cnx = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )

    return cnx


def messagePopUp(title, txt, icon="academy"):
    errorPage = customtkinter.CTk()
    errorPage.title(title)
    errorPage.geometry("400x200")
    iconText = """{}.ico""".format(icon)
    errorPage.iconbitmap(iconText)
    errorPage.resizable(False, False)
    errorPage.attributes("-alpha", 0.97)
    errorFrame = customtkinter.CTkFrame(errorPage)
    errorFrame.place(relx=0.5, rely=0.5, anchor=CENTER)
    title = customtkinter.CTkLabel(errorFrame, width=300, height=30, text_color=("white", "gray75"))
    title.configure(text=txt)
    title.grid(row=0, column=1, padx=10, pady=20, sticky="n")
    errorPage.mainloop()


def controlPopUp(title, txt, icon="info", resultFunc=None, id=None):
    questionPage = customtkinter.CTk()
    questionPage.title(title)
    questionPage.geometry("500x200")
    iconText = """{}.ico""".format(icon)
    questionPage.iconbitmap(iconText)
    questionPage.resizable(False, False)
    questionPage.attributes("-alpha", 0.97)

    questionFrame = customtkinter.CTkFrame(questionPage)
    questionFrame.place(relx=0.5, rely=0.5, anchor=CENTER)

    title = customtkinter.CTkLabel(questionFrame, width=450, height=30, text_color=("white", "gray75"))
    title.configure(text=txt)
    title.grid(row=0, column=1, padx=10, pady=20, sticky="n")

    optionsFrame = customtkinter.CTkFrame(questionFrame, fg_color="transparent")
    optionsFrame.grid(row=1, column=1, padx=10, pady=(5, 10))

    def checkButtons(btnNum):
        if btnNum == 0:
            questionPage.destroy()
        elif btnNum == 1:
            questionPage.destroy()
            resultFunc(id)

    acceptButton = customtkinter.CTkButton(optionsFrame)
    acceptButton.bind("<Button-1>", lambda x: checkButtons(1))
    acceptButton.configure(text="Evet")
    acceptButton.grid(row=0, column=0, padx=10, pady=(5, 10))

    cancelButton = customtkinter.CTkButton(optionsFrame)
    cancelButton.bind("<Button-1>", lambda x: checkButtons(0))
    cancelButton.configure(text="Hayır")
    cancelButton.grid(row=0, column=1, padx=10, pady=(5, 10))

    questionPage.mainloop()


def openAdminPage():
    adminPage = customtkinter.CTk()
    adminPage.title("Online Kurs Sistemi - Admin")
    adminPage.geometry("660x470")
    adminPage.iconbitmap("academy.ico")
    adminPage.resizable(False, False)
    adminPage.attributes("-alpha", 0.97)

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("mystyle1.Treeview", background="#212121", foreground="#bababa", rowheight=25,
                    fieldbackground="silver")
    style.configure("mystyle1.Treeview.Heading", background="#303030", foreground="#bababa", fieldbackground="silver",
                    borderwidth=0)
    style.map("mystyle1.Treeview.Heading", background=[('selected', '#212121')])
    style.layout("mystyle1.Treeview", [('mystyle1.Treeview.treearea', {'sticky': 'nswe', 'border': 0})])

    def coursePage():
        coursepg = customtkinter.CTk()
        coursepg.title("Online Kurs Sistemi - Admin")
        coursepg.geometry("680x470")
        coursepg.iconbitmap("academy.ico")
        coursepg.resizable(False, True)
        coursepg.attributes("-alpha", 0.97)

        courseLabel = customtkinter.CTkLabel(coursepg, text="", width=620,
                                               font=customtkinter.CTkFont(size=12), anchor="w")
        courseLabel.grid(row=0, column=0, padx=20, pady=(10, 10))

        courseMainFrame = customtkinter.CTkFrame(coursepg, width=500, height=400, corner_radius=0,
                                           fg_color="transparent")
        courseMainFrame.grid(row=3, column=0, sticky="nsew")

        courseCanvas = Canvas(courseMainFrame, bg="gray10", highlightthickness=0)
        courseCanvas.pack(side=LEFT, fill=BOTH, expand=1)

        courseScrollbar = customtkinter.CTkScrollbar(courseCanvas, command=courseCanvas.yview)
        courseScrollbar.pack(side=RIGHT, fill=Y)

        courseCanvas.configure(yscrollcommand=courseScrollbar.set)
        courseCanvas.bind("<Configure>", lambda e: courseCanvas.configure(scrollregion=courseCanvas.bbox("all")))

        courseSecondFrame = customtkinter.CTkFrame(courseCanvas, corner_radius=0, fg_color="transparent")

        courseCanvas.create_window((0, 0), window=courseSecondFrame, anchor="nw")

        def editCoursePage(courseId):
            courseEditPage = customtkinter.CTk()
            courseEditPage.title("Online Kurs Sistemi - Admin")
            courseEditPage.geometry("680x580")
            courseEditPage.iconbitmap("academy.ico")
            courseEditPage.resizable(False, False)
            courseEditPage.attributes("-alpha", 0.97)

            cnx = connectDb()
            crs = cnx.cursor(buffered=True)
            crs.execute("""SELECT courses.course_id, courses.name, courses.description, courses.price, courses.instructor_id, course_categories.category_id
                            FROM courses INNER JOIN course_categories ON courses.course_id = course_categories.course_id
                            WHERE courses.course_id = '{0}'""".format(courseId))
            item = crs.fetchone()
            editFrame = customtkinter.CTkFrame(courseEditPage, width=660, corner_radius=0)
            editFrame.grid(row=0, column=0, rowspan=4, sticky="nsew", pady=20, padx=10)
            editFrame.grid_rowconfigure(4, weight=1)

            idLabel = customtkinter.CTkLabel(editFrame, text="Kurs ID :", width=620,
                                             font=customtkinter.CTkFont(size=12), anchor="w")
            idLabel.grid(row=0, column=0, padx=20, pady=(20, 5))

            idEntry = customtkinter.CTkEntry(editFrame, placeholder_text=courseId)
            idEntry.grid(row=1, column=0, columnspan=3, padx=20, pady=(5, 10), sticky="nsew")
            idEntry.insert(0, courseId)
            idEntry.configure(state="disabled")

            nameLabel = customtkinter.CTkLabel(editFrame, text="Kurs Adı :", width=620,
                                               font=customtkinter.CTkFont(size=12), anchor="w")
            nameLabel.grid(row=2, column=0, padx=20, pady=(5, 5))

            nameEntry = customtkinter.CTkEntry(editFrame, placeholder_text="Kurs Adı")
            nameEntry.grid(row=3, column=0, columnspan=3, padx=20, pady=(5, 10), sticky="nsew")
            nameEntry.insert(0, item[1])

            descriptionLabel = customtkinter.CTkLabel(editFrame, text="Açıklama :", width=620,
                                                      font=customtkinter.CTkFont(size=12), anchor="w")
            descriptionLabel.grid(row=4, column=0, padx=20, pady=(5, 5))

            descriptionEntry = customtkinter.CTkEntry(editFrame, placeholder_text="Açıklama")
            descriptionEntry.grid(row=5, column=0, columnspan=3, padx=20, pady=(5, 10), sticky="nsew")
            descriptionEntry.insert(0, item[2])

            priceLabel = customtkinter.CTkLabel(editFrame, text="Fiyat :", width=620,
                                                font=customtkinter.CTkFont(size=12), anchor="w")
            priceLabel.grid(row=6, column=0, padx=20, pady=(5, 5))

            priceEntry = customtkinter.CTkEntry(editFrame, placeholder_text="Fiyat")
            priceEntry.grid(row=7, column=0, columnspan=3, padx=20, pady=(5, 10), sticky="nsew")
            priceEntry.insert(0, item[3])

            instructorLabel = customtkinter.CTkLabel(editFrame, text="Instructor ID :", width=620,
                                                     font=customtkinter.CTkFont(size=12), anchor="w")
            instructorLabel.grid(row=8, column=0, padx=20, pady=(5, 5))

            instructorEntry = customtkinter.CTkEntry(editFrame, placeholder_text="Instructor ID")
            instructorEntry.grid(row=9, column=0, columnspan=3, padx=20, pady=(5, 5), sticky="nsew")
            instructorEntry.insert(0, item[4])

            categoryLabel = customtkinter.CTkLabel(editFrame, text="Category ID :", width=620,
                                                     font=customtkinter.CTkFont(size=12), anchor="w")
            categoryLabel.grid(row=10, column=0, padx=20, pady=(5, 5))

            categoryEntry = customtkinter.CTkEntry(editFrame, placeholder_text="Category ID")
            categoryEntry.grid(row=11, column=0, columnspan=3, padx=20, pady=(5, 5), sticky="nsew")
            categoryEntry.insert(0, item[5])

            saveButton = customtkinter.CTkButton(editFrame, fg_color="green",
                                                 command=lambda: editCourse(courseId, nameEntry.get(),
                                                                            descriptionEntry.get(), priceEntry.get(),
                                                                            instructorEntry.get(), categoryEntry.get()))
            saveButton.configure(text="Kaydet")
            saveButton.grid(row=12, column=0, padx=10, pady=(5, 10))

            courseEditPage.mainloop()

        def editCourse(courseId, name, desc, price, instructor, category):
            cnx = connectDb()
            crs = cnx.cursor(buffered=True)
            crs.execute("""UPDATE courses SET name = '{1}', description = '{2}', price = '{3}', instructor_id = '{4}'
                        WHERE courses.course_id = {0};""".format(courseId, name, desc, price, instructor))
            cnx.commit()
            crs.execute("""UPDATE course_categories SET category_id = {0}
                            WHERE course_id = {1}""".format(category, courseId))
            cnx.commit()
            messagePopUp("İşlem Başarılı", "Kurs bilgileri başarıyla güncellenmiştir")

        def deleteCourse(courseId):
            cnx = connectDb()
            crs = cnx.cursor(buffered=True)
            crs.execute("""DELETE FROM course_categories WHERE course_id = {}""".format(courseId))
            cnx.commit()
            crs.execute("""DELETE FROM courses WHERE course_id = {}""".format(courseId))
            cnx.commit()
            messagePopUp("İşlem Başarılı", "ID'si {} olan kurs başarıyla silinmiştir".format(courseId))

        # kategorileri getir
        def getCategories(categoryName=None):
            cnx = connectDb()
            crs = cnx.cursor(buffered=True)
            crs.execute("""SELECT name FROM categories""")
            items = crs.fetchall()
            categoryList = []
            for i in items:
                categoryList.append(i[0])

            combobox = customtkinter.CTkOptionMenu(coursepg, values=categoryList,
                                                   command=lambda: getPageWidgets(combobox.get()))
            combobox.grid(row=0, column=0, padx=10, pady=20)

            if categoryName is None:
                combobox.set(categoryList[0])
            return categoryList, combobox

        # kategorideki kursları getir
        def getCategoryCourses(widget):
            courseItems = []
            cnx = connectDb()
            crs = cnx.cursor(buffered=True)
            crs.execute("""SELECT courses.course_id, courses.name, courses.description, courses.price, CONCAT(users.name, " ", users.surname)
                                        FROM users, courses, course_categories, categories
                                        WHERE courses.course_id = course_categories.course_id
                                        AND course_categories.category_id = categories.category_id
                                        AND courses.instructor_id = users.user_id
                                        AND categories.name = '{0}'""".format(widget.get()))
            items = crs.fetchall()
            for item in items:
                courseItems.append(item)
            return courseItems

        # kursları listele
        def listCourses(courseData):
            count = 0
            for course in courseData:
                courseFrame = customtkinter.CTkFrame(courseSecondFrame, width=430, height=300)
                if count == 0:
                    courseFrame.grid(row=(count * 3) + 1, column=0, padx=10, pady=(10, 5))
                elif 0 < count < (len(courseData) - 1):
                    courseFrame.grid(row=(count * 3) + 1, column=0, padx=10, pady=(5, 5))
                else:
                    courseFrame.grid(row=(count * 3) + 1, column=0, padx=10, pady=(5, 10))
                courseName = customtkinter.CTkLabel(courseFrame, text=course[1], width=425,
                                                    font=customtkinter.CTkFont(size=16, weight="bold"), anchor="w")
                courseName.grid(row=(count * 3), columnspan=2, padx=20, pady=(10, 5))

                courseDescription = customtkinter.CTkLabel(courseFrame, width=425, text=course[2],
                                                           font=customtkinter.CTkFont(size=12), anchor="w")
                courseDescription.grid(row=(count * 3) + 1, columnspan=2, padx=20, pady=(5, 5))

                courseInstructor = customtkinter.CTkLabel(courseFrame, width=425,
                                                          text="Instructor: {}".format(course[4]),
                                                          font=customtkinter.CTkFont(size=12), anchor="w")
                courseInstructor.grid(row=(count * 3) + 2, columnspan=2, padx=20, pady=(5, 10))
                priceLabel = customtkinter.CTkLabel(courseFrame, text=("{} TL".format(course[3])),
                                                    font=customtkinter.CTkFont(size=16, weight="bold"))
                priceLabel.grid(row=(count * 3), column=3, padx=20, pady=(10, 5))

                editButton = customtkinter.CTkButton(courseFrame, fg_color="green",
                                                     command=lambda x=course[0]: editCoursePage(x))
                editButton.configure(text="Düzenle")
                editButton.focus()
                editButton.grid(row=(count * 3) + 1, column=3, padx=10, pady=(5, 5))

                deleteButton = customtkinter.CTkButton(courseFrame, fg_color="#782c2c",
                                                       command=lambda x=course[0]: controlPopUp("Kurs Silme İşlemi",
                                                                                                "ID'si {} olan kursu silmek istediğinizden emin misiniz ?".format(
                                                                                                    x), "info",
                                                                                                deleteCourse, x))
                deleteButton.configure(text="Sil")
                deleteButton.grid(row=(count * 3) + 2, column=3, padx=10, pady=(5, 10))
                count += 1

        def getPageWidgets(comboboxVal=None):
            if comboboxVal is not None:
                categories, comboBox = getCategories(comboboxVal)
            else:
                categories, comboBox = getCategories()
            courses = getCategoryCourses(comboBox)
            listCourses(courses)

        getPageWidgets()

        coursepg.mainloop()

    def categoriesPage():
        categoriespg = customtkinter.CTkToplevel()
        categoriespg.title("Online Kurs Sistemi - Admin")
        categoriespg.geometry("680x470")
        categoriespg.iconbitmap("academy.ico")
        categoriespg.resizable(False, True)
        categoriespg.attributes("-alpha", 0.97)

        def findCategory():
            for i in categoryTree.get_children():
                categoryTree.delete(i)
            cnx = connectDb()
            crs = cnx.cursor(buffered=True)
            if categorySearchEntry.get() is None:
                crs.execute("""SELECT category_id,name FROM categories""")
            else:
                findWord = None
                try:
                    findWord = int(categorySearchEntry.get())
                except:
                    findWord = categorySearchEntry.get()
                if findWord is not None and type(findWord) is str:
                    crs.execute(
                        """SELECT category_id,name FROM categories
                        WHERE categories.name LIKE '%{0}%'""".format(findWord))
                elif findWord is not None and type(findWord) is int:
                    crs.execute(
                        """SELECT category_id,name FROM categories
                        WHERE categories.category_id = {0}""".format(findWord))
            newCategoryItems = crs.fetchall()
            for nCtItem in newCategoryItems:
                categoryTree.insert("", 'end', iid=nCtItem[0], text=nCtItem[0],
                                    values=(nCtItem[0], nCtItem[1]))
            cnx.close()

        def deleteCategory():
            cnx = connectDb()
            crs = cnx.cursor(buffered=True)
            findWord = None
            try:
                findWord = int(categorySearchEntry.get())
            except:
                findWord = categorySearchEntry.get()
            if findWord is not None and type(findWord) is str:
                crs.execute(
                    """SELECT category_id,name FROM categories
                    WHERE categories.name LIKE '%{0}%'""".format(findWord))
                checkItems = crs.fetchall()
                if len(checkItems) > 1:
                    messagePopUp("İşlem Başarısız",
                                 "Kurs silme işlemi başarısız.\n Lütfen daha spesifik bir arama yapınız.", "cross")
                elif len(checkItems) == 1:
                    crs.execute(
                        """DELETE FROM categories
                        WHERE categories.name LIKE '%{0}%'""".format(findWord))
                    cnx.commit()
                    messagePopUp("İşlem Başarılı", "Kurs silme işlemi başarıyla tamamlandı.", "info")
                else:
                    messagePopUp("İşlem Başarısız",
                                 "Kurs silme işlemi başarısız.\n Aradağınız kriterlere uygun kurs bulunamadı.", "cross")
            elif findWord is not None and type(findWord) is int:
                crs.execute(
                    """SELECT category_id,name FROM categories
                    WHERE categories.category_id = {0}""".format(findWord))
                checkItem = crs.fetchall()
                if checkItem is not None and (0 < len(checkItem) < 2):
                    crs.execute(
                        """DELETE FROM categories
                        WHERE categories.category_id = {0}""".format(findWord))
                    cnx.commit()
                    messagePopUp("İşlem Başarılı", "Kurs silme işlemi başarıyla tamamlandı.", "info")
                else:
                    messagePopUp("İşlem Başarısız", "kurs silme işlemi başarısız.\n Aradığınız kriterlere uygun kurs bulunamadı.", "cross")

        def addCategoryPage():
            addcategorypg = customtkinter.CTkToplevel()
            addcategorypg.title("Online Kurs Sistemi - Admin")
            addcategorypg.geometry("680x470")
            addcategorypg.iconbitmap("academy.ico")
            addcategorypg.resizable(False, True)
            addcategorypg.attributes("-alpha", 0.97)

            addCategoryFrame = customtkinter.CTkFrame(addcategorypg, width=660, corner_radius=0)
            addCategoryFrame.grid(row=0, column=0, rowspan=4, sticky="nsew", pady=20, padx=10)
            addCategoryFrame.grid_rowconfigure(4, weight=1)

            cnx = connectDb()
            crs = cnx.cursor(buffered=True)
            crs.execute("""SELECT * FROM categories""")
            ctItems = crs.fetchall()
            newId = len(ctItems) + 1

            categoryIdLabel = customtkinter.CTkLabel(addCategoryFrame, text="Kurs ID :", width=620,
                                             font=customtkinter.CTkFont(size=12), anchor="w")
            categoryIdLabel.grid(row=0, column=0, padx=20, pady=(20, 5))

            categoryIdLabel = customtkinter.CTkEntry(addCategoryFrame)
            categoryIdLabel.grid(row=1, column=0, columnspan=3, padx=20, pady=(5, 10), sticky="nsew")
            categoryIdLabel.insert(0, newId)
            categoryIdLabel.configure(state="disabled")

            categoryNameLabel = customtkinter.CTkLabel(addCategoryFrame, text="Kategori Adı :", width=620,
                                               font=customtkinter.CTkFont(size=12), anchor="w")
            categoryNameLabel.grid(row=2, column=0, padx=20, pady=(5, 5))

            categoryNameEntry = customtkinter.CTkEntry(addCategoryFrame, placeholder_text="Kategori Adı")
            categoryNameEntry.grid(row=3, column=0, columnspan=3, padx=20, pady=(5, 10), sticky="nsew")

            def addProgress(newId, name):
                addcategorypg.destroy()
                addCategory(newId, name)

            saveButton = customtkinter.CTkButton(addCategoryFrame, fg_color="green",
                                                 command=lambda: addProgress(newId, categoryNameEntry.get()))
            saveButton.configure(text="Kaydet")
            saveButton.grid(row=4, column=0, padx=10, pady=(5, 10))

            addcategorypg.mainloop()

        def addCategory(newId, name):
            cnx = connectDb()
            crs = cnx.cursor(buffered=True)
            crs.execute("""INSERT INTO categories(category_id, name) VALUES({0}, '{1}')""".format(newId, name))
            cnx.commit()
            messagePopUp("İşlem Başarılı", "Kategori ekleme işlemi başarıyla tamamlandı.", "info")

        def editCategoryPage(event):
            editcategorypg = customtkinter.CTkToplevel()
            editcategorypg.title("Online Kurs Sistemi - Admin")
            editcategorypg.geometry("680x470")
            editcategorypg.iconbitmap("academy.ico")
            editcategorypg.resizable(False, True)
            editcategorypg.attributes("-alpha", 0.97)

            selectedRole = categoryTree.item(categoryTree.selection()[0])['values']

            editCategoryFrame = customtkinter.CTkFrame(editcategorypg, width=660, corner_radius=0)
            editCategoryFrame.grid(row=0, column=0, rowspan=4, sticky="nsew", pady=20, padx=10)
            editCategoryFrame.grid_rowconfigure(4, weight=1)

            editCategoryIdLabel = customtkinter.CTkLabel(editCategoryFrame, text="Kategori ID :", width=620,
                                             font=customtkinter.CTkFont(size=12), anchor="w")
            editCategoryIdLabel.grid(row=0, column=0, padx=20, pady=(20, 5))

            editCategoryIdEntry = customtkinter.CTkEntry(editCategoryFrame)
            editCategoryIdEntry.grid(row=1, column=0, columnspan=3, padx=20, pady=(5, 10), sticky="nsew")
            editCategoryIdEntry.insert(0, selectedRole[0])
            editCategoryIdEntry.configure(state="disabled")

            editCategoryNameLabel = customtkinter.CTkLabel(editCategoryFrame, text="Kategori Adı :", width=620,
                                               font=customtkinter.CTkFont(size=12), anchor="w")
            editCategoryNameLabel.grid(row=2, column=0, padx=20, pady=(5, 5))

            editCategoryNameEntry = customtkinter.CTkEntry(editCategoryFrame, placeholder_text="Kategori Adı")
            editCategoryNameEntry.insert(0, selectedRole[1])
            editCategoryNameEntry.grid(row=3, column=0, columnspan=3, padx=20, pady=(5, 10), sticky="nsew")

            def editProgress(newId, name):
                editcategorypg.destroy()
                editCategory(newId, name)

            editButton = customtkinter.CTkButton(editCategoryFrame, fg_color="green",
                                                 command=lambda: editProgress(selectedRole[0], editCategoryNameEntry.get()))
            editButton.configure(text="Kaydet")
            editButton.grid(row=4, column=0, padx=10, pady=(5, 10))

            editcategorypg.mainloop()

        def editCategory(categoryId, name):
            cnx = connectDb()
            crs = cnx.cursor(buffered=True)
            crs.execute("""SELECT categories.category_id, categories.name FROM categories WHERE categories.name = '{0}'""".format(name))
            checkOthers = crs.fetchall()
            if len(checkOthers) > 0:
                messagePopUp("İşlem Başarısız", "Kategori güncelleme işlemi başarısız.\nBu isimde zaten bir kategori kayıtlı.", "cross")
            else:
                crs.execute("""UPDATE categories SET name = '{1}' WHERE categories.category_id = {0}""".format(categoryId, name))
                cnx.commit()
                messagePopUp("İşlem Başarılı", "Rol başarıyla güncellendi", "info")

        categoryFrame = customtkinter.CTkFrame(categoriespg, width=570, corner_radius=0)
        categoryFrame.place(relx=0.5, rely=0.5, anchor=CENTER)

        categorySearchEntry = customtkinter.CTkEntry(categoryFrame, placeholder_text="Kategori Ara")
        categorySearchEntry.grid(row=2, column=0, columnspan=3, padx=(10, 0), pady=(20, 10), sticky="nsew")

        categorySearchBtn = customtkinter.CTkButton(categoryFrame, fg_color="transparent", border_width=2, width=80,
                                                    text_color=("gray10", "#DCE4EE"), command=findCategory)
        categorySearchBtn.configure(text="Ara")
        categorySearchBtn.grid(row=2, column=3, padx=(10, 10), pady=(20, 10), sticky="nsew")

        categoryDeleteBtn = customtkinter.CTkButton(categoryFrame, fg_color="#782c2c", border_width=0, width=300,
                                                    text_color=("gray10", "#DCE4EE"), command=deleteCategory)
        categoryDeleteBtn.configure(text="Sil")
        categoryDeleteBtn.grid(row=3, column=0, columnspan=4, padx=(10, 10), pady=(5, 5), sticky="nsew")

        categoryAddBtn = customtkinter.CTkButton(categoryFrame, border_width=0, width=300, command=addCategoryPage)
        categoryAddBtn.configure(text="Ekle")
        categoryAddBtn.grid(row=4, column=0, columnspan=4, padx=(10, 10), pady=(5, 5), sticky="nsew")

        categoryTree = ttk.Treeview(categoryFrame)
        categoryTree.configure(style="mystyle1.Treeview")

        categoryTree["columns"] = ("category_id", "name")
        categoryTree["show"] = "headings"
        categoryTree.column("category_id", width=100)
        categoryTree.column("name", width=200)

        categoryTree.heading("category_id", text="ID")
        categoryTree.heading("name", text="Kategori")

        categoryTree.grid(row=5, column=0, columnspan=4, pady=20, padx=20, sticky="nsew")
        categoryTree.bind("<Double-1>", editCategoryPage)
        cnx = connectDb()
        crs = cnx.cursor(buffered=True)
        crs.execute("""SELECT category_id, name FROM categories""")
        categoryItems = crs.fetchall()
        for ctItem in categoryItems:
            categoryTree.insert("", 'end', iid=ctItem[0], text=ctItem[0], values=(ctItem[0], ctItem[1]))
        cnx.close()

        categoriespg.mainloop()

    def rolesPage():
        rolespg = customtkinter.CTkToplevel()
        rolespg.title("Online Kurs Sistemi - Admin")
        rolespg.geometry("680x470")
        rolespg.iconbitmap("academy.ico")
        rolespg.resizable(False, True)
        rolespg.attributes("-alpha", 0.97)

        def findRole():
            for i in roleTree.get_children():
                roleTree.delete(i)
            cnx = connectDb()
            crs = cnx.cursor(buffered=True)
            if roleSearchEntry.get() is None:
                crs.execute("""SELECT role_id,name FROM roles""")
            else:
                findWord = None
                try:
                    findWord = int(roleSearchEntry.get())
                except:
                    findWord = roleSearchEntry.get()
                if findWord is not None and type(findWord) is str:
                    crs.execute(
                        """SELECT role_id,name FROM roles
                        WHERE roles.name LIKE '%{0}%'""".format(findWord))
                elif findWord is not None and type(findWord) is int:
                    crs.execute(
                        """SELECT role_id,name FROM roles
                        WHERE roles.role_id = {0}""".format(findWord))
            newRoleItems = crs.fetchall()
            for nRlItem in newRoleItems:
                roleTree.insert("", 'end', iid=nRlItem[0], text=nRlItem[0],
                                    values=(nRlItem[0], nRlItem[1]))
            cnx.close()

        def addRolePage():
            addrolepg = customtkinter.CTkToplevel()
            addrolepg.title("Online Kurs Sistemi - Admin")
            addrolepg.geometry("680x470")
            addrolepg.iconbitmap("academy.ico")
            addrolepg.resizable(False, True)
            addrolepg.attributes("-alpha", 0.97)

            addRoleFrame = customtkinter.CTkFrame(addrolepg, width=660, corner_radius=0)
            addRoleFrame.grid(row=0, column=0, rowspan=4, sticky="nsew", pady=20, padx=10)
            addRoleFrame.grid_rowconfigure(4, weight=1)

            cnx = connectDb()
            crs = cnx.cursor(buffered=True)
            crs.execute("""SELECT * FROM roles""")
            ctItems = crs.fetchall()
            newId = len(ctItems) + 1

            roleIdLabel = customtkinter.CTkLabel(addRoleFrame, text="Rol ID :", width=620,
                                             font=customtkinter.CTkFont(size=12), anchor="w")
            roleIdLabel.grid(row=0, column=0, padx=20, pady=(20, 5))

            roleIdLabel = customtkinter.CTkEntry(addRoleFrame)
            roleIdLabel.grid(row=1, column=0, columnspan=3, padx=20, pady=(5, 10), sticky="nsew")
            roleIdLabel.insert(0, newId)
            roleIdLabel.configure(state="disabled")

            roleNameLabel = customtkinter.CTkLabel(addRoleFrame, text="Rol Adı :", width=620,
                                               font=customtkinter.CTkFont(size=12), anchor="w")
            roleNameLabel.grid(row=2, column=0, padx=20, pady=(5, 5))

            roleNameEntry = customtkinter.CTkEntry(addRoleFrame, placeholder_text="Rol Adı")
            roleNameEntry.grid(row=3, column=0, columnspan=3, padx=20, pady=(5, 10), sticky="nsew")

            def addProgress(newId, name):
                addrolepg.destroy()
                addRole(newId, name)

            saveButton = customtkinter.CTkButton(addRoleFrame, fg_color="green",
                                                 command=lambda: addProgress(newId, roleNameEntry.get()))
            saveButton.configure(text="Kaydet")
            saveButton.grid(row=4, column=0, padx=10, pady=(5, 10))

            addrolepg.mainloop()

        def addRole(newId, name):
            cnx = connectDb()
            crs = cnx.cursor(buffered=True)
            crs.execute("""INSERT INTO roles(role_id, name) VALUES({0}, '{1}')""".format(newId, name))
            cnx.commit()
            messagePopUp("İşlem Başarılı", "Rol ekleme işlemi başarıyla tamamlandı.", "info")

        def editRolePage(event):
            editrolepg = customtkinter.CTkToplevel()
            editrolepg.title("Online Kurs Sistemi - Admin")
            editrolepg.geometry("680x470")
            editrolepg.iconbitmap("academy.ico")
            editrolepg.resizable(False, True)
            editrolepg.attributes("-alpha", 0.97)

            selectedRole = roleTree.item(roleTree.selection()[0])['values']

            editRoleFrame = customtkinter.CTkFrame(editrolepg, width=660, corner_radius=0)
            editRoleFrame.grid(row=0, column=0, rowspan=4, sticky="nsew", pady=20, padx=10)
            editRoleFrame.grid_rowconfigure(4, weight=1)

            editRoleIdLabel = customtkinter.CTkLabel(editRoleFrame, text="Rol ID :", width=620,
                                             font=customtkinter.CTkFont(size=12), anchor="w")
            editRoleIdLabel.grid(row=0, column=0, padx=20, pady=(20, 5))

            editRoleIdEntry = customtkinter.CTkEntry(editRoleFrame)
            editRoleIdEntry.grid(row=1, column=0, columnspan=3, padx=20, pady=(5, 10), sticky="nsew")
            editRoleIdEntry.insert(0, selectedRole[0])
            editRoleIdEntry.configure(state="disabled")

            editRoleNameLabel = customtkinter.CTkLabel(editRoleFrame, text="Rol Adı :", width=620,
                                               font=customtkinter.CTkFont(size=12), anchor="w")
            editRoleNameLabel.grid(row=2, column=0, padx=20, pady=(5, 5))

            editRoleNameEntry = customtkinter.CTkEntry(editRoleFrame, placeholder_text="Rol Adı")
            editRoleNameEntry.insert(0, selectedRole[1])
            editRoleNameEntry.grid(row=3, column=0, columnspan=3, padx=20, pady=(5, 10), sticky="nsew")

            def editProgress(newId, name):
                editrolepg.destroy()
                editRole(newId, name)

            editButton = customtkinter.CTkButton(editRoleFrame, fg_color="green",
                                                 command=lambda: editProgress(selectedRole[0], editRoleNameEntry.get()))
            editButton.configure(text="Kaydet")
            editButton.grid(row=4, column=0, padx=10, pady=(5, 10))

            editrolepg.mainloop()

        def editRole(roleId, name):
            cnx = connectDb()
            crs = cnx.cursor(buffered=True)
            crs.execute("""SELECT roles.role_id, roles.name FROM roles WHERE roles.name = '{0}'""".format(name))
            checkOthers = crs.fetchall()
            if len(checkOthers) > 0:
                messagePopUp("İşlem Başarısız", "Rol güncelleme işlemi başarısız.\nBu isimde zaten bir rol kayıtlı.", "cross")
            else:
                crs.execute("""UPDATE roles SET name = '{1}' WHERE roles.role_id = {0}""".format(roleId, name))
                cnx.commit()
                messagePopUp("İşlem Başarılı", "Rol başarıyla güncellendi", "info")

        def deleteRole():
            cnx = connectDb()
            crs = cnx.cursor(buffered=True)
            findWord = None
            try:
                findWord = int(roleSearchEntry.get())
            except:
                findWord = roleSearchEntry.get()
            if findWord is not None and type(findWord) is str:
                crs.execute(
                    """SELECT role_id,name FROM roles
                    WHERE roles.name LIKE '%{0}%'""".format(findWord))
                checkItems = crs.fetchall()
                if len(checkItems) > 1:
                    messagePopUp("İşlem Başarısız",
                                 "Rol silme işlemi başarısız.\n Lütfen daha spesifik bir arama yapınız.", "cross")
                elif len(checkItems) == 1:
                    crs.execute(
                        """DELETE FROM roles
                        WHERE roles.name LIKE '%{0}%'""".format(findWord))
                    cnx.commit()
                    messagePopUp("İşlem Başarılı", "Rol silme işlemi başarıyla tamamlandı.", "info")
                else:
                    messagePopUp("İşlem Başarısız",
                                 "Rol silme işlemi başarısız.\n Aradağınız kriterlere uygun kurs bulunamadı.", "cross")
            elif findWord is not None and type(findWord) is int:
                crs.execute(
                    """SELECT role_id,name FROM roles
                    WHERE roles.role_id = {0}""".format(findWord))
                checkItem = crs.fetchall()
                if checkItem is not None and (0 < len(checkItem) < 2):
                    crs.execute(
                        """DELETE FROM roles
                        WHERE roles.role_id = {0}""".format(findWord))
                    cnx.commit()
                    messagePopUp("İşlem Başarılı", "Rol silme işlemi başarıyla tamamlandı.", "info")
                else:
                    messagePopUp("İşlem Başarısız", "Rol silme işlemi başarısız.\n Aradığınız kriterlere uygun kurs bulunamadı.", "cross")

        rolesFrame = customtkinter.CTkFrame(rolespg, width=570, corner_radius=0)
        rolesFrame.place(relx=0.5, rely=0.5, anchor=CENTER)

        roleSearchEntry = customtkinter.CTkEntry(rolesFrame, placeholder_text="Rol Ara")
        roleSearchEntry.grid(row=2, column=0, columnspan=3, padx=(10, 0), pady=(20, 10), sticky="nsew")

        roleSearchBtn = customtkinter.CTkButton(rolesFrame, fg_color="transparent", border_width=2, width=80,
                                                    text_color=("gray10", "#DCE4EE"), command=findRole)
        roleSearchBtn.configure(text="Ara")
        roleSearchBtn.grid(row=2, column=3, padx=(10, 10), pady=(20, 10), sticky="nsew")

        roleAddBtn = customtkinter.CTkButton(rolesFrame, border_width=0, width=300, command=addRolePage)
        roleAddBtn.configure(text="Ekle")
        roleAddBtn.grid(row=3, column=0, columnspan=4, padx=(10, 10), pady=(5, 5), sticky="nsew")

        roleDeleteBtn = customtkinter.CTkButton(rolesFrame, fg_color="#782c2c", border_width=0, width=300,
                                                    text_color=("gray10", "#DCE4EE"), command=deleteRole)
        roleDeleteBtn.configure(text="Sil")
        roleDeleteBtn.grid(row=4, column=0, columnspan=4, padx=(10, 10), pady=(5, 5), sticky="nsew")

        roleTree = ttk.Treeview(rolesFrame)
        roleTree.configure(style="mystyle1.Treeview")

        roleTree["columns"] = ("role_id", "name")
        roleTree["show"] = "headings"
        roleTree.column("role_id", width=100)
        roleTree.column("name", width=200)

        roleTree.heading("role_id", text="ID")
        roleTree.heading("name", text="Rol")

        roleTree.grid(row=5, column=0, columnspan=4, pady=20, padx=20, sticky="nsew")
        roleTree.bind("<Double-1>", editRolePage)
        cnx = connectDb()
        crs = cnx.cursor(buffered=True)
        crs.execute("""SELECT role_id, name FROM roles""")
        roleItems = crs.fetchall()
        for roleItem in roleItems:
            roleTree.insert("", 'end', iid=roleItem[0], text=roleItem[0], values=(roleItem[0], roleItem[1]))
        cnx.close()

        rolespg.mainloop()

    def findUser():
        for i in tree.get_children():
            tree.delete(i)
        cnx = connectDb()
        crs = cnx.cursor(buffered=True)
        if mainEntry.get() is None:
            crs.execute("""SELECT user_id,name,surname,phone,email,cash FROM users""")
        else:
            crs.execute(
                """SELECT user_id,name,surname,phone,email,cash FROM users
                WHERE users.name LIKE '%{0}%' 
                OR users.surname LIKE '%{0}%'
                OR users.phone = '{0}'
                OR users.email LIKE '%{0}%'""".format(
                    mainEntry.get()))
        items = crs.fetchall()
        for item in items:
            tree.insert("", 'end', iid=item[0], text=item[0],
                        values=(item[0], item[1], item[2], item[3], item[4], item[5]))
        cnx.close()

    def editUserPage(event):
        editUsrPg = customtkinter.CTkToplevel()
        editUsrPg.title("Online Kurs Sistemi - Admin")
        editUsrPg.geometry("680x680")
        editUsrPg.iconbitmap("academy.ico")
        editUsrPg.resizable(False, True)
        editUsrPg.attributes("-alpha", 0.97)

        def editUser():
            cnx = connectDb()
            crs = cnx.cursor(buffered=True)

            crs.execute(
                """SELECT role_id,name FROM roles
                WHERE roles.name LIKE '%{0}%'""".format(usrRoleEntry.get()))
            checkRole = crs.fetchall()
            if 0 < len(checkRole) < 2:
                crs.execute("""SELECT users.user_id, roles.role_id FROM users INNER JOIN user_roles ON users.user_id = user_roles.user_id
                                INNER JOIN roles ON roles.role_id = user_roles.role_id
                                WHERE users.email = '{0}'""".format(usrMail))
                checkUsr = crs.fetchone()
                if (checkUsr[0] == selectedUsr[0]) and (checkUsr[1] != checkRole[0][0]):
                    messagePopUp("İşlem Başarısız", "Kullanıcı güncelleme işlemi başarısız.\nKendi rol bilgilerinizi güncelleyemezsiniz", "cross")
                else:
                    usrRoleId = checkRole[0][0]
                    crs.execute("""UPDATE users SET name = '{1}', surname = '{2}', phone = '{3}', cash = {4}
                                            WHERE users.user_id = {0};""".format(selectedUsr[0], usrNameEntry.get(),
                                                                                 usrSurnameEntry.get(),
                                                                                 usrPhoneEntry.get(),
                                                                                 usrCashEntry.get()))
                    cnx.commit()
                    crs.execute("""UPDATE user_roles SET role_id = {1}
                                                WHERE user_roles.user_id = {0}""".format(selectedUsr[0], usrRoleId))
                    cnx.commit()
                    messagePopUp("İşlem Başarılı", "Kullanıcı başarıyla güncellendi.", "info")
            else:
                messagePopUp("İşlem Başarısız", "Kullanıcı güncelleme işlemi başarısız.\nLütfen geçerli bir rol giriniz.", "cross")

        editUsrFrame = customtkinter.CTkFrame(editUsrPg)
        editUsrFrame.place(relx=0.5, rely=0.5, anchor=CENTER)

        selectedUsr = tree.item(tree.selection()[0])['values']

        usrIdLabel = customtkinter.CTkLabel(editUsrFrame, text="Kullanıcı ID :", width=620,
                                             font=customtkinter.CTkFont(size=12), anchor="w")
        usrIdLabel.grid(row=0, column=0, padx=20, pady=(20, 5))

        usrIdEntry = customtkinter.CTkEntry(editUsrFrame)
        usrIdEntry.grid(row=1, column=0, columnspan=3, padx=20, pady=(5, 10), sticky="nsew")
        usrIdEntry.insert(0, selectedUsr[0])
        usrIdEntry.configure(state="disabled")

        usrNameLabel = customtkinter.CTkLabel(editUsrFrame, text="İsim :", width=620,
                                               font=customtkinter.CTkFont(size=12), anchor="w")
        usrNameLabel.grid(row=2, column=0, padx=20, pady=(10, 5))

        usrNameEntry = customtkinter.CTkEntry(editUsrFrame, width=300, height=30, border_width=1,
                                           text_color="silver")
        usrNameEntry.insert("0", selectedUsr[1])
        usrNameEntry.grid(row=3, column=0, padx=20, pady=(5, 10), sticky="nsew")

        usrSurameLabel = customtkinter.CTkLabel(editUsrFrame, text="Soyisim :", width=620,
                                              font=customtkinter.CTkFont(size=12), anchor="w")
        usrSurameLabel.grid(row=4, column=0, padx=20, pady=(10, 5))
        usrSurnameEntry = customtkinter.CTkEntry(editUsrFrame, placeholder_text="Soyisim", width=300, height=30,
                                              border_width=1,
                                              text_color="silver")
        usrSurnameEntry.insert("0", selectedUsr[2])
        usrSurnameEntry.grid(row=5, column=0, padx=20, pady=(5, 10), sticky="nsew")

        usrPhoneLabel = customtkinter.CTkLabel(editUsrFrame, text="Telefon Numarası :", width=620,
                                                font=customtkinter.CTkFont(size=12), anchor="w")
        usrPhoneLabel.grid(row=6, column=0, padx=20, pady=(10, 5))
        usrPhoneEntry = customtkinter.CTkEntry(editUsrFrame, placeholder_text="Telefon Numarası", width=300, height=30,
                                            border_width=1, text_color="silver")
        usrPhoneEntry.insert("0", selectedUsr[3])
        usrPhoneEntry.grid(row=7, column=0, padx=20, pady=(5, 10), sticky="nsew")

        usrCashLabel = customtkinter.CTkLabel(editUsrFrame, text="Bakiye :", width=620,
                                              font=customtkinter.CTkFont(size=12), anchor="w")
        usrCashLabel.grid(row=8, column=0, padx=20, pady=(10, 5))
        usrCashEntry = customtkinter.CTkEntry(editUsrFrame, placeholder_text="Bakiye", width=300, height=30,
                                               border_width=1, text_color="silver")
        usrCashEntry.insert("0", selectedUsr[5])
        usrCashEntry.grid(row=9, column=0, padx=20, pady=(5, 10), sticky="nsew")

        usrRoleLabel = customtkinter.CTkLabel(editUsrFrame, text="Rol :", width=620,
                                              font=customtkinter.CTkFont(size=12), anchor="w")
        usrRoleLabel.grid(row=10, column=0, padx=20, pady=(10, 5))
        usrRoleEntry = customtkinter.CTkEntry(editUsrFrame, placeholder_text="Rol", width=300, height=30,
                                              border_width=1, text_color="silver")
        usrRoleEntry.insert("0", selectedUsr[6])
        usrRoleEntry.grid(row=11, column=0, padx=20, pady=(5, 10), sticky="nsew")

        saveButton = customtkinter.CTkButton(editUsrFrame,
                                                 command=editUser)
        saveButton.configure(text="Kaydet")
        saveButton.grid(row=12, column=0, padx=20, pady=(10, 20), sticky="n")

        editUsrPg.mainloop()

    adminFrame = customtkinter.CTkFrame(adminPage, width=500, corner_radius=0)
    adminFrame.grid(row=0, column=0, rowspan=4, sticky="nsew")
    adminFrame.grid_rowconfigure(4, weight=1)

    logo_label = customtkinter.CTkLabel(adminFrame, text="Admin Paneli",
                                        font=customtkinter.CTkFont(size=20, weight="bold"))
    logo_label.grid(row=0, column=0, padx=(20, 10), pady=(20, 20))

    navbarButton1 = customtkinter.CTkButton(adminFrame, command=coursePage)
    navbarButton1.configure(text="Kurslar")
    navbarButton1.grid(row=0, column=1, padx=10, pady=10)
    navbarButton2 = customtkinter.CTkButton(adminFrame, command=categoriesPage)
    navbarButton2.configure(text="Kategoriler")
    navbarButton2.grid(row=0, column=2, padx=10, pady=10)
    navbarButton3 = customtkinter.CTkButton(adminFrame, command=rolesPage)
    navbarButton3.configure(text="Roller")
    navbarButton3.grid(row=0, column=3, padx=10, pady=30)

    mainEntry = customtkinter.CTkEntry(adminFrame, placeholder_text="Kullanıcı Ara")
    mainEntry.grid(row=2, column=0, columnspan=3, padx=(20, 0), pady=(20, 20), sticky="nsew")

    main_button_1 = customtkinter.CTkButton(adminFrame, fg_color="transparent", border_width=2,
                                            text_color=("gray10", "#DCE4EE"), command=findUser)
    main_button_1.configure(text="Ara")
    main_button_1.grid(row=2, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

    tree = ttk.Treeview(adminPage)
    tree.configure(style="mystyle1.Treeview")

    tree["columns"] = ("id", "name", "surname", "phone", "email", "cash", "role")
    tree["show"] = "headings"
    tree.column("id", width=40, anchor=CENTER)
    tree.column("name", width=150)
    tree.column("surname", width=80)
    tree.column("phone", width=150, anchor=CENTER)
    tree.column("email", width=200, anchor=CENTER)
    tree.column("cash", width=100, anchor=CENTER)
    tree.column("role", width=100, anchor=CENTER)

    tree.heading("id", text="ID")
    tree.heading("name", text="Isim")
    tree.heading("surname", text="Soyisim")
    tree.heading("phone", text="Telefon Numarası")
    tree.heading("email", text="E-posta Adresi")
    tree.heading("cash", text="Bakiye")
    tree.heading("role", text="Rol")

    tree.grid(column=0, row=5, columnspan=3, pady=20)
    tree.bind("<Double-1>", editUserPage)
    cnx = connectDb()
    crs = cnx.cursor(buffered=True)
    crs.execute("""SELECT users.user_id,users.name,surname,phone,email,cash, roles.name
                    FROM users INNER JOIN user_roles ON users.user_id = user_roles.user_id
                    INNER JOIN roles ON roles.role_id = user_roles.role_id""")
    items = crs.fetchall()
    for item in items:
        tree.insert("", 'end', iid=item[0], text=item[0], values=(item[0], item[1], item[2], item[3], item[4], item[5], item[6]))
    cnx.close()

    adminPage.mainloop()


def openInstructorPage():
    instructorPage = customtkinter.CTk()
    instructorPage.title("Online Kurs Sistemi - Eğitmen")
    instructorPage.geometry("660x470")
    instructorPage.iconbitmap("academy.ico")
    instructorPage.resizable(False, False)
    instructorPage.attributes("-alpha", 0.97)

    def addCourse(newId, name, description, price, category):
        cnx = connectDb()
        crs = cnx.cursor(buffered=True)

        try:
            category = int(category)
            crs.execute(
                """SELECT category_id,name FROM categories WHERE categories.category_id = {}""".format(category))
            findCategory = crs.fetchone()
        except:
            crs.execute(
                """SELECT category_id,name FROM categories WHERE categories.name LIKE '%{}%'""".format(category))
            findCategory = crs.fetchone()

        if findCategory is not None:
            crs.execute("""SELECT user_id FROM users WHERE users.email = '{}'""".format(usrMail))
            instructorId = crs.fetchone()[0]
            crs.execute("""INSERT INTO courses(course_id, instructor_id, name, description, price) VALUES({0}, {1}, '{2}', 
                        '{3}', {4})""".format(newId, instructorId, name, description, price))
            cnx.commit()
            crs.execute("""INSERT INTO course_categories(course_id, category_id) VALUES({0}, {1})""".format(newId, findCategory[0]))
            cnx.commit()
            messagePopUp("İşlem Başarılı", "Kurs ekleme işlemi başarıyla tamamlandı.", "info")
        else:
            messagePopUp("İşlem Başarısız", "Kurs ekleme işlemi başarısız.\nLütfen geçerli bir kategori giriniz.",
                         "cross")

    def addCoursePage():
        courseaddpg = customtkinter.CTk()
        courseaddpg.title("Online Kurs Sistemi - Eğitmen")
        courseaddpg.geometry("680x580")
        courseaddpg.iconbitmap("academy.ico")
        courseaddpg.resizable(False, False)
        courseaddpg.attributes("-alpha", 0.97)

        cnx = connectDb()
        crs = cnx.cursor(buffered=True)
        crs.execute("""SELECT * FROM courses""")
        ctItems = crs.fetchall()
        newId = len(ctItems) + 1

        addFrame = customtkinter.CTkFrame(courseaddpg, width=660, corner_radius=0)
        addFrame.grid(row=0, column=0, rowspan=4, sticky="nsew", pady=20, padx=10)
        addFrame.grid_rowconfigure(4, weight=1)

        idLabel = customtkinter.CTkLabel(addFrame, text="Kurs ID :", width=620,
                                         font=customtkinter.CTkFont(size=12), anchor="w")
        idLabel.grid(row=0, column=0, padx=20, pady=(20, 5))

        idEntry = customtkinter.CTkEntry(addFrame)
        idEntry.grid(row=1, column=0, columnspan=3, padx=20, pady=(5, 10), sticky="nsew")
        idEntry.insert(0, newId)
        idEntry.configure(state="disabled")

        nameLabel = customtkinter.CTkLabel(addFrame, text="Kurs Adı :", width=620,
                                           font=customtkinter.CTkFont(size=12), anchor="w")
        nameLabel.grid(row=2, column=0, padx=20, pady=(5, 5))

        nameEntry = customtkinter.CTkEntry(addFrame, placeholder_text="Kurs Adı")
        nameEntry.grid(row=3, column=0, columnspan=3, padx=20, pady=(5, 10), sticky="nsew")

        descriptionLabel = customtkinter.CTkLabel(addFrame, text="Açıklama :", width=620,
                                                  font=customtkinter.CTkFont(size=12), anchor="w")
        descriptionLabel.grid(row=4, column=0, padx=20, pady=(5, 5))

        descriptionEntry = customtkinter.CTkEntry(addFrame, placeholder_text="Açıklama")
        descriptionEntry.grid(row=5, column=0, columnspan=3, padx=20, pady=(5, 10), sticky="nsew")

        priceLabel = customtkinter.CTkLabel(addFrame, text="Fiyat :", width=620,
                                            font=customtkinter.CTkFont(size=12), anchor="w")
        priceLabel.grid(row=6, column=0, padx=20, pady=(5, 5))

        priceEntry = customtkinter.CTkEntry(addFrame, placeholder_text="Fiyat")
        priceEntry.grid(row=7, column=0, columnspan=3, padx=20, pady=(5, 10), sticky="nsew")

        categoryLabel = customtkinter.CTkLabel(addFrame, text="Category ID :", width=620,
                                               font=customtkinter.CTkFont(size=12), anchor="w")
        categoryLabel.grid(row=10, column=0, padx=20, pady=(5, 5))

        categoryEntry = customtkinter.CTkEntry(addFrame, placeholder_text="Category ID")
        categoryEntry.grid(row=11, column=0, columnspan=3, padx=20, pady=(5, 5), sticky="nsew")

        saveButton = customtkinter.CTkButton(addFrame, fg_color="green",
                                             command=lambda: addCourse(newId, nameEntry.get(),
                                                                        descriptionEntry.get(), priceEntry.get(), categoryEntry.get()))
        saveButton.configure(text="Kaydet")
        saveButton.grid(row=12, column=0, padx=10, pady=(5, 10))

        courseaddpg.mainloop()

    def profilePage():
        profilePg = customtkinter.CTkToplevel()
        profilePg.title("Online Kurs Sistemi - Eğitmen")
        profilePg.geometry("680x540")
        profilePg.iconbitmap("academy.ico")
        profilePg.resizable(False, False)
        profilePg.attributes("-alpha", 0.97)

        def editProfile():
            cnx = connectDb()
            crs = cnx.cursor(buffered=True)
            crs.execute("""UPDATE users SET name = '{1}', surname = '{2}', phone = '{3}'
                                                                            WHERE users.user_id = {0};""".format(
                selectedUsr[0],
                usrNameEntry.get(),
                usrSurnameEntry.get(),
                usrPhoneEntry.get()))
            cnx.commit()
            messagePopUp("İşlem Başarılı", "Kullanıcı başarıyla güncellendi.", "info")

        def addCashPage():
            addcashpg = customtkinter.CTkToplevel()
            addcashpg.title("Online Kurs Sistemi - Eğitmen")
            addcashpg.geometry("680x270")
            addcashpg.iconbitmap("academy.ico")
            addcashpg.resizable(False, False)
            addcashpg.attributes("-alpha", 0.97)

            addCashFrame = customtkinter.CTkFrame(addcashpg, width=660, corner_radius=0)
            addCashFrame.place(relx=0.5, rely=0.5, anchor=CENTER)

            cashLabel = customtkinter.CTkLabel(addCashFrame, text="Eklemek İstediğiniz Miktarı Giriniz :", width=620,
                                                 font=customtkinter.CTkFont(size=12), anchor="w")
            cashLabel.grid(row=0, column=0, padx=20, pady=(20, 5))

            cashEntry = customtkinter.CTkEntry(addCashFrame)
            cashEntry.grid(row=1, column=0, columnspan=3, padx=20, pady=(5, 10), sticky="nsew")

            def addProgress(amount):
                addcashpg.destroy()
                addCash(amount)

            addCashButton = customtkinter.CTkButton(addCashFrame, fg_color="green",
                                                 command=lambda: addProgress(cashEntry.get()))
            addCashButton.configure(text="Ekle")
            addCashButton.grid(row=4, column=0, padx=10, pady=(5, 10))

            addcashpg.mainloop()

        def addCash(amount):
            cnx = connectDb()
            crs = cnx.cursor(buffered=True)
            crs.execute("""SELECT users.cash FROM users WHERE users.email = '{}'""".format(usrMail))
            currentCash = crs.fetchone()[0]
            try:
                amount = int(amount)
                newCash = int(currentCash) + amount
                crs.execute("""UPDATE users SET cash = {0} WHERE users.email = '{1}'""".format(newCash, usrMail))
                cnx.commit()
                messagePopUp("İşlem Başarılı", "Bakiye ekleme işlemi başarıyla tamamlandı.", "info")
            except:
                messagePopUp("İşlem Başarısız", "Bakiye ekleme işlemi başarısız.\nLütfen geçerli bir miktar giriniz.", "cross")

        profileFrame = customtkinter.CTkFrame(profilePg)
        profileFrame.place(relx=0.5, rely=0.5, anchor=CENTER)

        cnx = connectDb()
        crs = cnx.cursor(buffered=True)

        crs.execute("""SELECT users.user_id, users.name, users.surname, users.phone, users.cash FROM users 
                                INNER JOIN user_roles ON users.user_id = user_roles.user_id
                                INNER JOIN roles ON roles.role_id = user_roles.role_id
                                WHERE users.email = '{0}'""".format(usrMail))
        selectedUsr = crs.fetchone()

        usrIdLabel = customtkinter.CTkLabel(profileFrame, text="Kullanıcı ID :", width=620,
                                            font=customtkinter.CTkFont(size=12), anchor="w")
        usrIdLabel.grid(row=0, column=0, padx=20, pady=(20, 5))

        usrIdEntry = customtkinter.CTkEntry(profileFrame)
        usrIdEntry.grid(row=1, column=0, columnspan=3, padx=20, pady=(5, 10), sticky="nsew")
        usrIdEntry.insert(0, selectedUsr[0])
        usrIdEntry.configure(state="disabled")

        cashLabel = customtkinter.CTkLabel(profileFrame, text="Bakiye :", width=620,
                                            font=customtkinter.CTkFont(size=12), anchor="w")
        cashLabel.grid(row=2, column=0, padx=20, pady=(10, 5))

        cashEntry = customtkinter.CTkEntry(profileFrame)
        cashEntry.grid(row=3, column=0, columnspan=3, padx=20, pady=(5, 10), sticky="nsew")
        cashEntry.insert(0, selectedUsr[4])
        cashEntry.configure(state="disabled")

        usrNameLabel = customtkinter.CTkLabel(profileFrame, text="İsim :", width=620,
                                              font=customtkinter.CTkFont(size=12), anchor="w")
        usrNameLabel.grid(row=4, column=0, padx=20, pady=(10, 5))

        usrNameEntry = customtkinter.CTkEntry(profileFrame, width=300, height=30, border_width=1,
                                              text_color="silver")
        usrNameEntry.insert("0", selectedUsr[1])
        usrNameEntry.grid(row=5, column=0, padx=20, pady=(5, 10), sticky="nsew")

        usrSurameLabel = customtkinter.CTkLabel(profileFrame, text="Soyisim :", width=620,
                                                font=customtkinter.CTkFont(size=12), anchor="w")
        usrSurameLabel.grid(row=6, column=0, padx=20, pady=(10, 5))
        usrSurnameEntry = customtkinter.CTkEntry(profileFrame, placeholder_text="Soyisim", width=300, height=30,
                                                 border_width=1,
                                                 text_color="silver")
        usrSurnameEntry.insert("0", selectedUsr[2])
        usrSurnameEntry.grid(row=7, column=0, padx=20, pady=(5, 10), sticky="nsew")

        usrPhoneLabel = customtkinter.CTkLabel(profileFrame, text="Telefon Numarası :", width=620,
                                               font=customtkinter.CTkFont(size=12), anchor="w")
        usrPhoneLabel.grid(row=8, column=0, padx=20, pady=(10, 5))
        usrPhoneEntry = customtkinter.CTkEntry(profileFrame, placeholder_text="Telefon Numarası", width=300, height=30,
                                               border_width=1, text_color="silver")
        usrPhoneEntry.insert("0", selectedUsr[3])
        usrPhoneEntry.grid(row=9, column=0, padx=20, pady=(5, 10), sticky="nsew")

        buttonFrame = customtkinter.CTkFrame(profileFrame, width=600, corner_radius=0, fg_color="gray13")
        buttonFrame.grid(row=10, column=0, columnspan=2, sticky="ns")
        buttonFrame.grid_rowconfigure(4, weight=1)

        saveButton = customtkinter.CTkButton(buttonFrame,
                                             command=editProfile, fg_color="green")
        saveButton.configure(text="Kaydet")
        saveButton.grid(row=0, column=0, padx=20, pady=(10, 20), sticky="n")

        cashButton = customtkinter.CTkButton(buttonFrame,
                                             command=addCashPage)
        cashButton.configure(text="Bakiye Ekle")
        cashButton.grid(row=0, column=1, padx=20, pady=(10, 20), sticky="n")

        profilePg.mainloop()

    def deleteCourse(courseId):
        cnx = connectDb()
        crs = cnx.cursor(buffered=True)
        crs.execute("""DELETE FROM course_categories WHERE course_id = {}""".format(courseId))
        cnx.commit()
        crs.execute("""DELETE FROM courses WHERE course_id = {}""".format(courseId))
        cnx.commit()
        messagePopUp("İşlem Başarılı", "ID'si {} olan kurs başarıyla silinmiştir".format(courseId))

    def exit():
        global usrMail
        usrMail = ""
        instructorPage.destroy()

    instructorFrame = customtkinter.CTkFrame(instructorPage, width=500, corner_radius=0)
    instructorFrame.grid(row=0, column=0, rowspan=4, sticky="nsew")
    instructorFrame.grid_rowconfigure(4, weight=1)

    instructorLabel = customtkinter.CTkLabel(instructorFrame, text="Eğitmen Paneli",
                                        font=customtkinter.CTkFont(size=20, weight="bold"))
    instructorLabel.grid(row=0, column=0, padx=(20, 10), pady=(20, 20))

    navbarButton1 = customtkinter.CTkButton(instructorFrame, command=addCoursePage)
    navbarButton1.configure(text="Kurs Ekle")
    navbarButton1.grid(row=0, column=1, padx=10, pady=10)
    navbarButton2 = customtkinter.CTkButton(instructorFrame, command=profilePage)
    navbarButton2.configure(text="Profil")
    navbarButton2.grid(row=0, column=2, padx=10, pady=10)
    navbarButton3 = customtkinter.CTkButton(instructorFrame, fg_color="#782c2c", command=exit)
    navbarButton3.configure(text="Çıkış")
    navbarButton3.grid(row=0, column=3, padx=10, pady=30)

    instructorCourseLabel = customtkinter.CTkLabel(instructorPage, text="Verilen Kurslar :", width=620,
                                           font=customtkinter.CTkFont(size=12), anchor="w")
    instructorCourseLabel.grid(row=4, column=0, padx=20, pady=(10, 10))

    #scroll
    instructorCourseFrame = customtkinter.CTkFrame(instructorPage, width=500, height=400, corner_radius=0, fg_color="transparent")
    instructorCourseFrame.grid(row=5, column=0, sticky="nsew")

    instructorCanvas = Canvas(instructorCourseFrame, bg="gray10", highlightthickness=0)
    instructorCanvas.pack(side=LEFT, fill=BOTH, expand=1)

    instructorScrollbar = customtkinter.CTkScrollbar(instructorCanvas, command=instructorCanvas.yview)
    instructorScrollbar.pack(side=RIGHT, fill=Y)

    instructorCanvas.configure(yscrollcommand=instructorScrollbar.set)
    instructorCanvas.bind("<Configure>", lambda e: instructorCanvas.configure(scrollregion=instructorCanvas.bbox("all")))

    secondInstructorFrame = customtkinter.CTkFrame(instructorCanvas, corner_radius=0, fg_color="transparent")

    instructorCanvas.create_window((0, 0), window=secondInstructorFrame, anchor="nw")

    # egitmenin kurslarını getir
    def getInstructorCourses():
        courseItems = []
        cnx = connectDb()
        crs = cnx.cursor(buffered=True)
        crs.execute("""SELECT courses.course_id, courses.name, courses.description, courses.price, CONCAT(users.name, " ", users.surname), categories.name AS category
                            FROM users INNER JOIN courses ON users.user_id = courses.instructor_id
                            INNER JOIN course_categories ON course_categories.course_id = courses.course_id
                            INNER JOIN categories ON course_categories.category_id = categories.category_id
                            WHERE users.email = '{0}'""".format(usrMail))
        items = crs.fetchall()
        for item in items:
            courseItems.append(item)
        return courseItems

    # kursları listele
    def listCourses(courseData):
        count = 0
        for course in courseData:
            courseFrame = customtkinter.CTkFrame(secondInstructorFrame, width=430, height=300)
            if count == 0:
                courseFrame.grid(row=(count * 3) + 1, column=0, padx=10, pady=(10, 5))
            elif 0 < count < (len(courseData) - 1):
                courseFrame.grid(row=(count * 3) + 1, column=0, padx=10, pady=(5, 5))
            else:
                courseFrame.grid(row=(count * 3) + 1, column=0, padx=10, pady=(5, 10))
            courseName = customtkinter.CTkLabel(courseFrame, text=course[1], width=425,
                                                font=customtkinter.CTkFont(size=16, weight="bold"), anchor="w")
            courseName.grid(row=(count * 3), columnspan=2, padx=20, pady=(10, 5))

            courseDescription = customtkinter.CTkLabel(courseFrame, width=425, text=course[2],
                                                       font=customtkinter.CTkFont(size=12), anchor="w")
            courseDescription.grid(row=(count * 3) + 1, columnspan=2, padx=20, pady=(5, 5))

            courseInstructor = customtkinter.CTkLabel(courseFrame, width=425,
                                                      text="Instructor: {}".format(course[4]),
                                                      font=customtkinter.CTkFont(size=12), anchor="w")
            courseInstructor.grid(row=(count * 3) + 2, columnspan=2, padx=20, pady=(5, 10))

            detailsButton = customtkinter.CTkButton(courseFrame)
            detailsButton.configure(text="Detay")
            detailsButton.focus()
            detailsButton.grid(row=(count * 3) + 1, column=3, padx=10, pady=(5, 5))

            courseDeleteButton = customtkinter.CTkButton(courseFrame, fg_color="#782c2c",
                                                         command=lambda x=course[0]: controlPopUp("Kurs Silme İşlemi",
                                                                                                "ID'si {} olan kursu silmek istediğinizden emin misiniz ?".format(x), "info",
                                                                                                deleteCourse, x))
            courseDeleteButton.configure(text="Sil")
            courseDeleteButton.focus()
            courseDeleteButton.grid(row=(count * 3) + 2, column=3, padx=10, pady=(5, 5))
            count += 1

    courses = getInstructorCourses()
    listCourses(courses)

    instructorPage.mainloop()


def openClientPage():
    clientPage = customtkinter.CTk()
    clientPage.title("Online Kurs Sistemi - Müşteri")
    clientPage.geometry("680x470")
    clientPage.iconbitmap("academy.ico")
    clientPage.resizable(False, False)
    clientPage.attributes("-alpha", 0.97)

    def shopPage():
        shopPg = customtkinter.CTk()
        shopPg.title("Online Kurs Sistemi - Müşteri")
        shopPg.geometry("680x370")
        shopPg.iconbitmap("academy.ico")
        shopPg.resizable(False, False)
        shopPg.attributes("-alpha", 0.97)

        def addCashPage():
            addcashpg = customtkinter.CTkToplevel()
            addcashpg.title("Online Kurs Sistemi - Müşteri")
            addcashpg.geometry("680x270")
            addcashpg.iconbitmap("academy.ico")
            addcashpg.resizable(False, False)
            addcashpg.attributes("-alpha", 0.97)

            addCashFrame = customtkinter.CTkFrame(addcashpg, width=660, corner_radius=0)
            addCashFrame.place(relx=0.5, rely=0.5, anchor=CENTER)

            cashLabel = customtkinter.CTkLabel(addCashFrame, text="Eklemek İstediğiniz Miktarı Giriniz :", width=620,
                                                 font=customtkinter.CTkFont(size=12), anchor="w")
            cashLabel.grid(row=0, column=0, padx=20, pady=(20, 5))

            cashEntry = customtkinter.CTkEntry(addCashFrame)
            cashEntry.grid(row=1, column=0, columnspan=3, padx=20, pady=(5, 10), sticky="nsew")

            def addProgress(amount):
                addcashpg.destroy()
                addCash(amount)

            addCashButton = customtkinter.CTkButton(addCashFrame, fg_color="green",
                                                 command=lambda: addProgress(cashEntry.get()))
            addCashButton.configure(text="Ekle")
            addCashButton.grid(row=4, column=0, padx=10, pady=(5, 10))

            addcashpg.mainloop()

        def addCash(amount):
            cnx = connectDb()
            crs = cnx.cursor(buffered=True)
            crs.execute("""SELECT users.cash FROM users WHERE users.email = '{}'""".format(usrMail))
            currentCash = crs.fetchone()[0]
            try:
                amount = int(amount)
                newCash = int(currentCash) + amount
                crs.execute("""UPDATE users SET cash = {0} WHERE users.email = '{1}'""".format(newCash, usrMail))
                cnx.commit()
                messagePopUp("İşlem Başarılı", "Bakiye ekleme işlemi başarıyla tamamlandı.", "info")
            except:
                messagePopUp("İşlem Başarısız", "Bakiye ekleme işlemi başarısız.\nLütfen geçerli bir miktar giriniz.", "cross")

        def buyCourse(courseId):
            cnx = connectDb()
            crs = cnx.cursor(buffered=True)
            crs.execute("""SELECT user_id, cash FROM users WHERE users.email = '{}'""".format(usrMail))
            usrRslt = crs.fetchone()
            usrId = usrRslt[0]
            usrCash = usrRslt[1]
            crs.execute("""SELECT name,price FROM courses WHERE courses.course_id = {}""".format(courseId))
            courseRslt = crs.fetchone()
            courseName = courseRslt[0]
            coursePrice = courseRslt[1]
            if usrCash >= coursePrice:
                newCash = usrCash - coursePrice
                crs.execute("""INSERT INTO user_courses(user_id, course_id) VALUES({0}, {1})""".format(usrId, courseId))
                cnx.commit()
                crs.execute("""UPDATE users SET cash = {1} WHERE user_id = {0}""".format(usrId, newCash))
                cnx.commit()
                messagePopUp("İşlem Başarılı", "{} isimli kurs başarıyla satın alındı.".format(courseName), "info")
            else:
                messagePopUp("İşlem Başarısız", "Bakiyeniz yetersiz!", "cross")

        cnx = connectDb()
        crs = cnx.cursor(buffered=True)
        crs.execute("""SELECT cash FROM users WHERE users.email = '{}'""".format(usrMail))
        usrCash = crs.fetchone()[0]
        cashLabel = customtkinter.CTkLabel(shopPg, text="Bakiyeniz : {}".format(usrCash), width=470,
                                               font=customtkinter.CTkFont(size=14), anchor="w")
        cashLabel.grid(row=2, column=0, padx=20, pady=(20, 10))

        addCashBtn = customtkinter.CTkButton(shopPg)
        addCashBtn.configure(text="Bakiye Ekle", command=addCashPage)
        addCashBtn.grid(row=2, column=1, padx=10, pady=10)

        shopFrame = customtkinter.CTkFrame(shopPg, width=500, height=400, corner_radius=0,
                                               fg_color="transparent")
        shopFrame.grid(row=3, column=0, sticky="nsew", columnspan=2)

        shopCanvas = Canvas(shopFrame, bg="gray10", highlightthickness=0)
        shopCanvas.pack(side=LEFT, fill=BOTH, expand=1)

        shopScrollbar = customtkinter.CTkScrollbar(shopCanvas, command=shopCanvas.yview)
        shopScrollbar.pack(side=RIGHT, fill=Y)

        shopCanvas.configure(yscrollcommand=shopScrollbar.set)
        shopCanvas.bind("<Configure>", lambda e: shopCanvas.configure(scrollregion=shopCanvas.bbox("all")))

        shopSecondFrame = customtkinter.CTkFrame(shopCanvas, corner_radius=0, fg_color="transparent")

        shopCanvas.create_window((0, 0), window=shopSecondFrame, anchor="nw")

        courseItems = []
        userCourses = []
        cnx = connectDb()
        crs = cnx.cursor(buffered=True)
        crs.execute("""SELECT courses.course_id, courses.name, courses.description, courses.price, CONCAT(users.name, " ", users.surname), categories.name AS category
                                FROM users INNER JOIN user_courses ON users.user_id = user_courses.user_id
                                INNER JOIN courses ON user_courses.course_id = courses.course_id
                                INNER JOIN course_categories ON course_categories.course_id = courses.course_id
                                INNER JOIN categories ON course_categories.category_id = categories.category_id""")
        items = crs.fetchall()
        for item in items:
            courseItems.append(item)
        crs.execute("""SELECT courses.course_id, courses.name, courses.description, courses.price, CONCAT(users.name, " ", users.surname), categories.name AS category
                                FROM users INNER JOIN user_courses ON users.user_id = user_courses.user_id
                                INNER JOIN courses ON user_courses.course_id = courses.course_id
                                INNER JOIN course_categories ON course_categories.course_id = courses.course_id
                                INNER JOIN categories ON course_categories.category_id = categories.category_id
                                WHERE users.email = '{0}'""".format(usrMail))
        usrItems = crs.fetchall()
        for usrItem in usrItems:
            userCourses.append(usrItem)


        # kursları listele
        def listCourses(courseData, usrCourses):
            count = 0
            for course in courseData:
                courseFrame = customtkinter.CTkFrame(shopSecondFrame, width=430, height=300)
                if count == 0:
                    courseFrame.grid(row=(count * 3) + 1, column=0, padx=10, pady=(10, 5))
                elif 0 < count < (len(courseData) - 1):
                    courseFrame.grid(row=(count * 3) + 1, column=0, padx=10, pady=(5, 5))
                else:
                    courseFrame.grid(row=(count * 3) + 1, column=0, padx=10, pady=(5, 10))
                courseName = customtkinter.CTkLabel(courseFrame, text=course[1], width=425,
                                                    font=customtkinter.CTkFont(size=16, weight="bold"), anchor="w")
                courseName.grid(row=(count * 3), columnspan=2, padx=20, pady=(10, 5))

                courseDescription = customtkinter.CTkLabel(courseFrame, width=425, text=course[2],
                                                           font=customtkinter.CTkFont(size=12), anchor="w")
                courseDescription.grid(row=(count * 3) + 1, columnspan=2, padx=20, pady=(5, 5))

                courseInstructor = customtkinter.CTkLabel(courseFrame, width=425,
                                                          text="Instructor: {}".format(course[4]),
                                                          font=customtkinter.CTkFont(size=12), anchor="w")
                courseInstructor.grid(row=(count * 3) + 2, columnspan=2, padx=20, pady=(5, 10))

                if course in usrCourses:
                    infoLabel = customtkinter.CTkLabel(courseFrame, text=("Satın alındı"),
                                                       font=customtkinter.CTkFont(size=14, weight="bold"))
                    infoLabel.grid(row=(count * 3)+1, column=3, padx=20, pady=(10, 5))
                else:
                    priceLabel = customtkinter.CTkLabel(courseFrame, text=("{} TL".format(course[3])),
                                                        font=customtkinter.CTkFont(size=16, weight="bold"))
                    priceLabel.grid(row=(count * 3), column=3, padx=20, pady=(10, 5))

                    buyButton = customtkinter.CTkButton(courseFrame, fg_color="green", command=lambda x=course[0]: buyCourse(x))
                    buyButton.configure(text="Satın Al")
                    buyButton.grid(row=(count * 3) + 1, column=3, padx=10, pady=(5, 5))

                count += 1

        listCourses(courseItems, usrItems)

        shopPg.mainloop()

    def profilePage():
        profilePg = customtkinter.CTkToplevel()
        profilePg.title("Online Kurs Sistemi - Müşteri")
        profilePg.geometry("680x480")
        profilePg.iconbitmap("academy.ico")
        profilePg.resizable(False, True)
        profilePg.attributes("-alpha", 0.97)

        def editProfile():
            cnx = connectDb()
            crs = cnx.cursor(buffered=True)
            crs.execute("""UPDATE users SET name = '{1}', surname = '{2}', phone = '{3}'
                                                                            WHERE users.user_id = {0};""".format(
                selectedUsr[0],
                usrNameEntry.get(),
                usrSurnameEntry.get(),
                usrPhoneEntry.get()))
            cnx.commit()
            messagePopUp("İşlem Başarılı", "Kullanıcı başarıyla güncellendi.", "info")


        profileFrame = customtkinter.CTkFrame(profilePg)
        profileFrame.place(relx=0.5, rely=0.5, anchor=CENTER)

        cnx = connectDb()
        crs = cnx.cursor(buffered=True)

        crs.execute("""SELECT users.user_id, users.name, users.surname, users.phone FROM users 
                        INNER JOIN user_roles ON users.user_id = user_roles.user_id
                        INNER JOIN roles ON roles.role_id = user_roles.role_id
                        WHERE users.email = '{0}'""".format(usrMail))
        selectedUsr = crs.fetchone()

        usrIdLabel = customtkinter.CTkLabel(profileFrame, text="Kullanıcı ID :", width=620,
                                            font=customtkinter.CTkFont(size=12), anchor="w")
        usrIdLabel.grid(row=0, column=0, padx=20, pady=(20, 5))

        usrIdEntry = customtkinter.CTkEntry(profileFrame)
        usrIdEntry.grid(row=1, column=0, columnspan=3, padx=20, pady=(5, 10), sticky="nsew")
        usrIdEntry.insert(0, selectedUsr[0])
        usrIdEntry.configure(state="disabled")

        usrNameLabel = customtkinter.CTkLabel(profileFrame, text="İsim :", width=620,
                                              font=customtkinter.CTkFont(size=12), anchor="w")
        usrNameLabel.grid(row=2, column=0, padx=20, pady=(10, 5))

        usrNameEntry = customtkinter.CTkEntry(profileFrame, width=300, height=30, border_width=1,
                                              text_color="silver")
        usrNameEntry.insert("0", selectedUsr[1])
        usrNameEntry.grid(row=3, column=0, padx=20, pady=(5, 10), sticky="nsew")

        usrSurameLabel = customtkinter.CTkLabel(profileFrame, text="Soyisim :", width=620,
                                                font=customtkinter.CTkFont(size=12), anchor="w")
        usrSurameLabel.grid(row=4, column=0, padx=20, pady=(10, 5))
        usrSurnameEntry = customtkinter.CTkEntry(profileFrame, placeholder_text="Soyisim", width=300, height=30,
                                                 border_width=1,
                                                 text_color="silver")
        usrSurnameEntry.insert("0", selectedUsr[2])
        usrSurnameEntry.grid(row=5, column=0, padx=20, pady=(5, 10), sticky="nsew")

        usrPhoneLabel = customtkinter.CTkLabel(profileFrame, text="Telefon Numarası :", width=620,
                                               font=customtkinter.CTkFont(size=12), anchor="w")
        usrPhoneLabel.grid(row=6, column=0, padx=20, pady=(10, 5))
        usrPhoneEntry = customtkinter.CTkEntry(profileFrame, placeholder_text="Telefon Numarası", width=300, height=30,
                                               border_width=1, text_color="silver")
        usrPhoneEntry.insert("0", selectedUsr[3])
        usrPhoneEntry.grid(row=7, column=0, padx=20, pady=(5, 10), sticky="nsew")

        saveButton = customtkinter.CTkButton(profileFrame,
                                             command=editProfile)
        saveButton.configure(text="Kaydet")
        saveButton.grid(row=12, column=0, padx=20, pady=(10, 20), sticky="n")

        profilePg.mainloop()

    def exit():
        global usrMail
        usrMail = ""
        clientPage.destroy()

    clientFrame = customtkinter.CTkFrame(clientPage, width=500, corner_radius=0)
    clientFrame.grid(row=0, column=0, rowspan=2, sticky="nsew")
    clientFrame.grid_rowconfigure(4, weight=1)

    logo_label = customtkinter.CTkLabel(clientFrame, text="Müşteri Paneli",
                                        font=customtkinter.CTkFont(size=20, weight="bold"))
    logo_label.grid(row=0, column=0, columnspan=1, padx=(20, 40), pady=(20, 20))

    navbarButton1 = customtkinter.CTkButton(clientFrame, command=shopPage)
    navbarButton1.configure(text="Market")
    navbarButton1.grid(row=0, column=2, padx=10, pady=10)
    navbarButton2 = customtkinter.CTkButton(clientFrame, command=profilePage)
    navbarButton2.configure(text="Profil")
    navbarButton2.grid(row=0, column=3, padx=10, pady=10)
    navbarButton3 = customtkinter.CTkButton(clientFrame, fg_color="#782c2c", command=exit)
    navbarButton3.configure(text="Çıkış")
    navbarButton3.grid(row=0, column=4, padx=10, pady=30)

    myCourseLabel = customtkinter.CTkLabel(clientPage, text="Sahip Olunan Kurslar :", width=620,
                                           font=customtkinter.CTkFont(size=12), anchor="w")
    myCourseLabel.grid(row=2, column=0, padx=20, pady=(10, 10))

    #scroll
    myCourseFrame = customtkinter.CTkFrame(clientPage, width=500, height=400, corner_radius=0, fg_color="transparent")
    myCourseFrame.grid(row=3, column=0, sticky="nsew")

    canvas = Canvas(myCourseFrame, bg="gray10", highlightthickness=0)
    canvas.pack(side=LEFT, fill=BOTH, expand=1)

    ctk_textbox_scrollbar = customtkinter.CTkScrollbar(canvas, command=canvas.yview)
    ctk_textbox_scrollbar.pack(side=RIGHT, fill=Y)

    canvas.configure(yscrollcommand=ctk_textbox_scrollbar.set)
    canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    secondFrame = customtkinter.CTkFrame(canvas, corner_radius=0, fg_color="transparent")

    canvas.create_window((0,0), window=secondFrame, anchor="nw")

    # kullanıcının kurslarını getir
    def getUserCourses():
        courseItems = []
        cnx = connectDb()
        crs = cnx.cursor(buffered=True)
        crs.execute("""SELECT courses.course_id, courses.name, courses.description, courses.price, CONCAT(users.name, " ", users.surname), categories.name AS category
                        FROM users INNER JOIN user_courses ON users.user_id = user_courses.user_id
                        INNER JOIN courses ON user_courses.course_id = courses.course_id
                        INNER JOIN course_categories ON course_categories.course_id = courses.course_id
                        INNER JOIN categories ON course_categories.category_id = categories.category_id
                        WHERE users.email = '{0}'""".format(usrMail))
        items = crs.fetchall()
        for item in items:
            courseItems.append(item)
        return courseItems

    # kursları listele
    def listCourses(courseData):
        count = 0
        for course in courseData:
            courseFrame = customtkinter.CTkFrame(secondFrame, width=430, height=300)
            if count == 0:
                courseFrame.grid(row=(count * 3) + 1, column=0, padx=10, pady=(10, 5))
            elif 0 < count < (len(courseData) - 1):
                courseFrame.grid(row=(count * 3) + 1, column=0, padx=10, pady=(5, 5))
            else:
                courseFrame.grid(row=(count * 3) + 1, column=0, padx=10, pady=(5, 10))
            courseName = customtkinter.CTkLabel(courseFrame, text=course[1], width=425,
                                                font=customtkinter.CTkFont(size=16, weight="bold"), anchor="w")
            courseName.grid(row=(count * 3), columnspan=2, padx=20, pady=(10, 5))

            courseDescription = customtkinter.CTkLabel(courseFrame, width=425, text=course[2],
                                                       font=customtkinter.CTkFont(size=12), anchor="w")
            courseDescription.grid(row=(count * 3) + 1, columnspan=2, padx=20, pady=(5, 5))

            courseInstructor = customtkinter.CTkLabel(courseFrame, width=425,
                                                      text="Instructor: {}".format(course[4]),
                                                      font=customtkinter.CTkFont(size=12), anchor="w")
            courseInstructor.grid(row=(count * 3) + 2, columnspan=2, padx=20, pady=(5, 10))

            detailsButton = customtkinter.CTkButton(courseFrame)
            detailsButton.configure(text="Detay")
            detailsButton.focus()
            detailsButton.grid(row=(count * 3) + 1, column=3, padx=10, pady=(5, 5))
            count += 1

    courses = getUserCourses()
    listCourses(courses)

    clientPage.mainloop()


def validateLogin(userName, pword):
    cnx = connectDb()
    crs = cnx.cursor(buffered=True)
    hashedPassword = hashlib.md5(pword.encode('utf8')).hexdigest()
    query = """SELECT * FROM users WHERE email = '{}' AND pword = '{}'""".format(userName, hashedPassword)
    crs.execute(query)
    result = crs.fetchone()

    if result is None:
        messagePopUp("Hatalı Giriş", "Kullanıcı adı veya şifre hatalı !", "cross")
    else:
        query = """SELECT roles.role_id FROM users,roles,user_roles
        WHERE users.user_id = user_roles.user_id
        AND user_roles.role_id = roles.role_id
        AND users.user_id = {0}""".format(result[0])
        crs.execute(query)
        result = crs.fetchone()
        global usrMail
        usrMail = userName
        if result[0] == 1:
            # owner
            sys.destroy()
            openAdminPage()
        elif result[0] == 2:
            # admin
            sys.destroy()
            openAdminPage()
        elif result[0] == 3:
            # egitmen
            sys.destroy()
            openInstructorPage()
        else:
            sys.destroy()
            # musteri
            openClientPage()

    cnx.close()


def registerPage():
    rgs = customtkinter.CTk()
    rgs.title("Online Kurs Sistemi")
    rgs.geometry("570x520")
    rgs.iconbitmap("academy.ico")
    rgs.resizable(False, False)
    rgs.attributes("-alpha", 0.97)
    rgsFrame = customtkinter.CTkFrame(rgs)
    rgsFrame.place(relx=0.5, rely=0.5, anchor=CENTER)
    title = customtkinter.CTkLabel(rgsFrame, width=300, height=30, text_color=("white", "gray75"),
                                   font=customtkinter.CTkFont(size=20, weight="bold"))
    title.configure(text="ONLİNE KURS SİSTEMİ - KAYIT")
    title.grid(row=0, column=1, padx=10, pady=20, sticky="n")

    def validateRegister(name, surname, phone, email, pword):
        cnx = connectDb()
        crs = cnx.cursor(buffered=True)
        user_id = random.randint(10, 99999)
        crs.execute(
            """SELECT user_id FROM users
            WHERE users.email = '{0}'""".format(email))
        checkEmail = crs.fetchone()

        crs.execute(
            """SELECT user_id FROM users
            WHERE users.user_id = {0}""".format(user_id))
        checkUserId = crs.fetchone()

        if checkEmail is not None or checkUserId is not None:
            messagePopUp("İşlem Başarısız", "Sistemde aynı e-posta adresiyle farklı bir kullanıcı zaten bulunuyor.",
                         "cross")
        else:
            hashedPassword = hashlib.md5(pword.encode('utf8')).hexdigest()
            query = """INSERT INTO users(user_id, name, surname, phone, email, pword) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')""".format(
                user_id, name, surname, phone, email, hashedPassword)
            crs.execute(query)
            cnx.commit()
            crs.execute("""INSERT INTO user_roles(role_id, user_id) VALUES({0}, {1})""".format(4,
                                                                                               user_id))  # 4 defines the "user" role
            cnx.commit()
            rgs.destroy()
            messagePopUp("İşlem Başarılı", "Kayıt işlemi başarıyla tamamlandı")

    name = StringVar()
    nameEntry = customtkinter.CTkEntry(rgsFrame, width=300, height=30, border_width=1,
                                       textvariable=name,
                                       text_color="silver")

    nameEntry.insert("0", "İsim")
    nameEntry.grid(row=1, column=1, padx=10, pady=10, sticky="n")

    surname = StringVar()
    surnameEntry = customtkinter.CTkEntry(rgsFrame, placeholder_text="Soyisim", width=300, height=30, border_width=1,
                                          textvariable=surname,
                                          text_color="silver")
    surnameEntry.insert("0", "Soyisim")
    surnameEntry.grid(row=2, column=1, padx=10, pady=10, sticky="n")

    phone = StringVar()
    phoneEntry = customtkinter.CTkEntry(rgsFrame, placeholder_text="Telefon Numarası", width=300, height=30,
                                        border_width=1, textvariable=phone, text_color="silver")
    phoneEntry.insert("0", "Telefon Numarası")
    phoneEntry.grid(row=3, column=1, padx=10, pady=10, sticky="n")

    username = StringVar()
    usernameEntry = customtkinter.CTkEntry(rgsFrame, placeholder_text="E-posta Adresi", width=300, height=30,
                                           border_width=1, textvariable=username, text_color="silver")
    usernameEntry.insert("0", "E-posta Adresi")
    usernameEntry.grid(row=4, column=1, padx=10, pady=10, sticky="n")

    p_word = StringVar()
    pwordEntry = customtkinter.CTkEntry(rgsFrame, placeholder_text="Şifre", width=300, height=30, border_width=1,
                                        textvariable=p_word,
                                        text_color="silver", show="*")
    pwordEntry.insert("0", "Şifre")
    pwordEntry.grid(row=5, column=1, padx=10, pady=10, sticky="n")

    registerButton = customtkinter.CTkButton(rgsFrame,
                                             command=lambda: validateRegister(nameEntry.get(), surnameEntry.get(),
                                                                              phoneEntry.get(), usernameEntry.get(),
                                                                              pwordEntry.get()))
    registerButton.configure(text="Kaydol")
    registerButton.grid(row=6, column=1, padx=10, pady=10, sticky="n")

    rgs.mainloop()


def loginPage(sys):
    tkFrame = customtkinter.CTkFrame(sys)
    tkFrame.place(relx=0.5, rely=0.5, anchor=CENTER)
    title = customtkinter.CTkLabel(tkFrame, width=300, height=30, text_color=("white", "gray75"),
                                   font=customtkinter.CTkFont(size=20, weight="bold"))
    title.configure(text="ONLİNE KURS SİSTEMİ - GİRİŞ")
    title.grid(row=0, column=1, padx=10, pady=20, sticky="n")

    username = StringVar()
    usernameEntry = customtkinter.CTkEntry(tkFrame, placeholder_text="E-posta Adresi", width=300, height=30,
                                           border_width=1, textvariable=username,
                                           text_color="silver")
    usernameEntry.insert("0", "E-posta Adresi")
    usernameEntry.grid(row=1, column=1, padx=10, pady=10, sticky="n")

    p_word = StringVar()
    pwordEntry = customtkinter.CTkEntry(tkFrame, placeholder_text="Sifre", width=300, height=30, border_width=1,
                                        textvariable=p_word,
                                        text_color="silver", show="*")
    pwordEntry.insert("0", "Şifre")
    pwordEntry.grid(row=2, column=1, padx=10, pady=10, sticky="n")

    loginButton = customtkinter.CTkButton(tkFrame, command=lambda: validateLogin(username.get(), p_word.get()))
    loginButton.configure(text="Login")
    loginButton.grid(row=3, column=1, padx=10, pady=10, sticky="n")

    registerButton = customtkinter.CTkButton(tkFrame, fg_color=("black"),
                                             command=registerPage)
    registerButton.configure(text="Register")
    registerButton.grid(row=4, column=1, padx=10, pady=10, sticky="n")


loginPage(sys)

sys.mainloop()
