import tkinter as tk
from tkinter import colorchooser, filedialog

import ttkbootstrap as ttk
from PIL import Image, ImageDraw, ImageFont, ImageTk
from ttkbootstrap.constants import *

from font_names import font_names

UI_FONT = ("Arial", 18, "bold")
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
HEADER_HEIGHT = 50
SIDEBAR_WIDTH = 450
IMG_CANVAS_HEIGHT = WINDOW_HEIGHT - (HEADER_HEIGHT * 2)
IMG_CANVAS_WIDTH = WINDOW_WIDTH - SIDEBAR_WIDTH
WIDGET_PADDING = (40, 0)


class WatermarkAppUI:
    def __init__(self):
        self.window = ttk.Window(themename="lumen")
        self.window.title("Protect Your Work!")
        self.window.config(
            padx=10,
            pady=10,
            width=WINDOW_WIDTH,
            height=WINDOW_HEIGHT,
        )
        self.create_canvases()

        self.exit_button = ttk.Button(
            self.window,
            text="Exit Program",
            command=self.exit_program,
            bootstyle="warning-outline",
        )
        self.exit_button.grid(row=0, column=7, pady=10, sticky="E", padx=20)

        self.file_button = ttk.Button(
            self.window,
            text="Select File",
            command=self.ask_for_filename,
            bootstyle="primary",
        )
        self.file_button.grid(row=0, column=2)

        self.config_watermark_button = ttk.Button(
            self.window,
            text="Configure Watermark",
            command=self.config_watermark,
            bootstyle="primary",
        )
        self.config_watermark_button.grid(row=0, column=6, sticky="W")

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
            self.original_img = Image.open(self.original_filename).convert("RGBA")
        except IsADirectoryError or FileNotFoundError as e:
            print(f"Not possible to open file\n{e}")
            return
        else:
            self.show_scaled_img(self.original_img)

    def save_watermarked_file(self):
        try:
            self.final_img.save(self.new_filename)
        except NameError as e:
            print(f"Modified image not found, saving original.\n{e}")
            return

    def show_scaled_img(self, img):
        self.copy_img = img.copy()
        self.display_img = ImageTk.PhotoImage(self.copy_img)
        self.orig_h = self.display_img.height()
        self.orig_w = self.display_img.width()
        print(self.display_img.height())
        if self.orig_h > IMG_CANVAS_HEIGHT or self.orig_w > IMG_CANVAS_WIDTH:
            h_ratio = self.orig_h / IMG_CANVAS_HEIGHT
            w_ratio = self.orig_w / IMG_CANVAS_WIDTH
            scaling_ratio = max(h_ratio, w_ratio)
            self.new_h = int(round(self.orig_h / scaling_ratio, 0))
            self.new_w = int(round(self.orig_w / scaling_ratio, 0))
            self.tmp_img = self.copy_img.resize((self.new_w, self.new_h))
            self.display_img = ImageTk.PhotoImage(self.tmp_img)
            print("Large image, resizing for display")
        self.img_canvas.create_image(
            IMG_CANVAS_WIDTH / 2,
            IMG_CANVAS_HEIGHT / 2,
            image=self.display_img,
            anchor="center",
        )

    def create_canvases(self):
        self.img_canvas = ttk.Canvas(
            width=IMG_CANVAS_WIDTH,
            height=IMG_CANVAS_HEIGHT,
        )
        self.img_canvas.configure(highlightthickness=5)
        self.img_canvas.grid(
            row=1,
            column=0,
            columnspan=6,
            rowspan=12,
            padx=20,
        )
        self.sidebar_canvas = ttk.Canvas(
            width=SIDEBAR_WIDTH,
            height=IMG_CANVAS_HEIGHT,
        )
        self.sidebar_canvas.configure(highlightthickness=5)
        self.sidebar_canvas.grid(
            row=1,
            column=6,
            columnspan=2,
            rowspan=12,
            padx=(0, 20),
            pady=20,
        )

    def pick_color(self):
        self.selected_color = colorchooser.askcolor()[0]
        if self.selected_color:
            return

    def create_font_selection(self):
        # Create combobox for font selection
        self.font_name_label = ttk.Label(
            self.window,
            text="Font",
            bootstyle="primary",
        )
        self.font_name_label.grid(
            row=5,
            column=6,
            sticky="W",
            padx=WIDGET_PADDING,
        )
        self.font_name_option = ttk.Combobox(self.window, bootstyle="primary")
        self.font_name_option.configure(state="readonly")
        self.font_dict = {i.split(".")[0]: i for i in font_names}
        font_opts = list(self.font_dict.keys())
        self.font_name_option["values"] = font_opts
        # Set default to Arial
        self.font_name_option.current(5)
        self.font_name_option.grid(
            row=6,
            column=6,
            sticky="W",
            padx=WIDGET_PADDING,
        )

        # Create slider to select font size
        self.font_size_slider = ttk.Scale(
            self.window,
            from_=40,
            to=1000,
            orient=tk.HORIZONTAL,
            bootstyle="info",
        )
        self.font_size_slider.set(90)
        self.font_size_slider.grid(
            row=6,
            column=7,
            sticky="W",
            padx=WIDGET_PADDING,
        )

        # Create slider to select transparency
        self.alpha_slider = ttk.Scale(
            self.window,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            bootstyle="info",
        )
        self.alpha_slider.set(50)
        self.alpha_slider.grid(
            row=9,
            column=7,
            sticky="W",
            padx=WIDGET_PADDING,
        )

        # Create color choosing dialog
        # self.selected_color = (255, 175, 125)
        self.color_button = ttk.Button(
            self.window,
            text="Select Colour",
            command=self.pick_color,
            bootstyle="info-outline",
        )
        self.color_button.grid(
            row=9,
            column=6,
            columnspan=2,
            sticky="W",
            padx=WIDGET_PADDING,
        )

    def config_watermark(self):
        self.watermark_text_input = ttk.Entry(
            self.window,
            width=30,
            bootstyle="info",
        )
        self.watermark_text_input.insert(tk.END, "ENTER WATERMARK TEXT HERE")
        self.watermark_text_input.grid(
            row=3,
            column=6,
            columnspan=2,
            sticky="W",
            padx=WIDGET_PADDING,
        )
        self.create_font_selection()

        self.submit_text_button = ttk.Button(
            self.window,
            text="Apply",
            command=self.add_watermark_text,
            bootstyle="info-outline",
        )
        self.submit_text_button.grid(
            row=11,
            column=6,
            sticky="W",
            padx=WIDGET_PADDING,
        )

        self.save_file_button = ttk.Button(
            self.window,
            text="Save File",
            command=self.ask_for_filename_to_save,
            bootstyle="info-outline",
        )
        self.save_file_button.grid(
            row=11,
            column=7,
            sticky="W",
            padx=WIDGET_PADDING,
        )

    def add_watermark_text(self):
        self.open_image_file()
        self.show_scaled_img(self.original_img)
        self.watermark_text = self.watermark_text_input.get()
        selected_font_name = self.font_name_option.get()
        self.selected_font = self.font_dict.get(selected_font_name)
        self.selected_font_size = self.font_size_slider.get()
        fnt = ImageFont.truetype(self.selected_font, int(self.selected_font_size))
        self.selected_alpha = int(self.alpha_slider.get())
        self.watermark = Image.new("RGBA", self.original_img.size, (255, 255, 255, 0))
        d = ImageDraw.Draw(self.watermark)
        d.text(
            (self.new_h, self.new_w),
            text=self.watermark_text,
            font=fnt,
            fill=(*self.selected_color, self.selected_alpha),
        )
        self.final_img = Image.alpha_composite(self.original_img, self.watermark)
        self.show_scaled_img(self.final_img)
