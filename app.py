import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import pydeck as pdk
import json
import networkx as nx
import pydeck as pdk

df = pd.read_csv("updated_data.csv")


st.title("The Dynamics of Human Progress: A Journey Through the Human Development Index")

# Introduction
st.header("Introduction")
st.write("""
    The Human Development Index (HDI) offers a 
         omprehensive outlook on human progress, 
    extending beyond mere economic success to encompass education, health, and longevity.
    In this exploration, we delve into what constitutes human development and how various 
    nations fare in this multifaceted measure.
""")


# Part 1: D3.js Visualization - Split Horizontal Bar Chart for Top and Bottom 10 Countries
st.header("WHOSE ON TOP? LETS SEE!")
st.write("""
    Below you can find the countires who are performing well. OH the ones on top! 
    So, here an idea of putting 10 countires of top so that you get to know how the HDI is for the top countries.
    Now as we have the top we should also know which ones are on the other end, THE BOTTOM 10 countires. Trying to be better...
""")

# Visualizing HDI Rankings with D3.js

# Filter data for top and bottom 10 countries
top_countries = df.sort_values(by='HDI', ascending=False).head(10)
bottom_countries = df.sort_values(by='HDI', ascending=True).head(10)
filtered_data = pd.concat([top_countries, bottom_countries])

# Generate data for D3.js
d3_data_filtered = filtered_data[['Country', 'HDI']].to_dict(orient='records')
d3_data_filtered_json = json.dumps(d3_data_filtered)

# D3.js script for Split Horizontal Bar Chart
d3_script_split_horizontal_bar = f"""
    <script src="https://d3js.org/d3.v6.min.js"></script>
    <div id="d3-split-horizontal-bar-chart"></div>
    <script>
        var data = {d3_data_filtered_json};
        
        // D3.js code for split horizontal bar chart visualization
        var margin = {{top: 40, right: 30, bottom: 50, left: 80}},  // Adjusted top margin
            width = 800 - margin.left - margin.right,
            height = 400 - margin.top - margin.bottom;

        var svg = d3.select("#d3-split-horizontal-bar-chart")
            .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        // Split the data into top and bottom countries
        var topData = data.slice(0, 10);
        var bottomData = data.slice(10);

        // Define scales
        var x = d3.scaleLinear()
            .domain([0, d3.max(data, function(d) {{ return d.HDI; }})])
            .range([0, width]);

        var y = d3.scaleBand()
            .domain(data.map(function(d) {{ return d.Country; }}))
            .range([0, height])
            .padding(0.2);  // Adjusted padding

        // Draw top bars
        svg.selectAll(".top-bar")
            .data(topData)
            .enter().append("rect")
            .attr("class", "top-bar")
            .attr("x", 0)
            .attr("y", function(d) {{ return y(d.Country); }})
            .attr("width", function(d) {{ return x(d.HDI); }})
            .attr("height", y.bandwidth())
            .style("fill", "blue");

        // Draw bottom bars
        svg.selectAll(".bottom-bar")
            .data(bottomData)
            .enter().append("rect")
            .attr("class", "bottom-bar")
            .attr("x", 0)  // Changed x position to 0 for bottom bars
            .attr("y", function(d) {{ return y(d.Country); }})
            .attr("width", function(d) {{ return x(d.HDI); }})
            .attr("height", y.bandwidth())
            .style("fill", "pink");

        // Axes
        svg.append("g")
            .call(d3.axisLeft(y));

        svg.append("g")
            .attr("transform", "translate(0," + height + ")")
            .call(d3.axisBottom(x));
    </script>
"""

# Embed D3.js script for Split Horizontal Bar Chart in Streamlit app
st.components.v1.html(d3_script_split_horizontal_bar, height=500, width=900)


# Part 2: D3.js Visualization - Vertical Bar Chart for Top and Bottom 10 Countries
st.header("WANT TO KNOW HOW EXACTLY THE HDI IS FOR A COUNTRY?")
st.write("""
    We got you! below you can find what exactly is the figure for top and bottom 10 countries.
    You can find it by hovering onto the column. There you go, now you can see how they differ from each other exactly.
""")

