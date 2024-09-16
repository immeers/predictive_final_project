#test

data <- read.csv("~/Downloads/NFL Player Stats(1922 - 2022).csv")
dim(data)

new_data <- data %>%
  filter(Season > "1990")
dim(new_data)