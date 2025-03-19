# LLM-Based-Ticket-Reply-Evaluation

This repository contains a Python script to evaluate AI-generated responses to customer support tickets using OpenAI's GPT-4. The script assigns scores for content relevance and formatting quality, providing explanations for each rating.

The results output in `tickets_evaluated.csv` looks correct and the 4 tests pass succesfully

## Installation

1. Clone the repository (or download the script):

`git clone <repository_url>
cd <repository_directory>`

2. Install required Python libraries or use requirements.txt:

`pip install openai pandas python-dotenv pytest
`
3. Set up API credentials:

Create a .env file in the same directory as the script.

Add your OpenAI API key:
`OPENAI_API_KEY=your_openai_api_key
`
## Running the Script

Run the script in the CLI with:

`python evaluate_tickets.py`


## Running the Tests

Run the tests in the CLI with:

`pytest test_evaluate_tickets_script.py `


