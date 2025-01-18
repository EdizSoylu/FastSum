import tkinter as tk
import pymupdf


class PDFTab:
    def __init__(self, root, name):
        self.root = root
        self.name = name
        self.p_no = 0
        self.ref_display_height = 0

        # Note instance
        self.note = None

        # For text extraction
        self.canvas = None
        self.rect = None
        self.start_x = self.start_y = 0
        self.scale_factor = 1.0

        doc = pymupdf.open(self.name)
        self.p_max = len(doc)
        self.ref_display_height = doc[self.p_no].get_pixmap().height
        doc.close()

        # Parent frame for everything
        self.frame = tk.Frame(self.root, borderwidth=5, relief=tk.SOLID)

        # Frame to display pdf page
        self.display = tk.Frame(self.frame)
        self.display.grid(row=0, column=0)

        # Canvas to display references
        self.ref_display = tk.Canvas(self.frame, width=5, height=self.ref_display_height)
        self.ref_display.grid(row=0, column=1)

        # Toolbar for pdf navigation
        self.toolbar = tk.Frame(self.frame)
        self.toolbar.grid(row=1, column=0)

        # Event to run when in page number box
        def on_enter(event):
            user_input = int(self.pno_box.get())
            self.change_page(user_input-1-self.p_no)
            self.pno_box.delete(0, tk.END)
            self.pno_box.insert(0, str(self.p_no+1))

        # Page number box
        self.pno_box = tk.Entry(self.toolbar, width=3)
        self.pno_box.bind('<Return>', on_enter)
        self.pno_box.grid(row=0, column=2)

        # Previous page button
        self.prev_page = tk.Button(self.toolbar, text="<", command=lambda: self.change_page(-1))
        self.prev_page.grid(row=0, column=0)

        # Next page button
        self.next_page = tk.Button(self.toolbar, text=">", command=lambda: self.change_page(1))
        self.next_page.grid(row=0, column=1)

        # Display initial page
        self.change_page(self.p_no)


    def change_page(self, i):
        if 0 <= self.p_no + i < self.p_max:
            self.p_no = self.p_no + i

        # Update page number bar
        self.pno_box.delete(0, tk.END)
        self.pno_box.insert(0, str(self.p_no+1))

        # Display currently selected page
        self.display_page()

        if self.note is not None:
            self.display_refs()


    def display_page(self):
        doc = pymupdf.open(self.name)
        page = doc[self.p_no]
        rect = page.rect
        p_width, p_height = rect.width, rect.height
        pix = page.get_pixmap()
        self.ref_display_height = pix.height
        imgdata = pix.tobytes("ppm")
        tkimg = tk.PhotoImage(data=imgdata)
        doc.close()

        self.canvas = tk.Canvas(self.frame, bg='gray', width=p_width, height=p_height)
        self.canvas.create_image(0, 0, image=tkimg, anchor=tk.NW)
        self.canvas.image = tkimg
        self.get_text_in_doc()
        self.canvas.grid(row=0, column=0)


    def get_text_in_doc(self):
        # Initializes text extraction from drawn box utility

        def on_mouse_down(event):
            self.start_x = event.x
            self.start_y = event.y

            self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red')

        def on_mouse_drag(event):
            self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)

        def on_mouse_up(event):
            x1, y1, x2, y2 = self.canvas.coords(self.rect)

            pdf_x1 = x1 * self.scale_factor
            pdf_x2 = x2 * self.scale_factor
            pdf_y1 = y1 * self.scale_factor
            pdf_y2 = y2 * self.scale_factor

            pdf_rect = pymupdf.Rect(pdf_x1, pdf_y1, pdf_x2, pdf_y2)

            doc = pymupdf.open(self.name)
            page = doc[self.p_no]
            text = page.get_text("text", clip=pdf_rect).replace("\n", " ")
            doc.close()

            ref = (self.name, self.p_no, (y1, y2))

            self.canvas.delete(self.rect)

            content = (text, ref)

            if self.note is not None:
                self.note.add_content(content)
                self.display_refs()

        self.canvas.bind("<ButtonPress-1>", on_mouse_down)
        self.canvas.bind("<B1-Motion>", on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", on_mouse_up)


    def display_refs(self):
        self.ref_display.delete("all")
        for val in self.note.contents:
            if val[1][0] == self.name and val[1][1] == self.p_no:
                self.ref_display.create_rectangle(0, val[1][2][0], 5, val[1][2][1], outline='red', fill='red')