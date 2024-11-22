import os
import shutil
import random

# Define paths
image_path = r"C:\Users\jbull\OneDrive - Fayetteville State University\CSC490 SENIOR PROJECT\train_images2\train"
label_path = r"C:\Users\jbull\OneDrive - Fayetteville State University\CSC490 SENIOR PROJECT\train_labels2\train"

# Define destination paths
output_path = r"C:\Users\jbull\OneDrive - Fayetteville State University\CSC490 SENIOR PROJECT\dataset2"
train_images_path = os.path.join(output_path, "images", "train")
val_images_path = os.path.join(output_path, "images", "val")
train_labels_path = os.path.join(output_path, "labels", "train")
val_labels_path = os.path.join(output_path, "labels", "val")

# Create directories if they don't exist
os.makedirs(train_images_path, exist_ok=True)
os.makedirs(val_images_path, exist_ok=True)
os.makedirs(train_labels_path, exist_ok=True)
os.makedirs(val_labels_path, exist_ok=True)

# Split ratio for training and validation
train_split_ratio = 0.8  # 80% for training, 20% for validation

# List all image files
images = [f for f in os.listdir(image_path) if f.endswith(('.png', '.jpg', '.jpeg'))]

# Shuffle images randomly
random.shuffle(images)

# Split data into training and validation
train_size = int(len(images) * train_split_ratio)
train_images = images[:train_size]
val_images = images[train_size:]

# Function to copy files
def copy_files(image_files, src_image_path, src_label_path, dest_image_path, dest_label_path):
    for image in image_files:
        # Define corresponding label file
        label = os.path.splitext(image)[0] + ".txt"

        # Paths for source and destination
        src_image = os.path.join(src_image_path, image)
        src_label = os.path.join(src_label_path, label)
        dest_image = os.path.join(dest_image_path, image)
        dest_label = os.path.join(dest_label_path, label)

        # Copy files if label exists
        if os.path.exists(src_label):
            shutil.copy(src_image, dest_image)
            shutil.copy(src_label, dest_label)
        else:
            print(f"Warning: Label file for {image} not found, skipping.")

# Copy files to training and validation directories
copy_files(train_images, image_path, label_path, train_images_path, train_labels_path)
copy_files(val_images, image_path, label_path, val_images_path, val_labels_path)

print("Dataset setup complete!")
