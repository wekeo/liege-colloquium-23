# Machine Learning Regression for Ocean Parameters retrieval

Regression approaches for ocean parameter retrievals.

This repository contains the code used in the paper: Ana B Ruescas, Gonzalo Mateo-Garcia, Gustau Camps-Valls, Martin Hieronymi. Retrieval of case 2 water quality parameters with machine learning. IGARSS 2018-2018 IEEE International Geoscience and Remote Sensing Symposium

The repository contains:
* Notebook "1. Load_and_visualize_data.ipynb" that reads the dataset and performs the training of the models (15 KB)
* Notebook "2. Statistics_analysis.ipynb" that analyses the results of the models using metrics and plots to understand the accuracy and uncertainties (391 KB)
* Notebook "3. WQ_predict_image.ipynb" that applies the models to OLCI L2 images, focused on the C2RCC products (198 KB)

Scripts: the folder "ml" contains helper functions (64 KB)
1. "data_load_S3.py" loads the data set for training and testing
2. "models.py" 
3. "ml_regression.py" train and save the proposed models with the different combination of bands
4. "c2_processing.py" loads a Sentinel-3 image and apply a trained model to the data
5. "Py4R_plots.py" with function for plotting

OLCI images are stored in the folder Support_data folder
