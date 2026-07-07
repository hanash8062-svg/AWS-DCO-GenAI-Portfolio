import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox

try:
    from yt_dlp import YoutubeDL
except ImportError:
    YoutubeDL = None


def choose_folder():
    folder = filedialog.askdirectory()
    if folder:
        output_folder_var.set(folder)


def write_log(message):
    log_text.insert(tk.END, message + "\n")
    log_text.see(tk.END)


def safe_write_log(message):
    root.after(0, lambda: write_log(message))


def download_video():
    url = url_var.get().strip()
    output_folder = output_folder_var.get().strip()
    rights_checked = rights_var.get()

    if not url:
        messagebox.showwarning("입력 오류", "영상 URL을 입력해 주세요.")
        return

    if not output_folder:
        messagebox.showwarning("입력 오류", "저장 폴더를 선택해 주세요.")
        return

    if not rights_checked:
        messagebox.showwarning(
            "권리 확인 필요",
            "본인 소유 또는 다운로드 허가를 받은 영상만 사용할 수 있습니다."
        )
        return

    if YoutubeDL is None:
        messagebox.showerror(
            "라이브러리 오류",
            "yt-dlp가 설치되어 있지 않습니다.\n\n터미널에서 다음 명령어를 실행해 주세요:\npip install yt-dlp"
        )
        return

    start_button.config(state=tk.DISABLED)
    write_log("다운로드 작업을 시작합니다.")
    write_log("본인 소유 또는 다운로드 허가된 영상만 대상으로 진행합니다.")

    thread = threading.Thread(target=run_download, args=(url, output_folder))
    thread.daemon = True
    thread.start()


def run_download(url, output_folder):
    try:
        output_template = os.path.join(output_folder, "%(title).80s.%(ext)s")

        options = {
            "outtmpl": output_template,
            "format": "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]/best",
            "noplaylist": True,
            "quiet": True,
            "no_warnings": True,
        }

        safe_write_log("URL 정보를 확인하는 중입니다.")

        with YoutubeDL(options) as ydl:
            ydl.download([url])

        safe_write_log("다운로드가 완료되었습니다.")
        root.after(0, lambda: messagebox.showinfo("완료", "다운로드가 완료되었습니다."))

    except Exception as error:
        safe_write_log(f"오류 발생: {error}")
        root.after(0, lambda: messagebox.showerror("오류", f"다운로드 중 오류가 발생했습니다.\n\n{error}"))

    finally:
        root.after(0, lambda: start_button.config(state=tk.NORMAL))


root = tk.Tk()
root.title("한국어 유튜브 영상 저장 도구 - 교육용")
root.geometry("700x520")

url_var = tk.StringVar()
output_folder_var = tk.StringVar()
rights_var = tk.BooleanVar(value=False)

title_label = tk.Label(
    root,
    text="한국어 유튜브 영상 저장 도구",
    font=("맑은 고딕", 16, "bold")
)
title_label.pack(pady=10)

notice_label = tk.Label(
    root,
    text="본 프로그램은 교육용 예제이며, 본인 소유 또는 다운로드 허가를 받은 영상만 대상으로 합니다.",
    fg="red",
    wraplength=650,
    justify="center"
)
notice_label.pack(pady=5)

url_frame = tk.Frame(root)
url_frame.pack(fill="x", padx=20, pady=10)

tk.Label(url_frame, text="영상 URL").pack(anchor="w")
url_entry = tk.Entry(url_frame, textvariable=url_var, width=90)
url_entry.pack(fill="x")

folder_frame = tk.Frame(root)
folder_frame.pack(fill="x", padx=20, pady=10)

tk.Label(folder_frame, text="저장 폴더").pack(anchor="w")
folder_inner = tk.Frame(folder_frame)
folder_inner.pack(fill="x")

folder_entry = tk.Entry(folder_inner, textvariable=output_folder_var, width=70)
folder_entry.pack(side="left", fill="x", expand=True)

folder_button = tk.Button(folder_inner, text="폴더 선택", command=choose_folder)
folder_button.pack(side="left", padx=5)

rights_check = tk.Checkbutton(
    root,
    text="본인 소유 또는 다운로드 허가를 받은 영상만 사용합니다.",
    variable=rights_var
)
rights_check.pack(pady=10)

start_button = tk.Button(
    root,
    text="다운로드 시작",
    command=download_video,
    width=20,
    height=2
)
start_button.pack(pady=10)

log_label = tk.Label(root, text="실행 로그")
log_label.pack(anchor="w", padx=20)

log_text = tk.Text(root, height=10)
log_text.pack(fill="both", expand=True, padx=20, pady=10)

write_log("프로그램이 실행되었습니다.")
write_log("본인 소유 또는 다운로드 허가된 영상만 사용하세요.")

root.mainloop()
