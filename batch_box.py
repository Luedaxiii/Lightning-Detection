import numpy as np
import xarray
from pyltg.core.lis import LIS
from matplotlib import pyplot as plt
import cv2
import os
import glob

# Define directories for images and labels
bg_dir = r"C:\Users\jbull\OneDrive - Fayetteville State University\CSC490 SENIOR PROJECT\BG\TRMM"
images_output_dir = r"C:\Users\jbull\OneDrive - Fayetteville State University\CSC490 SENIOR PROJECT\train_images2"
labels_output_dir = r"C:\Users\jbull\OneDrive - Fayetteville State University\CSC490 SENIOR PROJECT\train_labels2"

# Create train and validation directories
os.makedirs(os.path.join(images_output_dir, "train"), exist_ok=True)
os.makedirs(os.path.join(labels_output_dir, "train"), exist_ok=True)

def process_file(sc_filepath, bg_filepath):
    # Load LIS data from SC file
    data = LIS(sc_filepath)
    print(f"Processing {sc_filepath}")
    print(len(data.flashes.id), 'flashes in file')
    print(len(data.groups.id), 'groups in file')
    print(len(data.events.id), 'events in file')

    # Load background data from BG file
    BG = xarray.open_dataset(bg_filepath)
   
    # Generate filename for output
    sc_filename = os.path.basename(sc_filepath)
    filename = '.'.join(sc_filename.split('.')[:5])

    # Sort flash times
    times = sorted(data.flashes.time)

    # Loop through flashes chronologically
    for t in times:
        # Index flash
        f = np.where(data.flashes.time == t)[0]
       
        # Convert flash and BG times to datetime64[ns] explicitly
        flash_time_ms = np.datetime64(data.flashes.time[f][0], 'ns')
        bg_time_ms = BG.bg_data_summary_TAI93_time.astype("datetime64[ns]")

        # Calculate time delta in milliseconds
        dt = (flash_time_ms - bg_time_ms).astype('timedelta64[ms]')
       
        # Find index of the closest BG time less than or equal to flash time
        ibg_candidates = np.where(dt.data > np.timedelta64(0, 'ms'))[0]
       
        if len(ibg_candidates) > 0:
            ibg = ibg_candidates[-1]
        else:
            print(f"No suitable BG entry found for flash time {t}")
            continue

        # Check for the next BG image after the flash time for interpolation
        next_ibg_candidates = np.where(dt.data < np.timedelta64(0, 'ms'))[0]
        if len(next_ibg_candidates) > 0:
            ibg_next = next_ibg_candidates[0]
            print(f"Using images {ibg} and {ibg_next} for interpolation.")
           
            # Convert images to float32 before interpolation
            bg_data_1 = BG.bg_data[ibg].data.astype(np.float32)
            bg_data_2 = BG.bg_data[ibg_next].data.astype(np.float32)
           
            # Calculate interpolation weight
            delta_t = (bg_time_ms[ibg_next] - bg_time_ms[ibg]).astype('timedelta64[ms]').astype(float).item()
            weight = ((flash_time_ms - bg_time_ms[ibg]).astype('timedelta64[ms]').astype(float).item()) / delta_t

            # Perform interpolation using addWeighted
            interpolated_bg = cv2.addWeighted(bg_data_1, 1 - weight, bg_data_2, weight, 0)
        else:
            # Use the closest BG if no next image is found
            interpolated_bg = BG.bg_data[ibg].data.astype(np.float32)

        # Normalize and scale the interpolated background image to 0-255 range
        interpolated_bg = cv2.normalize(interpolated_bg, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

        # Get image dimensions for bounding box calculations
        img_height, img_width = interpolated_bg.shape

        # Select the first flash ID for comparison
        flash_id = data.flashes.id[f][0]

        # Index all groups in flash using a single flash ID
        gids = np.where(data.groups.parent_id == flash_id)[0]

        # Index all events in flash
        eids = np.zeros([0], dtype=np.int16)
        for g in gids:
            ie = np.where(data.events.parent_id == data.groups.id[g])[0]
            eids = np.concatenate((eids, ie), dtype=np.int16)

        # Get event coordinates with sub-pixel precision
        ex = data.events.px[eids].astype(np.float32)
        ey = data.events.py[eids].astype(np.float32)

        # Calculate precise bounding box coordinates with boundary checks
        x_min = max(ex.min(), 0)  # Clamp to 0 if negative
        y_min = max(ey.min(), 0)  # Clamp to 0 if negative
        x_max = min(ex.max(), img_width)  # Clamp to image width if exceeding bounds
        y_max = min(ey.max(), img_height)  # Clamp to image height if exceeding bounds

        # Draw a red bounding box on the image
        top_left = (int(x_min), int(y_min))
        bottom_right = (int(x_max), int(y_max))
        annotated_image = cv2.cvtColor(interpolated_bg, cv2.COLOR_GRAY2BGR)  # Convert to BGR for colored bounding box
        cv2.rectangle(annotated_image, top_left, bottom_right, (0, 0, 255), 2)  # Red color in BGR (0, 0, 255)

        # Convert bounding box to YOLO format with normalization
        x_center = ((x_min + x_max) / 2) / img_width
        y_center = ((y_min + y_max) / 2) / img_height
        width = (x_max - x_min) / img_width
        height = (y_max - y_min) / img_height

        # Ensure valid positive values for YOLO format
        if width > 0 and height > 0:
            # Save bounding box in YOLO format with high precision
            yolo_label_filename = os.path.join(labels_output_dir, "train", f"{filename}_flash_{flash_id:04}.txt")
            with open(yolo_label_filename, 'w') as label_file:
                label_file.write(f"0 {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")  # Class ID is assumed to be 0

            # Save the annotated background image for YOLO training
            output_image_path = os.path.join(images_output_dir, "train", f"{filename}_flash_{flash_id:04}.png")
            cv2.imwrite(output_image_path, annotated_image)
            print(f"Saved image with bounding box and YOLO label for flash ID {flash_id}")

def main():
    # Get list of all .nc files in the BG directory
    all_files = glob.glob(os.path.join(bg_dir, "*.nc"))
   
    # Separate SC and BG files based on their naming
    sc_files = [f for f in all_files if "SC" in os.path.basename(f)]
    bg_files = {os.path.basename(f).replace("BG", "SC"): f for f in all_files if "BG" in os.path.basename(f)}
   
    # Process each SC file with the corresponding BG file
    for sc_file in sc_files:
        sc_filename = os.path.basename(sc_file)
        bg_file = bg_files.get(sc_filename)
       
        if bg_file:
            print(f"Processing pair: {sc_file} and {bg_file}")
            process_file(sc_file, bg_file)
        else:
            print(f"No corresponding BG file found for SC file: {sc_file}")

if __name__ == "__main__":
    main()

