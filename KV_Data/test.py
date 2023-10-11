import subprocess
import time

# Hàm để gửi lệnh ADB từ Python
def run_adb_command(command):
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Lỗi khi thực hiện lệnh ADB: {e}")

# Hàm để mở ứng dụng Camera
def open_camera():
    run_adb_command("adb shell am start -a android.media.action.IMAGE_CAPTURE")

# Hàm để chụp ảnh
def take_photo():
    run_adb_command("adb shell input keyevent KEYCODE_CAMERA")

# Hàm để quay video
def start_video_recording():
    run_adb_command("adb shell am start -a android.media.action.VIDEO_CAPTURE")
    time.sleep(2)
    run_adb_command("adb shell input keyevent KEYCODE_CAMERA")

# Hàm để dừng quay video
def stop_video_recording():
    run_adb_command("adb shell input keyevent KEYCODE_CAMERA")

# Mở ứng dụng Camera
open_camera()
time.sleep(5)  # Chờ một chút để ứng dụng Camera mở

# Chụp ảnh
take_photo()
time.sleep(5)  # Chờ một chút để hoàn thành việc chụp ảnh

# Bắt đầu quay video
start_video_recording()
time.sleep(10)  # Quay video trong 5 giây

# Dừng quay video
stop_video_recording()
time.sleep(5)  # Chờ một chút để dừng quay video

print("Hoàn thành")
