# Tableau User Filter Automation 🔄

Automate the tedious process of creating user filters in Tableau, simply by converting between XML and CSV formats.

> **Important** Please ensure you have a backup of your Tableau workbook before making any changes. If you have questions, please open an issue in this repository.

> **🎥** Watch the introductory video on [YouTube](https://youtu.be/pQrJjdo_f2w).

## Installation 📥

`Tableau User Filter Automation` requires Python 3.6 or higher. If you don't have Python installed, you can download it from [here](https://www.python.org/downloads/).

After you've installed Python, you can set up the Tableau User Filter Automation by following these steps:

```bash
git clone https://github.com/YourUsername/TableauUserFilterAutomation.git
cd TableauUserFilterAutomation

# Install requirements (if any)
 pip install -r requirements.txt

```

No additional libraries are required as the scripts use Python's standard libraries.

## Usage 🛠️

### Converting XML to CSV

1. Open your Tableau workbook (.twb file) in a text editor
2. Locate the user filter XML section and save it as `access.xml`
3. Run the XML to CSV script:

    ```bash
    python xml_to_csv_script.py
    ```

4. Find the resulting CSV file at `output.csv`

### Converting CSV to XML

1. Prepare your CSV file with user permissions data (use `output.csv` as a template)
2. Run the CSV to XML script:

    ```bash
    python csv_to_xml_script.py
    ```

3. Find the resulting XML file at `testaccess.xml`
4. Copy the generated XML and paste it back into your Tableau workbook file, replacing the original user filter XML snippet

## File Formats 📄

### CSV Format

The CSV file should have the following structure:

```csv
Member,Set1,Set2
user1,Permission1,Permission2
user2,Permission3,Permission4
```

### XML Format

The XML format follows Tableau's structure for user filters. Our scripts handle the specific formatting required by Tableau, including namespaces and special characters.

## Customization 🔧

You can customize various aspects of the scripts:

- In the CSV to XML script, modify these variables to match your Tableau workbook's configuration:
  
  ```python
  filter_name = "[User Filter 1]"
  primary_group_function = "intersection"
  secondary_group_function = "level-members"
  secondary_group_level = "DIVISION"
  ```

- Adjust the `create_iscurrentuser_expression` function if your user domain differs from the default "www.google.com".

## Troubleshooting 🔍

- Ensure your input files are correctly formatted and located in the same directory as the scripts.
- Check that the file paths in the scripts match your actual file names.
- If you encounter XML parsing errors, make sure your Tableau workbook XML is well-formed and doesn't contain any special characters that might interfere with parsing.

For any additional issues or questions, please open an issue in this repository.

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.

## License 📜

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
