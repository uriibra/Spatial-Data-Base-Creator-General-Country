import os
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import pandas as pd
from utils import tools

#DELETE FILES FROM A SELECTED FOLDER
def remove_files_from_folder(route: str) -> None:
    if not os.path.isdir(route):
        raise ValueError(f"Route Not Found: {route}")

    for name in os.listdir(route):
        file = os.path.join(route, name)
        if os.path.isfile(file):
            os.remove(file)


#PLOT MATRIX AND SAVE TO RESULTS
def plot_matrix(matrix_list: tuple[pd.DataFrame], filename: str, output_folder: str) -> None:
    #Remove Previous Files
    tools.remove_files_from_folder(f'./outputs/plots/{output_folder}')
    
    # Convert To List If It Is A Single DataFrame
    if not isinstance(matrix_list, list):
        matrix_list = [matrix_list]
    
    colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink', 'gray']
    
    # Ensure There Are Enough Colors
    while len(colors) < len(matrix_list):
        colors.extend(colors)
    
    # Calculate Global Limits Comparing All Matrices
    min_lat = min(df['min_lat'].min() for df in matrix_list)
    max_lat = max(df['max_lat'].max() for df in matrix_list)
    min_lon = min(df['min_lon'].min() for df in matrix_list)
    max_lon = max(df['max_lon'].max() for df in matrix_list)
    
    # Create Figure
    fig, ax = plt.subplots(figsize=(12, 10))
    
    # Your Basemap Configuration
    my_map = Basemap(
        projection='merc',
        llcrnrlon=min_lon - 0.7,
        llcrnrlat=min_lat - 0.7,
        urcrnrlon=max_lon + 0.7,
        urcrnrlat=max_lat + 0.7,
        resolution='i',
        area_thresh=10000,
        suppress_ticks=False
    )
    my_map.drawcoastlines(linewidth=1)
    my_map.drawcountries(linewidth=0.5, color='black')
    
    # Draw Each Matrix With Its Color
    for matrix_idx, matrix_df in enumerate(matrix_list):
        current_color = colors[matrix_idx]
        
        # Draw Each Cell Of The Matrix
        for idx, row in matrix_df.iterrows():
            # Convert Geographic Coordinates To Map Coordinates
            x1, y1 = my_map(row['min_lon'], row['min_lat'])
            x2, y2 = my_map(row['max_lon'], row['max_lat'])
            
            # Draw Cell Rectangle
            rect = plt.Rectangle(
                (x1, y1),
                x2 - x1,
                y2 - y1,
                linewidth=1.5,
                edgecolor=current_color,
                facecolor='none',
                alpha=0.7
            )
            ax.add_patch(rect)
    
    # Title With Matrix Information
    title = f'Matrix Plot\n'
    plt.title(title, fontsize=12, weight='bold')
    
    # Legend If There Are Multiple Matrices
    if len(matrix_list) > 1:
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='none', edgecolor=colors[i], linewidth=2, 
                  label=f'MatriX {i+1} ({len(matrix_list[i])} cells)')
            for i in range(len(matrix_list))
        ]
        ax.legend(handles=legend_elements, loc='upper right', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(f'./outputs/plots/{output_folder}/matrix_plot_{filename}.png', bbox_inches='tight')
    #plt.show()
    plt.close()
