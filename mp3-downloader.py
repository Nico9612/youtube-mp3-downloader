import customtkinter as ctk
import yt_dlp as youtube_dl
import tkinter as tk
from tkinter import filedialog

# Imposta il tema scuro
ctk.set_appearance_mode("dark")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        # Configurazione della finestra principale
        self.geometry("800x200")
        self.title("mp3-Downloader")
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)

        # Aggiunta dei componenti
        # Etichetta
        self.label = ctk.CTkLabel(self, text="Inserire l'URL del video da convertire", fg_color="transparent")
        self.label.grid(row=0, column=1, columnspan=2, pady=10)

        # Casella di testo
        self.entry = ctk.CTkEntry(self, placeholder_text="Inserire URL", width=600, height=40)
        self.entry.grid(row=1, column=1, columnspan=2, padx=20, pady=10)

        # Bottone per selezionare la cartella
        self.folder_button = ctk.CTkButton(self, command=self.select_folder, text="Scegli Cartella", width=150, height=40)
        self.folder_button.grid(row=2, column=3, padx=10, pady=10)

        # Etichetta per mostrare la cartella selezionata
        self.folder_label = ctk.CTkLabel(self, text="", fg_color="transparent")
        self.folder_label.grid(row=2, column=1, padx=10, pady=10)

        # Bottone per scaricare il video
        self.download_button = ctk.CTkButton(self, command=self.download_video, text="SCARICA", width=150, height=40)
        self.download_button.grid(row=1, column=3, padx=10, pady=10)

        # Etichetta per il messaggio di fine download
        self.label_end = ctk.CTkLabel(self, text="", fg_color="transparent")
        self.label_end.grid(row=3, column=1, columnspan=2, pady=10)

        self.download_folder = None

    def select_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.download_folder = folder_selected
            self.folder_label.configure(text=folder_selected)

    def download_video(self):
        print("Downloading...")
        self.label_end.configure(text="")
       
        try:
            video_url = self.entry.get()
            if not self.download_folder:
                self.label_end.configure(text="Seleziona una cartella di destinazione")
                return

            print(video_url)
            video_info = youtube_dl.YoutubeDL().extract_info(url=video_url, download=False)
            filename = f"{video_info['title']}.mp3"
            output_path = f"{self.download_folder}/%(title)s.%(ext)s"
            options = {
                'format': 'bestaudio/best',
                'outtmpl': output_path,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'noplaylist': True,
            }

            with youtube_dl.YoutubeDL(options) as ydl:
                ydl.download([video_url])
            
            self.label_end.configure(text=f"Download di {filename} completato")
        except Exception as e:
            print(e)
            self.label_end.configure(text="Download fallito")

if __name__ == "__main__":
    app = App()
    app.mainloop()
