import csv
from bs4 import BeautifulSoup

# Map colors
### GRAYSCALE
# colors = ["#ffffff", "#f0f0f0", "#d9d9d9", "#bdbdbd", "#969696", "#737373", "#525252", "#252525"]
# colors = ["#f7f7f7", "#d9d9d9", "#bdbdbd", "#969696", "#636363", "#252525"]
# colors = ["#f7f7f7", "#cccccc", "#969696", "#525252"]

### REDS
# colors = ["#FFF5F0", "#FEE0D2", "#FCBBA1", "#FC9272", "#FB6A4A", "#EF3B2C", "#CB181D", "#99000D"]
# colors = ["#fee5d9", "#fcbba1", "#fc9272", "#fb6a4a", "#de2d26", "#a50f15"]
# colors = ["#FEE5D9", "#FCAE91", "#FB6A4A", "#CB181D"]

### Y/OR/RED
# colors = ["#FFFFCC", "#FFEDA0", "#FED976", "#FEB24C", "#FD8D3C", "#FC4E2A", "#E31A1C", "#B10026"]
# colors = ["#FFFFB2", "#FED976", "#FEB24C", "#FD8D3C", "#F03B20", "#BD0026"]




# Read in unemployment rates
unemployment = {}
min_value = 100; max_value = 0
reader = csv.reader(open('data/unemployment08.csv'), delimiter=",")
for row in reader:
    try:
        full_fips = row[1] + row[2]
        rate = float( row[8].strip() )
        unemployment[full_fips] = rate
        if rate > max_value:
            max_value = rate
        if rate < min_value:
            min_value = rate
    except:
        pass


### Purple/Red color scheme. Replace line below with colors above to try others.
colors = ["#F1EEF6", "#D4B9DA", "#C994C7", "#DF65B0", "#DD1C77", "#980043"]


# Load the SVG map
svg = open('USA_Counties_with_FIPS_and_names.svg', 'r').read()
soup = BeautifulSoup(svg, "html.parser")

paths = soup.findAll('path')

# Change colors accordingly
path_style = 'font-size:12px;fill-rule:nonzero;stroke:#000000;stroke-opacity:1;stroke-width:0.1;stroke-miterlimit:4;stroke-dasharray:none;stroke-linecap:butt;marker-start:none;stroke-linejoin:bevel;fill:'
for p in paths:
    
    if p['id'] not in ["State_Lines", "separator"]:
        
        try:
            rate = unemployment[p['id']]
        except:
            continue
            
        if rate > 10:
            color_class = 5
        elif rate > 8:
            color_class = 4
        elif rate > 6:
            color_class = 3
        elif rate > 4:
            color_class = 2
        elif rate > 2:
            color_class = 1
        else:
            color_class = 0


        color = colors[color_class]
        p['style'] = path_style + color

print soup.prettify()