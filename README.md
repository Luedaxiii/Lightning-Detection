# Lightning-Detection

A Python-based project for detecting and analyzing lightning events using satellite data and machine learning techniques.

## Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Technologies Used](#technologies-used)
6. [Contributing](#contributing)
7. [License](#license)
8. [Acknowledgements](#acknowledgements)

## Introduction

The Lightning-Detection project aims to identify and analyze lightning events by processing satellite data. Utilizing machine learning models, it provides insights into lightning patterns, contributing to improved weather forecasting and environmental research.

## Features

- **Lightning Detection Model**: Predicts lightning strikes with a current accuracy of 51%, with ongoing improvements.
- **Data Correlation**: Associates satellite imagery with lightning events to construct bounding boxes.
- **Visualization Tools**: Offers interactive plots and maps for data exploration.

## Installation

To set up the project locally:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Luedaxiii/Lightning-Detection.git
   ```

2. **Navigate to the project directory**:
   ```bash
   cd Lightning-Detection
   ```

3. **Install dependencies**:
   - **Python Packages**: Use `pip` to install the required packages:
     ```bash
     pip install -r requirements.txt
     ```
   - **CUDA Toolkit**: Ensure that the CUDA Toolkit is installed for GPU acceleration. Refer to the [CUDA Toolkit Documentation](https://docs.nvidia.com/cuda/) for installation instructions.

## Usage

### 1. Prepare the Dataset
- Place your `.nc` dataset files in the `data/` folder.
- Ensure the data files are named appropriately to be referenced by the analysis scripts.

### 2. Running the Analysis
- To begin the analysis of the lightning dataset, use the following command:
  ```bash
  python run_analysis.py
  ```
  This script will read the dataset, process it, and generate the required outputs.

- During the analysis, the script performs data pre-processing, feature extraction, and lightning event detection using the pre-trained machine learning model.

### 3. Configuring Parameters
- You can modify parameters for the analysis by editing the `config.json` file located in the root directory.
  - **Model Parameters**: Adjust parameters such as batch size, epochs, or learning rate.
  - **Data Parameters**: Configure paths for input datasets or output directories.

  Example configuration change:
  ```json
  {
    "batch_size": 32,
    "learning_rate": 0.001,
    "epochs": 50,
    "data_path": "data/",
    "output_path": "results/"
  }
  ```

### 4. Viewing Results
- Once the analysis completes, the results are saved in the `results/` directory.
  - **Plots and Graphs**: The directory will contain plots showing the detected lightning strikes and relevant statistics.
  - **CSV Output**: A CSV file is generated with details of detected lightning events, including timestamps and locations.

- Use visualization tools to explore the data interactively:
  ```bash
  python visualize_results.py
  ```
  This command will open an interactive interface for exploring the generated plots and datasets.

### 5. Training a New Model (Optional)
- If you wish to train a new machine learning model, run:
  ```bash
  python train_model.py
  ```
  - Ensure that you have configured the training dataset paths and parameters in `config.json`.
  - The training script will create a new model based on the dataset and save it in the `models/` directory.

### 6. Running Unit Tests
- To verify that the installation and all components are functioning as expected, run the unit tests:
  ```bash
  python -m unittest discover tests
  ```
  This will run all the tests in the `tests/` directory to ensure the code behaves as intended.

## Technologies Used

- **Programming Language**: Python
- **Libraries**: NumPy, Pandas, TensorFlow, Matplotlib, NetCDF4, pyltg
- **Tools**: Microsoft Visio for ERDs, DBeaver for database management
- **CUDA Toolkit**: For GPU acceleration

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- **Advisor**: Dr. Bhattacharya for guidance throughout the project.
- **Team Members**: Joshua Bulluck, Demarche Hilliard, Lucinky Lucien.
- **Data Source**: [TRMM Satellite Data](https://trmm.gsfc.nasa.gov/).
