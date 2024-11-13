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

1. **Prepare the Dataset**:
   - Place your `.nc` dataset files in the `data/` folder.

2. **Run the Analysis**:
   ```bash
   python run_analysis.py
   ```

3. **Visualization**:
   - Access the results in the `results/` directory as images and plots.

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
