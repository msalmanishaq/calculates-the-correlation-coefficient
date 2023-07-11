import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import statsmodels.api as sm

# Read the CSV files and combine the data
df1 = pd.read_csv("Actual Generation per Production Type_202307060000-202307070000.csv")
df2 = pd.read_csv("Total Load - Day Ahead _ Actual_202307060000-202307070000 (1).csv")
combined_data = pd.concat([df1, df2], axis=1)
combined_data.to_csv("combined_data.csv", index=False)

# Read the combined data
df2 = pd.read_csv('combined_data.csv', index_col="MTU", parse_dates=True)
columns_to_keep = ["Solar  - Actual Aggregated [MW]", "Wind Offshore  - Actual Aggregated [MW]",
                   "Wind Onshore  - Actual Aggregated [MW]", "Day-ahead Total Load Forecast [MW] - BZN|AL"]
df2 = df2[columns_to_keep]
df2.dropna(inplace=True)


def login():
    users = {
        "sajjad ili": "sajjad123",
        "Ali jan": "loveyou",
        "salman ishaq": "salman123",
        "hussainsyed.kazmi": "hussain321"
    }

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in users and users[username] == password:
            st.success("Logged in successfully!")
            show_dashboard()
        else:
            st.error("Invalid username or password")


def show_dashboard():
    # Streamlit app
    st.title("Correlation and Scatter Plot")
    st.markdown("This app calculates the correlation coefficient, displays a scatter plot, and shows the combined clean dataset.")

    # Calculate the correlation coefficient
    var1 = df2["Wind Offshore  - Actual Aggregated [MW]"]
    var2 = df2["Day-ahead Total Load Forecast [MW] - BZN|AL"]
    correlation_coefficient = np.corrcoef(var1, var2)[0, 1]

    # Display the correlation coefficient
    st.subheader("Correlation Coefficient:")
    st.write(correlation_coefficient)

    # Display the description text
    st.subheader("Description:")
    description = "A correlation coefficient of 0.8081 indicates a strong positive correlation between the variables " \
                  "'Wind Onshore - Actual Aggregated [MW]' and 'Day-ahead Total Load Forecast [MW] - BZN|AL'. " \
                  "A correlation coefficient of 0.8081 suggests a strong positive linear relationship between the " \
                  "variables, meaning that as the 'Wind Onshore - Actual Aggregated [MW]' increases, there is a " \
                  "tendency for the 'Day-ahead Total Load Forecast [MW] - BZN|AL' to also increase."
    st.write(description)

    # Display the scatter plot
    st.subheader("Scatter Plot:")
    scatter_fig = px.scatter(df2, x="Wind Offshore  - Actual Aggregated [MW]",
                             y="Day-ahead Total Load Forecast [MW] - BZN|AL", trendline="ols")
    scatter_fig.update_layout(title="Scatter Plot: Wind Offshore vs. Day-ahead Total Load Forecast",
                              xaxis_title="Wind Offshore - Actual Aggregated [MW]",
                              yaxis_title="Day-ahead Total Load Forecast [MW] - BZN|AL")
    st.plotly_chart(scatter_fig)

    # Display the scatter plot
    st.subheader("Scatter Plot:")
    scatter_fig1 = px.scatter(df2, x="Wind Onshore  - Actual Aggregated [MW]",
                              y="Day-ahead Total Load Forecast [MW] - BZN|AL", trendline="ols")
    scatter_fig1.update_layout(title="Scatter Plot: Wind Onshore vs. Day-ahead Total Load Forecast",
                               xaxis_title="Wind Onshore - Actual Aggregated [MW]",
                               yaxis_title="Day-ahead Total Load Forecast [MW] - BZN|AL")
    st.plotly_chart(scatter_fig1)

    # Rest of your code for the correlation matrix and summary...
    df_clean = pd.read_csv('combined_data.csv', index_col="MTU", parse_dates=True)

    # Select the columns of interest
    columns_of_interest = ["Day-ahead Total Load Forecast [MW] - BZN|AL",
                           "Solar  - Actual Aggregated [MW]",
                           "Wind Offshore  - Actual Aggregated [MW]",
                           "Wind Onshore  - Actual Aggregated [MW]"]

    # Create a subset DataFrame with the selected columns
    subset_df = df_clean[columns_of_interest]

    # Calculate the correlation matrix
    correlation_matrix = subset_df.corr()

    # Streamlit app
    st.title("Correlation Analysis")
    st.markdown("This app calculates and displays the correlation matrix for the selected variables.")

    # Display the correlation matrix
    st.subheader("Correlation Matrix:")
    st.write(correlation_matrix)

    # Correlation Summary
    st.subheader("Correlation Summary:")

    # Correlation explanation 1
    st.write("### Day-ahead Total Load Forecast [MW] - BZN|AL and Wind Offshore - Actual Aggregated [MW]:")
    st.write("- Strong positive correlation (0.8081).")
    st.write("- As the forecasted total load increases, there is a tendency for offshore wind power generation to also increase.")
    st.write("- Indicates a relationship between total load forecast and offshore wind power generation.")

    # Correlation explanation 2
    st.write("### Day-ahead Total Load Forecast [MW] - BZN|AL and Wind Onshore - Actual Aggregated [MW]:")
    st.write("- Strong positive correlation (0.8659).")
    st.write("- As the forecasted total load increases, there is a tendency for onshore wind power generation to also increase.")
    st.write("- Indicates a relationship between total load forecast and onshore wind power generation.")

    # Correlation explanation 3
    st.write("### Solar - Actual Aggregated [MW] and Day-ahead Total Load Forecast [MW] - BZN|AL:")
    st.write("- Moderate negative correlation (-0.7264).")
    st.write("- As the forecasted total load increases, there is a tendency for solar power generation to decrease.")
    st.write("- Indicates an inverse relationship between total load forecast and solar power generation.")

    # Correlation explanation 4
    st.write("### Solar - Actual Aggregated [MW] and Wind Onshore - Actual Aggregated [MW]:")
    st.write("- Weak negative correlation (-0.5501).")
    st.write("- As solar power generation increases, there is a tendency for onshore wind power generation to decrease.")
    st.write("- Suggests a potential trade-off between solar power generation and onshore wind power generation.")


def main():
    login()


if __name__ == "__main__":
    main()
