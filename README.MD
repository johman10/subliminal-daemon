# Subliminal Daemon

I wanted to run Subliminal in a monitoring kind of state so I build this little tool that can run as a python program, so that's what this is.

## Requirements:
 - Pip
 - Python 3.8
 - Unrar

## Installation

1. Create .env file based on .env.example.
1. Install dependecies: `pip install -r requirements.txt`
1. Start with `python app.py`

## Startup script
For Linux there is a startup script available in the repo for systemd.
1. Copy the existing file: `cp subliminal-daemon.example.service subliminal-daemon.service`
2. Edit the file to your liking (user, paths etc)
3. Symlink the startup file to systemd: `ln -s /path/to/subliminal-daemon/subliminal-daemon.service /etc/systemd/system/subliminal-daemon.service`
4. Enable it with: `systemctl enable subliminal-daemon`
5. Start it now with: `systemctl start subliminal-daemon`
