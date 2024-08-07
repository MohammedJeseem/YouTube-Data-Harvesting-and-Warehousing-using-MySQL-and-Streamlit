# YouTube Data Harvesting and Warehousing

Welcome to the **YouTube Data Harvesting and Warehousing** project! This project involves collecting and storing YouTube data using MySQL and Streamlit.

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Examples](#examples)
6. [Contributing](#contributing)
7. [Credits](#credits)
8. [Contact](#contact)

## 📌 Project Overview

This project is designed to extract data from YouTube, store it in a MySQL database, and visualize it using Streamlit. The main goals are to:

- Harvest data from YouTube channels and videos.
- Store and manage data efficiently using MySQL.
- Create interactive visualizations with Streamlit.
  
 ### Demo video : [LinkedIn](https://www.linkedin.com/posts/mohammed-jeseem-25894b29b_youtubedataharvest-activity-7226920496104103936-ODrj?utm_source=share&utm_medium=member_desktop)

## 🚀 Features

- **Data Harvesting:** Extract channel details, playlists, videos, and comments.
- **Data Warehousing:** Store and manage YouTube data in MySQL.
- **Data Visualization:** Interactive charts and tables to analyze YouTube data using Streamlit.
- **SQL Queries:** Retrieve insights such as top-viewed videos, most liked videos, and more.

## 🛠️ Installation

### Clone the Repository

```bash
git clone https://github.com/MohammedJeseem/YouTube-Data-Harvesting-and-Warehousing-using-MySQL-and-Streamlit.git
cd YouTube-Data-Harvesting-and-Warehousing-using-MySQL-and-Streamlit
```

### Create and Activate a Virtual Environment

- **Create Environment**
  ```bash
  python -m venv .venv
  ```

- **Windows command prompt**
  ```
  .venv\Scripts\activate.bat
  ```

- **Windows PowerShell**
  ```
  .venv\Scripts\Activate.ps1
  ```

- **macOS and Linux**
  ```
  source .venv/bin/activate
  ```
Once activated, you will see your environment name in parentheses before your prompt. "(.venv)"


### Install Dependencies

```bash
pip install -r requirements.txt
```

### Set Up MySQL Database

1. **Install MySQL:** Follow the [MySQL Installation Guide](https://dev.mysql.com/doc/mysql-installation-excerpt/5.7/en/).
2. **Create a Database:** Use the provided SQL schema to set up your database.

## 🌐 Getting the YouTube Data API Key

To fetch data from YouTube, you'll need an API key. Follow these steps to obtain one:

1. **Create a Google Cloud Project:**
   - Go to the [Google Cloud Console](https://console.cloud.google.com/).
   - Click on **Select a Project** at the top of the page and then **New Project**.
   - Enter a project name and click **Create**.

2. **Enable the YouTube Data API:**
   - In the Google Cloud Console, navigate to **APIs & Services** > **Library**.
   - Search for **YouTube Data API v3**.
   - Click on **YouTube Data API v3** and then **Enable**.

3. **Create Credentials:**
   - Go to **APIs & Services** > **Credentials**.
   - Click on **Create Credentials** and choose **API key**.
   - Copy the API key that is generated.

4. **Configure API Key in Your Project:**
   - Update the `src/config.ini` file with your API key.

### Configure Your Environment

Update the database connection settings and youtube api settings in `src/config.ini`.
```
[mysqlDB]
host = localhost
db = youtube
user = root
pass = root


[youtubeAPI]
api_service_name = youtube
api_version = v3
api_Key = PASTE_YOUR_API_HERE
```

## 💻 Usage

### Run the Streamlit Application

```bash
streamlit run app.py
```

### Example Queries

To get insights, use the following Streamlit components:

- **Top 10 Viewed Videos:** View top 10 videos by total views.
- **Channel Subscriber Counts:** Visualize subscriber counts for each channel.
- **Average Video Duration:** Analyze average video duration per channel.

## 🎨 Examples

Here are some example screenshots of the Streamlit application:

![Example 1](screenshots/screenshot1.png)
![Example 2](screenshots/screenshot2.png)
![Example 3](screenshots/screenshot3.png)
![Example 4](screenshots/screenshot4.png)

## 🤝 Contributing

We welcome contributions! If you want to improve this project, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## 🏅 Credits

- **Gokul M** - For his project reference [YouTube Data Harvesting and Warehousing using SQL and Streamlit](https://github.com/Gokul170601/YouTube-Data-Harvesting-and-Warehousing-using-SQL-and-Streamlit).
  - **LinkedIn:** [Gokul M](https://www.linkedin.com/in/gokul-m-j17/)
  - **Gmail:** [gokulgokul6847@gmail.com](mailto:gokulgokul6847@gmail.com)

## 📧 Contact

For any inquiries or suggestions, please contact:

### Mohammed Jeseem .M

- **Gmail:** [mohammedjezeem786@gmail.com](mailto:mohammedjezeem786@gmail.com)
- **LinkedIn:** [Mohammed Jeseem](https://www.linkedin.com/in/mohammed-jeseem-25894b29b/)
