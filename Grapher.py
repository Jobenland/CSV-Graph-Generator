#!/usr/bin/env python
'''
This is a program to be used to easily make customizable graphs from CVS files with
all sorts of customizable functions to be able to graph your data

'''

__author__ = "Jonathan Obenland"
__copyright__ = "Copyright 2019, MEII"
__credits__ = ["Jonathan Obenland", "Mikethewatchguy"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Jonathan Obenland"
__email__ = "jobenland1@gmail.com"
__status__ = "Production"


import csv
import pandas as pd
import pandas
import sys
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource
if sys.version_info[0] >= 3:
    import PySimpleGUI as sg
else:
    import PySimpleGUI27 as sg

#Main method that runs all features of the program 
def Main():
    
    #adds the options panel to the top
    sg.SetOptions(element_padding=(0,0))

    #adds the options to the bar at top
    menu_def = [['File', ['Open', 'Save', 'Exit']],
                ['Generate', ['Graph', ['line', 'bar',], 'Undo'],],
                ['Help', 'About...'],]

    columm_layout = [[]]

    #creates the preview portion to look at the opened csv file
    MAX_ROWS = 800
    MAX_COL = 10

    #ammends the columns and set up the key to utilize features of the preview tab
    for i in range(MAX_ROWS):
        inputs = [sg.T('{}'.format(i), size=(4,1), justification='right')] + [sg.In(size=(10, 1), pad=(1, 1), justification='right', key=(i,j), do_not_clear=True) for j in range(MAX_COL)]
        columm_layout.append(inputs)

    #sets the preview pane to see the preview portion
    Preview = [ [sg.Menu(menu_def)],
               [sg.Column(columm_layout, size=(300,100), scrollable=True)] ]

    #sets the layout for the graph settings on the box
    Setting = [[sg.Slider(range=(1,1000), default_value=500, size=(10,10), orientation='horizontal', key = 'height',font=('Helvetica', 12)),
                    sg.Text('  Name:  ', size=(8,1)), sg.InputText(key='graphtitle', size=(8,1))],
               [sg.Text('Enter graph Height')],
               [sg.Slider(range=(1,1000), default_value=500, size=(10,10), orientation='horizontal', key = 'width', font=('Helvetica', 12)),
                    sg.Text('       '),sg.InputCombo(['Red', 'Green', 'Blue', 'Yellow', 'Orange'])],
               [sg.Text('Enter graph Width')]]
              
    #general layout bringing all the smaller frames together
    layout = [[sg.Text('use open to load the csv')], 
              [sg.Frame('Preview', Preview, title_color='green', font = 'Any 12')],
              [sg.Frame('Graph Settings', Setting, title_color='blue', font = 'Any 12')]]

    #names the table and creates the layout
    window = sg.Window('Table', return_keyboard_events=True).Layout(layout)

    #starts the event listener for the window
    while True:

        #reads the window
        event, values = window.Read()
        
        #if exit
        if event is None or event == 'Exit':
            break

        #if they click about
        elif event == 'About...':
            sg.Popup('A simple graphing program to plot various headers and points from a CSV')

        #if they click open
        elif event == 'Open':

            #opens up a window to choose a file with the extension .csv
            filename = sg.PopupGetFile('filename to open', no_window=True, file_types=(("CSV Files","*.csv"),))
            
            #opens in read and populates var with everything in the csv
            if filename is not None:
                with open(filename, "r") as infile:
                    reader = csv.reader(infile)
                    try:
                        data = list(reader)
                          # read everything else into a list of rows

                    #error handling to make sure that the file is readable
                    except:

                        #let the user know they tried to load a bad file
                        sg.PopupError('Error reading file')
                        continue

                # clear the table
                [window.FindElement((i,j)).Update('') for j in range(MAX_COL) for i in range(MAX_ROWS)]

                #cycles through the array of rows and enumerates the data
                for i, row in enumerate(data):

                    #for each row in enumerated data then item -- var j
                    for j, item in enumerate(row):

                        #location of each box in the preview
                        location = (i,j)

                        #for each part try and read the table
                        try:            
                            target_element = window.FindElement(location)
                            new_value = item
                            if target_element is not None and new_value != '':
                                target_element.Update(new_value)

                        #no work no do
                        except:
                            pass
        #TODO fix the save function to allow a user to change a field and save it as a csv
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


        #if the user decides to select line graph
        elif event == 'line':

            #names everything for use in the rest of the program            
            name = values['graphtitle']
            plotwidthfloat= values['width']
            plotheightfloat= values['height']

            #changes the type floats to type Ints
            plotwidth=int(plotwidthfloat)
            plotheight=int(plotheightfloat)

            #read the csv of the given filename
            weight = pd.read_csv(filename)

            #TODO make this variable based off user input
            xx=weight["time(hours)"]
            yy1=weight["Electrode"]
            yy2=weight["Ohmic"]
            yy3=weight["tasr"]

            #sets the name and adds html so launch in browser and display graph
            output_file(name+'.html')
            p = figure(title = name, plot_width=plotwidth, plot_height=plotheight)
            p.circle(xx,yy1, legend="Electrode")
            p.line(xx,yy1, legend="Electrode")
            p.line(xx,yy2, legend="Ohmic", line_color='green')
            p.square(xx,yy2, legend="Ohmic", fill_color='green',line_color='green')
            p.line(xx,yy3, legend="Tasr", line_color='red')
            p.diamond(xx,yy3, legend="Tasr", line_color='red', fill_color='red')


            #TODO add ability for user to choose location
            p.legend.location = "top_right"

            #show the graph
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

Main()