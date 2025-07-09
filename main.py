import os
import shutil
import time
import zipfile
from datetime import datetime, timedelta


def ignore_locked_files(src, names):
    ignored_names = []
    for name in names:
        full_path = os.path.join(src, name)
        try:
            with open(full_path, 'rb'):
                pass  # 尝试打开文件，如果失败就加入忽略列表
        except (IOError, PermissionError):
            ignored_names.append(name)
    return ignored_names


def copy_data():
    source_file = 'C:\\Users\\Administrator\\Desktop\\MCSERVER\\world'
    destination_folder = 'C:\\Users\\Administrator\\Desktop\\MCDataBakckUp\\'
    if os.path.exists(destination_folder):
        shutil.rmtree(destination_folder)
    shutil.copytree(source_file, destination_folder, ignore=ignore_locked_files)


def compress_folder(source_folder, output_zip):
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_folder):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, os.path.dirname(source_folder))
                try:
                    zipf.write(
                        file_path,
                        arcname)
                except Exception as e:
                    print(f"⚠️ 跳过文件: {file_path} | 错误: {e}")
    print(f"✅ 压缩完成: {output_zip}")


def cleanup_old_backups(folder_path):
    now = datetime.now()
    files = [f for f in os.listdir(folder_path) if f.endswith('.zip')]
    for file in files:
        try:
            # 提取文件名中的时间戳部分，格式为 'YYYY-MM-DD-HH-MM-SS'
            timestamp_str = file.split('.')[0]  # 去掉 .zip 后缀
            file_time = datetime.strptime(timestamp_str, "%Y-%m-%d-%H-%M-%S")
            delta = now - file_time
            # 按照规则保留：
            if delta <= timedelta(days=1):
                continue  # 保留所有 <1天 的备份

            if delta <= timedelta(days=7):
                # 只保留每4小时一次的备份
                if file_time.hour % 4 != 0:
                    os.remove(os.path.join(folder_path, file))
                    print(f"🗑️ 删除非4小时粒度备份: {file}")
                continue

            if delta <= timedelta(days=30):
                # 只保留每12小时一次的备份
                if file_time.hour % 12 != 0:
                    os.remove(os.path.join(folder_path, file))
                    print(f"🗑️ 删除非12小时粒度备份: {file}")
                continue

            if delta > timedelta(days=30):
                # 只保留每天一次的备份（例如中午12点）
                if file_time.hour != 12:
                    os.remove(os.path.join(folder_path, file))
                    print(f"🗑️ 删除非每日粒度备份: {file}")
                continue

        except Exception as e:
            print(f"⚠️ 无法解析文件名时间: {file}, 错误: {e}")


def main():
    source_folder = 'C:\\Users\\Administrator\\Desktop\\MCSERVER\\world'
    backup_folder = 'C:\\Users\\Administrator\\Desktop\\MCDataBakckUp'
    while True:
        output_zip = 'C:\\Users\\Administrator\\Desktop\\MCDataBakckUp\\' + time.strftime("%Y-%m-%d-%H-%M-%S",
                                                                                          time.localtime()) + '.zip'
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(f"当前时间: {current_time}")
        compress_folder(source_folder, output_zip)

        cleanup_old_backups(backup_folder)
        time.sleep(60 * 60)


if __name__ == '__main__':
    main()
