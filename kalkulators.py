import PySimpleGUI as sg 

bw: dict = {'size':(7,2), 'font':('Franklin Gothic Book', 24), 'button_color':("white","#b88bd6")}
bt: dict = {'size':(7,2), 'font':('Franklin Gothic Book', 24), 'button_color':("white","#8558a3")}
bo: dict = {'size':(15,2), 'font':('Franklin Gothic Book', 24), 'button_color':("white","#5d456e"), 'focus':True}

# Kalkulatora uzbūve un vizuālais izskats
layout: list = [
    [sg.Text('Mans kalkulators', size=(50,1), justification='right', background_color="#000000", 
        text_color='white', font=('Franklin Gothic Book', 14, 'bold'))],
    [sg.Text('0.0000', size=(18,1), justification='right', background_color='#e8d5f5', text_color='purple', 
        font=('Digital-7',48), relief='sunken', key="_DISPLAY_")],
    [sg.Button('C',**bt), sg.Button('CE',**bt), sg.Button('%',**bt), sg.Button("/",**bt)],
    [sg.Button('7',**bw), sg.Button('8',**bw), sg.Button('9',**bw), sg.Button("*",**bt)],
    [sg.Button('4',**bw), sg.Button('5',**bw), sg.Button('6',**bw), sg.Button("-",**bt)],
    [sg.Button('1',**bw), sg.Button('2',**bw), sg.Button('3',**bw), sg.Button("+",**bt)],    
    [sg.Button('0',**bw), sg.Button('.',**bw), sg.Button('=',**bo, bind_return_key=True)]
]

window: object = sg.Window('Mans kalkulators', layout=layout, background_color="#000000", size=(580, 660), return_keyboard_events=True)


# Kalkulatora funkcijas
var: dict = {'front':[], 'back':[], 'decimal':False, 'x_val':0.0, 'y_val':0.0, 'result':0.0, 'operator':''}

def format_number() -> float:
    return float(''.join(var['front']).replace(',','') + '.' + ''.join(var['back']))

def update_display(display_value: str):
    try:
        window['_DISPLAY_'].update(value='{:,.4f}'.format(display_value))
    except:
        window['_DISPLAY_'].update(value=display_value)

def number_click(event: str):
    global var
    if var['decimal']:
        var['back'].append(event)
    else:
        var['front'].append(event)
    update_display(format_number())
    
def clear_click():
    global var
    var['front'].clear()
    var['back'].clear()
    var['decimal'] = False 

def operator_click(event: str):
    global var
    var['operator'] = event
    try:
        var['x_val'] = format_number()
    except:
        var['x_val'] = var['result']
    clear_click()

def calculate_click():
    global var
    try:
        var['y_val'] = format_number()
    except ValueError: 
        var['x_val'] = var['result']
    try:
        var['result'] = eval(str(var['x_val']) + var['operator'] + str(var['y_val']))
        update_display(var['result'])
        clear_click()    
    except:
        update_display("Kļūda!")
        clear_click()


while True:
    event, values = window.read()
    print(event)
    if event is None:
        break
    if event in ['0','1','2','3','4','5','6','7','8','9']:
        number_click(event)
    if event in ['Escape:27','C','CE']: 
        clear_click()
        update_display(0.0)
        var['result'] = 0.0
    if event in ['+','-','*','/']:
        operator_click(event)
    if event == '=':
        calculate_click()
    if event == '.':
        var['decimal'] = True
    if event == '%':
        update_display(var['result'] / 100.0)