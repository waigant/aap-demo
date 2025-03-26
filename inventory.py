#!/usr/bin/env python3
import csv
import json
import sys
import argparse

def parse_csv(file_path):
    # Initialisiere das Inventory im Ansible-Format
    inventory = {"_meta": {"hostvars": {}}}
    
    try:
        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                host = row.get("host")
                if not host:
                    continue  # Falls keine Hostspalte vorhanden ist, überspringen
                
                # Bestimme die Gruppe. Falls keine Gruppe angegeben, wird "ungrouped" genutzt.
                group = row.get("group", "ungrouped")
                if group not in inventory:
                    inventory[group] = {"hosts": []}
                inventory[group]["hosts"].append(host)
                
                # Entferne die Standardspalten "host" und "group" aus den Hostvariablen
                host_vars = {key: value for key, value in row.items() if key not in ["host", "group"]}
                inventory["_meta"]["hostvars"][host] = host_vars
    except FileNotFoundError:
        sys.stderr.write(f"CSV-Datei {file_path} nicht gefunden.\n")
        sys.exit(1)
    except Exception as e:
        sys.stderr.write(f"Fehler beim Einlesen der CSV-Datei: {e}\n")
        sys.exit(1)
    
    return inventory

def main():
    parser = argparse.ArgumentParser(description="Dynamische Inventory-Quelle für Ansible basierend auf CSV-Daten")
    parser.add_argument("--list", action="store_true", help="Gesamte Inventory-Liste ausgeben")
    parser.add_argument("--host", help="Host-spezifische Variablen ausgeben (wird hier nicht verwendet)")
    parser.add_argument("--csv", default="inventory.csv", help="Pfad zur CSV-Datei (Standard: inventory.csv)")
    args = parser.parse_args()
    
    if args.list:
        inventory = parse_csv(args.csv)
        print(json.dumps(inventory, indent=2))
    elif args.host:
        print(json.dumps({}))
    else:
        print(json.dumps({}))

if __name__ == "__main__":
    main()