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

Download the [latest release](https://github.com/yacoubean/TextRecaster/releases/download/0.1/TextRecaster-win-x64.zip), unzip the folder, and run:
TextRecaster.exe

If you want to build TextRecaster from source on Windows, a helper PowerShell build script is included:
.\pyinstaller_command.ps1


## Platform Notes

Text Recaster is primarily built and packaged for Windows.

The source code uses Python standard-library modules and Tkinter, so it may also run on macOS or Linux if Python and Tkinter are installed. However, packaged builds are platform-specific. A Windows build cannot be used as a macOS or Linux app; users on those platforms would need to build the app on their own system using PyInstaller.
