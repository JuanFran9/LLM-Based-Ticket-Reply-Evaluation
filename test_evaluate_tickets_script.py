import pytest
import pandas as pd
from unittest.mock import patch
from evaluate_tickets_script import evaluate_reply, process_tickets

# Mock OpenAI API response
MOCK_RESPONSE = {
    "content_score": 4,
    "content_explanation": "Relevant but lacks details.",
    "format_score": 5,
    "format_explanation": "Well-structured and clear.",
}


# Mock API failure response
def mock_openai_failure(*args, **kwargs):
    raise Exception("OpenAI API error")


def test_evaluate_reply():
    ticket = "How do I reset my password?"
    reply = "You can reset it in settings."
    with patch("evaluate_tickets_script.evaluate_reply", return_value=MOCK_RESPONSE):
        result = evaluate_reply(ticket, reply)
        assert isinstance(result, dict)  # Ensure result is a dictionary
        assert (
            1 <= result["content_score"] <= 5
        )  # Ensure content score is between 1 and 5
        assert (
            1 <= result["format_score"] <= 5
        )  # Ensure format score is between 1 and 5
        assert (
            isinstance(result["content_explanation"], str)
            and len(result["content_explanation"]) > 0
        )  # Ensure explanation is in content_explanation
        assert (
            isinstance(result["format_explanation"], str)
            and len(result["format_explanation"]) > 0
        )  # Ensure explanation is in format_explanation


def test_process_tickets(tmp_path):
    input_file = tmp_path / "tickets.csv"
    output_file = tmp_path / "tickets_evaluated.csv"

    df = pd.DataFrame(
        {
            "ticket": ["How do I reset my password?"],
            "reply": ["You can reset it in settings."],
        }
    )
    df.to_csv(input_file, index=False)

    with patch("evaluate_tickets_script.evaluate_reply", return_value=MOCK_RESPONSE):
        process_tickets(input_file, output_file)

    df_result = pd.read_csv(output_file)

    assert "content_score" in df_result.columns  # Ensure content_score is in columns
    assert "format_score" in df_result.columns  # Ensure format_score is in columns
    assert df_result.loc[0, "content_score"] == 4  # Ensure content_score is 4
    assert df_result.loc[0, "format_score"] == 5  # Ensure format_score is 5


def test_process_tickets_with_missing_data(tmp_path):
    input_file = tmp_path / "tickets.csv"
    output_file = tmp_path / "tickets_evaluated.csv"

    df = pd.DataFrame(
        {
            "ticket": ["How do I reset my password?", None],
            "reply": [None, "This is a reply."],
        }
    )
    df.to_csv(input_file, index=False)  # This creates a csv file with the dataframe

    with patch("evaluate_tickets_script.evaluate_reply", return_value=MOCK_RESPONSE):
        process_tickets(input_file, output_file)

    df_result = pd.read_csv(output_file)
    assert df_result.isnull().sum().sum() > 0  # Ensure missing data is preserved


def test_openai_api_failure():
    ticket = "How do I reset my password?"
    reply = "You can reset it in settings."

    # Patch the OpenAI API call inside the evaluate_reply function
    with patch(
        "evaluate_tickets_script.client.chat.completions.create",
        side_effect=mock_openai_failure,
    ):
        result = evaluate_reply(ticket, reply)

        assert result["content_score"] is None  # Ensure content_score is None
        assert result["format_score"] is None  # Ensure format_score is None
        assert (
            "Error" in result["content_explanation"]
        )  # Ensure error is in content_explanation
        assert (
            "Error" in result["format_explanation"]
        )  # Ensure error is in format_explanation
