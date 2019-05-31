#!/usr/bin/env python
import sys
if sys.version_info[0] >= 3:
    import PySimpleGUI as sg
else:
    import PySimpleGUI27 as sg
import csv
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource
import pandas as pd
import pandas


def TableSimulation():
    """
    Display data in a table format
    """
    sg.SetOptions(element_padding=(0,0))

    menu_def = [['File', ['Open', 'Save', 'Exit']],
                ['Generate', ['Graph', ['line', 'bar',], 'Undo'],],
                ['Help', 'About...'],]

    columm_layout = [[]]

    MAX_ROWS = 800
    MAX_COL = 10
    for i in range(MAX_ROWS):
        inputs = [sg.T('{}'.format(i), size=(4,1), justification='right')] + [sg.In(size=(10, 1), pad=(1, 1), justification='right', key=(i,j), do_not_clear=True) for j in range(MAX_COL)]
        columm_layout.append(inputs)

    Preview = [ [sg.Menu(menu_def)],
               [sg.Column(columm_layout, size=(300,100), scrollable=True)] ]

    Setting = [[sg.Slider(range=(1,1000), default_value=500, size=(10,10), orientation='horizontal', key = 'height',font=('Helvetica', 12)),
                    sg.Text('  Name:  ', size=(8,1)), sg.InputText(key='graphtitle', size=(8,1))],
               [sg.Text('Enter graph Height')],
               [sg.Slider(range=(1,1000), default_value=500, size=(10,10), orientation='horizontal', key = 'width', font=('Helvetica', 12)),
                    sg.Text('       '),sg.InputCombo(['Red', 'Green', 'Blue', 'Yellow', 'Orange'])],
               [sg.Text('Enter graph Width')]]
              

    layout = [[sg.Text('use open to load the csv')], 
              [sg.Frame('Preview', Preview, title_color='green', font = 'Any 12')],
              [sg.Frame('Graph Settings', Setting, title_color='blue', font = 'Any 12')]]

    window = sg.Window('Table', return_keyboard_events=True).Layout(layout)

    while True:
        event, values = window.Read()
        # --- Process buttons --- #
        if event is None or event == 'Exit':
            break
        elif event == 'About...':
            sg.Popup('A simple graphing program to plot various headers and points from a CSV')
        elif event == 'Open':
            filename = sg.PopupGetFile('filename to open', no_window=True, file_types=(("CSV Files","*.csv"),))
            # --- populate table with file contents --- #
            if filename is not None:
                with open(filename, "r") as infile:
                    reader = csv.reader(infile)
                    try:
                        data = list(reader)
                          # read everything else into a list of rows
                    except:
                        sg.PopupError('Error reading file')
                        continue
                # clear the table
                [window.FindElement((i,j)).Update('') for j in range(MAX_COL) for i in range(MAX_ROWS)]

                for i, row in enumerate(data):
                    for j, item in enumerate(row):
                        location = (i,j)
                        try:            # try the best we can at reading and filling the table
                            target_element = window.FindElement(location)
                            new_value = item
                            if target_element is not None and new_value != '':
                                target_element.Update(new_value)
                        except:
                            pass

        elif event == 'Save':
            filename = sg.PopupGetFile('filename to open', save_as = True,no_window=True, file_types=(("CSV Files","*.csv"),))
            for i, row in enumerate(data):
                for j, item in enumerate(row):
                    location = (i,j)
                    try:
                        target_element = window.FindElement(location)
                    except:
                        pass
                    deform = values[target_element]
                    print (deform)

        elif event == 'line':

            #filename = sg.PopupGetFile('filename to open', no_window=True, file_types=(("CSV Files","*.csv"),))
            
            name = values['graphtitle']
            plotwidthfloat= values['width']
            plotheightfloat= values['height']

            plotwidth=int(plotwidthfloat)
            plotheight=int(plotheightfloat)

            weight = pd.read_csv(filename)

            xx=weight["time(hours)"]
            yy1=weight["Electrode"]
            yy2=weight["Ohmic"]
            yy3=weight["tasr"]

            output_file(name+'.html')
            p = figure(title = name, plot_width=plotwidth, plot_height=plotheight)
            p.circle(xx,yy1, legend="Electrode")
            p.line(xx,yy1, legend="Electrode")
            p.line(xx,yy2, legend="Ohmic", line_color='green')
            p.square(xx,yy2, legend="Ohmic", fill_color='green',line_color='green')
            p.line(xx,yy3, legend="Tasr", line_color='red')
            p.diamond(xx,yy3, legend="Tasr", line_color='red', fill_color='red')

            p.legend.location = "top_right"

            show(p)

        
            
            


        # if a valid table location entered, change that location's value
        try:
            location = (int(values['inputrow']), int(values['inputcol']))
            target_element = window.FindElement(location)
            new_value = values['value']
            if target_element is not None and new_value != '':
                target_element.Update(new_value)
        except:
            pass

TableSimulation()