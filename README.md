# Text Recaster

**Text Recaster** is a small Windows desktop utility for cleaning, reformatting, and “recasting” pasted text into a more readable form.

The app was built for common developer, database, and reporting workflows where text is often copied from logs, database tools, XML payloads, JSON output, emails, tickets, or chat messages and needs to be cleaned up quickly.

## Features

Text Recaster currently supports:

- **Clean up SQL Agent job logs**
  - Removes repetitive/noisy SQL Agent log fragments
  - Splits dense log text into more readable sections
  - Removes duplicate lines

- **Decode SQL from SSIS DTSX files**
  - SQL in DTSX files has white space and special characters encoded to be compatible as an XML string. This decodes all that so you can easily read the SQL copied from a DTSX file.

- **Pretty print XML**
  - Converts compact or unstructured XML into an indented, readable format

- **Pretty print JSON**
  - Converts compact JSON into an indented, readable format
  - Displays parser errors when invalid JSON is provided
 
- **URL Decode and Encode**
  - Decode percent encoded URLs so to be easily readable, or encode them.

It is not intended to replace full-featured developer tools, SQL formatters, XML editors, or JSON editors. It is meant to be a quick copy/paste cleanup utility.

## Screenshots

### DTSX SQL Before

<img width="801" height="717" alt="image" src="https://github.com/user-attachments/assets/1e97078a-fc69-4212-9695-f4eb3ed988bd" />

### DTSX SQL After

Select **DTSX SQL Decode** and click **Process text**:

<img width="802" height="632" alt="image" src="https://github.com/user-attachments/assets/d9ffc584-a690-4347-aeba-504a548692fe" />


## Download / Run

Download the [latest release](https://github.com/yacoubean/TextRecaster/releases/), unzip the folder, and run:
TextRecaster.exe

If you want to build TextRecaster from source on Windows, a helper PowerShell build script is included:
.\pyinstaller_command.ps1


## Platform Notes

Text Recaster is primarily built and packaged for Windows.

The source code uses Python standard-library modules and Tkinter, so it may also run on macOS or Linux if Python and Tkinter are installed. However, packaged builds are platform-specific. A Windows build cannot be used as a macOS or Linux app; users on those platforms would need to build the app on their own system using PyInstaller.
