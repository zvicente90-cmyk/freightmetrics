#!/usr/bin/env python
"""Find CBP ports with actual wait time data"""
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
    
    # Find ports with actual wait times
    found = 0
    for port in root.iter("port"):
        if found >= 5:
            break
            
        nombre = port.findtext("port_name", "")
        comercial = port.find("commercial_vehicle_lanes")
        
        if comercial is not None:
            standard = comercial.find("standard_lanes")
            if standard is not None:
                delay = standard.findtext("delay_minutes", "")
                op_status = standard.findtext("operational_status", "")
                
                # Only show ports with actual data
                if delay and delay.strip() and delay != "None":
                    found += 1
                    print(f"\n✅ {nombre}:")
                    print(f"   Delay: {delay} min")
                    print(f"   Status: {op_status}")
                    print(f"   Lanes: {standard.findtext('lanes_open', '')}")
                    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