# Filter data for top and bottom 10 countries
filtered_data = pd.concat([top_countries, bottom_countries])

# Generate data for D3.js
d3_data_filtered = filtered_data[['Country', 'HDI']].to_dict(orient='records')
d3_data_filtered_json = json.dumps(d3_data_filtered)



# D3.js script for Vertical Bar Chart with HDI on Hover (Adjusted for Display)
d3_script_vertical_bar_filtered = f"""
    <style>
        .bar:hover {{ cursor: pointer; fill-opacity: 0.7; }}
    </style>
    <script src="https://d3js.org/d3.v6.min.js"></script>
    <div id="d3-vertical-bar-chart"></div>
    <script>
        var data = {d3_data_filtered_json};
        
        // D3.js code for vertical bar chart visualization
        var margin = {{top: 40, right: 30, bottom: 70, left: 120}},  // Adjusted top margin
            width = 1000 - margin.left - margin.right,  // Increased frame width
            height = 500 - margin.top - margin.bottom;

        var svg = d3.select("#d3-vertical-bar-chart")
            .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        var x = d3.scaleBand()
            .domain(data.map(function(d) {{ return d.Country; }}))
            .range([0, width])
            .padding(0.2);  // Adjusted padding

        var y = d3.scaleLinear()
            .domain([0, d3.max(data, function(d) {{ return d.HDI; }})])
            .range([height, 0]);

        svg.selectAll(".bar")
            .data(data)
            .enter().append("rect")
            .attr("class", "bar")
            .attr("x", function(d) {{ return x(d.Country); }})
            .attr("width", x.bandwidth())
            .attr("y", function(d) {{ return y(d.HDI); }})
            .attr("height", function(d) {{ return height - y(d.HDI); }})
            .style("fill", "steelblue")
            .on("mouseover", function(event, d) {{  // Tooltip on mouseover
                d3.select(this)
                    .transition()
                    .duration(100)
                    .style("fill", "orange");  // Change color on hover

                d3.select("#tooltip")
                    .style("left", event.pageX + "px")
                    .style("top", event.pageY + "px")
                    .style("opacity", 0.9)
                    .html(d.Country + "<br/>HDI: " + d.HDI);
            }})
            .on("mouseout", function(d) {{  // Reset color and hide tooltip on mouseout
                d3.select(this)
                    .transition()
                    .duration(100)
                    .style("fill", "steelblue");

                d3.select("#tooltip").style("opacity", 0);
            }});

        // Axes
        svg.append("g")
            .attr("transform", "translate(0," + height + ")")
            .call(d3.axisBottom(x))
            .selectAll("text")
            .style("text-anchor", "end")
            .attr("transform", "rotate(-45)")
            .attr("dx", "-0.8em")
            .attr("dy", "0.15em");

        svg.append("g")
            .call(d3.axisLeft(y));

        // Add tooltip container
        d3.select("#d3-vertical-bar-chart")
            .append("div")
            .attr("id", "tooltip")
            .style("position", "absolute")
            .style("z-index", "10")
            .style("opacity", 0);
    </script>
"""

# Embed D3.js script for Vertical Bar Chart with HDI on Hover in Streamlit app
st.components.v1.html(d3_script_vertical_bar_filtered, height=500, width=1000)




# Part 3: D3.js Visualization - Pie Chart for Top and Bottom 10 Countries based on Rank_old
st.header("LIFE EXPECTENCY, PLAYS AN IMPORTANT ROLE IN DEVELOPMENT OF A COUNTRY!!!")
st.write("""
    The life Expectency of countries is shown by the pie chart below. You can checkout how much life expectency a country have. this shows a clear idea on how it affects the human developemnt index of a specifc country.
    Also, it connects with the second assignment as we took the data coloumn from our second assignment which was about heart failure clinical data and we gathered it for all countries
""")

