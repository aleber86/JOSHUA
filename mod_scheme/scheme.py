
class URL_Converter:
    URL_convert_symbols_to_url = {
                "%":"%25", "!":"%21", "#":"%23", "&":"%26",
               "'":"%27", "(":"%28", ")":"%29", "*":"%2A",
               "+":"%2B", ",":"%2C", "/":"%2F", ":":"%3A",
               ";":"%3B", "=":"%3D", "?":"%3F", "@":"%40",
               "[":"%5B", "]":"%5D", " ":"%20", '"':"%22",
               "-":"%2D", ".":"%2E", "<":"%3C", ">":"%3E",
               "\\":"%5C", "^":"%5E", "_":"%5F", "`":"%60",
        "{":"%7B", "|":"%7C", "}":"}", "~":"%7E","´":"%C2%B4"}


    def Data_text_convert_to_url(self, text_to_convert : str):
        text_raw_string = text_to_convert
        for symbol, code in self.URL_convert_symbols_to_url.items():
            text_raw_string = text_raw_string.replace(symbol, code)
        return text_raw_string


def Data_content(result_object : dict):
    dictionary_defined = {}
    dictionary_defined["update_id"] = result_object["update_id"]
    dictionary_defined["chat_id"] = result_object["message"]["chat"]["id"]
    try:
        dictionary_defined["message_id"] = result_object["message"]["message_id"]
        dictionary_defined["from_id"] = result_object["message"]["from"]["id"]
        dictionary_defined["from_bot"] = result_object["message"]["from"]["is_bot"]
        dictionary_defined["from_name"] = result_object["message"]["from"]["first_name"]
        dictionary_defined["from_language_code"] = result_object["message"]["from"]["language_code"]
        dictionary_defined["chat_name"] = result_object["message"]["chat"]["first_name"]
        dictionary_defined["chat_type"] = result_object["message"]["chat"]["type"]
        dictionary_defined["date"] = result_object["message"]["date"]
        dictionary_defined["text"] = result_object["message"]["text"]
    except KeyError:
        pass
    try:
        dictionary_defined["entity"] = result_object["message"]["entities"]
    except KeyError as error:
        pass
    return dictionary_defined












