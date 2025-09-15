# Social Media Analytics Dashboard

A comprehensive interactive web dashboard for analyzing social media performance across multiple platforms (Facebook, Instagram, Twitter, YouTube). Built with Python Dash and Plotly for data visualization.

🔗 **Live Demo:** [cu-social-media-analytics.herokuapp.com](https://cu-social-media-analytics.herokuapp.com/)

## 📊 Features

### Overview Page
- **Platform Popularity**: Visual comparison of social media platforms by number of accounts and engagement levels
- **Time-based Analysis**: Best posting times and day-of-week patterns for maximum engagement
- **Growth Tracking**: Monthly follower growth trends across all platforms
- **Top Performers**: Identification of highest-engaging accounts per platform

### Detailed Analytics Page
- **Content Performance**: Analysis of different post types (images vs videos on Instagram)
- **Audience Segmentation**: Fan base categorization and engagement patterns
- **Funnel Analysis**: Facebook engagement funnel by audience size
- **Interactive Filtering**: Dynamic charts with platform-specific insights

## 🛠 Technology Stack

- **Backend**: Python, Dash, Flask
- **Visualization**: Plotly, Plotly Express
- **Data Processing**: Pandas, NumPy
- **Frontend**: Dash HTML/Core Components, Custom CSS
- **Deployment**: Heroku (Gunicorn server)

## 📋 Prerequisites

- Python 3.7+
- pip package manager

## 🚀 Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/kittipat1413/Social-media-analytics.git
   cd Social-media-analytics
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python index.py
   ```

4. **Access the dashboard**
   - Open your browser and navigate to `http://localhost:8050`
   - Use the navigation menu to switch between Overview and Detail pages

## 📁 Project Structure

```
Social-media-analytics/
├── app.py                # Main Dash application setup
├── index.py              # Application entry point and routing
├── requirements.txt      # Python dependencies
├── Procfile              # Heroku deployment configuration
├── Dockerfile            # Docker containerization
├── layouts/              # Page layouts and components
│   ├── page1.py          # Overview page layout
│   └── page2.py          # Detailed analytics page
├── datasets/             # Data files (CSV format)
│   ├── df_channel_engagement.csv
│   ├── df_day_vs_time.csv
│   ├── df_fan_each_month.csv
│   └── ... other data files
└── assets/               # Static files (CSS, images)
    ├── style.css         # Main stylesheet
    ├── topnav.css        # Navigation bar styles
    └── facebook_heatmap.svg
```

## 📈 Data Sources

The dashboard analyzes social media data including:
- **Account Information**: Platform-specific account details and metadata
- **Engagement Metrics**: Likes, shares, comments, views across platforms
- **Temporal Data**: Time-series data for trend analysis
- **Content Categorization**: Post types, audience segments, and performance metrics

## 🎨 Visualizations

### Facebook Engagement Time Heatmap
<img src="./assets/facebook_heatmap.svg" alt="Facebook Engagement Heatmap" width="600">

*Interactive heatmap showing optimal posting times for Facebook content*