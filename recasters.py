import re
import xml.dom.minidom
import json
from urllib.parse import quote, unquote


def clean_sql_log(content):
    try:
        cleaned = content

        # Normalize all incoming line endings to Tkinter-friendly \n
        cleaned = cleaned.replace("\r\n", "\n").replace("\r", "\n")

        regex_match = re.search(r"(?im)^\s*Message\s*$", cleaned)
        if regex_match:
            cleaned = cleaned[regex_match.end():].strip()
        else:
            cleaned = cleaned.strip()

        cleaned = re.sub(r"Executed.*?\d+-\d+\s\d+:\d+:\d+\.\d+\s+", "", cleaned).strip()
        cleaned = re.sub(r"Code:\s\dx.*?\s+", "", cleaned).strip()
        cleaned = re.sub(r"\sEnd\sError\s", "", cleaned).strip()
        cleaned = re.sub(r"Error:.*?\.\d\d\s\s", "", cleaned).strip()

        # If the SQL Agent text uses multiple spaces as separators,
        # convert those runs of spaces/tabs into paragraph breaks.
        # This avoids matching existing line feeds.
        cleaned = re.sub(r"[ \t]{2,}", "\n\n", cleaned).strip()

        cleaned_lines = []

        for line in cleaned.splitlines():
            line = line.strip()
            if not line:
                continue
            if line not in cleaned_lines:
                cleaned_lines.append(line)

        return "\n\n".join(cleaned_lines)

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


def dtsx_decode(dtsx_string):
    try:
        cleaned = dtsx_string
        cleaned = re.sub(r"&#xA;", "\n", cleaned).strip()
        cleaned = re.sub(r"&#xD;", "\r", cleaned).strip()
        cleaned = re.sub(r"&#x9;", "\t", cleaned).strip()
        cleaned = re.sub(r"&#x20;", " ", cleaned).strip()
        cleaned = re.sub(r"&#x26;", "&", cleaned).strip()
        cleaned = re.sub(r"&#x27;", "'", cleaned).strip()
        cleaned = re.sub(r"&#x3C;", "<", cleaned).strip()
        cleaned = re.sub(r"&#x3E;", ">", cleaned).strip()
        cleaned = re.sub(r"&quot;", "\"", cleaned).strip()
        cleaned = re.sub(r"&apos;", "'", cleaned).strip()
        cleaned = re.sub(r"&amp;", "&", cleaned).strip()
        cleaned = re.sub(r"&lt;", "<", cleaned).strip()
        cleaned = re.sub(r"&gt;", ">", cleaned).strip()
        return cleaned
    except Exception as e:
        return f"Error decoding DTSX: {e}"
