import csv
from datetime import datetime
from bokeh.plotting import figure, output_file, show

data={'Date':[], 'Volume':[]}

with open('MSFT.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        data['Date'].append(datetime.strptime(row['Date'],'%Y-%m-%d'))
        data['Volume'].append(int(row['Volume']))

output_file("exemple.html")

print(data['Date'])

p = figure(plot_width=800, plot_height=250, x_axis_type="datetime")

p.line(data['Date'], data['Volume'], color="black", alpha=0.5)
show(p)