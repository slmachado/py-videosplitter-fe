import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os


class VideoSplitterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("VideoSplitter")

        self.video_file = None
        self.output_dir = os.getcwd()

        self.create_widgets()
        self.configure_grid()

    def create_widgets(self):
        self.drag_drop_label = tk.Label(self.root, text="Drag and drop a MP4 file here or click 'Browse'")
        self.drag_drop_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        self.browse_button = tk.Button(self.root, text="Browse", command=self.browse_file)
        self.browse_button.grid(row=1, column=0, padx=10, pady=10)

        self.split_time_label = tk.Label(self.root, text="Split time (seconds):")
        self.split_time_label.grid(row=2, column=0, padx=10, pady=10)

        self.split_time_entry = tk.Entry(self.root)
        self.split_time_entry.grid(row=2, column=1, padx=10, pady=10)

        self.split_button = tk.Button(self.root, text="Split", command=self.split_video)
        self.split_button.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

        self.output_dir_label = tk.Label(self.root, text="Output Directory:")
        self.output_dir_label.grid(row=4, column=0, padx=10, pady=10)

        self.output_dir_entry = tk.Entry(self.root)
        self.output_dir_entry.grid(row=4, column=1, padx=10, pady=10)
        self.output_dir_entry.insert(0, self.output_dir)

        self.output_dir_button = tk.Button(self.root, text="Browse", command=self.browse_output_dir)
        self.output_dir_button.grid(row=4, column=2, padx=10, pady=10)

    def configure_grid(self):
        for i in range(5):
            self.root.grid_rowconfigure(i, weight=1)
            self.root.grid_columnconfigure(i, weight=1)

    def browse_file(self):
        self.video_file = filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4")])
        if self.video_file:
            self.drag_drop_label.config(text=self.video_file)

    def browse_output_dir(self):
        self.output_dir = filedialog.askdirectory()
        if self.output_dir:
            self.output_dir_entry.delete(0, tk.END)
            self.output_dir_entry.insert(0, self.output_dir)

    def split_video(self):
        if not self.video_file:
            messagebox.showerror("Error", "Please select a video file.")
            return

        split_time = self.split_time_entry.get()
        if not split_time.isdigit():
            messagebox.showerror("Error", "Please enter a valid split time in seconds.")
            return

        output1 = os.path.join(self.output_dir, "part1.mp4")
        output2 = os.path.join(self.output_dir, "part2.mp4")

        # Full path to exec
        executavel_rust = "/home/sergio/RustRoverProjects/video_splitter/target/release/video_splitter"

        try:
            subprocess.run([
                executavel_rust,
                self.video_file,
                output1,
                output2,
                split_time
            ], check=True)

            messagebox.showinfo("Success", f"Video successfully split into:\n{output1}\n{output2}")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to split video: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = VideoSplitterApp(root)
    root.mainloop()
