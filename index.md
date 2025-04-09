# Garmin Fitness Data Analysis

This project explores trends and insights from my personal Garmin fitness tracker data over the year of 2024. The goal is to better understand patterns in my activity, health, and wellness using data analysis and visualizations.

---

## Introduction

Wearable tech generates massive amounts of data, but it often goes unused. In this project, I analyze my exported Garmin data to explore monthly trends in activity levels, sleep, calories burned, and more. By visualizing this data, I aim to uncover personal behavioral patterns and create a replicable template for others interested in doing the same.

---

## Methodology

### Tools Used

- **Python**
- `pandas`, `matplotlib`, `seaborn` for data wrangling and visualization

### Data Source

- Exported from Garmin Connect in CSV format
- Data categories included:
  - **Activities** (type and count)
  - **Calories** (active + resting)
  - **Floors Climbed**
  - **Intensity Minutes**
  - **Heart Rate** (average, max)
  - **Sleep Patterns**
  - **Stress Levels**

### Cleaning Process

- Standardized all date columns to `Month YYYY`
- Aggregated data by month
- Removed missing values and non-numeric fields
- Calculated summary statistics and correlations

---

## 📊 Key Visualizations

### Monthly Activity Trends
![Activity Trends](activity_by_month.png)

### Intensity Minutes vs. Calories Burned
![Calories vs Intensity](calories_vs_intensity.png)

### Resting Heart Rate vs. Stress
![RHR vs Stress](resting_heart_rate_vs_stress.png)

### Monthly Sleep Duration
![Sleep Duration](monthly_sleep_minutes.png)

### Stress Levels by Month
![Monthly Stress](monthly_stress_average.png)

---

## Key Results & Insights

### Activity Analysis
- **Most Active Month:** September  
- **Least Active Month:** March  
- Activity levels were strongly influenced by season, peaking in summer and dipping in winter.
- September had the highest step counts, floors climbed, and intensity minutes.

### Heart Rate & Recovery
- **Strong correlation (0.73)** between average heart rate and training intensity.
- Resting heart rate (RHR) increased during intense training months (e.g., September).
- **Lowest RHR:** November, likely a natural recovery phase.

### Calories & Movement
- **Peak Calorie Burn:** September 2024  
- **Strong correlation (0.89)** between intensity minutes and total calories burned.
- **Floors climbed** had a better correlation with calorie burn (0.74) than total steps.

### Sleep Patterns
- **Average sleep duration:** ~507 minutes (~8 hrs 27 min)
- June had the highest average sleep, while August was the lowest.
- Minimal correlation between activity and sleep duration (~0.037).

### Stress Insights
- **Highest Stress Month:** October  
- **Lowest Stress Month:** September  
- Weak link between activity and reduced stress, but **moderate negative correlation (-0.43)** between stress and resting heart rate—suggesting cardiovascular fitness may help reduce stress.

---

## ✅ Conclusion

This Garmin analysis revealed clear seasonal trends, strong fitness levels, and the relationship between intense training, recovery, and stress. The patterns uncovered here are not only useful for personal reflection but also demonstrate how wearable data can guide health decisions.

All analysis was done in Python using open-source tools and is fully reproducible.

---

