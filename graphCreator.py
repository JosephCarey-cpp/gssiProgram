# CREDIT: Geeks For Geeks. See issue #7 for code origin and documentation
import matplotlib.pyplot as plt
import csv
import numpy as np

yAxis = []
x1Axis = []
x2Axis = []
x3Axis = []
x4Axis = []
x5Axis = []
x6Axis = []
x7Axis = []

layerMaxmimum = []
layerMinimum =[]



def barGraph(x,y):
    with open('graphTestCSV.csv','r') as csvfile:
        plots = csv.reader(csvfile, delimiter = ',')
        
        for row in plots:
            x.append(row[0])
            y.append(float(row[1]))
    
    plt.bar(x, y, color = 'g', width = 0.72, label = "Accuracy")
    plt.xlabel('Data used %')
    plt.ylabel('Accuracy %')
    plt.title('Graph Test', fontsize = 20)
    plt.legend()
    plt.show()


def lineGraph(yAxis,x1Axis,x2Axis,x3Axis,x4Axis,x5Axis,x6Axis,x7Axis,layerMaxmimum,layerMinimum):
    with open('graphTestCSV.csv','r') as csvfile:
        lines = csv.reader(csvfile, delimiter=',')
        for row in lines:
            yAxis.append(row[0])
            x1Axis.append(float(row[1]))
            x2Axis.append(float(row[2]))
            x3Axis.append(float(row[3]))
            x4Axis.append(float(row[4]))
            x5Axis.append(float(row[5]))
            x6Axis.append(float(row[6]))
            x7Axis.append(float(row[7]))
            layerMaxmimum.append(float(row[8]))
            layerMinimum.append(float(row[9]))

            
    
    plt.plot(yAxis, x1Axis, color = 'red', linestyle = 'solid', marker = 'o',label = "Layer 4")
    plt.plot(yAxis, x2Axis, color = 'green', linestyle = 'solid', marker = 'o',label = "Layer 5")
    plt.plot(yAxis, x3Axis, color = 'purple', linestyle = 'solid', marker = 'o',label = "Layer 6")
    plt.plot(yAxis, x4Axis, color = 'darkorange', linestyle = 'solid', marker = 'o',label = "Layer 7")
    plt.plot(yAxis, x5Axis, color = 'royalblue', linestyle = 'solid', marker = 'o',label = "Layer 8")
    plt.plot(yAxis, x6Axis, color = 'black', linestyle = 'solid', marker = 'o',label = "Layer 9")
    plt.plot(yAxis, x7Axis, color = 'turquoise', linestyle = 'solid', marker = 'o',label = "Layer 10")
    plt.plot(yAxis, layerMaxmimum, color = 'grey', linestyle = 'dashed', label = "Size Bounds")
    plt.plot(yAxis, layerMinimum, color = 'grey', linestyle = 'dashed')
    

    plt.xticks(rotation = 25)
    plt.xlabel('Sample Count')
    plt.ylabel('Accuracy (%)')
    plt.title('Three Families Accuracy with Minimal Data by Sample Count Final Results', fontsize = 15)
    plt.grid()
    plt.legend()
    plt.show()

lineGraph(yAxis,x1Axis,x2Axis,x3Axis,x4Axis,x5Axis,x6Axis,x7Axis,layerMaxmimum,layerMinimum)