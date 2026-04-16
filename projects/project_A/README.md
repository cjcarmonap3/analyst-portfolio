# PROJECT A

## 📌 Overview
This project analyzes customer churn for a subscription-based service to identify key drivers and predict which customers are likely to leave.

---

## 🎯 Business Problem
Customer retention is critical for subscription businesses. The company is experiencing high churn rates and needs insights into:
- Why customers are leaving
- Which customers are at risk
- How to reduce churn

---

## 📊 Dataset
- Source: Kaggle (Telco Customer Churn dataset)
- Size: ~7,000 customers
- Features: demographics, account info, services, billing

---

## 🧠 Approach

### 1. Data Cleaning
- Handled missing values
- Converted categorical variables
- Standardized formats

### 2. Exploratory Data Analysis (EDA)
Key findings:
- Month-to-month contracts → highest churn
- Higher churn among customers with no tech support
- Early churn within first 6 months

### 3. Feature Engineering
- Tenure groups
- Service usage flags
- Contract type encoding

### 4. Modeling
- Logistic Regression
- Random Forest

**Best Model:** Random Forest  
- Accuracy: 82%  
- Recall (churn): 78%

---

## 📈 Key Insights
- Contract type is the strongest predictor of churn
- Customers without add-on services are more likely to leave
- Early engagement is critical for retention

---

## 💡 Recommendations
- Incentivize long-term contracts
- Promote bundled services
- Target at-risk customers within first 3 months

---

## 📂 Project Structure


---

## 📊 Visualizations
*(Insert charts here — churn by contract, tenure distribution, etc.)*

---

## 🚀 Next Steps
- Deploy model as API
- Build real-time churn dashboard
- A/B test retention strategies