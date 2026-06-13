# Update system
echo "Update system"
sudo apt update && sudo apt -y full-upgrade

# Install apt packages
echo "Install apt packages"
sudo apt install -y python3 python3-pip i2c-tools git

# Enable I2C interface
echo "Enable I2C interface"
sudo raspi-config nonint do_i2c 0

# Check the I2C status
echo "Check the I2C status"
sudo i2cdetect -y 1

# Reboot system
echo "Reboot system"
sudo reboot
