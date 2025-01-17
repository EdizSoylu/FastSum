import tkinter as tk
import pickle
from pathlib import Path
from modules import note_handler, pdf_handler, ifallelsefails


class Project:
    def __init__(self):
        self.pdf_tab = None
        self.note = None

        root = tk.Tk()
        root.title("Fast Summary |  Save feature is broken but hey i added a converter")
        root.configure(background='#35383d')
        root.state('zoomed')
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        self.root = root

        menubar = tk.Menu(root)
        root.config(menu=menubar)

        # Open PDF button
        open_pdf_ = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Open PDF", menu=open_pdf_)
        for f in [f for f in (Path(".") / "PDFs").iterdir()]:
            open_pdf_.add_cascade(label=Path(f).name, command=lambda file=f: self.open_pdf(file))

        # Create new note button
        def enter_name():
            popup = tk.Toplevel(root)
            popup.title("Name")
            popup.geometry("200x50")

            tk.Label(popup, text="Enter Note Name").grid(row=0, column=0)
            entry = tk.Entry(popup, width=30)
            entry.grid(row=1, column=0)

            def get_name(event):
                self.new_note(entry.get())
                popup.destroy()

            entry.bind("<Return>", get_name)

        menubar.add_command(label="New Note", command=enter_name)
        self.new_note("a")

        # Open note button
        open_note_ = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Open Note", menu=open_note_)
        for f in [f for f in (Path(".") / "Notes").iterdir()]:
            open_note_.add_cascade(label=Path(f).name, command=lambda file=f: self.open_note(Path(file).name))

        # Save note button
        menubar.add_command(label="Save Note", command=self.save_note)

        menubar.add_command(label="Converter", command=lambda: ifallelsefails.imhopeless(self.root))

        root.mainloop()


    def open_pdf(self, file_path):
        if self.pdf_tab is not None:
            self.pdf_tab.frame.destroy()
            del self.pdf_tab

        self.pdf_tab = pdf_handler.PDFTab(self.root, file_path)

        if self.note is not None:
            self.pdf_tab.note = self.note

        self.pdf_tab.frame.grid(row=0, column=0, sticky="w")


    def new_note(self, note_name):
        if self.note is not None:
            self.note.note_frame.destroy()
            del self.note

        note = note_handler.Note(self.root, note_name)
        note.note_frame.grid(row=0, column=1, sticky="w")
        self.note = note

        if self.pdf_tab is not None:
            self.pdf_tab.note = self.note


    def open_note(self, name):
        if self.note is not None:
            self.note.note_frame.destroy()
            self.note = None

        with open(Path(".")/"Notes"/name, "rb") as f:
            content = pickle.load(f)
            self.note = note_handler.Note(self.root, name, content)
            self.note.note_frame.grid(row=0, column=0, sticky="e")
            if self.pdf_tab is not None:
                self.pdf_tab.note = self.note


    def save_note(self):
        if self.note is not None:
            with open(Path(".")/"Notes"/(self.note.name+".pkl"), "wb") as file:
                pickle.dump(self.note.contents, file=file)


if __name__ == "__main__":
    project = Project()