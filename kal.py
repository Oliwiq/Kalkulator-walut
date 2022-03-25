import os
from urllib.request import urlopen
from xml.etree import ElementTree
from tkinter import *
from tkinter.ttk import *
import requests

def is_internet_available():
    try:
        urlopen('https://www.nbp.pl/kursy/xml/a083z190429.xml', timeout=1)
        return True
    except:
        return False

def data():
    internet = is_internet_available()
    if internet == True:
        URL = "https://www.nbp.pl/kursy/xml/a083z190429.xml"
        response = requests.get(URL)
        with open('waluty.xml', 'wb') as file:
            file.write(response.content)
    else:
        pass

file_name = 'waluty.xml'
full_file = os.path.abspath(file_name)
home = ElementTree.parse(full_file)
name = home.findall('pozycja/nazwa_waluty')
currency = home.findall('pozycja/kurs_sredni')
code = home.findall('pozycja/kod_waluty')
name_list = [i.text for i in name]
currency_list = [i.text.replace(',', '.') for i in currency]
code_list = [i.text for i in code]

window = Tk()


window.title("KALKULATOR WALUT")
window.geometry('500x300')
label1 = Label(window, text="KALKULATOR WALUT", font=("Arial Bold", 20))
label1.grid(column=0, row=0, sticky=W + E)

combo_in = Combobox(window)  # z jakiej waluty zmieniamy
combo_in['values'] = tuple(name_list)
combo_in.grid(column=0, row=2)
label_in = Label(window, text='Wybierz walutę wejściową')
label_in.grid(column=0, row=1)

combo_out = Combobox(window)  # na jaka walute zmieniamu
combo_out['values'] = tuple(name_list)
combo_out.grid(column=0, row=4)
label_in = Label(window, text='Wybierz walutę wyjściową')
label_in.grid(column=0, row=3)

value = Entry(window, width=10)
value.grid(column=0, row=6)
label_value = Label(window, text='Wprowadź kwotę')
label_value.grid(column=0, row=5)


def klikniecie():
    kw = value.get()
    label_value.configure(text='Podano kwotę  ' + kw)
    w = (float(value) * float(currency_list[combo_in.current()])) / float(currency_list[combo_out.current()])
    text = '{} {} to {} {}'.format(value, code_list[combo_in.current()], round(w, 2), code_list[combo_out.current()])
    result = Label(window, text=text, font=("Arial Bold", 15))
    result.grid(column=1, row=3)


button = Button(window, text="Rozpocznij obliczenia", command=klikniecie)
button.grid(column=0, row=8)

exit_button = Button(window, text='Wyjscie', command=window.destroy)
exit_button.grid(column=1, row=8)

window.mainloop()
