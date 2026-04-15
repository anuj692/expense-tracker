import streamlit as st
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # This tells Matplotlib to run without a GUI
import streamlit as st

import matplotlib.pyplot as plt
import seaborn as sns
import datetime

# -------------------- INITIALIZATION --------------------
# Session state mein dataframe banate hain agar wo pehle se nahi hai
if 'expenses' not in st.session_state:
    st.session_state.expenses = pd.DataFrame(columns=['Date', 'Category', 'Amount', 'Description'])

# File loading track karne ke liye state
if 'loaded_file_name' not in st.session_state:
    st.session_state.loaded_file_name = None

# -------------------- FUNCTIONS ----------------
def clean_data(df):
    """
    Data ko clean karta hai:
    - Dates ko sahi format mein convert karta hai
    - Numbers ko float banata hai
    - Empty descriptions fill karta hai
    """
    # 1. Date Format Fix
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    
    # 2. Amount Format Fix
    df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
    
    # 3. Missing Values
    df.dropna(subset=['Amount', 'Date'], inplace=True) # Agar date ya paise nahi hain to row hata do
    df['Category'] = df['Category'].fillna('Uncategorized')
    df['Description'] = df['Description'].fillna('No Description')
    
    return df

def add_expense(date, category, amount, description):
    """Naya kharcha list mein add karta hai"""
    # Date ko datetime object mein convert karte hain taaki format same rahe
    date = pd.to_datetime(date)
    
    new_expense = pd.DataFrame([[date, category, amount, description]], 
                               columns=st.session_state.expenses.columns)
    
    # Naye data ko existing data ke saath jodna (Concatenate)
    st.session_state.expenses = pd.concat([st.session_state.expenses, new_expense], ignore_index=True)

def show_one_time_success(message: str) -> None:
    """Show a one-time success message using session_state."""
    if st.session_state.get("show_added_popup"):
        st.success(message)
        st.session_state["show_added_popup"] = False

def load_expenses():
    """Ab ye CSV, JSON, aur Excel teeno format accept karega"""
    
    # 1. Type mein 'json' aur 'xlsx' add kar diya
    uploaded_file = st.sidebar.file_uploader("Upload File", type=['csv', 'json', 'xlsx'])
    
    if uploaded_file is not None:
        if st.session_state.loaded_file_name != uploaded_file.name:
            
            try:
                # 2. Check karo file extension kya hai aur us hisab se read karo
                if uploaded_file.name.endswith('.csv'):
                    new_data = pd.read_csv(uploaded_file)
                    
                elif uploaded_file.name.endswith('.json'):
                    # JSON read karne ke liye
                    new_data = pd.read_json(uploaded_file)
                    
                elif uploaded_file.name.endswith('.xlsx'):
                    # Excel read karne ke liye (openpyxl install hona chahiye)
                    new_data = pd.read_excel(uploaded_file)

                # Baki process same rahega (Cleaning & Appending)
                new_data = clean_data(new_data)
                
                old_data = st.session_state.expenses
                combined_data = pd.concat([old_data, new_data], ignore_index=True)
                combined_data.drop_duplicates(inplace=True)
                
                st.session_state.expenses = combined_data
                st.session_state.loaded_file_name = uploaded_file.name
                
                st.sidebar.success("File loaded successfully!")
                st.rerun()
                
            except Exception as e:
                st.error(f"Error reading file: {e}")

def save_expenses():
    """Current data ko CSV file mein save karta hai"""
    if not st.session_state.expenses.empty:
        csv = st.session_state.expenses.to_csv(index=False).encode('utf-8')
        st.sidebar.download_button(
            label="Download Data as CSV",
            data=csv,
            file_name='my_expenses.csv',
            mime='text/csv',
        )
    else:
        st.sidebar.warning("No data to save yet!")

def visualize_expenses():
    """Graphs draw karta hai"""
    if not st.session_state.expenses.empty:
        st.subheader("Category-wise Expenses")
        
        # Grouping data
        df_viz = st.session_state.expenses.groupby('Category')['Amount'].sum().reset_index()
        
        # Plotting
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(data=df_viz, x='Category', y='Amount', ax=ax, palette="viridis")
        plt.xticks(rotation=45)
        plt.title('Total Expenses by Category')
        
        st.pyplot(fig)
    else:
        st.warning("No data available for visualization.")

# -------------------- UI LAYOUT --------------------

st.title('💰 Expense Tracker')

# --- SIDEBAR ---
with st.sidebar:
    st.header('➕ Add New Expense')

    # One-time notification flag (so message stays visible after submit)
    if "show_added_popup" not in st.session_state:
        st.session_state["show_added_popup"] = False
    
    # Input Form
    with st.form("expense_form", clear_on_submit=True):
        date_in = st.date_input('Date', datetime.date.today())
        cat_in = st.selectbox('Category', ['Food', 'Transport', 'Entertainment', 'Utilities', 'Shopping', 'Other'])
        amt_in = st.number_input('Amount', min_value=0.0, format="%.2f")
        desc_in = st.text_input('Description')
        
        submitted = st.form_submit_button("Add Expense")
        
        if submitted:
            add_expense(date_in, cat_in, amt_in, desc_in)
            st.session_state["show_added_popup"] = True

    # Show success just below the Add Expense button (in the sidebar).
    show_one_time_success("Added successfully!")

    st.header('📂 File Operations')
    # Load function ko call kiya (Uploader sidebar mein hi dikhega)
    load_expenses()
    
    # Save button
    save_expenses()

# --- MAIN PAGE ---
st.header('📋 Your Expenses')

# Dataframe dikhana (Sort karke taaki latest upar dikhe)
if not st.session_state.expenses.empty:
    # Display ke liye thoda clean format
    display_df = st.session_state.expenses.sort_values(by='Date', ascending=False)
    
    # Date column ko sirf Date dikhane ke liye format karna (Time hata dena)
    display_df['Date'] = pd.to_datetime(display_df['Date'])
    display_df['Date'] = display_df['Date'].dt.date
    
    st.dataframe(display_df, use_container_width=True)
    
    # Total dikhana
    total_spent = st.session_state.expenses['Amount'].sum()
    st.metric(label="Total Spent", value=f"₹ {total_spent:.2f}")
    
    st.divider()
    
    # Visualization Section
    visualize_expenses()

else:
    st.info("Start by adding an expense from the sidebar or upload a CSV file.")
