import re
def check_type(text):
    if text is None or (text.startswith('"') and text.endswith('"')):
        return text
    elif isinstance(text,str):
        return f'"{text}"'
    elif text.lower() == "none":
        return None
    else:
        try:
            result = int(text) if '.' not in text else float(text)
            return result
        except ValueError:
            return ""


def extract_empty_head(input_string):
    match = re.match(r'^(\s*)', input_string)
    if match:
        print(1,match.group(1),1)
        return match.group(1)
    else:
        return ""

