

WORKSPACE_NAME <- "ml-flow-test"
SUBSCRIPTION_ID <- "b242efdc-f14b-4f3e-a454-0377fa50302b"
RESOURCE_GROUP = "MLflow-analytics"
MODEL_NAME <- "housing_model_gertjan_test"
IMAGE_NAME <- "housing_model_gertjan_test-image"
EXPERIMENT_NAME <- "housing_model_gertjan_test_experiment"
MODEL_PATH <-"house_models_gertjan_path"



install.packages("mlflow")
install.packages("glmnet")
install.packages("carrier")
install.packages("Matrix")
install.packages("reticulate")
install.packages("azuremlsdk")

library(mlflow)
library(glmnet)
library(carrier)
library(data.table)
library(Matrix)
library(reticulate)
library(azuremlsdk)

mlflow::install_mlflow()
Sys.setenv("PATH" = paste(Sys.getenv("PATH"), "/anaconda3/bin", sep = .Platform$path.sep))

ws <- load_workspace_from_config()
mlflow_set_tracking_uri(ws)

experiment_name <- "MLflow_R_test0"
exp <- experiment(ws,experiment_name)




#load the data

setwd("/Users/Julie.Vranken/Desktop/Data Science/MLflow_Houses")
data <- read.csv("Train.csv")


#Clean the data

#data cleaning
data$LotFrontage[is.na(data$LotFrontage)] <- as.integer(0)
data$Alley = factor(data$Alley, levels=c(levels(data$Alley), "NoAlley"))
data$Alley[is.na(data$Alley)] <- "NoAlley"
data$FireplaceQu = factor(data$FireplaceQu, levels=c(levels(data$FireplaceQu), "NoFP"))
data$FireplaceQu[is.na(data$FireplaceQu)] <- "NoFP"
data$GarageType = factor(data$GarageType, levels=c(levels(data$GarageType), "NoGarage"))
data$GarageType[is.na(data$GarageType)] <- "NoGarage"
data$GarageYrBlt[is.na(data$GarageYrBlt)] <- as.integer(0)
data$GarageFinish = factor(data$GarageFinish, levels=c(levels(data$GarageFinish), "NoGarage"))
data$GarageFinish[is.na(data$GarageFinish)] <- "NoGarage"
data$GarageQual = factor(data$GarageQual, levels=c(levels(data$GarageQual), "NoGarage"))
data$GarageQual[is.na(data$GarageQual)] <- "NoGarage"
data$GarageCond = factor(data$GarageCond, levels=c(levels(data$GarageCond), "NoGarage"))
data$GarageCond[is.na(data$GarageCond)] <- "NoGarage"
data$PoolQC = factor(data$PoolQC, levels=c(levels(data$PoolQC), "NoPl"))
data$PoolQC[is.na(data$PoolQC)] <- "NoPl"
data$Fence = factor(data$Fence, levels=c(levels(data$Fence), "NoFnc"))
data$Fence[is.na(data$Fence)] <- "NoFnc"
data$MiscFeature = factor(data$MiscFeature, levels=c(levels(data$MiscFeature), "None"))
data$MiscFeature[is.na(data$MiscFeature)] <- "None"
data$Id <- NULL
data <- na.omit(data)

# Split the data into training and test sets. (0.75, 0.25) split.
sampled <- sample(1:nrow(data), 0.75 * nrow(data))
train <- data[sampled, ]
test <- data[-sampled, ]

labels(data)

# The predicted column is "SalePrice"
train_x <- train[, !(names(train) == "SalePrice")]
train_x <- model.matrix( ~ .,train_x)
test_x <- test[, !(names(train) == "SalePrice")]
test_x <- model.matrix( ~ .,test_x)
train_y <- train[, "SalePrice"]
test_y <- test[, "SalePrice"]

alpha <- mlflow_param("alpha", 0.5, "numeric")
lambda <- mlflow_param("lambda", 0.5, "numeric")


with(mlflow_start_run(), {
  
  model <- glmnet(train_x, train_y, alpha = alpha, lambda = lambda, family= "gaussian", standardize = FALSE)
  predictor <- crate(~ glmnet::predict.glmnet(!!model, as.matrix(.x)), !!model)
  predicted <- predictor(test_x)
  
  rmse <- sqrt(mean((predicted - test_y) ^ 2))
  mae <- mean(abs(predicted - test_y))
  r2 <- as.numeric(cor(predicted, test_y) ^ 2)
  
  message("Elasticnet model (alpha=", alpha, ", lambda=", lambda, "):")
  message("  RMSE: ", rmse)
  message("  MAE: ", mae)
  message("  R2: ", r2)
  
  mlflow_log_param("alpha", alpha)
  mlflow_log_param("lambda", lambda)
  mlflow_log_metric("rmse", rmse)
  mlflow_log_metric("r2", r2)
  mlflow_log_metric("mae", mae)
  mlflow_log_model(predictor, artifact_path ="model")
})




