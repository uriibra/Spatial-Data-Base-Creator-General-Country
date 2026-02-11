from utils import create_rectangular_matrix
from utils import tools

def main(bounds: tuple[float, float, float, float], num_cells_lat: int, num_cells_lon: int, outputs_route: str) -> None:
    #Delete Previous Output Files
    tools.remove_files_from_folder(outputs_route)
    
    #Create Intial Matrix
    main_matrix = create_rectangular_matrix.create_matrix(bounds, num_cells_lat, num_cells_lon, 'main', outputs_route)

    #Create Shifted Matrix
    vertical_shift_matrix, horizontal_shift_matrix = create_rectangular_matrix.set_shifted_matrix(bounds, num_cells_lat, num_cells_lon, outputs_route)

    #Plot Results for Visualization
    tools.plot_matrix([main_matrix, vertical_shift_matrix, horizontal_shift_matrix], 'general', 'general')


if __name__ == "__main__":
    #Define Output folder Routes
    outputs_route = './outputs/matrix_csv/general'
       
    #Define Bounds
    min_lat = 18.1593
    min_lon = 73.5577
    max_lat = 53.56
    max_lon = 134.7739

    #Define Matrix variables
    num_cells_lat = 30
    num_cells_lon = 30
    bounds = (min_lat, min_lon, max_lat, max_lon)
    
    #Run Code
    main(bounds, num_cells_lat, num_cells_lon, outputs_route)