# Filter data for top and bottom 10 countries
top_countries_rank = df.sort_values(by='HDI', ascending=False).head(10)
bottom_countries_rank = df.sort_values(by='HDI', ascending=True).head(10)
filtered_data_rank = pd.concat([top_countries_rank, bottom_countries_rank])

# Generate data for D3.js
d3_data_filtered_rank = filtered_data_rank[['Country', 'Exp_Life']].to_dict(orient='records')
d3_data_filtered_rank_json = json.dumps(d3_data_filtered_rank)

# D3.js script for Pie Chart with Tooltips, Legends, and Smooth Hover
d3_script_pie_chart = f"""
    <style>
        .arc path:hover {{ cursor: pointer; fill-opacity: 0.7; }}
        .legend-container {{ display: flex; flex-direction: column; align-items: flex-start; margin-left: 20px; max-height: 400px; overflow-y: auto; }}
        .legend rect {{ width: 18px; height: 18px; margin-right: 4px; }}
        .tooltip {{ position: absolute; z-index: 10; opacity: 0; transition: opacity 0.2s; }}
    </style>
    <script src="https://d3js.org/d3.v6.min.js"></script>
    <div id="chart-container" style="display: flex;">
        <div id="d3-pie-chart"></div>
        <div id="legend-container" class="legend-container"></div>
        <div id="tooltip" class="tooltip"></div>
    </div>
    <script>
        var data = {d3_data_filtered_rank_json};

        // D3.js code for pie chart visualization with tooltips, legends, and smooth hover
        var width = 400,
            height = 400,
            radius = Math.min(width, height) / 2;

        var color = d3.scaleOrdinal(d3.schemeCategory10);

        var arc = d3.arc()
            .outerRadius(radius - 10)
            .innerRadius(0);

        var pie = d3.pie()
            .sort(null)
            .value(function(d) {{ return d.Exp_Life; }});

        var svg = d3.select("#d3-pie-chart")
            .append("svg")
            .attr("width", width)
            .attr("height", height)
            .append("g")
            .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

        var g = svg.selectAll(".arc")
            .data(pie(data))
            .enter().append("g")
            .attr("class", "arc");

        g.append("path")
            .attr("d", arc)
            .style("fill", function(d) {{ return color(d.data.Country); }})
            .on("mouseover", function(event, d) {{  // Tooltip on mouseover
                d3.select(this)
                    .transition()
                    .duration(100)
                    .attr("d", d3.arc().innerRadius(0).outerRadius(radius + 10));

                d3.select("#tooltip")
                    .style("left", event.pageX + "px")
                    .style("top", event.pageY + "px")
                    .style("opacity", 0.9)
                    .html(d.data.Country + "<br/>Life Exp: " + d.data.Exp_Life);
            }})
            .on("mouseout", function(d) {{  // Hide tooltip on mouseout
                d3.select(this)
                    .transition()
                    .duration(100)
                    .attr("d", arc);

                d3.select("#tooltip").style("opacity", 0);
            }});

        // Add legend
        var legend = d3.select("#legend-container")
            .selectAll(".legend")
            .data(color.domain())
            .enter().append("div")
            .attr("class", "legend");

        legend.append("div")
            .attr("class", "legend-rect")
            .style("background-color", color)
            .style("width", "18px")
            .style("height", "18px")
            .style("margin-right", "4px");

        legend.append("div")
            .attr("class", "legend-text")
            .text(function(d) {{ return d; }});

        // Add tooltip container
        d3.select("#d3-pie-chart")
            .append("div")
            .attr("id", "tooltip")
            .style("position", "absolute")
            .style("z-index", "10")
            .style("opacity", 0)
            .style("transition", "opacity 0.2s");
    </script>
"""

# Embed D3.js script for Pie Chart with Legends and Smooth Hover in Streamlit app
st.components.v1.html(d3_script_pie_chart, height=500)










