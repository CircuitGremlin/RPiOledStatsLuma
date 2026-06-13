#!/bin/sh

FILENAME="RPiOledStatsLuma.service"

# Disable service
echo "Disable $FILENAME"
sudo sudo systemctl disable $FILENAME

# Remove service
echo "Remove $FILENAME from /lib/systemd/system/"
sudo sudo rm /lib/systemd/system/$FILENAME

# Reload deamon
echo "Reload deamon"
sudo sudo systemctl daemon-reload

# Done
echo "Done!"
