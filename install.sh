# python3 -m Tkinter
sudo apt-get install python3-tk -y
sudo apt install python3-pip -y
pip3 install pillow
sudo apt-get install python3-pil python3-pil.imagetk -y
pip3 install pygame
# python3 main.py
echo "[Desktop Entry]" > avocado_linux_run.desktop
echo "Version=1.0" >> avocado_linux_run.desktop
echo "Type=Application" >> avocado_linux_run.desktop
echo "Terminal=true" >> avocado_linux_run.desktop
echo "Icon=mate-panel-launcher" >> avocado_linux_run.desktop
echo "Icon[ru]=mate-panel-launcher" >> avocado_linux_run.desktop
echo "Name[ru]=avocado_linux_run" >> avocado_linux_run.desktop
echo "Exec=python3 $( dirname -- "$( readlink -f -- "$0"; )"; )/src/main.py" >> avocado_linux_run.desktop # echo "dirname/readlink: $( dirname -- "$( readlink -f -- "$0"; )"; )"
echo "Name=test" >> avocado_linux_run.desktop
#gio set avocado_linux_run.desktop "metadata::trusted" yes
sudo chmod +x avocado_linux_run.desktop








