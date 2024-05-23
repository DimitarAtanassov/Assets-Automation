from automator import Automator
import csv
import xml.etree.ElementTree as ET
def main():
    automator = Automator()
    # Create a session by logging in
    session_created = automator._create_session(30353894)
    if not session_created:
        return

    all_assets = automator.get_all_assets()

    #Export to csv
    header = all_assets[0].keys() if all_assets else []
    filename= "assets.csv"
   
    # Write assets to CSV file
    with open('assets.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Asset'])  # Write header
        for asset in all_assets:
            xml_string = ET.tostring(asset, encoding='unicode')
            writer.writerow([xml_string])  # Write each asset XML string as a row

    #Close Session
    automator._close_session(30353894)

if __name__ == "__main__":
    main()
