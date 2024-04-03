def get_card_billing_prompt(document_text):
    base_prompt = """
        You are an assistant to accountants.
        Your are given the data extracted from a credit card billing statetement by google document ai.
        Your job is to skim through its content and return the necessary information.
        The information I want you to return are  "date", "payee", and "amount".
        Format the extracted data in the following json form.
        {"total_price": int, "billing_date": "yyyy-mm-dd",
            "items": [
                {
                    "date":"yyyy-mm-dd",
                    "payee": string,
                    "amount": int
                },
                {
                    "date":"yyyy-mm-dd",
                    "payee": string,
                    "amount": int
                }
            ]
        }
        ##DATA
    """
    prompt = base_prompt + "\n" + document_text
    return prompt


def get_bankbook_prompt(document_text):
    base_prompt = """
        You are an assistant to accountants.
        Your are given the data extracted from bankbook information by google document ai.
        Your job is to skim through its content and return the necessary information.
        The information I want you to return the following five elements:"date", "summary", "deposit", "withdrawal" and "balance".
        The names for each element usually appear at the beginning in the order same as the data that follow.
        Format the extracted data in the following json form.
        {
            "items": [
                {
                    "date":"yyyy-mm-dd",
                    "summary": string,
                    "deposit": int,
                    "withdrawal": int,
                    "balance": int
                },
                {
                    "date":"yyyy-mm-dd",
                    "summary": string,
                    "deposit": int,
                    "withdrawal": int,
                    "balance": int
                }
            ]
        }
        ##DATA
    """
    prompt = base_prompt + "\n" + document_text
    return prompt