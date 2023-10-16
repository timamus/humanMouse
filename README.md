# humanMouse

A script written in Python to cheat time-keeping programs such as CrocoTime. Bezier curves are used to simulate the movement of the mouse cursor.

## Quick start

- `sudo apt update && sudo apt install -y git`
- `git clone https://github.com/timamus/humanMouse.git`
- `cd humanMouse/`
- `find ./ -name "*.sh" -exec chmod +x {} \;`
- `python3 -m venv venv`
- `source venv/bin/activate`
- `pip install -r requirements.txt`
- `deactivate`

## Creating a .desktop File

To create a `.desktop` file that will be accessible from your Linux distribution’s application menu, execute the following commands in the terminal:

```bash
# Ensure the necessary directory exists
mkdir -p ~/.local/share/applications/

# Create or overwrite the .desktop file with the content you provided
cat > ~/.local/share/applications/HumanMouse.desktop << EOF
[Desktop Entry]
Name=Human Mouse
Exec=/home/test/humanMouse/run_humanMouse.sh
Icon=system-icon-name
Type=Application
Terminal=true
Categories=Utility;
EOF
```

This script first ensures that the ~/.local/share/applications/ directory exists. Then it creates or overwrites the HumanMouse.desktop file in that directory with the content you specified. After executing these commands, "Human Mouse" should be accessible from your application menu.
