import subprocess, ipaddress, pprint, time
import PySimpleGUI as sg
import pandas as pd

def scan_df(ips):
    try:
        if ips:
            ipList = ipaddress.ip_network(str(ips))
            ip = []
            stat = []
            for i in ipList:
                check = subprocess.call(['ping', '-n', '1', str(i)]) == 0
                ip.append(str(i))
                stat.append('Success' if check else 'Failed')
            df = pd.DataFrame({
                'Ip':ip,
                'State':stat
            })
            return df
    except:
        pass   


def scan(ips):
    try:
        if ips:
            ipList = ipaddress.ip_network(str(ips))
            var = []
            ip = []
            stat = []
            df = pd.DataFrame()
            for i in ipList:
                check = subprocess.call(['ping', '-n', '1', str(i)]) == 0
                ip.append(str(i))
                stat.append('Success' if check else 'Failed')
                var.append(f'{str(i)}: Success'.lstrip() if check else f'{str(i)}: Failed')
            df.DataFrame({
                'Ip':ip,
                'State':stat
            })
            return str(var).replace('[', '').replace('\'', '').replace(']', '\n').replace(',', '\n')
    except:
        return 'Error'
    
sg.theme('Reddit')
data = [['' for row in range(2)] for col in range(25)]
layout = [  [sg.Text("IP Network Address: "), sg.Text("Output: ")],
            [sg.Multiline(key='-input-', size=(20,5)), 
            sg.Table(
                values=data,
                headings=[],
                enable_events=True,
                display_row_numbers=True,
                key='-output-', 
                size=(40, 40),
                )],
            [sg.Button('Scan', bind_return_key=True), sg.Button('Close')],
        ]
window = sg.Window('Network Scanner', grab_anywhere=False).layout(layout)
while True:
    event, values = window.read()
    if event == 'Close' or event == sg.WIN_CLOSED:
        break
    elif event == 'Scan':
        ips = ''.join(str(values['-input-'])).split('\n')[:-1]
        print(ips)
        #window['-output-'].update(value=('\n'.join([scan(str(i)) for i in ips])))
        vals = pd.concat([scan_df(str(i)) for i in ips])
        print(vals)
        values['-output-'].append(pd.DataFrame(vals).values.tolist())
        window['-output-'].update(pd.DataFrame(vals).values.tolist())
window.close()

