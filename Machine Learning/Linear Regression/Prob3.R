setwd("~/Documents/Grad School/Machine Learning/HW1/data_csv")

#Reading in data to data frame
cars <- data.frame(scan("legend.txt", what="", sep="\n"))
y <- read.table("y.txt", sep = ",", col.names = "miles per gallon")
x <- read.table("X.txt", sep = ",", col.names = c("intercept", "number of cylinders", "displacement", "horsepower", "weight", "acceleration", "model year"))
data <- data.frame(y, x)

#Dividing data to training and testing
indexes = sample(1:nrow(data), size = 20)
test = data[indexes,]
training = data[-indexes,]

#Part 1a (solving least squares)
trainingmatrix <- data.matrix(training)
w <- solve(t(trainingmatrix[,2:ncol(trainingmatrix)]) %*% trainingmatrix[,2:ncol(trainingmatrix)]) %*% t(trainingmatrix[,2:ncol(trainingmatrix)]) %*% trainingmatrix[,1]
colnames(w) <- "Coefficients"
w
pred <- rowSums(mapply("*",test[2:ncol(test)],w))

#Solving least squares using built in function is below but not used
#reg <- lm(miles.per.gallon ~ ., data = training[,-c(2)])
#coef(reg)
#w <- coef(reg)
#pred <- rowSums(t(t(test[2:8])*w))


#Looping through 1000 experiments for each value of p
RMSE_table <- matrix(,nrow=4,ncol=2)
loglik_table <- matrix(,nrow=4,ncol=1)
par(mfrow=c(2,2))
for (p in 1:4){
  MAE <- 0
  RMSE <- 0
  diff <- 0
  for (i in 1:1000){
    indexes1 <- sample(1:nrow(data), size = 20)
    test1 <- data[indexes1,]
    training1 <- data[-indexes1,]
    if(p > 1){
      test1 <- data.frame(test1,data.frame((test1[3:8])^2))
      training1 <- data.frame(training1,data.frame((training1[3:8])^2))
    }
    if(p > 2){
      test1 <- data.frame(test1,data.frame((test1[3:8])^3))
      training1 <- data.frame(training1,data.frame((training1[3:8])^3))
    }
    if(p > 3){
      test1 <- data.frame(test1,data.frame((test1[3:8])^4))
      training1 <- data.frame(training1,data.frame((training1[3:8])^4))
    }
    #reg1 <- lm(miles.per.gallon ~ ., data = training1[,-c(2)])
    #w1 <- coef(reg1)
    #pred1 <- rowSums(t(t(test1[2:ncol(test1)])*w1))
    trainingmatrix1 <- data.matrix(training1)
    w1 <- solve(t(trainingmatrix1[,2:ncol(trainingmatrix1)]) %*% trainingmatrix1[,2:ncol(trainingmatrix1)]) %*% t(trainingmatrix1[,2:ncol(trainingmatrix1)]) %*% trainingmatrix1[,1]
    pred1 <- rowSums(mapply("*",test1[2:ncol(test1)],w1))
    if(p == 1){
      MAE[i] <- sum(abs(pred1-test1[1]))/20
    }
    RMSE[i] <- sqrt(sum((pred1-test1[1])^2)/20)
    diff[i] <- test1[1]-pred1
  }
  if(p == 1){
#Part 1b
    cat("Mean MAE for p = ", p, "is: ", mean(MAE))
    cat("\nSt. Dev. MAE for p = ", p, "is: ", sd(MAE))
  }
#Part 2a
  cat("\nMean RMSE for p = ", p, "is: ", mean(RMSE))
  RMSE_table[p,1] <- mean(RMSE)
  cat("\nSt. Dev. RMSE for p = ", p, "is: ", sd(RMSE))
  RMSE_table[p,2] <- sd(RMSE)
#Part 2b
  title = paste("Histogram of errors for p = ", p)
  hist(unlist(diff), xlab = "Error", main = title, xlim = c(-10,10), ylim = c(0,4000), breaks = 20)
#Part 2c
  meanmle <- sum(unlist(diff))/length(unlist(diff))
  sdmle <- (sum(unlist(diff)^2)/length(unlist(diff)))^.5
  #gauss <- dnorm(unlist(diff), mean = meanmle, sd = sdmle, log = TRUE)
  gauss <- log((1/((2*pi)^.5*sdmle))*exp(-(unlist(diff)-meanmle)^2/(2*sdmle^2)))
  cat("\nLog-Likelihood for p = ", p, " is: ", sum(gauss))
  loglik_table[p,1] <- sum(gauss)
}

#Part 2a cont'd
RMSE_table <- data.frame(RMSE_table)
colnames(RMSE_table) <- c("Mean RMSE", "St. Dev. RMSE")
rownames(RMSE_table) <- c("p = 1", "p = 2", "p = 3", "p = 4")
RMSE_table

#Part 2c cont'd
loglik_table <- data.frame(loglik_table)
colnames(loglik_table) <- "Log-Likelihood"
rownames(loglik_table) <- c("p = 1", "p = 2", "p = 3", "p = 4")
loglik_table
