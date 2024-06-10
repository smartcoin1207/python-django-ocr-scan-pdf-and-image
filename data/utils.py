def get_card_billing_prompt(document_text):
    base_prompt = """
        You are an assistant to accountants.
        Your are given the data extracted from a credit card billing statetement by google document ai.
        Your job is to skim through its content and return the necessary information.
        The information I want you to return are  "日時", "支払い先", and "金額".
        Format the extracted data in the following json form.
        If there is no valid data passed, generate the empty json object.
        There is no need any description in response.
        {"total_price": int, "billing_date": "yyyy-mm-dd",
            "items": [
                {
                    "日時":"yyyy-mm-dd",
                    "支払い先": string,
                    "金額": int
                },
                {
                    "日時":"yyyy-mm-dd",
                    "支払い先": string,
                    "金額": int
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
        The information I want you to return the following five elements:"日時", "取引内容", "入金", "出金" and "残高".
        The names for each element usually appear at the beginning in the order same as the data that follow.
        Format the data in the following json form.
        If there is no valid data passed, generate the empty json object.
        There is no need any description in response.
        {
            "items": [
                {
                    "日時":"yyyy-mm-dd",
                    "取引内容": string,
                    "入金": int,
                    "出金": int,
                    "残高": int
                }
            ]
        }
        ##DATA
    """
    prompt = base_prompt + "\n" + document_text
    return prompt