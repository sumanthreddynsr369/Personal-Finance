import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Set the title of the dashboards
st.title("Personal Finance Dashboard")

# Sidebar for user input
st.sidebar.header("Input Your Expenses")

# Function to add user expense input
def get_user_input():
    categories = ['Rent', 'Groceries', 'Entertainment', 'Utilities', 'Transport', 'Miscellaneous']
    expenses = {category: st.sidebar.number_input(f'Enter {category} expense', min_value=0, value=0) for category in categories}
    return expenses

# Get user input
user_expenses = get_user_input()

# Show the user's input as a DataFrame
expense_df = pd.DataFrame(list(user_expenses.items()), columns=['Category', 'Amount'])
st.subheader("Your Expenses")
st.write(expense_df)

# Calculate total expenses
total_expense = sum(user_expenses.values())
st.subheader(f"Total Expenses: ${total_expense}")

# Visualize the expenses using a pie chart
st.subheader("Expenses Breakdown by Category")

fig, ax = plt.subplots()
ax.pie(expense_df['Amount'], labels=expense_df['Category'], autopct='%1.1f%%', startangle=90)
ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.
st.pyplot(fig)

# Save expenses data as a CSV file for download
st.subheader("Download Your Expense Data")
st.download_button(label="Download as CSV", data=expense_df.to_csv(index=False), file_name="expenses.csv")

