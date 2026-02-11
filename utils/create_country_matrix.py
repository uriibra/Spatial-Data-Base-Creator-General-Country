import geopandas as gpd
import pandas as pd
from shapely.geometry import box
from utils import tools
from utils import create_rectangular_matrix

def matrix_boundary(country_name: str, matrix_route: str, num_cells_lat: int, num_cells_lon: int) -> None:
    #Read data
    country = gpd.read_file(f'./data/country boundary/{country_name}.json')

    #Find Max and Min Coordinates
    limits = country.geometry.bounds
    min_lon = limits['minx'].min().astype(float)
    max_lon = limits['maxx'].max().astype(float)
    min_lat = limits['miny'].min().astype(float)
    max_lat = limits['maxy'].max().astype(float)
    bounds = min_lat, min_lon, max_lat, max_lon
    
    #Create General Rectangular Matrix Main and Shifted
    main_matrix = create_rectangular_matrix.create_matrix(bounds, num_cells_lat, num_cells_lon, 'main', matrix_route)
    vertical_matrix, horizontal_matrix = create_rectangular_matrix.set_shifted_matrix(bounds, num_cells_lat, num_cells_lon, matrix_route)
    
    #Check inside
    main_matrix['cell'] = main_matrix.apply(lambda row: box(row['min_lon'], row['min_lat'], row['max_lon'], row['max_lat']), axis=1)
    main_matrix['inside'] = main_matrix['cell'].apply(lambda r: country.geometry.apply(lambda poly: poly.intersects(r)).any())
    filtered_main_matrix = main_matrix[main_matrix['inside'] == True].reset_index()
    
    
    #Find Country Cells and Filter Shifted Matrix
    country_cells_list = filtered_main_matrix['cell_id'].tolist()
    filtered_vertical_matrix = vertical_matrix[vertical_matrix['cell_id'].isin(country_cells_list)]
    filtered_horizontal_matrix = horizontal_matrix[horizontal_matrix['cell_id'].isin(country_cells_list)]
    
    filtered_main_matrix.to_csv(f'{matrix_route}/{country_name}_main.csv', index=False, sep = ';', decimal = ',')
    filtered_vertical_matrix.to_csv(f'{matrix_route}/{country_name}_vertical_shift.csv', index=False, sep = ';', decimal = ',')
    filtered_horizontal_matrix.to_csv(f'{matrix_route}/{country_name}_horizontal_shift.csv', index=False, sep = ';', decimal = ',')

    return (filtered_main_matrix, filtered_vertical_matrix, filtered_horizontal_matrix)
    