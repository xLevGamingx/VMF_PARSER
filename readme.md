# VMF Parser for CS2 Danger Zone Maps

A Python script that parses Valve Map Format (.vmf) files and extracts Danger Zone game mode data into a structured JSON format.

## Features

- **Automatic VMF Detection**: Automatically finds and parses any `.vmf` file in the script directory
- **Weapon Spawn Extraction**: Extracts all `point_dz_weaponspawn` entities with their positions, angles, and security door associations
- **Security Door Mapping**: Parses `dz_door` entities including their target names, models, and open directions
- **Clean JSON Output**: Exports data in a organized JSON format with separate arrays for each entity type

## Output Format

The script generates a JSON file with the following structure:
```json
{
    "WeaponSpawns": [
        {
            "Origin": "x y z",
            "Angles": "pitch yaw roll",
            "GroupId": null,
            "DefaultWeight": "100",
            "DoorName": "door_name or null"
        }
    ],
    "SecurityDoors": [
        {
            "Origin": "x y z",
            "Angles": "pitch yaw roll",
            "TargetName": "door_targetname",
            "OpenDir": "2",
            "Model": "model_path"
        }
    ]
}
```

## Usage

1. Place your `.vmf` file in the same directory as `vmf_parser.py`
2. Run the script:
```bash
   python vmf_parser.py
```
3. The script will generate a JSON file with the same name as your VMF file (e.g., `dz_mapname.vmf` → `dz_mapname.json`)

## Requirements

- Python 3.6+
- No external dependencies (uses only standard library)

## Use Cases

- Creating Danger Zone map configurations
- Analyzing weapon spawn distributions
- Mapping security door locations
- Extracting play area boundaries for custom game modes
