# Qualys Asset Automation Script

This Python script automates the retrieval of assets from Qualys using the Qualys API. It retrieves assets with a specific tag name and exports the asset information to a CSV file.

## Prerequisites

Before running the script, ensure you have the following:

- Python 3.x installed on your system.
- Necessary Python libraries installed (`requests`, `xml.etree.ElementTree`, `concurrent.futures`, `time`, `csv`).

## Usage

1. Clone the repository or download the `automator.py` script.
2. Open the `automator.py` file and provide your Qualys credentials (`qualys_username` and `qualys_password`) and the Qualys API URL (`qualys_guard_url`).
3. Update the tag name in the `get_all_assets` method if needed.
4. Manually set the total asset count if required.
5. Run the script:

    ```bash
    python automator.py
    ```

6. The script will prompt you to enter the asset count.
7. After execution, the script will generate an `assets.csv` file containing asset information.

## Configuration

- `qualys_username`: Enter your Qualys username.
- `qualys_password`: Enter your Qualys password.
- `qualys_guard_url`: Enter the Qualys API URL.
- `search_assets_url`: URL for searching assets.

## File Structure

- `automator.py`: Main Python script.
- `assets.csv`: CSV file containing asset information.

## License

This project is licensed under the [MIT License](LICENSE).
