# 🏏 Cricket Data App

This is a comprehensive Cricket Data Application built using Streamlit and Snowflake. The app allows users to interactively filter, view, and analyze cricket match data. It integrates seamlessly with Snowflake to query large datasets and provides real-time insights into cricket matches.

## 🌟 Overview

The Cricket Data App is designed to make cricket data easily accessible and interactive. Users can filter matches by year and event, select teams to view specific match details, and retrieve important information such as toss results. The app leverages Snowflake for data storage and retrieval, ensuring that even large datasets are processed efficiently.

![Picture13](https://github.com/user-attachments/assets/1603b893-fcbb-4dec-a130-63209785503a)

## 🚀 Features

- **Year & Event Filtering**: Choose a specific year and event to view related cricket matches.
- **Team Selection**: Select teams involved in a match to view detailed information.
- **Toss Information**: Get insights into which team won the toss and their decision.
- **Data Visualization**: The app is built with Streamlit, providing a clean and interactive interface for data exploration.

## 🛠 Installation

### 1. Clone the Repository

Clone the repository to your local machine using the following command:

```bash
git clone https://github.com/your-username/cricket-data-app.git

## 2. Navigate to the Project Directory

```bash
cd cricket-data-app

Configure Snowflake Connection

Ensure your Snowflake connection details are set correctly in the script:

connection_parameters = {
    "account": "your_account_name",
    "user": "your_username",
    "password": "your_password",
    "warehouse": "your_warehouse",
    "database": "your_database",
    "schema": "your_schema"
}
Replace your_account_name, your_username, your_password, your_warehouse, your_database, and your_schema with your actual Snowflake credentials.

🏃‍♂️ Usage
Running the App
To start the Streamlit app, run the following command:
streamlit run app.py
Open your web browser and navigate to http://localhost:8501 to access the app.

Example Workflow
Select a Year: Use the dropdown menu to choose the year of the matches you want to view.
Select an Event: Filter the matches further by selecting an event.
Choose Teams: Pick the two teams involved in the match you’re interested in.
View Match Details: See detailed information about the match, including toss results and more.
🤝 Contributing
Contributions are welcome! If you have ideas to improve the app or find any issues, feel free to fork the repository, make changes, and submit a pull request.

📜 License
This project is licensed under the MIT License. See the LICENSE file for details.

This Markdown can be directly used in your `README.md` file or any other Markdown-supported platform!





