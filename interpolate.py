import os
import numpy as np
import xarray as xr
from pyltg.core.lis import LIS
from matplotlib import pyplot as plt

# Define paths
input_dir = r"C:\Users\jbull\OneDrive - Fayetteville State University\CSC490 SENIOR PROJECT\BG"
output_dir = r"C:\Users\jbull\OneDrive - Fayetteville State University\CSC490 SENIOR PROJECT\BG\output6"

# Function to process a pair of SC and BG files
def process_files(sc_filepath, bg_filepath):
    try:
        # Load SC and BG data files
        sc_data = LIS(sc_filepath)
        bg_data = xr.open_dataset(bg_filepath)

        print(f"Processing {sc_filepath}")
        print(f"{len(sc_data.flashes.id)} flashes in file")
        print(f"{len(sc_data.groups.id)} groups in file")
        print(f"{len(sc_data.events.id)} events in file")

        # Sort flash times for chronological processing
        flash_times = sorted(sc_data.flashes.time)

        # Process each flash
        for flash_time in flash_times:
            # Index for the current flash
            f = np.where(sc_data.flashes.time == flash_time)[0][0]
            
            # Compute time delta with BG data times
            flash_time_ns = flash_time.astype('datetime64[ns]')
            bg_time_ns = bg_data.bg_data_summary_TAI93_time.astype('datetime64[ns]')
            
            # Calculate time deltas and handle scalar cases
            time_deltas = np.abs((bg_time_ns - flash_time_ns).astype('timedelta64[ms]'))
            
            if time_deltas.size == 1:
                print("Only one background time available, using it directly.")
                closest_bg_idx = 0
            else:
                closest_bg_idx = np.argmin(time_deltas.data)
            
            # Debug information
            print(f"Flash time: {flash_time}, Closest BG index: {closest_bg_idx}, Delta: {time_deltas[closest_bg_idx]} ms")
            
            # Index groups and events related to the flash
            group_ids = np.where(sc_data.groups.parent_id == sc_data.flashes.id[f])[0]
            event_ids = np.hstack([np.where(sc_data.events.parent_id == sc_data.groups.id[g])[0] for g in group_ids])
            
            # Extract event positions
            event_x = sc_data.events.px[event_ids]
            event_y = sc_data.events.py[event_ids]

            # Generate and save figure
            plt.figure(figsize=(6, 6))
            plt.imshow(bg_data.bg_data[closest_bg_idx].data, cmap='gray')
            plt.plot(event_x, event_y, '.r', markersize=1)
            
            # Titles and labels
            title = (
                f"bg {closest_bg_idx}: {bg_data.bg_data_summary_TAI93_time.data[closest_bg_idx]}\n"
                f"flash {sc_data.flashes.id[f][0]}: {flash_time}\n"
                f"timedelta: {time_deltas[closest_bg_idx]} milliseconds\n"
                f"{len(event_ids)} events in flash"
            )
            plt.title(title)
            plt.xlabel('x')
            plt.ylabel('y')
            
            # Save figure
            output_filename = os.path.join(
                output_dir,
                f"{os.path.basename(sc_filepath).split('.')[0]}_bg_{closest_bg_idx:04}_flash_{sc_data.flashes.id[f][0]:04}.png"
            )
            plt.savefig(output_filename)
            plt.close()
            print(f"Saved {output_filename}")

    except Exception as e:
        print(f"Error processing {sc_filepath} and {bg_filepath}: {e}")

# Main function to process all file pairs in the directory
def main():
    # Get SC and BG files
    sc_files = sorted([f for f in os.listdir(input_dir) if f.startswith("TRMM_LIS_SC") and f.endswith(".nc")])
    bg_files = sorted([f for f in os.listdir(input_dir) if f.startswith("TRMM_LIS_BG") and f.endswith(".nc")])

    # Pair SC and BG files by matching date and time in the filenames
    for sc_file, bg_file in zip(sc_files, bg_files):
        sc_filepath = os.path.join(input_dir, sc_file)
        bg_filepath = os.path.join(input_dir, bg_file)
        print(f"Processing pair: {sc_filepath} and {bg_filepath}")
        process_files(sc_filepath, bg_filepath)

if __name__ == "__main__":
    main()




