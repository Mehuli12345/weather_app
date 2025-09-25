# weather_pipeline.py
import pandas as pd
import numpy as np
from scipy import stats
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# -----------------------------
# 1️⃣ Load Dataset
# -----------------------------
df = pd.read_csv("GlobalWeatherRepository.csv")
print("Dataset loaded. First 5 rows:")
print(df.head())
print("\nDataset info:")
print(df.info())

# -----------------------------
# 2️⃣ Preprocessing
# -----------------------------
# Convert date column to datetime if exists
if 'lastupdated' in df.columns:
    df['lastupdated'] = pd.to_datetime(df['lastupdated'], errors='coerce')

# Handle missing values
df.fillna(method='ffill', inplace=True)
df.fillna(method='bfill', inplace=True)

# Remove outliers using Z-score for numeric columns
numeric_cols = df.select_dtypes(include=[np.number]).columns
df = df[(np.abs(stats.zscore(df[numeric_cols])) < 3).all(axis=1)]

# Normalize numeric features
scaler = MinMaxScaler()
df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

# Save cleaned dataset
cleaned_csv = "GlobalWeatherRepository_cleaned.csv"
df.to_csv(cleaned_csv, index=False)
print(f"\nData preprocessing complete. Cleaned data saved as {cleaned_csv}")

# -----------------------------
# 3️⃣ Exploratory Data Analysis (EDA)
# -----------------------------
# Correlation heatmap
plt.figure(figsize=(10,8))
sns.heatmap(df.corr(), annot=True, cmap='coolwarm')
plt.title("Feature Correlation")
plt.savefig("correlation_heatmap.png")
plt.show()

# Temperature trend over time if lastupdated exists
if 'lastupdated' in df.columns and 'temperature' in df.columns:
    plt.figure(figsize=(12,6))
    sns.lineplot(x='lastupdated', y='temperature', data=df)
    plt.title("Temperature Trend Over Time")
    plt.savefig("temperature_trend.png")
    plt.show()

# Distribution plots of numeric features
plt.figure(figsize=(15,10))
df[numeric_cols].hist(bins=15)
plt.tight_layout()
plt.savefig("feature_distributions.png")
plt.show()

# -----------------------------
# 4️⃣ Prepare ML Features
# -----------------------------
# Automatically select numeric columns except target
target_column = 'temperature'  # change target column if needed
feature_cols = [col for col in numeric_cols if col != target_column]
X = df[feature_cols]
y = df[target_column]

print("\nFeature sample:")
print(X.head())
print("\nTarget sample:")
print(y.head())


X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Save split data
X_train.to_csv("X_train.csv", index=False)
X_test.to_csv("X_test.csv", index=False)
y_train.to_csv("y_train.csv", index=False)
y_test.to_csv("y_test.csv", index=False)

print("\nTrain-test split complete. Saved as X_train.csv, X_test.csv, y_train.csv, y_test.csv")
print("\nPipeline complete! ✅ Cleaned data + plots + ML-ready splits are ready.")
