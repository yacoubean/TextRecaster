# Text Recaster

**Text Recaster** is a small Windows desktop utility for cleaning, reformatting, and “recasting” pasted text into a more readable form.

The app was built for common developer, database, and reporting workflows where text is often copied from logs, database tools, XML payloads, JSON output, emails, tickets, or chat messages and needs to be cleaned up quickly.

## Features

Text Recaster currently supports:

- **Clean up SQL Agent job logs**
  - Removes repetitive/noisy SQL Agent log fragments
  - Splits dense log text into more readable sections
  - Removes duplicate lines

- **Pretty print XML**
  - Converts compact or unstructured XML into an indented, readable format

- **Pretty print JSON**
  - Converts compact JSON into an indented, readable format
  - Displays parser errors when invalid JSON is provided
  - 
It is not intended to replace full-featured developer tools, SQL formatters, XML editors, or JSON editors. It is meant to be a quick copy/paste cleanup utility.

## Screenshots

### XML Before

Paste unformatted XML into Text Recaster:

<img width="802" height="672" alt="image" src="https://github.com/user-attachments/assets/41e01ed5-616f-49c7-ad05-e38bf6892a51" />

### XML After

Select **Format XML** and click **Process text**:

<img width="800" height="629" alt="image" src="https://github.com/user-attachments/assets/e6f8242a-8da1-4f53-b4a2-005a68cee40a" />

## Download / Run

Download the latest release from the project’s GitHub releases page, unzip the folder, and run:

```text
TextRecaster.exe
