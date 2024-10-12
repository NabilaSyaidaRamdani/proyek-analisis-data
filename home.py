import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import base64

# Function to add background image from local file
def add_bg_from_local(image_file):
    with open(image_file, "rb") as f:
        img = f.read()
    b64 = base64.b64encode(img).decode()
    st.markdown(
        f"""
        <style>
        .stSidebar {{
            background-image: url(data:image/jpeg;base64,{b64});
            background-size: cover;
            background-repeat: no-repeat;
            background-position: center;
            color: white;  /* Warna teks sidebar */
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Set page configuration
st.set_page_config(page_title="Customer Analysis Dashboard", page_icon="🌏", layout="wide")

# Add background image
add_bg_from_local("download.jpeg")

# Add title and subtitle
st.title("Customer Analysis")
st.subheader("Top 10 Cities by Number of Customers")

# Create a container for Sign In / Sign Up buttons
col1, col2 = st.columns(2)

with col1:
    if st.button("Sign In"):
        st.session_state.page = "sign_in"

with col2:
    if st.button("Sign Up"):
        st.session_state.page = "sign_up"

# Create tabs for Sign In and Sign Up
if 'page' in st.session_state:
    if st.session_state.page == "sign_in":
        st.header("Sign In")
        st.text_input("Username")
        st.text_input("Password", type='password')
        if st.button("Submit"):
            st.success("Signed In!")
    elif st.session_state.page == "sign_up":
        st.header("Sign Up")
        st.text_input("Username")
        st.text_input("Email")
        st.text_input("Password", type='password')
        if st.button("Register"):
            st.success("Registered Successfully!")

# Load data
data = pd.read_csv("customer.csv")

# Sidebar header and filter
st.sidebar.header("Please Filter Here")
state = st.sidebar.multiselect(
    "Customer State",
    options=data["customer_state"].unique(),
    default=data["customer_state"].unique()
)
df_selection = data[(data["customer_state"].isin(state))]

# Calculate top 10 cities by customer count
city_counts = df_selection["customer_city"].value_counts().head(10)

# Plotting Top 10 Cities using matplotlib
fig, ax = plt.subplots()
ax.barh(city_counts.index, city_counts.values)
ax.set_xlabel("Number of Customers")
ax.set_title("Top 10 Cities by Number of Customers")

# Add data labels
for index, value in enumerate(city_counts.values):
    ax.text(value, index, str(value))

# Display plot in Streamlit
st.pyplot(fig)

# Plotting Top 5 States using Pie Chart
st.subheader("Top 5 States by Number of Customers")
state_counts = df_selection["customer_state"].value_counts().head(5)

# Plotting Pie Chart using matplotlib
fig, ax = plt.subplots(figsize=(7, 7))
colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0']
ax.pie(state_counts.values, labels=state_counts.index, autopct='%1.1f%%', 
       startangle=90, colors=colors, wedgeprops={'edgecolor': 'black'})
ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
ax.set_title("Top 5 States by Number of Customers", fontsize=16, fontweight='bold')

# Display plot in Streamlit
st.pyplot(fig)

df = pd.DataFrame(data)
city_counts = df['customer_city'].value_counts()
plt.figure(figsize=(10, 6))
city_counts.plot(kind='bar', color='saddlebrown', alpha=0.7)
plt.xlabel('City')
plt.ylabel('Number of Customers')
plt.title('Number of Customers by City')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()



