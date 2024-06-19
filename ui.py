import tkinter as tk
from tkinter import colorchooser, filedialog, ttk

from PIL import Image, ImageDraw, ImageFont, ImageTk

from font_names import font_names

BG_COLOR_SCREEN = "#95D2B3"
BG_COLOR = "#F1F8E8"
TXT_COLOR = "#55AD9B"
UI_FONT = ("Arial", 18, "bold")
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
HEADER_HEIGHT = 50
BODY_CANVAS_HEIGHT = WINDOW_HEIGHT - (HEADER_HEIGHT * 2)
SIDEBAR_WIDTH = 350


class WatermarkAppUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Protect Your Work!")
        self.window.config(
            bg=BG_COLOR_SCREEN,
            padx=10,
            pady=10,
            width=WINDOW_WIDTH,
            height=WINDOW_HEIGHT,
        )
        self.create_canvases()

        self.exit_button = tk.Button(
            self.window,
            text="Exit Program",
            command=self.exit_program,
            highlightbackground=BG_COLOR_SCREEN,
        )
        self.exit_button.grid(row=0, column=0, pady=10)

        self.file_button = tk.Button(
            self.window,
            text="Select File",
            command=self.ask_for_filename,
            highlightbackground=BG_COLOR_SCREEN,
        )
        self.file_button.grid(row=0, column=3)

        self.watermark_inst_text = self.sidebar_canvas.create_text(
            SIDEBAR_WIDTH / 2,
            60,
            text="Upload Image To Config Watermark",
            fill=BG_COLOR_SCREEN,
            font=UI_FONT,
            justify="center",
        )

        self.config_watermark_button = tk.Button(
            self.window,
            text="Configure Watermark",
            command=self.config_watermark,
            highlightbackground=BG_COLOR_SCREEN,
            bg=BG_COLOR,
        )
        self.config_watermark_button.grid(row=0, column=5)

        self.window.mainloop()

    def exit_program(self):
        self.window.destroy()

    def ask_for_filename(self):
        self.original_filename = filedialog.askopenfilename()
        self.open_image_file()

    def ask_for_filename_to_save(self):
        self.new_filename = filedialog.asksaveasfilename()
        self.save_watermarked_file()

    def open_image_file(self):
        try:
            self.original_img = Image.open(self.original_filename)
        except IsADirectoryError or FileNotFoundError:
            print("Not possible to open file")
            return
        else:
            self.show_scaled_img()

    def save_watermarked_file(self):
        self.original_img.save(self.new_filename)

    def show_scaled_img(self):
        self.copy_img = self.original_img.copy()
        self.display_img = ImageTk.PhotoImage(self.copy_img)
        h = self.display_img.height()
        w = self.display_img.width()
        print(self.display_img.height())
        if h > WINDOW_HEIGHT or w > WINDOW_WIDTH:
            h_ratio = h / WINDOW_HEIGHT
            w_ratio = w / WINDOW_WIDTH
            scaling_ratio = max(h_ratio, w_ratio)
            self.new_h = int(round(h / scaling_ratio, 0))
            self.new_w = int(round(w / scaling_ratio, 0))
            self.tmp_img = self.copy_img.resize((self.new_h, self.new_w))
            self.display_img = ImageTk.PhotoImage(self.tmp_img)
            print("large image, need to resize")
        self.img_canvas.create_image(0, 0, image=self.display_img, anchor="nw")

    def create_canvases(self):
        self.img_canvas = tk.Canvas(
            width=WINDOW_WIDTH - SIDEBAR_WIDTH,
            height=BODY_CANVAS_HEIGHT,
            bg=BG_COLOR,
        )
        self.img_canvas.grid(row=1, column=0, columnspan=6, rowspan=7)
        self.sidebar_canvas = tk.Canvas(
            width=SIDEBAR_WIDTH,
            height=BODY_CANVAS_HEIGHT,
            bg=BG_COLOR,
        )
        self.sidebar_canvas.grid(row=1, column=6, rowspan=7, padx=20, pady=20)

    def pick_color(self):
        self.selected_color = colorchooser.askcolor()[0]
        if self.selected_color:
            return

    def create_font_selection(self):
        self.font_name_option = ttk.Combobox(
            self.window,
            width=27,
            state="readonly",
        )
        self.font_dict = {i.split(".")[0]: i for i in font_names}
        font_opts = list(self.font_dict.keys())
        # Adding combobox drop down list
        self.font_name_option["values"] = font_opts
        self.font_name_option.grid(row=3, column=6)

        # Can't get the default to work?
        self.font_name_option.current(5)

        # Create slider to select font size
        self.font_size_slider = tk.Scale(
            self.window,
            from_=40,
            to=1000,
            orient=tk.HORIZONTAL,
        )
        self.font_size_slider.set(90)
        self.font_size_slider.grid(row=4, column=6)

        # Create color choosing dialog
        self.color_button = tk.Button(
            self.window,
            text="Choose a color for your watermark",
            command=self.pick_color,
        )
        self.color_button.grid(row=5, column=6)

    def config_watermark(self):
        self.sidebar_canvas.itemconfig(
            self.watermark_inst_text, text="Config Watermark"
        )
        self.watermark_text_input = tk.Entry(self.window)
        self.watermark_text_input.grid(row=2, column=6)
        self.create_font_selection()

        self.submit_text_button = tk.Button(
            self.window,
            text="Apply",
            command=self.add_watermark_text,
        )
        self.submit_text_button.grid(row=6, column=6)

        self.save_file_button = tk.Button(
            self.window,
            text="Save File",
            command=self.ask_for_filename_to_save,
        )
        self.save_file_button.grid(row=7, column=6)

    def add_watermark_text(self):
        self.open_image_file()
        self.show_scaled_img()
        self.watermark_text = self.watermark_text_input.get()
        selected_font_name = self.font_name_option.get()
        self.selected_font = self.font_dict.get(selected_font_name)
        self.selected_font_size = self.font_size_slider.get()
        print(f"The selected color is: {self.selected_color}")
        fnt = ImageFont.truetype(self.selected_font, int(self.selected_font_size))
        self.watermark = ImageDraw.Draw(self.original_img)
        self.watermark.text(
            (self.new_h, self.new_w),
            text=self.watermark_text,
            font=fnt,
            fill=self.selected_color,
        )
        self.show_scaled_img()
