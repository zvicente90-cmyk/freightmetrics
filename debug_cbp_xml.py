#!/usr/bin/env python
"""Debug CBP XML structure"""
import requests
import xml.etree.ElementTree as ET

url = 'https://bwt.cbp.gov/api/waittimes'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Accept': 'application/xml, text/xml, */*',
    'Referer': 'https://bwt.cbp.gov/',
}

try:
    print("Fetching CBP XML...")
    resp = requests.get(url, headers=headers, timeout=10)
    root = ET.fromstring(resp.content)
    
    # Find first Laredo port
    for port in root.iter("port"):
        nombre = port.findtext("port_name", "")
        if "Laredo" in nombre:
            print(f"\n=== PORT: {nombre} ===")
            
            # Print all direct children
            print("\nDirect children of <port>:")
            for child in port:
                print(f"  <{child.tag}> = {child.text[:50] if child.text else 'None'}")
                
                # If it's commercial_vehicle_lanes, print its children
                if child.tag == "commercial_vehicle_lanes":
                    print(f"    Children of <{child.tag}>:")
                    for subchild in child:
                        print(f"      <{subchild.tag}> = {subchild.text[:50] if subchild.text else 'None'}")
                        
                        # If standard_lanes, print its children
                        if subchild.tag == "standard_lanes":
                            print(f"        Children of <{subchild.tag}>:")
                            for subsubchild in subchild:
                                print(f"          <{subsubchild.tag}> = {subsubchild.text}")
            break
            
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
