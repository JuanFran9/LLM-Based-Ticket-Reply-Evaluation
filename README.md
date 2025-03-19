# LLM-Based-Ticket-Reply-Evaluation

## Installation

1. Clone the repository (or download the script):

git clone <repository_url>
cd <repository_directory>

2. Install required Python libraries or use requirements.txt:

pip install openai pandas python-dotenv

3. Set up API credentials:

Create a .env file in the same directory as the script.

Add your OpenAI API key:
OPENAI_API_KEY=your_openai_api_key

## Running the Script

Ensure your input file (tickets.csv) is in the same directory and follows this format:

ticket

reply

Customer's message

AI-generated response

Run the script with:

`python evaluate_tickets.py`

##Error Handling

Missing Data: Rows with missing ticket or reply are skipped.

API Errors: If the OpenAI API fails, the script will log the issue and proceed.

Rate Limits: The script waits 1 second between requests to prevent API throttling.

