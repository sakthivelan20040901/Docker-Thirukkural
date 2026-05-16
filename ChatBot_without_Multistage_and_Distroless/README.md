# Thirukkural Chatbot

This project is a Natural Language Processing (NLP)-based chatbot designed to provide Thirukkural verses and explanations. Users can query in Tamil or English or enter a specific Thirukkural number to retrieve the corresponding verse and explanations. Built with Flask, the application leverages TF-IDF to vectorize explanations and match relevant verses based on the user's input.

## Features

- **Bilingual Search**: Accepts English and Tamil queries.
- **Direct Access by Number**: Retrieve specific Thirukkural verses by number.
- **Complete Verse Information**: Displays the Tamil verse, English translation, Tamil explanation, and English explanation.

## Technologies Used

- **Python**: Core programming language.
- **Flask**: For the web application.
- **NLP**: Uses TF-IDF vectorization for textual similarity.
- **Pandas**: For data manipulation.
- **Scikit-Learn**: To implement TF-IDF and cosine similarity.
- **NLTK**: For text preprocessing, including stopwords.

## Project Structure

project-folder/ ├── app.py # Main Flask app ├── requirements.txt # List of dependencies ├── templates/ # HTML templates │ └── index.html ├── static/ # Static assets like CSS/images │ ├── style.css │ └── background.jpg └── data/ # Dataset file


## Setup Instructions

### Prerequisites

- **Python 3.7+**: Install from [python.org](https://www.python.org/downloads/).
- **pip**: Python package manager.

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/sakthivelan20040901/NLP-Based-Thirukkural-Verse-Offline-Chatbot.git
  

2.Set up a virtual environment (recommended):
   python -m venv venv
   source venv/bin/activate       # On macOS/Linux
   venv\Scripts\activate          # On Windows

3.Install the required packages:
   pip install -r requirements.txt

4.Download NLTK stopwords:
   import nltk
   nltk.download('stopwords')

5.Add your dataset:

   Ensure the Thirukkural dataset is in CSV format and saved in the data/           folder.
   The CSV file should have the following columns:
NUMBER, TAMIL_VERSE, ENGLISH_VERSE, TAMIL_EXPLANATION, ENGLISH_EXPLANATION.

Usage

Run the Flask app:

bash

python app.py
Open the app in your browser: Go to http://127.0.0.1:5000 to access the chatbot.

Using the Chatbot:

Enter a keyword in Tamil or English to find a relevant Thirukkural verse.
Or enter a Thirukkural number to view the specific verse and its explanations.
Sample Query
Enter a term like "wisdom" or a Tamil word, or try a Thirukkural number, such as 1, to see the corresponding verse and explanations.

Troubleshooting
Ensure that your dataset is correctly formatted and placed in the data/ folder.
If you encounter issues with NLTK, verify that stopwords are downloaded by running nltk.download('stopwords').
License
This project is open-source and available under the MIT License.

Acknowledgments
Thirukkural for the inspiring literature.
NLTK, Scikit-Learn, and Flask for powerful tools.
markdown
Copy code

### Key Points

1. **Explanation** of the project and its purpose.
2. **Setup instructions** with commands for installation.
3. **Usage guide** for running and interacting with the chatbot.
4. **Dataset requirements** with column names.
5. **Troubleshooting tips** for common issues.
6. **Acknowledgments and License** details (optional).

This `README.md` file provides a clear overview of the project and all the information needed to get started with your Thirukkural chatbot.
