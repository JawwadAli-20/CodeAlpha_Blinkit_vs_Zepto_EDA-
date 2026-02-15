import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- STEP 1: LOADING DATA ---
# File ko load kar rahe hain analysis shuru karne ke liye
file_path = "Blinkit VS Zepto file.xlsx"
raw_data = pd.read_excel(file_path)

# --- STEP 2: DATA CLEANING & STRUCTURING ---
# Excel messy hai, isliye specific rows aur columns nikal rahe hain
# Blinkit Data (Category aur Sales)
blinkit_data = raw_data.iloc[2:14, [0, 1]].copy()
blinkit_data.columns = ['Category', 'Blinkit_Sales']

# Zepto Data
zepto_data = raw_data.iloc[4:14, [4, 5]].copy()
zepto_data.columns = ['Category', 'Zepto_Sales']

# Ratings Data (Customer engagement check karne ke liye)
ratings_info = raw_data.iloc[4:14, [7, 8]].copy()
ratings_info.columns = ['Category', 'Ratings_Count']

# Data types fix kar rahe hain taaki math calculations ho sakein
blinkit_data['Blinkit_Sales'] = pd.to_numeric(blinkit_data['Blinkit_Sales'], errors='coerce')
zepto_data['Zepto_Sales'] = pd.to_numeric(zepto_data['Zepto_Sales'], errors='coerce')
ratings_info['Ratings_Count'] = pd.to_numeric(ratings_info['Ratings_Count'], errors='coerce')

# --- STEP 3: MASTER TABLE CREATION ---
# Saare alag tables ko ek jagah merge kar rahe hain comparison ke liye
main_df = pd.merge(blinkit_data, zepto_data, on='Category', how='outer')
main_df = pd.merge(main_df, ratings_info, on='Category', how='outer')

# Cleaning final table: Remove Grand Total and fill empty values
analysis_df = main_df[main_df['Category'] != 'Grand Total'].fillna(0)

print("--- Final EDA Master Table ---")
print(analysis_df.head(10))

# --- STEP 4: VISUALIZATION (TRENDS & PATTERNS) ---
# Bar Chart: Comparing Sales Performance
plt.figure(figsize=(12, 6))
analysis_df.set_index('Category')[['Blinkit_Sales', 'Zepto_Sales']].plot(kind='bar', color=['#3498db', '#e67e22'])
plt.title('Sales Comparison: Blinkit vs Zepto', fontsize=14)
plt.ylabel('Sales Amount')
plt.xticks(rotation=45)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.show()

# --- STEP 5: HYPOTHESIS TESTING (SALES VS RATINGS) ---
# Scatter plot dekhne ke liye ki kya zyada sales matlab zyada ratings?
plt.figure(figsize=(10, 5))
sns.regplot(data=analysis_df, x='Blinkit_Sales', y='Ratings_Count', color='blue', label='Blinkit Trend')
plt.title('Validation: Does Sales Volume Affect Ratings?')
plt.legend()
plt.show()

# --- STEP 6: ANOMALY DETECTION (MARKET GAPS) ---
# Check kar rahe hain kaunse items sirf ek platform par milte hain
only_b = analysis_df[(analysis_df['Blinkit_Sales'] > 0) & (analysis_df['Zepto_Sales'] == 0)]['Category'].tolist()
only_z = analysis_df[(analysis_df['Zepto_Sales'] > 0) & (analysis_df['Blinkit_Sales'] == 0)]['Category'].tolist()

print("\n--- Market Anomalies Detected ---")
print(f"Items exclusive to Blinkit: {only_b}")
print(f"Items exclusive to Zepto: {only_z}")

# Final Correlation Matrix for the report
print("\n--- Correlation Results ---")
print(analysis_df[['Blinkit_Sales', 'Zepto_Sales', 'Ratings_Count']].corr())