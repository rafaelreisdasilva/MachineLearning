# FGV/EAESP Principles of Machine Learning Evaluation

This repository contains the starter code that you should use to prepare and assemble the Machine Learning model for the Principles of Machine Learning evaluation at FGV/EAESP.

## Assignment Overview

The evaluation consists of multiple stages:

1. **Model Delivery and Oral Presentation** (100% of the partial exam grade) - You should present your understanding of the problem and propose a solution.
2. **Model Predictions Collection** (50% of the final exam grade) - Collect predictions from your models for some weeks in May 2023.
3. **Final Presentation** (50% of the final exam grade) - Present your final results and predictions for specific weeks in June 2023.

The assignment can be performed in groups of up to 3 students.

## Problem Description

The objective is to predict a target (based on net inflow - see section 4) using a machine learning algorithm. The idea is to train models with historical series of features (e.g., number of investors, inflows, outflows, etc.) to predict the z-score of net inflow in the subsequent week.

Refer to section 4 for details on how the target was calculated.

## Features and Data

The features have already been manipulated for ease of exercise execution and correspond to the weekly average values reported in the daily report. The index date (`DT_COMPTC`) corresponds to Friday, representing the week.

Two other dataframes contain data that can be used as features: `cadastro` and `laminas`. These dataframes contain a mix of numerical, categorical, and textual data.

## Scope of Analysis

The analysis will be limited to a subset of funds defined by the following selection criteria:

- Selection via the `informes` dataframe:
  - Funds with fund type ('TP_FUNDO') 'FI'
  - Funds created before June 1, 2021
  - Funds with the number of investors ('NR_COTST') greater than 100 on January 3, 2022
- Selection via the `cadastro` dataframe:
  - Funds with status ('SIT') other than 'CANCELADA'
  - Duplicate entries will be removed, and only the last entry will be considered
  - Funds whose class ('CLASSE') is 'Fundo Multimercado'

## Repository Structure

- `starter-code.ipynb`: Starter code for loading and manipulating dataframes, model creation, and prediction submission.
- `data/`: Directory for storing data files.
- `raw/`: Directory for storing raw data files.
- `models/`: Directory for storing trained model files.
- `predictions/`: Directory for storing prediction files.

## Instructions

1. Clone this repository to your local machine.
2. Open and execute the `starter-code.ipynb` notebook.
3. Follow the provided instructions to load data, manipulate dataframes, create and train your model, and generate predictions.
4. Store your trained models in the `models/` directory.
5. Submit your predictions in the specified format to the `predictions/` directory.

## Usage

Refer to the instructions provided in the `starter-code.ipynb` notebook for detailed usage guidelines.

## Evaluation

Your performance will be evaluated based on the accuracy of your predictions compared to the actual values for the specified weeks. Additionally, your understanding of the problem and the proposed solution will be assessed during the oral presentation.

## Additional Notes

- Lookback and selection of the date range for training are critical decisions that may affect performance.
- Pay attention to cross-validation in time series problems (i.e., temporal split, not random).
- Additional data sources may be used as features, such as the CDI rate.

## References

- [CVM Data Portal](https://dados.cvm.gov.br/)
- [CVM Data - Informe Diario](https://dados.cvm.gov.br/dados/FI/DOC/INF_DIARIO/DADOS/)

If you have any questions or need further assistance, feel free to reach out to the course instructors.

Best regards,
Rafael Reis
