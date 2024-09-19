#test

data <- read.csv("~/Downloads/NFL Player Stats(1922 - 2022).csv")
dim(data)

new_data <- data %>%
  filter(Season > "1990")
dim(new_data)


library(httr)
library(rvest)

# Base URL
base_url <- "https://www.nfl.com/injuries/league/%d/reg%d"

# Function to scrape data for a given year and week
scrape_injuries <- function(year, week) {
  url <- sprintf(base_url, year, week)
  response <- GET(url)
  if (status_code(response) == 200) {
    page <- read_html(content(response, "text"))
    # Extract relevant data here
    # Example: print the page title
    title <- page %>% html_node("title") %>% html_text()
    page %>% html_table()
    cat(sprintf("Year: %d, Week: %d, Title: %s\n", year, week, title))
  } else {
    cat(sprintf("Failed to retrieve data for Year: %d, Week: %d\n", year, week))
  }
}

# Loop through years and weeks
for (year in 2013:2023) {  # Adjust the range as needed
  for (week in 1:3) {  # NFL regular season has 17 weeks
    scrape_injuries(year, week)
  }
}
