
# InfoCric-A Cricket Information Dashboard

## Overview

The Cricket Stats Dashboard is a web application built using Django that allows users to search for cricket players and view their statistics, including batting and bowling records. The application fetches data from the Cricbuzz API to provide real-time cricket statistics.

## Features

- **Player Search**: Users can search for cricketers by name.
- **Player Stats**: Displays detailed statistics, including batting and bowling averages, matches played, runs scored, and more.
- **Responsive Design**: The UI is designed to be user-friendly and responsive on different devices.
- **Error Handling**: Graceful handling of API errors and no-data scenarios.

## Technologies Used

- **Backend**: Django
- **Frontend**: HTML, CSS, JavaScript
- **API**: Cricbuzz API
- **Database**: SQLite (default with Django)
- **Version Control**: Git

## Setup Instructions

### Prerequisites

- Python 3.x
- pip (Python package installer)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/cricket-stats-dashboard.git
   cd cricket-stats-dashboard
   ```

2. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Create a configuration file**:
   Create a file named `configure.py` in the project stats directory and add your API keys:
   ```python
   # configure.py
   API_KEY = "your_api_key_here"
   API_HOST = "your_api_host_here"
   ```

5. **Run the server**:
   ```bash
   python manage.py runserver
   ```

6. **Access the application**:
   Open your web browser and navigate to `http://127.0.0.1:8000/`.

## Usage

1. On the home page, enter the name of a cricketer in the search box.
2. Click the search button to view the player's statistics.
3. The statistics will be displayed in a tabular format for both batting and bowling.

## API KEY

Get your API KEY from 
```
https://rapidapi.com/cricketapilive/api/cricbuzz-cricket/playground/apiendpoint_cf992c8a-4262-4682-a0bd-7fa16b609e5f
```
Create a file named `configure.py` in the project stats directory and add your API keys:
   ```python
   # config.py
   API_KEY = "your_api_key_here"
   API_HOST = "your_api_host_here"
```

## Future Plans

- **Team Information**: Extend the application to provide details about cricket teams, including player rosters and team history.
- **Stadium Information**: Include information about various cricket stadiums, such as location, capacity, and historical significance.
- **Images**: Add player images and stadium pictures for a more visually appealing interface.
- **Caching**: Implement chaching and storing stats to save API calls.
- **Statistics Comparison**: Enable users to compare statistics between multiple players.

## Contributing

Contributions are welcome! If you have suggestions or improvements, feel free to fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

