import re
import json
from typing import List, Dict, Any

class VMFParser:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.weapon_spawns = []
        self.security_doors = []
        
    def parse(self) -> Dict[str, List[Dict[str, Any]]]:
        """Parse VMF file and extract weapon spawns and security doors"""
        with open(self.filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Find all entity blocks
        entity_pattern = r'entity\s*\{([^}]*(?:\{[^}]*\}[^}]*)*)\}'
        entities = re.findall(entity_pattern, content, re.DOTALL)
        
        for entity_block in entities:
            self._parse_entity(entity_block)
        
        return {
            "WeaponSpawns": self.weapon_spawns,
            "SecurityDoors": self.security_doors
        }
    
    def _parse_entity(self, block: str):
        """Parse individual entity block"""
        # Extract key-value pairs
        kv_pattern = r'"([^"]+)"\s+"([^"]*)"'
        matches = re.findall(kv_pattern, block)
        
        entity_dict = {key: value for key, value in matches}
        classname = entity_dict.get('classname', '')
        
        # Parse weapon spawns
        if classname == 'point_dz_weaponspawn':
            weapon_spawn = {
                "Origin": entity_dict.get('origin', ''),
                "Angles": entity_dict.get('angles', ''),
                "GroupId": None,
                "DefaultWeight": int(entity_dict.get('DefaultWeight', '100')),
                "DoorName": entity_dict.get('is_security_door', None) if entity_dict.get('is_security_door') else None
            }
            self.weapon_spawns.append(weapon_spawn)
        
        # Parse security doors
        elif classname == 'dz_door':
            security_door = {
                "Origin": entity_dict.get('origin', ''),
                "Angles": entity_dict.get('angles', ''),
                "TargetName": entity_dict.get('targetname', ''),
                "OpenDir": entity_dict.get('OpenDir', '2'),
                "Model": entity_dict.get('model', '')
            }
            self.security_doors.append(security_door)
    
    def to_json(self, output_file: str = None) -> str:
        """Export parsed data to JSON format"""
        data = {
            "WeaponSpawns": self.weapon_spawns,
            "SecurityDoors": self.security_doors
        }
        json_data = json.dumps(data, indent=4)
        
        if output_file:
            with open(output_file, 'w') as f:
                f.write(json_data)
        
        return json_data
    
    def print_summary(self):
        """Print summary of parsed entities"""
        print(f"Weapon Spawns found: {len(self.weapon_spawns)}")
        print(f"Security Doors found: {len(self.security_doors)}")
        
        # Count weapon spawns with security doors
        spawns_with_doors = sum(1 for ws in self.weapon_spawns if ws['DoorName'])
        print(f"Weapon Spawns with security doors: {spawns_with_doors}")


# Example usage
if __name__ == "__main__":
    import os
    import glob
    
    # Find all .vmf files in the current directory
    vmf_files = glob.glob("*.vmf")
    
    if not vmf_files:
        print("Error: No .vmf files found in the current directory!")
        print("Please place a .vmf file in the same folder as this script.")
        input("Press Enter to exit...")
        exit(1)
    
    print(f"Found {len(vmf_files)} VMF file(s): {', '.join(vmf_files)}")
    print("="*50)
    
    # Process each VMF file
    for vmf_file in vmf_files:
        print(f"\nProcessing: {vmf_file}")
        print("="*50)
        
        # Parse VMF file
        parser = VMFParser(vmf_file)
        data = parser.parse()
        
        # Print summary
        parser.print_summary()
        
        # Print sample data
        print("\n" + "="*50)
        print("Sample Weapon Spawns (first 3):")
        print("="*50)
        for i, spawn in enumerate(data["WeaponSpawns"][:3], 1):
            print(f"\nWeapon Spawn {i}:")
            for key, value in spawn.items():
                print(f"  {key}: {value}")
        
        print("\n" + "="*50)
        print("Sample Security Doors (first 3):")
        print("="*50)
        for i, door in enumerate(data["SecurityDoors"][:3], 1):
            print(f"\nSecurity Door {i}:")
            for key, value in door.items():
                print(f"  {key}: {value}")
        
        # Export to JSON (use the same name as the VMF file)
        output_name = os.path.splitext(vmf_file)[0] + ".json"
        parser.to_json(output_name)
        print("\n" + "="*50)
        print(f"Exported to {output_name}")
        print("="*50)
    
    print(f"\n\nAll done! Processed {len(vmf_files)} file(s).")
    input("\nPress Enter to exit...")