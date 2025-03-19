# LLM-Based-Ticket-Reply-Evaluation

Installation

Clone the repository (or download the script):

git clone <repository_url>
cd <repository_directory>

Install required Python libraries:

pip install openai pandas python-dotenv

Set up API credentials:

Create a .env file in the same directory as the script.

Add your OpenAI API key:
OPENAI_API_KEY=your_openai_api_key

Running the Script

Ensure your input file (tickets.csv) is in the same directory and follows this format:

ticket

reply

Customer's message

AI-generated response

Run the script with:

python evaluate_tickets.py

This will generate an output file tickets_evaluated.csv with additional columns:

content_score (1-5)

content_explanation

format_score (1-5)

format_explanation

Example Output

ticket

reply

content_score

content_explanation

format_score

format_explanation

"How do I reset my password?"

"You can reset it in settings."

4

"Correct, but lacks step-by-step details."

5

"Clear and concise response."

Error Handling

Missing Data: Rows with missing ticket or reply are skipped.

API Errors: If the OpenAI API fails, the script will log the issue and proceed.

Rate Limits: The script waits 1 second between requests to prevent API throttling.

