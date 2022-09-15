import mysql.connector
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import io

window = tk.Tk()
window.title('حفظ معلومات العميل')
window.option_add('*Font', 'Times 15')


def upload_image():
    global filename, img
    f_types = [('Png files', '*.png'), ('Jpg Files', '*.jpg')]
    filename = filedialog.askopenfilename(filetypes=f_types)
    if (filename):
        img = Image.open(filename)
        img = img.resize((500, 500))
        img = ImageTk.PhotoImage(img)
        label = tk.Label(master=frame, image=img, width=500, height=500)
        label.place(x= 30, y=120)


def submit():
    fb = open(filename, 'rb')  # filename from upload_file()
    fb = fb.read()
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="mydatabase"
        )
        mycursor = mydb.cursor()
        sql = "INSERT INTO customers (name, IMAGE) VALUES (%s, %s)"
        val = [(edit.get(), fb)]
        mycursor.executemany(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "record inserted successfuly.")
    except mysql.connector.Error as error:
        print("Failed to insert into customer table {}".format(error))

    finally:
        if mydb.is_connected():
            mycursor.close()
            mydb.close()
            print("MySQL connection is closed")


frame = tk.Frame(master=window, width=550, height=650, bg= 'white')
frame.place(x=20, y=15)
labeln = tk.Label(master=frame, text='اسم العميل')
labeln.place(x=400, y=15)

button = tk.Button(master=frame, text='رفع الصورة', command=upload_image)
button.place(x=10, y=15)

edit = tk.Entry(master=frame, width=20)
edit.place(x=150, y=15)

buttonl = tk.Button(master=frame, text='سجل', command=submit)
buttonl.place(x=200, y=80)

window['bg'] = '#F5C800'
window.geometry("1350x690")
window.iconbitmap('images/glasses.ico')



frame2 = tk.Frame(master=window, width=550, height=650, bg='white')
frame2.place(x=750, y=15)


def get():
    global img
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="mydatabase"
        )
        mycursor = mydb.cursor()
        mycursor.execute("SELECT IMAGE FROM customers WHERE name='%s'" % edit.get())
        myresult = mycursor.fetchone()
        img = Image.open(io.BytesIO(myresult[0]))
        img = img.resize((300, 300))
        img = ImageTk.PhotoImage(img)
        label = tk.Label(master=frame2, image=img, width=600, height=400)
        label.place(x=100, y=100)
    except mysql.connector.Error as error:
        print("Failed to get from customer table {}".format(error))

    finally:
        if mydb.is_connected():
            mycursor.close()
            mydb.close()
            print("MySQL connection is closed")



labeln2 = tk.Label(master=frame2, text='اسم العميل', fg='black')
labeln2.place(x=400, y=15)

edit2 = tk.Entry(master=frame2, width=20)
edit2.place(x= 150, y=15)
buttonl2 = tk.Button(master=frame2, text='بحث', command=get)
buttonl2.place(x= 80, y=15)
window.mainloop()