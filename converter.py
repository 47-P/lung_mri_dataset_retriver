import os
import pydicom
import cv2
import numpy as np


def convert_dcm_to_jpeg(dcm_path, jpeg_path):
    try:
        # Read the .dcm file
        dcm_data = pydicom.dcmread(dcm_path)
        
        # Extract the pixel array from the DICOM file
        pixel_array = dcm_data.pixel_array
        
        # Normalize the pixel values to the range [0, 255]
        pixel_array = ((pixel_array - pixel_array.min()) / (pixel_array.max() - pixel_array.min()) * 255).astype(np.uint8)
        
        # Save the image as JPEG
        cv2.imwrite(jpeg_path, pixel_array)
        print(f"Converted: {dcm_path} -> {jpeg_path}")
    except Exception as e:
        print(f"Failed to convert {dcm_path}: {e}")


def convert_all_dcm_to_jpeg(input_directory, output_directory):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    # Walk through all subdirectories and files in the input directory
    for root, _, files in os.walk(input_directory):
        for file in files:
            if file.lower().endswith(".dcm"):
                # Define the full path to the .dcm file
                dcm_path = os.path.join(root, file)
                
                # Define the corresponding path for the .jpeg file in the output directory
                relative_path = os.path.relpath(root, input_directory)
                jpeg_directory = os.path.join(output_directory, relative_path)
                if not os.path.exists(jpeg_directory):
                    os.makedirs(jpeg_directory)
                
                jpeg_path = os.path.join(jpeg_directory, f"{os.path.splitext(file)[0]}.jpeg")
                
                # Convert the .dcm file to .jpeg
                convert_dcm_to_jpeg(dcm_path, jpeg_path)


if __name__ == "__main__":
    import argparse

    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Convert DICOM (.dcm) files to JPEG (.jpeg) format.")
    parser.add_argument("input_directory", help="Path to the input directory containing .dcm files.")
    parser.add_argument("output_directory", help="Path to the output directory where .jpeg files will be saved.")
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Convert all DICOM files to JPEG
    convert_all_dcm_to_jpeg(args.input_directory, args.output_directory)