st.header("WHAT OTHER FACTORS DOES HUMAN DEVELOPMENT INDEX RELIES ON?")
st.write("""
   There are three major factor factors which have a direct effect on HDI of a country. They are Life expectancy of people residing, Schooling 
    i.e. the educated and knowledgeable population of a country and the Gross national income (GNI)
""")
st.write("""
   Want to see how? Below you can plug and see how much of each factor are for top 10 and bottom 10 countries
""")

# Sort the dataframe for top and bottom 10 countries based on HDI
top_countries = df.sort_values(by='HDI', ascending=False).head(10)
bottom_countries = df.sort_values(by='HDI').head(10)
combined = pd.concat([top_countries, bottom_countries])

# Define the function to plot the interactive bar chart
def plot_interactive_bar(metric):
    fig = px.bar(
        combined,
        x='Country',
        y=metric,
        color='HDI_Cat',
        labels={'HDI_Cat': 'HDI Category'},
        title=f'Top and Bottom Countries by {metric}',
        color_discrete_map={
            'VH': 'skyblue',  # Assuming 'VH' is the category for top countries
            'L': 'salmon'     # Assuming 'L' is the category for bottom countries
        }
    )
    st.plotly_chart(fig)

# Main interface for buttons
st.header('Select a Metric to Display')
col1, col2, col3 = st.columns(3)

# Initialize variable to store the selected option
selected_metric = None

# Define the mapping of options to dataset columns
metrics_map = {
    'Life Expectancy': 'Exp_Life',
    'Mean Schooling': 'Mean_School',
    'GNI': 'GNI'
}

# Create buttons for each metric and check if they are clicked
with col1:
    if st.button('Life Expectancy'):
        selected_metric = metrics_map['Life Expectancy']
with col2:
    if st.button('Mean Schooling'):
        selected_metric = metrics_map['Mean Schooling']
with col3:
    if st.button('GNI'):
        selected_metric = metrics_map['GNI']

# Plot the interactive bar chart if a metric is selected
if selected_metric:
    plot_interactive_bar(selected_metric)



st.header("YOU MUST BE THINKING WHY WE ARE ONLY LEANING ABOUT TOP AND BOTTOM 10 COUNTRIES ONLY")
st.write("""
   This was just to get you on track how exactly does the Human Development Index gets calculated 
""")


st.header("WORLD MAP")
st.write("""
   Now that we have the knowledge of how the HDI plays an important role in a country's development by the factors of Life expectency, Schooling 
   and the Gross National Income (GNI). Below is the world map with all the countries which we are researching and you can find all the details 
   and information of that certain country.
""")

st.header("THE BIGGER PICTURE")
# World Map with HDI category on Hover
def hdi_category_to_color(hdi_cat):
    if hdi_cat == 'VH':
        return [0, 128, 0, 160]  # Dark green for Very High HDI
    elif hdi_cat == 'H':
        return [0, 0, 255, 160]  # Blue for High HDI
    elif hdi_cat == 'M':
        return [255, 165, 0, 160]  # Orange for Medium HDI
    elif hdi_cat == 'L':
        return [255, 0, 0, 160]  # Red for Low HDI
    else:
        return [128, 128, 128, 160]  # Grey for undefined categories

# Add a column with the color based on the HDI category
df['color'] = df['HDI_Cat'].apply(hdi_category_to_color)

# Create a PyDeck layer
layer = pdk.Layer(
    'ScatterplotLayer',  # Use a scatter plot layer
    df,
    get_position=['Longitude', 'Latitude'],
    get_color='color',
    get_radius=200000,  # Radius is in meters
    pickable=True  # Enable picking for interaction
)

# Set the viewport location
view_state = pdk.ViewState(
    latitude=df['Latitude'].mean(),
    longitude=df['Longitude'].mean(),
    zoom=1,
    pitch=0,
)

