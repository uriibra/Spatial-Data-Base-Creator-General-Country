import pandas as pd
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

#FROM INITIAL MATRIX CREATE NEW SHIFTED MATRIX
def set_shifted_matrix(bounds: tuple[float, float, float, float], num_cells_lat: int, num_cells_lon: int, output_route: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    #Define Initial Variables
    min_lat, min_lon, max_lat, max_lon = bounds
    
    #Set Start Displacement, half of the cell size
    jumps_lat_shifted = ((max_lat - min_lat)/num_cells_lat)/2
    jumps_lon_shifted = ((max_lon - min_lon)/num_cells_lon)/2
    
    #Add Shift Value to Coordinates for Matrix Creation
    min_lat_shift = round(min_lat + jumps_lat_shifted,2)
    min_lon_shift = round(min_lon + jumps_lon_shifted,2)
    max_lat_shift = round(max_lat + jumps_lat_shifted,2)
    max_lon_shift = round(max_lon + jumps_lon_shifted,2) 
    
    #Call Create Matrix Function with Shifted Values
    #Vertical Shift (Lat)
    vertical_shift_matrix = create_matrix((min_lat,min_lon_shift,max_lat,max_lon_shift),  num_cells_lat, num_cells_lon, 'vertical_shift', output_route) 
    #Horizontal Shift (Lon)
    horizontal_shift_matrix = create_matrix((min_lat_shift,min_lon,max_lat_shift,max_lon), num_cells_lat, num_cells_lon, 'horizontal_shift', output_route) 
    return (vertical_shift_matrix, horizontal_shift_matrix)


#CREATE INITIAL MATRIX FROM POSITION AND SELECTED SIZE
def create_matrix(bounds: tuple[float, float, float, float], num_cells_lat: int, num_cells_lon: int, code: str, output_route: str) -> pd.DataFrame:
    #Define Initial Variables
    min_lat, min_lon, max_lat, max_lon = bounds
    jumps_lat = (max_lat - min_lat)/num_cells_lat
    jumps_lon = (max_lon - min_lon)/num_cells_lon
    
    #Set Initial Data Lists
    lats = [min_lat]
    lons = [min_lon]
    tmp_lat = min_lat
    tmp_lon = min_lon

    #Sum Values and Add to Data List
    for i in range(num_cells_lat):
        tmp_lat = round((tmp_lat + jumps_lat),2)
        lats.append(tmp_lat)
        
    for i in range(num_cells_lon):
        tmp_lon = round((tmp_lon + jumps_lon),2)
        lons.append(tmp_lon)
        
    #Read Lists and Append Coordinates Combinations for df
    data = []
    count = 0
    
    for i in range(num_cells_lat):
        for j in range(num_cells_lon):
            data.append([count, lats[i], lons[j], lats[i+1], lons[j+1], i, j]) 
            count += 1
    
    #Create DF and Return Result
    columns = ['cell_id', 'min_lat', 'min_lon', 'max_lat', 'max_lon', 'line', 'column']
    result_df = pd.DataFrame(data,columns=columns)
    result_df['matrix_id'] = code
    result_df.to_csv(f'{output_route}/matrix_{num_cells_lat}x{num_cells_lon}_{code}.csv', index=False, sep = ';', decimal = ',')
    return result_df
