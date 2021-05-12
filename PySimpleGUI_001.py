import subprocess, ipaddress
import PySimpleGUI as sg
import pandas as pd

def scan_df(ips):
    try:
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        if ips:
            ipList = ipaddress.ip_network(str(ips))
            ip = []
            stat = []
            for i in ipList:
                check = subprocess.call(['ping', '-n', '1', '-w', '500', str(i)], startupinfo=si) == 0
                ip.append(str(i))
                stat.append('Success' if check else 'Failed')
            df = pd.DataFrame({
                'Ip_Address':ip,
                'Status':stat
            })
            return df
    except:
        pass

    
sg.theme('Reddit')
layout = [  [sg.Text("IP Network Address: "), sg.Text("Output: ")],
            [sg.Multiline(key='-input-', size=(20,5)), 
            sg.Table(
                values=list(),
                headings=list(),
                enable_events=True,
                display_row_numbers=False,
                key='-output-',
                )],
            [sg.Button('Scan', bind_return_key=True), sg.Button('Close')],
        ]
window = sg.Window('Network Scanner', grab_anywhere=False).layout(layout)
while True:
    event, values = window.read()
    print(event)
    if event == 'Close' or event == sg.WIN_CLOSED:
        break
    elif event == 'Scan':
        ips = ''.join(str(values['-input-'])).split('\n')[:-1]
        vals = pd.concat([scan_df(str(i)) for i in ips])
        if ips:
            layout_two = [
                [sg.Button('Export')],
                [sg.Text("IP Network Address: "), sg.Text("          Output: ")],
                [sg.Multiline(values['-input-'], key='-input-', size=(20,5)), 
                sg.Table(
                    values=vals.values.tolist(),
                    headings=list(vals.keys()),
                    enable_events=True,
                    display_row_numbers=False,
                    key='-output-',
                    )],
                [sg.Button('Scan', bind_return_key=True), sg.Button('Close', pad=(0, 40))]
                ]
            window.close()
            window = sg.Window('Network Scanner', grab_anywhere=False).layout(layout_two)
    elif event == 'Export':
        while True:
            layout_save = [
                [sg.Input('Save Location . . .', key='loc', size=(20, 5)), sg.FileSaveAs('Browse', target='loc', file_types=(('XLSX', '.xlsx'),))],
                [sg.Button('Save'), sg.Button('Close')]
            ]
            window2 = sg.Window('Save Location: ', grab_anywhere=False).layout(layout_save)
            event2, values2 = window2.read()
            if event2 == 'Save':
                if '.xlsx' not in values2['loc']:
                    fname = str(values2['loc']) + '.xlsx'
                else:
                    fname = str(values2['loc'])
                try:
                    vals.to_excel(fname, index=False)
                    window2.close()
                    break
                except:
                    sg.popup('Failed to save file -- Perhaps it is overwriting an open file?')
            elif event2 == 'Close' or event2 == sg.WIN_CLOSED:
                window2.close()
                break
window.close()