# Create a legend for the HDI categories
st.write("Legend:")
st.write("VH: Very High HDI - Dark Green")
st.write("H: High HDI - Blue")
st.write("M: Medium HDI - Orange")
st.write("L: Low HDI - Red")



# Use a light map style
light_map_style = 'mapbox://styles/mapbox/light-v9'

tooltip = {
    "html": (
        "<b>{Country}</b><br/>"
        "HDI: {HDI}<br/>"
        "Life Expectancy: {Exp_Life}<br/>"
        "GNI: {GNI}<br/>"
        "Mean Schooling: {Mean_School}"
    ),
    "style": {"backgroundColor": "steelblue", "color": "white"}
}


# Render the map with the light theme
st.pydeck_chart(pdk.Deck(
    map_style=light_map_style,
    layers=[layer],
    initial_view_state=view_state,
    tooltip=tooltip  # Add the tooltip to the PyDeck Deck
))




st.header("HOW DOES THESE COUNTRIES CONNECTED WITH HDI ")
st.write("""
        For this we have used a network visualization to show how are each nationality connects with their hdi 
        NetworkX and Matplotlib are used to create a Directed Graph Visualization. The user can select the top and bottom N countries. 
        A larger node size represents high level of HDI whereas the link between nodes shows the HDI relationship between countries based on old  and new ranking. 
        The graph is displayed using the Reingold-Tilford layout. 
         

""")

def read_data(file_path):
    return pd.read_csv(file_path)

def create_directed_graph(data):
    G = nx.DiGraph()

    for _, row in data.iterrows():
        G.add_node(row['Country'], HDI=row['HDI'], Rank_Old=row['Rank_Old'], HDI_Cat=row['HDI_Cat'], GNI=row['GNI'])
        if pd.notnull(row['Rank_Old']):
            G.add_edge(row['Rank_Old'], row['Country'], GNI_HDI=row['GNI_HDI'])

    return G

def visualize_graph(graph, positions, figure_size=(14, 10)):
    fig, ax = plt.subplots(figsize=figure_size)

    # Color map based on HDI categories
    color_map = {'Low': 'red', 'Medium': 'orange', 'High': 'green'}

    # Ensure that 'HDI_Cat' and 'GNI' are present in the data dictionary
    node_colors = [color_map.get(data.get('HDI_Cat', 'Unknown'), 'gray') for node, data in graph.nodes(data=True)]

    # Ensure that 'GNI' is present in the data dictionary
    node_sizes = [data.get('GNI', 0) * 0.01 for node, data in graph.nodes(data=True)]

    # Normalize GNI_HDI values for edge thickness
    edge_widths = [data.get('GNI_HDI', 0) * 0.1 for _, _, data in graph.edges(data=True)]

    nx.draw(graph, positions, with_labels=True, arrows=True, node_size=node_sizes, node_color=node_colors,
            font_size=10, font_color='black', font_weight='bold', edge_color='gray', width=edge_widths, ax=ax)

    # Add some space around the graph
    ax.margins(0.01)

    # Display the graph
    st.pyplot(fig)

def main():
    file_path = r"updated_data.csv"
    df = read_data(file_path)

    # Sort the DataFrame by HDI in descending order
    df_sorted = df.sort_values(by='HDI', ascending=False)

    # Select the top and bottom N countries
    top_n = st.slider("Select Top N Countries", min_value=1, max_value=len(df_sorted), value=20)
    bottom_n = st.slider("Select Bottom N Countries", min_value=1, max_value=len(df_sorted), value=20)

    df_selected = pd.concat([df_sorted.head(top_n), df_sorted.tail(bottom_n)])

    # Create a directed graph
    G = create_directed_graph(df_selected)

    # Choose a root node for the Reingold-Tilford layout (e.g., the first node)
    root_node = list(G.nodes())[0]

    # Calculate positions manually for Reingold-Tilford layout
    pos = nx.spring_layout(G, seed=42)  # You can experiment with different layout algorithms

    # Visualize the graph
    visualize_graph(G, pos)

if __name__ == "__main__":
    main()

