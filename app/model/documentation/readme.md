## Improvement Points

- The "Property-Friends-basic-model" file could have a more intuitive name to facilitate typing and improve reproducibility.

- The initial model provided was functioning perfectly and as mentioned in the Challenge.md file:

  "After some experimentation, the Client is happy with the current results and wants to bring the model into a deployable solution."

  Thus, it would have been sufficient to leave the model with the initial results as shown in the image /images/initial_values.png.
  Despite the rmse not being good.

## Exploratory Analysis

Initially, my goal was to understand the training dataset.

In the initial dataset, the columns consisted of:

- type
- sector
- net_usable_area
- net_area
- n_rooms
- n_bathroom
- latitude
- longitude
- price

I conducted an initial exploration to identify any `missing values` in the dataset, and fortunately, no missing values were found.

To gain a better understanding of the dataset's format, I utilized functions such as `info()` and `describe()`. Additionally, I examined the shape and columns attributes.

For `univariate analysis`, I created histograms to visualize the distributions of the variables.

Moving on to `bivariate analysis`, I plotted categorical variables and generated scatter plots to explore the relationships between price and net_area, as well as price and net_usable_area. I was particularly interested in understanding the area-to-price ratio.

During this analysis, I discovered that there were only two types of properties: "department" or "house," and there were only five sectors: "vitacura," "la reina," "las condes," "lo barnechea," and "providencia." Further research revealed that these sectors are referred to as "communes" and exclusively represent the metropolitan region of Santiago, providing valuable geolocation insights.

For `multivariate analysis`, I created a correlation matrix to examine the relationships between variables. The initial correlation matrix revealed a strong correlation between the number of rooms and the number of bathrooms, as well as between latitude and longitude.

## Assumptions

File structure:

```plaintext
Bain [Folder]
└─ app [Folder]
   └─ model [Folder]
      └─ documentation [Folder]
         ├─ Challenge.md (File containing initial instructions)
         └─ readme.md (File containing instructions and analysis)
      └─ images [Folder] (Directory containing images comparing results based on different approaches)
      └─ learningFiles [Folder]
         ├─ test.csv
         ├─ train.csv
         └─ api.csv
      └─ Exploratory_Analysis.ipynb (Jupyter notebook for performing exploratory analysis)
      └─ modelApiEndPoint.py (Python file that serves as the endpoint for API requests)
      └─ Property-Friends-basic-model.ipynb (Template provided)
   Dockerfile (Dockerfile containing the Docker settings; we chose to use the default image)
   log_modelApiEndPoint.log (File containing logs for the API endpoint)
   log.log (File containing general logs)
   requirements.txt (File containing the Docker requirements to run the files)
```

## How to Run the Code?

1. The first step is to generate the Docker image. Execute the following command:

   ```bash
   docker build -t prediction-chile .
   ```

   Note: Don't forget the period at the end.

2. The second step is to create containers from the previously created image (`prediction-chile`). Use the following command:

   ```bash
   docker container run -p 80:80 prediction-chile
   ```

   We are using port 80.

3. To access the API, open your browser and type:

   http://localhost/ or http://0.0.0.0:80

4. In addition to the introduction provided on the main route, you can access the FASTAPI API documentation at:

   http://localhost/docs

5. Additionally, here are some useful Docker commands:
   - `docker container run containername`: Runs a container.
   - `docker container ls -a`: Lists all containers.
   - `docker container ls`: Lists only running containers.
   - `docker container rm id` or `containername`: Removes a container.
   - `docker ps`: Lists processes.

6. In the commercial software market, logs are important. Therefore, we have created two files:
   - `log_modelApiEndpoint.log`: Monitors API requests.
   - `log.log`: Contains all the logs.

## Error Handling

To handle errors, we use `try` blocks and specific methods such as `exception_handler` from FastAPI.

## API Points

We utilized FASTAPI, and the documentation can be found at http://localhost/docs.

## Results

- When using categorical variables as n-1 dummies, the model's performance improved. However, the root mean squared error (RMSE) remained high, as depicted in the image `/images/using_categorical_columns_as_dummies.png`.

- Incorporating feature engineering to analyze certain ratios improved the model, but the improvement was not significant, as shown in the image `/images/feature_eng_adding_ratio.png`.

- To further reduce the RMSE, we increased the learning_rate from 0.01 to 0.03 and the n_estimators to 2500, with a max_depth of 6. This adjustment led to longer processing times but within acceptable limits. The impact on prediction time was negligible for a single prediction, but it resulted in an RMSE with an acceptable outcome.

- The final result, as depicted in the image `/image/final_result.png`, shows an RMSE of 71 Chilean pesos.

## Acknowledgments

We would like to thank the client for their valuable feedback and collaboration throughout the project.