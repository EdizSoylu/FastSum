import tkinter as tk


class Note:
    def __init__(self, root, name, save_content = None):
        self.root = root
        self.note_text = ""
        self.name = name
        self.contents = []

        note_frame = tk.Frame(self.root, relief=tk.SOLID, borderwidth=5)
        self.note_frame = note_frame

        note_canvas = tk.Canvas(note_frame, height=800, width=800, background="#21262c")
        note_canvas.grid(row=0, column=0, sticky=tk.NSEW)
        self.canvas = note_canvas

        if save_content is not None:
            for val in save_content:
                self.add_content(val)


    def add_content(self, content):
        content = [i for i in content]
        self.contents.append(content)
        self.show_content()


    def show_content(self):
        y = 10

        for content in self.contents:

            def save_changes(event):
                content[0] = text_box.get(1.0, tk.END)

            note = content[0]
            text_box = tk.Text(self.canvas, height=int(len(str(note))/90)+1, width=90, wrap=tk.WORD)
            text_box.insert(tk.END, note)
            self.canvas.create_window(10, y, window=text_box, anchor=tk.NW)
            self.root.update_idletasks()
            y += text_box.winfo_height() + 10

            text_box.bind("<Return>", save_changes)