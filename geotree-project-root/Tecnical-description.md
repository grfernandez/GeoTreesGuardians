# Project: GeoTrees Guardians - Tecnical Description


## Tecnical Description

This technical description will mention the logical and technical components that are used and those that are planned to be scaled in this project.

## 1.Infraestructure as Code



Technological Stack: 
    Terraform - Docker 

## 2.Data Flow



### 2.1 Data Lake

In the data lake, structured and unstructured data will be received and stored, such as data entered by users who georeference trees. This data includes coordinates, photos, and descriptions. Other types of data from other sources such as drones or satellites will be stored.

### 2.2 Exploratory Data Analysis 

In the Exploratory Dara Analysis sector, an exploratory analysis of the data stored in the data like is carried out with the aim of achieving greater understanding and rationality about the data.

### 2.3 Data Streaming 

Based on the results of the Exploratory Data Analysis, data flows are implemented in striping where data is extracted, transformed and loaded in the data clean.

### 2.4 Storage Data Clean
  #### 2.4.1 Data Feature
  #### 2.4.1 Data Tree New

### 2.6 Models ML


### 2.6.1 Dev and Training

Use of development and training environments that allow collaborative work, constant visualization, training run planning as well as traceability and versioning of training.

### 2.6.1 Validate
* Acurracy of models
* Detect Drift


### 2.7 Deployment Models

### 2.8 Loging and Monitoring

## 3.App

### 3.1 Collaborative repository
### 3.2 Local development
Developer:

    Writes or updates code and tests.
    Runs pytest locally to verify the code.


### 3.3 Deployment
Push to GitHub:

    Makes a commit and pushes the changes to the repository.
### 3.4 Automated CI Pipeline
GitHub Actions:

    Detects the new commit/pull request.
    Executes the workflow defined in .github/workflows/python-app.yml.
    Installs dependencies and runs pytest to execute the tests.
    Reports whether the tests passed or failed.

Results:

    If the tests pass, the code can be deployed automatically if configured that way.
    If the tests fail, the process stops and the developer receives feedback to correct the issue.

### 3.4 Loging and Monitoring

Logging: 

    Involves capturing detailed information about model execution, such as predictions, errors, metrics, and input/output data. This helps track and audit model behavior and diagnose issues.

Monitoring: 

    Involves tracking model performance over time in production. It includes metrics like latency, accuracy, data drift, and service availability, allowing detection of performance changes or issues like model degradation due to data drift.


