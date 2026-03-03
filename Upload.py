import requests
import base64
import os
import tkinter as tk
from tkinter import filedialog, messagebox

# --- ТВОИ НАСТРОЙКИ ---
GITHUB_TOKEN = "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"
REPO_OWNER = "Romanfoks"
REPO_NAME = "My-git"
# ----------------------

def upload_to_github(file_path):
    file_name = os.path.basename(file_path)
    # GitHub API URL для загрузки файла
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{file_name}"
    
    try:
        with open(file_path, "rb") as f:
            content = base64.b64encode(f.read()).decode("utf-8")
        
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        data = {
            "message": f"Upload {file_name} via Python App",
            "content": content
        }
        
        # Проверяем, есть ли уже такой файл (нужен sha для обновления, но мы просто льем новый)
        response = requests.put(url, json=data, headers=headers)
        
        if response.status_code in [200, 201]:
            messagebox.showinfo("Success", f"Done! {file_name} is now on your site.")
        else:
            error_msg = response.json().get('message', 'Unknown error')
            messagebox.showerror("Error", f"GitHub says: {error_msg}")
            
    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong: {str(e)}")

# Графический интерфейс
root = tk.Tk()
root.title("My-git Video Uploader")
root.geometry("400x200")
root.configure(bg="#0f0f0f")

# Стиль как на сайте
label = tk.Label(root, text="Select video to upload to My-git", 
                 fg="#f1f1f1", bg="#0f0f0f", font=("Roboto", 12), pady=30)
label.pack()

def start_upload():
    path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.mkv *.webm"), ("All files", "*.*")])
    if path:
        label.config(text="Uploading... Please wait", fg="#58a6ff")
        root.update()
        upload_to_github(path)
        label.config(text="Select video to upload to My-git", fg="#f1f1f1")

btn = tk.Button(root, text="CHOOSE FILE", command=start_upload, 
                bg="#238636", fg="white", font=("Roboto", 10, "bold"), 
                padx=20, pady=10, border=0, cursor="hand2")
btn.pack()

root.mainloop()