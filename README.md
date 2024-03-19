# Web Scraping Project README

This project focuses on scraping data from the ClinicalTrials.gov API using only the `requests` library in Python. The scraped data is then structured and stored in the form of tables within a SQLite3 database. The project includes models for organizing and managing the scraped data efficiently.

## Project Overview

The primary goal of this project is to gather pertinent information from the ClinicalTrials.gov API related to clinical trials. The API provides a wealth of data regarding clinical studies, including trial descriptions, locations, conditions, interventions, and more. By utilizing the `requests` library, we efficiently fetch this data and organize it into a structured format for further analysis and use.

## Project Structure

The project is structured as follows:

- **`load_study_data.py`**: This script contains the functionality to interact with the ClinicalTrials.gov API using the `requests` library. It fetches data from the API and parses the JSON responses.
  
- **`db`**: This module handles the creation of a SQLite3 database and the creation of tables to store the scraped data. It includes functions for connecting to the database and executing SQL queries.

- **`models.py`**: This module defines classes that represent the data models used to structure the scraped data. These models correspond to the tables created in the SQLite3 database.

- **`manage.py`**: This script serves as the entry point to the project. It orchestrates the scraping process, database creation, and data storage.

## Getting Started

To get started with this project, follow these steps:

1. Clone the repository to your local machine.
2. Ensure you have Python installed.
3. Install the required dependencies by running `pip install -r requirements.txt`.
4. Run the `py manage.py makemigratins` script to initiate the scraping process and store the data in the SQLite3 database.

## Dependencies

This project relies on the following Python libraries:

- `requests`: For making HTTP requests to the ClinicalTrials.gov API.
- `sqlite3`: For interacting with the SQLite3 database.

## Usage

To use this project, you can run the `main.py` script. This will initiate the scraping process and store the fetched data in the SQLite3 database. You can then query the database or integrate it with other applications as needed.

## Contributions

Contributions to this project are welcome. If you find any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request on GitHub.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

This README provides an overview of the project, its structure, usage instructions, and guidelines for contributions. For more detailed information, refer to the individual scripts and modules within the project. If you have any questions or need further assistance, feel free to contact the project maintainer. Thank you for your interest in this web scraping project!
