import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import os

# Define the directory containing NetCDF files and the output directory for images
input_dir = r'C:/Users/jbull/OneDrive - Fayetteville State University/CSC490 SENIOR PROJECT/BG'
output_dir = r'C:/Users/jbull/OneDrive - Fayetteville State University/CSC490 SENIOR PROJECT/BG/output2'
os.makedirs(output_dir, exist_ok=True)

# Iterate over all .nc files in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith('.nc'):
        # Load the NetCDF file
        file_path = os.path.join(input_dir, filename)
        dataset = xr.open_dataset(file_path)

        # Check if 'lightning_flash_lat' and 'lightning_flash_lon' exist in the dataset
        if 'lightning_flash_lat' in dataset.variables and 'lightning_flash_lon' in dataset.variables:
            lightning_lats = dataset['lightning_flash_lat'].values
            lightning_lons = dataset['lightning_flash_lon'].values

            # Check if there's radiance or some other attribute to color the points
            if 'lightning_flash_radiance' in dataset.variables:
                lightning_radiance = dataset['lightning_flash_radiance'].values
            else:
                lightning_radiance = np.ones_like(lightning_lats)  # Default to 1 if radiance isn't available

            # Get the time variables for each lightning flash
            lightning_TAI93_time = dataset['lightning_flash_TAI93_time'].values
            lightning_delta_time = dataset['lightning_flash_delta_time'].values
            lightning_observe_time = dataset['lightning_flash_observe_time'].values

            # Dynamically set the map boundaries based on lat/lon
            lon_min, lon_max = lightning_lons.min(), lightning_lons.max()
            lat_min, lat_max = lightning_lats.min(), lightning_lats.max()

            # Add padding to the boundaries
            lon_padding = (lon_max - lon_min) * 0.1
            lat_padding = (lat_max - lat_min) * 0.1

            lon_min -= lon_padding
            lon_max += lon_padding
            lat_min -= lat_padding
            lat_max += lat_padding

            # Create a Basemap instance based on the dynamic boundaries
            mp = Basemap(projection='merc', llcrnrlon=lon_min, llcrnrlat=lat_min, urcrnrlon=lon_max, urcrnrlat=lat_max, resolution='i')

            # Loop through each lightning strike and plot them one by one
            for i in range(len(lightning_lats)):
                plt.figure(figsize=(8, 8))

                # Add color to the land and ocean to enhance visibility
                mp.drawmapboundary(fill_color='aqua')  # Ocean color
                mp.fillcontinents(color='brown', lake_color='aqua')  # Land and lake colors

                # Draw coastlines, countries, and states
                mp.drawcoastlines()
                mp.drawcountries()
                mp.drawstates()

                # Convert lat/lon to Basemap projection coordinates
                x, y = mp([lightning_lons[i]], [lightning_lats[i]])

                # Plot only one lightning flash at a time
                scatter = mp.scatter(x, y, marker='o', c=[lightning_radiance[i]], cmap='jet', zorder=5)

                # Add a color bar for the radiance
                cbar = plt.colorbar(scatter, orientation='vertical')
                cbar.set_label('Radiance (W/m^2)')

                # Format time for display in the plot title
                flash_time_str = f"TAI93 Time: {lightning_TAI93_time[i]}, Delta Time: {lightning_delta_time[i]}, Observation Time: {lightning_observe_time[i]}"
                
                # Add a title and labels
                plt.title(f"Lightning Flash {i+1} - {filename} \n{flash_time_str}")

                # Save the figure as an image
                output_image = os.path.join(output_dir, f'{os.path.splitext(filename)[0]}_lightning_flash_{i+1}.png')
                plt.savefig(output_image, dpi=300)
                plt.close()

        else:
            print(f"'lightning_flash_lat' or 'lightning_flash_lon' not found in {filename}")

        dataset.close()

print("All images have been created.")


