from utils import create_country_matrix
from utils import tools

def main(country_name: str, outputs_route: str, num_cells_lat: int, num_cells_lon: int):
    #Delete Previous Output Files
    tools.remove_files_from_folder(outputs_route)
    
    #Run Matrix from Country Creation and plot results
    main_matrix, vertical_matrix, horizontal_matrix = create_country_matrix.matrix_boundary(country_name, outputs_route, num_cells_lat, num_cells_lon)
    tools.plot_matrix([main_matrix, vertical_matrix, horizontal_matrix], country_name, 'country')


if __name__ == "__main__":
    #Define Inital Variables
    outputs_route = './outputs/matrix_csv/country'
    num_cells_lat = 30
    num_cells_lon = 30
    country_name = 'china'

    #Run Code
    main(country_name, outputs_route, num_cells_lat, num_cells_lon)

    