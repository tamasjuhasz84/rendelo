import PySimpleGUI as sg
import datetime
import sqlite3

conn = sqlite3.Connection('rendelo.db')
c = conn.cursor()

c.execute('''
          CREATE TABLE IF NOT EXISTS tb(
          dátum TEXT,
          óra TEXT,
          perc TEXT,
          név TEXT,
          telefon TEXT,
          orvosok TEXT)
          ''')
conn.commit()

sg.theme('lightblue')

dt = datetime.datetime.now()
év  = dt.year
hó  = dt.month
nap = dt.day

dátum = f'{év}-{hó}-{nap}'

with open ('orvosok.txt', 'r', encoding = 'UTF-8')  as f:
    orvosok = [sor.strip() for sor in f]

col1=[
     [sg.Text('')],
     [sg.Text('dátum', size=(12, 1)),   sg.Input(key='dátum')],
     [sg.Text('óra', size=(12, 1)),     sg.Input(key='óra')],
     [sg.Text('perc', size=(12, 1)),    sg.Input(key='perc')],
     [sg.Text('név', size=(12, 1)),     sg.Input(key='név')],
     [sg.Text('telefon', size=(12, 1)), sg.Input(key='telefon')],
     [sg.Button('Ment'),  sg.Button('Keres')]
     ]

col2=[
     [sg.Text('orvosok')],
     [sg.Listbox(orvosok, size=(12, 14), key='orvosok')]
     ]

előjegyzések = []

col3=[
     [sg.Text('előjegyzések')],
     [sg.Listbox(előjegyzések, size=(30, 14), key='előjegyzések')],
     [sg.Button('Töröl')]
     ]

layout = [[sg.Column(col1), sg.Column(col2), sg.Column(col3)]]
window = sg.Window('rendelő', layout, font='Helvetica 14', default_element_size=(12, 1), auto_size_buttons=False,)
window.read(100)
window['dátum'].update(dátum)

while True:
    event, values = window.read()
    print(event, values)

    dátum   = values['dátum']
    óra     = values['óra']
    perc    = values['perc']
    név     = values['név']
    telefon = values['telefon']
    orvos   = values['orvosok'][0]
        
    if event in (None, 'Exit'):
        break
    
    if event in ("Ment"):
        if (dátum and óra and perc and név and telefon and orvos):
            print('remek')
            c.execute ('INSERT INTO tb VALUES (?,?,?,?,?,?)', (dátum, óra, perc, név, telefon, orvos))
            conn.commit()
        else:
            print('nem remek')
    
    if event in ("Keres"):
        if dátum and orvos and not (óra or perc or név or telefon):
            c.execute('SELECT dátum, név, telefon FROM tb WHERE dátum LIKE ? AND orvosok LIKE ?', (dátum, orvos))
            x = c.fetchall()
            előjegyzések = x
            window['előjegyzések'].update(előjegyzések)
            
    
    if event in ("Töröl"):
        print(values)
        dátum   = values['előjegyzések'][0][0]
        név     = values['előjegyzések'][0][1]
        telefon = values['előjegyzések'][0][2]
        
        c.execute('DELETE FROM tb WHERE dátum LIKE ? AND név LIKE ? AND telefon LIKE ?', (dátum, név, telefon))
        conn.commit()
        c.execute('SELECT dátum, név, telefon FROM tb WHERE dátum LIKE ? AND orvosok LIKE ?', (dátum, orvos))
        x = c.fetchall()
        előjegyzések = x
        window['előjegyzések'].update(előjegyzések)