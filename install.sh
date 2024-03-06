#!/bin/bash

# links:
# no output: https://stackoverflow.com/questions/18062778/how-to-hide-command-output-in-bash
# python to sh: https://trstringer.com/python-in-shell-script/
# goto: https://stackoverflow.com/questions/9639103/is-there-a-goto-statement-in-bash
# if in one line: https://andreyex.ru/linux/kak-proverit-uspeshnost-vypolneniya-komandy-v-bash/

wget -q --tries=10 --timeout=20 --spider http://google.com
if [ $? -eq 0 ]; then
    echo "Установка необходимых зависимостей..."
    # python3 -m Tkinter
    {
    sudo apt update
    sudo apt install python3-tk -y
    sudo apt install python3-pip -y
    pip3 install pillow
    sudo apt install python3-pil python3-pil.imagetk -y
    pip3 install pygame
    sudo apt-get install libbluetooth-dev
    pip install git+https://github.com/pybluez/pybluez.git #egg=pybluez
    } &> /dev/null
    echo "Необходимые зависимости установлены"
else
    echo "ОШИБКА: Отсутствует подключение к интернету, необходимые зависимости НЕ БУДУТ установлены!!!"
fi

echo "Создаем файл-ярлык, для запуска программы..."
{
PYCMD=$(cat <<EOF
file = open("avocado_linux_run.desktop",'w')
file.write("[Desktop Entry]\n")
file.write("Version=1.0\n")
file.write("Type=Application\n")
file.write("Terminal=true\n")
file.write("Icon=mate-panel-launcher\n")
file.write("Icon[ru]=mate-panel-launcher\n")
file.write("Name[ru]=avocado_linux_run\n")
def test_line(a):
    if " " in a: a = '\'' + a + '\''
    return a
import os
path = os.path.abspath("src/main.py")
path = '/'.join(map(test_line, path.split("/")))
file.write(f"Exec=python3 {path}\n")
file.write("Name=test\n")
file.close()

EOF
)
python3 -c "$PYCMD"
sudo chmod +x avocado_linux_run.desktop
} &> /dev/null
echo "Файл-ярлык создан, конец"







