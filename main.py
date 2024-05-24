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

      # Define the CSV file header
    header = [
        'Asset ID', 'Name', 'Created', 'Modified', 'Type', 'Tags', 'Source Location', 
        'VM Size', 'VM ID', 'State', 'OS Type', 'Subnet', 'IPv6', 'Subscription ID', 
        'Resource Group Name', 'MAC Address', 'Private IP Address', 'Virtual Network'
    ]

    filename = "assets.csv"

    # Write assets to CSV file
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)  # Write header
        for asset in all_assets:
            # Extracting data from XML
            asset_id_element = asset.find('.//id')
            asset_id = asset_id_element.text if asset_id_element is not None else ''
            
            name_element = asset.find('.//name')
            name = name_element.text if name_element is not None else ''
            
            created_element = asset.find('.//created')
            created = created_element.text if created_element is not None else ''
            
            modified_element = asset.find('.//modified')
            modified = modified_element.text if modified_element is not None else ''
            
            type_element = asset.find('.//type')
            type_ = type_element.text if type_element is not None else ''
            
            tags_elements = asset.findall('.//TagSimple')
            tags = ', '.join([tag.find('.//name').text for tag in tags_elements]) if tags_elements else ''
            
            source_location_element = asset.find('.//location')
            source_location = source_location_element.text if source_location_element is not None else ''
            
            vm_size_element = asset.find('.//vmSize')
            vm_size = vm_size_element.text if vm_size_element is not None else ''
            
            vm_id_element = asset.find('.//vmId')
            vm_id = vm_id_element.text if vm_id_element is not None else ''
            
            state_element = asset.find('.//state')
            state = state_element.text if state_element is not None else ''
            
            os_type_element = asset.find('.//osType')
            os_type = os_type_element.text if os_type_element is not None else ''
            
            subnet_element = asset.find('.//subnet')
            subnet = subnet_element.text if subnet_element is not None else ''
            
            ipv6_element = asset.find('.//ipv6')
            ipv6 = ipv6_element.text if ipv6_element is not None else ''
            
            subscription_id_element = asset.find('.//subscriptionId')
            subscription_id = subscription_id_element.text if subscription_id_element is not None else ''
            
            resource_group_name_element = asset.find('.//resourceGroupName')
            resource_group_name = resource_group_name_element.text if resource_group_name_element is not None else ''
            
            mac_address_element = asset.find('.//macAddress')
            mac_address = mac_address_element.text if mac_address_element is not None else ''
            
            private_ip_address_element = asset.find('.//privateIpAddress')
            private_ip_address = private_ip_address_element.text if private_ip_address_element is not None else ''
            
            virtual_network_element = asset.find('.//virtualNetwork')
            virtual_network = virtual_network_element.text if virtual_network_element is not None else ''
            
            # Write asset data as a row
            writer.writerow([
                asset_id, name, created, modified, type_, tags, source_location, 
                vm_size, vm_id, state, os_type, subnet, ipv6, subscription_id, 
                resource_group_name, mac_address, private_ip_address, virtual_network
            ])


    #Close Session
    automator._close_session(30353894)

if __name__ == "__main__":
    main()
