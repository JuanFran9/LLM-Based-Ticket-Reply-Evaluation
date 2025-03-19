import os
import pandas as pd
import openai
from dotenv import load_dotenv
import time


# Load API key from .env file
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


openai.api_key = OPENAI_API_KEY

client = openai.OpenAI(api_key=OPENAI_API_KEY)


def evaluate_reply(ticket, reply):
    """Sends the ticket and reply to OpenAI's GPT-4 for evaluation."""
    prompt = f"""
    You are an AI evaluator for customer support responses. 
    Given a customer support ticket and an AI-generated reply, you will assess:
    
    1. **Content Score (1-5)** - How relevant, correct, and complete is the response?
    2. **Content Explanation** - A short justification of the score.
    3. **Format Score (1-5)** - How clear, well-structured, and grammatically correct is the response?
    4. **Format Explanation** - A short justification of the score.
    
    Respond in JSON format:
    {{
        "content_score": <integer from 1-5>,
        "content_explanation": "<brief explanation>",
        "format_score": <integer from 1-5>,
        "format_explanation": "<brief explanation>"
    }}
    
    Example:
    {{
        "content_score": 4,
        "content_explanation": "The response addresses the question well but lacks additional troubleshooting steps.",
        "format_score": 5,
        "format_explanation": "The response is well-structured, grammatically correct, and easy to read."
    }}
    
    **Ticket:** {ticket}
    **Reply:** {reply}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,  # Lower temperature to reduce randomness
        )

        result = response.choices[0].message.content
        return eval(result)  # Convert string response to dictionary
    except Exception as e:
        print(f"Error processing ticket: {e}")
        return {
            "content_score": None,
            "content_explanation": "Error occurred during evaluation.",
            "format_score": None,
            "format_explanation": "Error occurred during evaluation.",
        }


def process_tickets(input_file="tickets.csv", output_file="tickets_evaluated.csv"):
    """Reads the CSV, evaluates replies using OpenAI, and writes results to a new CSV."""
    df = pd.read_csv(input_file)

    # Ensure required columns exist
    if "ticket" not in df.columns or "reply" not in df.columns:
        raise ValueError("CSV file must contain 'ticket' and 'reply' columns.")

    # Initialize new columns
    df["content_score"] = None
    df["content_explanation"] = None
    df["format_score"] = None
    df["format_explanation"] = None

    # Process each row
    for index, row in df.iterrows():
        # Skip rows with missing values
        if pd.isna(row["ticket"]) or pd.isna(row["reply"]):
            continue

        evaluation = evaluate_reply(
            row["ticket"], row["reply"]
        )  # This function calls the OpenAI API for the evaluation
        df.at[index, "content_score"] = evaluation[
            "content_score"
        ]  # This assigns the content_score to the dataframe in the same row
        df.at[index, "content_explanation"] = evaluation[
            "content_explanation"
        ]  # This assigns the content_explanation to the dataframe in the same row
        df.at[index, "format_score"] = evaluation[
            "format_score"
        ]  # This assigns the format_score to the dataframe in the same row
        df.at[index, "format_explanation"] = evaluation[
            "format_explanation"
        ]  # This assigns the format_explanation to the dataframe in the same row

        # Rate-limit requests to avoid hitting API limits
        time.sleep(1)

    df.to_csv(output_file, index=False)
    print(f"Processed results saved to {output_file}")


if __name__ == "__main__":
    process_tickets()
