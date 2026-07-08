import re
import xml.dom.minidom
import json
from urllib.parse import quote, unquote


def clean_sql_log(content):
    try:
        cleaned = content
        regex_match = re.search(r"(?im)^\s*Message\s*$", cleaned)
        if regex_match:
            cleaned = cleaned[regex_match.end():].strip()
        else:
            cleaned = cleaned.strip()

        cleaned = re.sub("Executed.*?\\d+-\\d+\\s\\d+:\\d+:\\d+\\.\\d+\\s+", "", cleaned).strip()
        cleaned = re.sub("Code:\\s\\dx.*?\\s+", "", cleaned).strip()
        cleaned = re.sub("\\sEnd\\sError\\s", "", cleaned).strip()
        cleaned = re.sub("Error:.*?\\.\\d\\d\\s\\s", "", cleaned).strip()
        cleaned = re.sub("\\s\\s", "\r\n\r\n", cleaned).strip()

        cleaned_lines = ""
        # loop over each line from the input
        for line in cleaned.splitlines():
            if cleaned_lines.find(line.strip()) == -1:  # remove duplicates
                # trim extra whitspace and add two line breaks back to the end of each line
                cleaned_lines += line.strip() + "\r\n\r\n"
        return cleaned_lines.strip()
    except Exception as e:
        return f"Error parsing SQL Agent log: {e}"


def format_xml(xml_string):
    try:
        # Parse the XML string and pretty print it
        dom = xml.dom.minidom.parseString(xml_string)
        pretty_xml_as_string = dom.toprettyxml(indent="   ")
        return pretty_xml_as_string.strip()
    except Exception as e:
        return f"Error formatting XML: {e}"


def format_json(json_string):
    try:
        # Parse the JSON string and pretty print it
        parsed_json = json.loads(json_string)
        pretty_json_as_string = json.dumps(parsed_json, indent=3)
        return pretty_json_as_string.strip()
    except Exception as e:
        return f"Error formatting JSON: {e}"


def url_decode(url_string):
    try:
        return unquote(url_string)
    except Exception as e:
        return f"Error decoding URL: {e}"


def url_encode(url_string):
    try:
        if url_string.find('?'):
            query_string_start = url_string.find('?') + 1
            base_url = url_string[:query_string_start]
            query_string = url_string[query_string_start:]
            encoded_query_string = quote(query_string, safe='=&')
            return base_url + encoded_query_string
        else:
            return quote(url_string, safe='=&')
    except Exception as e:
        return f"Error encoding URL: {e}"
