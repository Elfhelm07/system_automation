#auto update applications or selected applications using winget or chocolatey when the current version is less than 2 of new

import subprocess

def get_winget_upgrades():
    try:
        result = subprocess.run(["winget", "upgrade"], capture_output=True, text=True, check=True)
        lines = result.stdout.split('\n')
        header = next(line for line in lines if 'Name' in line and 'Id' in line and 'Version' in line and 'Available' in line)
        name_index = header.index('Name')
        id_index = header.index('Id')
        version_index = header.index('Version')
        available_index = header.index('Available')
        for line in lines[lines.index(header)+1:]:
            if line.strip() and not line.startswith('--'):
                name = line[name_index:version_index].strip()
                id = line[id_index:version_index].strip().replace('¦','').strip()
                version = ''.join(filter(str.isdigit, line[version_index:available_index].strip()))
                available = ''.join(filter(str.isdigit, line[available_index:].strip().split()[0]))
                print(f"Name: {name}, Id: {id}, Version: {version}, Available: {available}")
                upgrade_result = subprocess.run(["winget", "upgrade", id], check=True)
                print(f"Upgrade result for {id}:")
                break
    except subprocess.CalledProcessError as e:
        print(f"Error executing winget upgrade: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    get_winget_upgrades()