# CREDIT: Geeks For Geeks. See issue #7 for code origin and documentation
import matplotlib.pyplot as plt
import csv
  
x = []
y = []

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


def lineGraph(x,y):
    with open('graphTestCSV.csv','r') as csvfile:
        lines = csv.reader(csvfile, delimiter=',')
        for row in lines:
            x.append(row[0])
            y.append(float(row[1]))
    
    plt.plot(x, y, color = 'g', linestyle = 'dashed',
            marker = 'o',label = "Data change")
    
    plt.xticks(rotation = 25)
    plt.xlabel('Data used %')
    plt.ylabel('Accuracy %')
    plt.title('Graph Test', fontsize = 20)
    plt.grid()
    plt.legend()
    plt.show()

lineGraph(x,y)