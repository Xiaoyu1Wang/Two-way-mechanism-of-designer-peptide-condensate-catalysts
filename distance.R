library(ggplot2)
library(tidyr)

names <- c("annealing_cubic_WGR2H@10_WGE2H@10_ION@15_box8_1",
           "annealing_cubic_WGR2H@3_WGE2H@3_ION@15_box8_1",
           "annealing_cubic_WGR2H@20_ION@15_box8_1",
           "annealing_cubic_WGR2H@6_ION@15_box8_1")

labels <- c("R2H 10 + E2H 10", "R2H 3 + E2H 3", "R2H 20", "R2H 6")

result_df <- tibble()

for (name in names) {
  csvpath <- sprintf("/mnt/sto1/yyq/2023.LLPS/md_amber/analysis/CA_dis/data/%s.csv", name)
  
  # 步骤 2: 读取 CSV 文件
  df <- read_csv(csvpath, col_names = FALSE)
  colnames(df)[1] <- "frame"
  colnames(df)[2] <- "trjname"
  df <- df[df$frame > 100, ] %>%
    pivot_longer(cols = -c("frame", "trjname"))
  df$name <- name
  
  result_df <- rbind(result_df, df)
}
result_df$name <- factor(result_df$name, levels = names, labels = labels)

df <- result_df

ggplot(df, aes(x = value, fill = name)) +
  geom_density(alpha = 0.5) +
  labs(title = "Density Distribution of Distance between His's CA",
       x = "Distance",
       y = "Density") +
  scale_fill_manual(values = c("R2H 10 + E2H 10" = "red", "R2H 3 + E2H 3" = "blue", "R2H 20" = "green", "R2H 6" = "purple")) +
  theme_minimal()

# 如果需要保存图形
ggsave("output_plot.png", dpi = 300)
