#!/usr/bin/env python
'''
This is a program to be used to easily make customizable graphs from CVS files with
all sorts of customizable functions to be able to graph your data

'''

__author__ = "Jonathan Obenland"
__copyright__ = "Copyright 2019, MEII"
__credits__ = ["Jonathan Obenland", "Mikethewatchguy"]
__license__ = "GPL"
__version__ = "1.4.7"
__maintainer__ = "Jonathan Obenland"
__email__ = "jobenland1@gmail.com"
__status__ = "Production"

import csv
import pandas as pd
import pandas
import sys
import np
import webbrowser
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource,HoverTool
if sys.version_info[0] >= 3:
    import PySimpleGUI as sg
else:
    import PySimpleGUI27 as sg



#Main method that runs all features of the program 
def Main():
    
    #adds the options panel to the top
    sg.SetOptions(element_padding=(0,0))

    #adds the options to the bar at top
    menu_def = [['File', ['Open', 'Exit']],
                ['Generate', ['Preview','Graph', ['line', 'bar',], 'Reset'],],
                ['Help', ['About...','Submit An Issue']]]

    columm_layout = [[]]

    #creates the preview portion to look at the opened csv file
    MAX_ROWS = 800
    MAX_COL = 10
    data=[]
    header_lisst=[1,2,3,4,5,6,7]
    #ammends the columns and set up the key to utilize features of the preview tab
    for i in range(MAX_ROWS):
        inputs = [sg.T('{}'.format(i), size=(4,1), justification='right')] + [sg.In(size=(10, 1), pad=(1, 1), justification='right', key=(i,j), do_not_clear=True) for j in range(MAX_COL)]
        columm_layout.append(inputs)

    #sets the preview pane to see the preview portion
    Preview = [ [sg.Menu(menu_def)],
                [sg.Text('To preview imported data, select '),sg.Text("Generate -> Preview", text_color = 'blue')], 
                [sg.Text('Make sure the text is green below before proceeding')],
                [sg.Text('                                                    ')],
                [sg.Text('No CSV has been entered', size = (51,1),text_color = 'red',key = 'fn')],
                [sg.Text('                                                        ')]]
               #[sg.Column(columm_layout, size=(410,100), scrollable=True)],
               #[sg.Table(values=data,max_col_width=1,headings=header_lisst,
               #auto_size_columns=False, justification='right',alternating_row_color = 'lightblue',vertical_scroll_only=False,key='tab')]]
    #sets the layout for the graph settings on the box
    Setting = [[sg.Slider(range=(1,1500), default_value=610, size=(10,10), orientation='horizontal', key = 'height',font=('Helvetica', 12)),
                    sg.Text('    Name: ', size=(10,1)), sg.InputText(key='graphtitle', size=(15,1)), sg.Text('   Title of x-axis ', size = (14,1)),
                    sg.InputText(key='xlabel', size=(15,1))],
               [sg.Text('Enter graph Height')],
               [sg.Slider(range=(1,1500), default_value=650, size=(10,10), orientation='horizontal', key = 'width', font=('Helvetica', 12)),
                    sg.Text('       '),sg.Text(' Legend Location  '), sg.InputCombo(['Top Left','Top Right','Bottom Left', 'Bottom Right'], key = 'legendloc'),
                    sg.Text('  Title of y-axis ', size=(13,1)), sg.InputText(key='ylabel',size=(15,1))],
               [sg.Text('Enter graph Width')],
               [sg.Text(' ')],
               [sg.Checkbox('Graph Multiple Data Sets ',default = False,key='multiA'),sg.Combo(['Dot','No Marker', 'Square', 'Triangle', 'Inverted Triangle','Diamond'], key= 'dot'),
                    sg.Text('    '),sg.Text('Size of Mark      '),sg.Slider(range=(1,50), default_value=5, size=(10,10), orientation='horizontal', key = 'size', font=('Helvetica', 12))],
               [sg.Text(' ')],
               [sg.Text('Select the X axis'), sg.Text('                              Select the y axis(s)')],
               [sg.Listbox(['Load CSV to See available headers'], key = 'xheaders', size=(30,6)),sg.Listbox(['Load CSV to See available headers'],select_mode='multiple',key = 'yheaders', size=(30,6)), sg.Checkbox('Maintain Aspect',default = False,key='ASR')]]
              
    #general layout bringing all the smaller frames together
    layout = [[sg.Text('First, Use Open to load a CSV into the program and verify the correct path in the preview box.')],
              [sg.Text('Note to keep the box a perfect square, leave the height and width at 610 by 650')], 
              [sg.Frame('Preview', Preview, title_color='green', font = 'Any 12'), sg.Image('Img/UMD.png')],
              [sg.Frame('Graph Settings', Setting, title_color='blue', font = 'Any 12')],
              [sg.Text('Property of Maryland Energy Innovation Institute                                           written by Jonathan Obenland', text_color = 'red')],
              [sg.Text('All rights reserved under GNU-GPL version 3                                                Python 3.x   Build: ', text_color = 'blue'),sg.Text("PASSING",text_color = 'green')]]

    #names the table and creates the layout
    window1 = sg.Window('Table', return_keyboard_events=True).Layout(layout).Finalize()

    #starts the event listener for the window
    window2_active = False
    while True:

        #reads the window
        event1, values1 = window1.Read()
        
        #if exit
        if event1 is None or event1 == 'Exit':
            break

        #if they click about
        elif event1 == 'About...':
            sg.Popup('A simple graphing program to plot various headers and points from a CSV')

        #if they click open
        elif event1 == 'Open':
            
            #opens up a window to choose a file with the extension .csv
            filename = sg.PopupGetFile('filename to open', no_window=True, file_types=(("CSV Files","*.csv"),))

            nameUpdate = window1.FindElement('fn')
            nameUpdate.Update(filename, text_color = 'green')

            #populates the first box for choosing the x axis
            if filename is not None:
                with open(filename, "r") as infile:
                    #sets the headers to an array
                    reader = csv.reader(infile)
                    header_list=[]
                    header_list = next(reader)
                    print(header_list)
                    #updates the box with the array of x headers
                    headerupdate = window1.FindElement('xheaders')
                    headerupdate.Update(header_list)

            #populates the secound box for choosing the y axis to include     
            if filename is not None:
                with open(filename, "r") as infile:
                    #sets the headers to an array
                    reader = csv.reader(infile)
                    header_list2=[]
                    header_list2 = next(reader)
                    print(header_list)
                    #updates the box with the new headers from the array
                    headerupdate2 = window1.FindElement('yheaders')
                    headerupdate2.Update(header_list2)  
            
            #opens in read and populates var with everything in the csv
            if filename is not None:
                with open(filename, "r") as infile:
                    reader = csv.reader(infile)
                    try:
                        #read everything into rows
                        data = list(reader)

                    #error handling to make sure that the file is readable
                    except:

                        #let the user know they tried to load a bad file
                        sg.PopupError('Error reading file')
                        continue
                '''
                if filename is not None:
                    with open(filename,'r') as infile:
                        reader = csv.reader(infile)
                        header_lisst=next(reader)
                        try:
                            data=list(reader)
                        except:
                            sg.PopupError("error reading file")
                        table = window.FindElement('tab')
                        table.Update(values=data)
                '''        
                '''
                
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
            '''
                
        #TODO fix the save function to allow a user to change a field and save it as a csv
        #FIXME saves in an unreadable corrupt CSV
        elif event1 == 'Save':
            filename = sg.PopupGetFile('filename to open', save_as = True,no_window=True, file_types=(("CSV Files","*.csv"),))
            for i, row in enumerate(data):
                for j, item in enumerate(row):
                    location = (i,j)
                    try:
                        target_element = window1.FindElement(location)
                    except:
                        pass
                    deform = values1[target_element]
                    print (deform)
        elif event1 == "Preview":
            if not window2_active:
                window2_active=True
                if filename is not None:
                    with open(filename, 'r') as infile:
                        reader = csv.reader(infile)
                        header_lisst = next(reader)
                        data = list(reader)
                layout2 = [[sg.Table(values = data,
                                        headings = header_lisst,
                                        auto_size_columns = False,
                                        max_col_width = 15,
                                        justification = 'right',
                                        alternating_row_color = 'lightblue',
                                        vertical_scroll_only = False,
                                        num_rows = min(len(data),20))]]

                window2 = sg.Window(filename + '   PREVIEW').Layout(layout2)
            if window2_active:
                event2, values2 = window2.Read(timeout=100)
                if event2 is None or event2 == 'Exit':
                    window2_active = False
                    window2.Close()

        #if the user decides to select line graph
        elif event1 == 'line':

            #names everything for use in the rest of the program            
            name = values1['graphtitle']
            plotwidthfloat= values1['width']
            plotheightfloat= values1['height']
            xaxisname = values1['xlabel']
            yaxisname = values1['ylabel']

            #changes the type floats to type Ints
            plotwidth=int(plotwidthfloat)
            plotheight=int(plotheightfloat)

            #read the csv of the given filename
            weight = pd.read_csv(filename)

            #gets the values of the headers
            xhead = values1['xheaders']
            yhead = values1['yheaders']

            #array of colors to choose from
            #TODO add more colors
            colorar = ['green','blue','red','orange','aqua','black', 'pink', 'cyan', 'purple', 'magenta']

            #headers.Update(header_list)
            if values1['ASR'] == True:
                p = figure(title = name, plot_width=plotwidth, plot_height=plotheight, match_aspect=True)
            if values1['ASR'] == False:
                p = figure(title = name, plot_width=plotwidth, plot_height=plotheight)

            p.xaxis.axis_label = xaxisname
            p.yaxis.axis_label = yaxisname
            i=0
            
            if values1['multiA'] == True:
                
                '''
                for i in range(len(xhead)):
                    xxGet=weight[xhead[i]]
                    print(xxGet)
                    xxIndex = xxGet[i]
                    print(xxIndex)
                    splitTest = xxIndex.split(',')
                    print (splitTest)
                    xx = splitTest[0]
                    yy = splitTest[1]
                    print (xx)
                '''
                #goes through each of the headers selected and uses them in the program
                for i in range(len(yhead)):
                    #headerupdate2 = window1.FindElement('xheaders')
                    #headerupdate2.Update('Multi Axis enabled, Select Y only')
                    #sets the color to the array at the index. leave for now
                    ccolor = colorar[i]
                    print(ccolor)
                    xx=[]
                    yy=[]
                    #increments yy with a number at the end for adding more lines
                    varYY = 'yy'+str(i)
                    varYY = weight[yhead[i]]
                    yList = varYY.tolist()
                    
                    for line in yList:
                        splitter = line.strip('(')
                        
                        splitter = splitter.strip(')')
                        splitter = splitter.split(',')
                        splitterIntX = (float(splitter[0]))
                        splitterIntY = (float(splitter[1]))
                        xx.append(splitterIntX)
                        yy.append(splitterIntY)


                    
                    #creates the lines
                    dotMrk = values1['dot']
                    sizeOfMrk = values1['size']
                    markSize = int(sizeOfMrk)
                     
                    if dotMrk == 'Dot':
                        p.line(xx,yy, legend=yhead[i],line_color=ccolor)
                        p.circle(xx,yy, legend=yhead[i],fill_color=ccolor,line_color=ccolor,size= markSize)
                    if dotMrk == 'No Marker':
                        p.line(xx,yy, legend=yhead[i],line_color=ccolor)
                    if dotMrk == 'Square':
                        p.line(xx,yy, legend=yhead[i],line_color=ccolor)
                        p.square(xx,yy, legend=yhead[i],fill_color=ccolor,line_color=ccolor,size= markSize)
                    if dotMrk == 'Triangle':
                        p.line(xx,yy, legend=yhead[i],line_color=ccolor)
                        p.triangle(xx,yy, legend=yhead[i],fill_color=ccolor,line_color=ccolor,size= markSize)
                    if dotMrk == 'Inverted Triangle':
                        p.line(xx,yy, legend=yhead[i],line_color=ccolor)
                        p.inverted_triangle(xx,yy, legend=yhead[i],fill_color=ccolor,line_color=ccolor,size= markSize)
                    if dotMrk == 'Diamond':
                        p.line(xx,yy, legend=yhead[i],line_color=ccolor)
                        p.diamond(xx,yy, legend=yhead[i],fill_color=ccolor,line_color=ccolor,size= markSize)

                    p.circle(xx,yy, legend=yhead[i],fill_color=ccolor,line_color=ccolor)
                    p.line(xx,yy, legend=yhead[i],line_color=ccolor)
                    #testing...
                    print(yhead[i])


            if values1['multiA'] == False:
            #unecessary but still leave here for now
                for i in range(len(xhead)):
                    xx=weight[xhead[i]]
                
                #goes through each of the headers selected and uses them in the program
                for i in range(len(yhead)):
                    
                    #sets the color to the array at the index. leave for now
                    ccolor = colorar[i]
                    print(ccolor)
                    
                    #increments yy with a number at the end for adding more lines
                    var = 'yy'+str(i)
                    var = weight[yhead[i]]
                    print(var)
                    #creates the lines
                    dotMrk = values1['dot']
                    sizeOfMrk = values1['size']
                    markSize = int(sizeOfMrk)
                     
                    if dotMrk == 'Dot':
                        p.line(xx,var, legend=yhead[i],line_color=ccolor)
                        p.circle(xx,var, legend=yhead[i],fill_color=ccolor,line_color=ccolor,size= markSize)
                    if dotMrk == 'No Marker':
                        p.line(xx,var, legend=yhead[i],line_color=ccolor)
                    if dotMrk == 'Square':
                        p.line(xx,var, legend=yhead[i],line_color=ccolor)
                        p.square(xx,var, legend=yhead[i],fill_color=ccolor,line_color=ccolor,size= markSize)
                    if dotMrk == 'Triangle':
                        p.line(xx,var, legend=yhead[i],line_color=ccolor)
                        p.triangle(xx,var, legend=yhead[i],fill_color=ccolor,line_color=ccolor,size= markSize)
                    if dotMrk == 'Inverted Triangle':
                        p.line(xx,var, legend=yhead[i],line_color=ccolor)
                        p.inverted_triangle(xx,var, legend=yhead[i],fill_color=ccolor,line_color=ccolor,size= markSize)
                    if dotMrk == 'Diamond':
                        p.line(xx,var, legend=yhead[i],line_color=ccolor)
                        p.diamond(xx,var, legend=yhead[i],fill_color=ccolor,line_color=ccolor,size= markSize)
                    
                    

                    #testing...
                    print(yhead[i])

            #output for the html file
            output_file(name+'.html')

            #grabbing the data from the legend area spot
            lloc = values1['legendloc']
            
            #user selected location of legend
            if lloc == 'Top Right':
                p.legend.location = "top_right"

            elif lloc == 'Top Left':
                p.legend.location = "top_left"

            elif lloc == 'Bottom Right':
                p.legend.location = "bottom_right"

            elif lloc == 'Bottom Left':
                p.legend.location ="bottom_left" 




            #show the graph
            '''
            p.add_tools(HoverTool(
                tooltips=[
                    ( 'date',   '@date{%F}'            ),
                    ( 'close',  '$@{adj close}{%0.2f}' ), # use @{ } for field names with spaces
                    ( 'volume', '@volume{0.00 a}'      ),
                ],

                formatters={
                    'date'      : 'datetime', # use 'datetime' formatter for 'date' field
                    'adj close' : 'printf',   # use 'printf' formatter for 'adj close' field
                                            # use default 'numeral' formatter for other fields
                },

                # display a tooltip whenever the cursor is vertically in line with a glyph
                mode='vline'
            ))   
            '''        

            show(p)

        #if the user wants to reset the program
        elif event1 == "Reset":
                window1.Close()
                Main()

        elif event1 == 'Submit An Issue':
            a_website = "https://github.com/Jobenland/CSV-Graph-Generator/issues"
            webbrowser.open_new(a_website)

        # if a valid table location entered, change that location's value
        try:
            location = (int(values1['inputrow']), int(values1['inputcol']))
            target_element = window1.FindElement(location)
            new_value = values1['value']
            if target_element is not None and new_value != '':
                target_element.Update(new_value)
        except:
            pass

Main()