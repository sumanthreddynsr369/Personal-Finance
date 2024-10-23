import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Set the title of the dashboards
st.title("Retirement Calculator Dashboard")

# Sidebar for user input
st.sidebar.header("Input Your finances")

# Function to add user expense input
def get_user_input():
    categories = ['Current yearly expenses', 'Inflation', 'Current age', 'Retirement age', "Lump sum availabale at current age",'SIP expected returns']
    expenses = {category: st.sidebar.number_input(f'Enter {category}', min_value=0, value=0) for category in categories}
    return expenses

# Get user input
user_expenses = get_user_input()

# Show the user's input as a DataFrame
expense_df = pd.DataFrame(list(user_expenses.items()), columns=['Category', 'Amount'])
st.subheader("Your finances")
st.write(expense_df)

curr_age=expense_df.loc[expense_df['Category'] == 'Current age', 'Amount'].values[0]
ret_age=expense_df.loc[expense_df['Category'] == 'Retirement age', 'Amount'].values[0]
len_invest=int(ret_age-curr_age)#length of the investment 
curr_expense=expense_df.loc[expense_df['Category'] == 'Current yearly expenses', 'Amount'].values[0]
infl=expense_df.loc[expense_df['Category'] == 'Inflation', 'Amount'].values[0]
r=expense_df.loc[expense_df['Category'] == 'SIP expected returns', 'Amount'].values[0]
req_expenses_ret=curr_expense*(1+ infl/100)**len_invest
lump_sum=expense_df.loc[expense_df['Category'] == "Lump sum availabale at current age", 'Amount'].values[0]
lump_sum_returns=lump_sum* (1 + r/100)**len_invest
#sip final value calculation 
#FV=P×(((1+r)^n −1))/r)×(1+r)
FV=req_expenses_ret*33 - lump_sum_returns

yearly_SIP_required=(FV*(r/100))/((((1+(r/100))**len_invest) - 1))
Monthly_SIP_required=yearly_SIP_required/12
# # Calculate total expenses
# total_expense = sum(user_expenses.values())
# st.subheader(f"Total Expenses: ${total_expense}")
st.subheader(f"Required amount for expenses at retirement: ${int(req_expenses_ret)}")
st.subheader(f"Required corpus at the retirement: ${int(FV)}")

st.subheader(f"Required SIP amount: ${int(Monthly_SIP_required)}")



corpus_data={"Amount":[lump_sum_returns,FV],"Category":["Lump sum returns","SIP required corpus"]}

corpus_df=pd.DataFrame(corpus_data)

# Visualize the expenses using a pie chart
st.subheader("Contribution of the retirement corpus")


fig, ax = plt.subplots()
ax.pie(corpus_df['Amount'], labels=corpus_df['Category'], autopct=lambda p: f'{int(p * corpus_df["Amount"].sum() / 100)}', startangle=90)
ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.
st.pyplot(fig)
monthly_returns_df=pd.DataFrame(columns=["Lump sum returns", "SIP returns", "Total"])
lump_sum_returns_monthly=lump_sum
n_months = len_invest * 12  # Total months
    


for i in range(n_months):

    lump_sum_returns_monthly=lump_sum* (1 + r/(12*100))**i
    sip_returns=Monthly_SIP_required* (((1+r/1200)**i -1)/(r/1200))*(1+ r/1200)
    total_value=lump_sum_returns_monthly + sip_returns
    monthly_returns_df[i]=[int(lump_sum), int(sip_returns), int(total_value)]
   # monthly_row={"Lump sum returns":int(lump_sum), "SIP returns":int(sip_returns), "Total":int(total_value)}
    #monthly_returns_df=monthly_returns_df.append(monthly_row,ignore_index=True)
# Save expenses data as a CSV file for download
st.subheader("Download Your Corpus Creation Data")
st.download_button(label="Download as CSV", data=monthly_returns_df.to_csv(index=False), file_name="sip_returns.csv")






