# An Ensemble-Based Machine Learning Model for the Early Detection of Diabetic Retinopathy

## About
This project focuses on the early detection and classification of Diabetic Retinopathy using an ensemble-based machine learning approach. It utilizes the VGG16 and ResNet50 base models to build a strong foundation for detecting retinopathy cases
## Features
- Early detection of Diabetic Retinopathy
- Classification of retinopathy severity levels
- Utilizes VGG16 and ResNet50 base models
- Ensemble method: Bagging
## Data Source
The retinal images used for training and evaluation in this project were obtained from the following sources:

- **Messidor Dataset:** The Messidor dataset provides retinal images for the detection of various eye diseases, including Diabetic Retinopathy. You can find more information about the dataset [here](https://www.adcis.net/en/third-party/messidor/).

- **Kaggle Dataset:** Kaggle is a popular platform for machine learning competitions and datasets. The specific Kaggle dataset used for this project can be found [here](https://www.kaggle.com/datasets/tanlikesmath/diabetic-retinopathy-resized).
 
# Models
## VGG16 Base Model
The VGG16 model is used as a base model for detecting retinopathy features. Refer to ENSEMBLE_VGG16_MAIN.ipynb for detailed implementation and usage.

## ResNet50 Base Model
The ResNet50 model is utilized to capture intricate features of retinal images. Refer to ENSEMBLE_RESNET50.ipynb for detailed implementation and usage.

## Ensemble Method
This project employs the Bagging ensemble method, combining predictions from multiple base models to improve the overall accuracy and robustness of the Diabetic Retinopathy detection and classification.
