import os
import paramiko
from scp import SCPClient
from tkinter import filedialog, Tk

import time

# вроде бы, тут просто доп. оболочка, чтобы можно было запустить программу start.py.
def main():
    # --- Настройки подключения ---
    SERVER_IP = '80.90.178.157'
    USERNAME = 'root'
    PASSWORD = 'cD#xE?aZ5+dGje'  # Или используй ключ, если хочешь
    REMOTE_DIR = '/www/parserrr/'

    # --- Выбор файла ---
    root = Tk()
    root.withdraw()
    root.lift()
    root.update_idletasks()
    root.geometry('+500+300')  # X=500, Y=300 — примерно центр экрана
    root.attributes('-topmost', True)
    root.after(100, lambda: root.attributes('-topmost', False))  # вернуть обычное поведение
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    root.destroy()

    if not file_path:
        print("Файл не выбран.")
        exit(1)

    file_name = os.path.basename(file_path)

    # --- SSH + SCP ---
    print(f"Подключаемся к {SERVER_IP} и передаём файл {file_name}...")


    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(SERVER_IP, username=USERNAME, password=PASSWORD)
    ssh.get_transport().set_keepalive(30)

    # Передача файла
    with SCPClient(ssh.get_transport()) as scp:
        scp.put(file_path, os.path.join(REMOTE_DIR, file_name))

    print("Файл передан. Запускаем парсер...")
    # чтобы посмотреть OOM: dmesg | grep -i 'oom\|kill'. Это происходит из-за того, что ты сохраняешь результаты в RAM, а не сразу записываешь в файл.
    # --- Команды на сервере ---
    commands = f"""
    cd {REMOTE_DIR}
    exec ./venv/bin/python3 start.py {file_name}
    """

    stdin, stdout, stderr = ssh.exec_command(commands)

    # Ждём завершения команды
    while not stdout.channel.exit_status_ready():
        time.sleep(1)

    # Теперь можно безопасно читать
    print("--- STDOUT ---")
    print(stdout.read().decode())
    print("--- STDERR ---")
    print(stderr.read().decode())
    time.sleep(20)
    # --- Запрос папки для сохранения merged.csv ---
    # Явно создаём и настраиваем окно
    save_root = Tk()
    save_root.withdraw()
    save_root.lift()
    save_root.update_idletasks()
    save_root.geometry('+500+300')  # X=500, Y=300 — примерно центр экрана
    save_root.attributes('-topmost', True)
    save_root.after(100, lambda: save_root.attributes('-topmost', False))  # вернуть обычное поведение
    local_save_dir = filedialog.askdirectory(parent=save_root, title="Выберите папку для сохранения результата")
    save_root.destroy()


    if not local_save_dir:
        print("Папка не выбрана, скачивание пропущено.")
    else:
        remote_result_file = os.path.join(REMOTE_DIR, 'merged.csv')
        local_result_path = os.path.join(local_save_dir, 'merged.csv')

        with SCPClient(ssh.get_transport(), socket_timeout=3000) as scp:
            print("Скачиваем merged.csv...")
            scp.get(remote_result_file, local_result_path)

        print(f"Файл merged.csv сохранён в: {local_result_path}")

    ssh.close()
if __name__ == '__main__':
    main()
