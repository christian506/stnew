import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px

file_path = 'https://linked.aub.edu.lb/pkgcube/data/df6527f0de0990b7237dbcef186a3d52_20240904_215117.csv'
df = pd.read_csv(file_path)
st.title('Guest House Distribution in Batroun and Other Towns')

all_towns = df['Town'].unique()
selected_towns = st.multiselect('Select Towns for Comparison (including Batroun)', all_towns, default=['Batroun'])

filtered_data = df[df['Town'].isin(selected_towns)]
batroun_data = filtered_data[filtered_data['Town'] == 'Batroun']
batroun_guest_houses = batroun_data['Total number of guest houses'].sum()
total_guesthouses = filtered_data['Total number of guest houses'].sum()

calc_method = st.selectbox(
    'Select how to calculate percentages:',
    ['Percentage of total guest houses in all towns', 'Percentage of selected towns only']
)

if calc_method == 'Percentage of total guest houses in all towns':
    total_all_towns = df['Total number of guest houses'].sum()
    batroun_percentage = (batroun_guest_houses / total_all_towns) * 100
    other_percentage = ((total_all_towns - batroun_guest_houses) / total_all_towns) * 100
    labels = ['Batroun', 'All Other Towns']
    values = [batroun_guest_houses, total_all_towns - batroun_guest_houses]
else:
    batroun_percentage = (batroun_guest_houses / total_guesthouses) * 100
    other_percentage = ((total_guesthouses - batroun_guest_houses) / total_guesthouses) * 100
    labels = ['Batroun', 'Other Selected Towns']
    values = [batroun_guest_houses, total_guesthouses - batroun_guest_houses]

show_percent = st.checkbox("Show Percentages on the Pie Chart", value=True)

# Create the pie chart
fig = go.Figure(data=[go.Pie(
    labels=labels,
    values=values,
    hole=0.3,  # Donut chart
    textinfo='label+percent' if show_percent else 'label',
)])

fig.update_layout(
    title=f'Guest House Distribution in Batroun vs. {labels[1]} ({calc_method})',
)

# Display the pie chart
st.plotly_chart(fig)

# Show detailed percentages as a table below the chart
st.write(f'Percentage of guest houses in Batroun: {batroun_percentage:.2f}%')
st.write(f'Percentage of guest houses in {labels[1]}: {other_percentage:.2f}%')












# Title of the app
st.title('Proportion of Towns in Lebanon with/without Hotels')

display_mode = st.radio('Display as:', ('Proportion (%)', 'Absolute Counts'))

bar_color_exist = st.color_picker('Pick a color for "Hotels Exist" bar', '#636EFA')
bar_color_not_exist = st.color_picker('Pick a color for "Hotels Do Not Exist" bar', '#EF553B')
if display_mode == 'Proportion (%)':
    proportions = df['Existence of hotels - does not exist'].value_counts(normalize=True) * 100
    y_label = 'Proportion (%)'
else:
    proportions = df['Existence of hotels - does not exist'].value_counts()
    y_label = 'Absolute Counts'

x = ['Hotels Exist', 'Hotels Do Not Exist']
y = proportions.sort_index()  # Sorting to ensure 0 (does not exist) is before 1 (exists)
show_grid = st.checkbox('Show Grid Lines', value=True)

# Create the bar chart
fig = go.Figure(data=[go.Bar(
    x=x,
    y=y,
    marker=dict(
        color=[bar_color_exist, bar_color_not_exist],  # Dynamic colors based on user input
    )
)])

# Update layout
fig.update_layout(
    title=f'Distribution of Towns with/without Hotels ({display_mode})',
    title_x=0.5,  # Center the title
    xaxis_title='Hotel Existence',
    yaxis_title=y_label,
    xaxis=dict(
        title='Existence of Hotels',
        tickvals=[0, 1],
        ticktext=['Does Not Exist', 'Exists'],
        zeroline=False,  # Hide the zero line
        gridcolor='LightGray' if show_grid else 'white',  # Grid lines based on user preference
        gridwidth=1  # Width of the grid lines
    ),
    yaxis=dict(
        title=y_label,
        zeroline=False,  # Hide the zero line
        gridcolor='LightGray' if show_grid else 'white',  # Grid lines based on user preference
        gridwidth=1  # Width of the grid lines
    ),
    plot_bgcolor='white',  # Background color of the plot
    paper_bgcolor='lightgrey',  # Background color of the entire figure
    margin=dict(l=40, r=40, t=40, b=40)  # Margins around the plot
)

# Show the plot
st.plotly_chart(fig)

# Optional: Show the raw data table for better insights
if st.checkbox('Show Raw Data'):
    st.write(df)












st.title("Interactive Tourism Data Plot")

# Slider for 'Tourism Index'
min_index = df['Tourism Index'].min()
max_index = df['Tourism Index'].max()
selected_index = st.slider('Select Tourism Index', min_value=int(min_index), max_value=int(max_index), value=int(min_index))

# Filter data based on slider
filtered_df = df[df['Tourism Index'] == selected_index]

# Create Plotly plot
fig = px.scatter(
    filtered_df,
    x='Total number of hotels',
    y='Total number of restaurants',
    color='Town',
    hover_name='Town',
    title=f"Tourism Data for Index {selected_index}"
)

# Display plot
st.plotly_chart(fig)



















# Title
st.title("Sunburst Chart of Tourism Metrics by Town")

# User selects a metric to visualize
metric = st.selectbox(
    "Select Metric to Visualize",
    ["Total number of cafes", "Total number of guest houses", "Total number of restaurants", "Total number of hotels"],
    key="metric_selectbox"  # Unique key for this widget
)

# Filter out rows where the selected metric is zero or NaN
filtered_data = df[df[metric].notnull() & (df[metric] > 0)]

# Check if there is valid data remaining
if filtered_data.empty:
    st.warning(f"No data available for '{metric}'. Please select another metric or adjust the filter.")
else:
    # Define a custom color scale
    custom_color_scale = [
        [0, 'white'],        # Color for the lower end (0)
        [0.1, 'white'],      # Color for the range 0-10
        [0.1, 'blue'],       # Transition point (10)
        [1, 'red']           # Color for the upper end (100)
    ]
    
    # Create the sunburst chart with custom color scale
    fig = px.sunburst(
        filtered_data,
        path=["Town"],  # Hierarchical structure: Town
        values=metric,
        color=metric,
        hover_data=[],
        color_continuous_scale=custom_color_scale,  # Apply custom color scale
        range_color=[0, 100],  # Set the color range from 0 to 100
        title=f"{metric} Distribution Across Towns"
    )

    # Update layout for a better appearance and color bar customization
    fig.update_layout(
        margin=dict(t=50, l=25, r=25, b=25),
        title_x=0.5,
        coloraxis_colorbar=dict(
            title=metric,
            ticks="outside",
            tickvals=[0, 10, 50, 100],
            ticktext=['0', '10', '50', '100'],
            tickmode='array'
        )
    )

    # Show the chart
    st.plotly_chart(fig)
