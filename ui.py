import tkinter as tk
from tkinter import filedialog
from tkinter.colorchooser import askcolor

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
            command=lambda: self.ask_for_filename(True),
            bootstyle="primary",
        )
        self.file_button.grid(row=0, column=2)

        self.window.mainloop()

    def exit_program(self):
        self.window.destroy()

    def ask_for_filename(self, first_time=False):
        self.original_filename = filedialog.askopenfilename()
        self.open_image_file(first_time)

    def ask_for_filename_to_save(self):
        self.new_filename = filedialog.asksaveasfilename()
        self.save_watermarked_file()

    def open_image_file(self, first_time=False):
        try:
            self.original_img = Image.open(self.original_filename).convert("RGBA")
        except IsADirectoryError or FileNotFoundError as e:
            print(f"Not possible to open file\n{e}")
            return
        else:
            self.show_scaled_img(self.original_img)
            if first_time:
                self.config_watermark_menu()

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
        self.selected_color = askcolor()[0]
        if self.selected_color:
            return

    def create_font_selection(self):
        # Create combobox for font selection
        self.font_name_label = ttk.Label(
            self.window,
            text="Font",
            bootstyle="primary",
            font=UI_FONT,
        )
        self.font_name_label.grid(
            row=3,
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
            row=4,
            column=6,
            sticky="W",
            padx=WIDGET_PADDING,
        )

        # Create slider to select font size
        self.font_size_label = ttk.Label(
            self.window,
            text="Font Size",
            bootstyle="primary",
            font=UI_FONT,
        )
        self.font_size_label.grid(
            row=3,
            column=7,
            sticky="E",
            padx=(0, 50),
        )
        self.font_size_slider = ttk.Scale(
            self.window,
            from_=40,
            to=500,
            orient=tk.HORIZONTAL,
            bootstyle="info",
        )
        self.font_size_slider.set(250)
        self.font_size_slider.grid(
            row=4,
            column=7,
            sticky="E",
            padx=(0, 50),
        )

        # Create slider to select transparency
        self.alpha_label = ttk.Label(
            self.window,
            text="Transparency",
            bootstyle="primary",
            font=UI_FONT,
        )
        self.alpha_label.grid(
            row=5,
            column=7,
            sticky="E",
            padx=(0, 50),
        )
        self.alpha_slider = ttk.Scale(
            self.window,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            bootstyle="info",
        )
        self.alpha_slider.set(100)
        self.alpha_slider.grid(
            row=6,
            column=7,
            sticky="E",
            padx=(0, 50),
        )

        # Create color choosing dialog
        self.color_label = ttk.Label(
            self.window,
            text="Colour",
            bootstyle="primary",
            font=UI_FONT,
        )
        self.color_label.grid(
            row=5,
            column=6,
            sticky="W",
            padx=WIDGET_PADDING,
        )
        self.selected_color = (66, 255, 0)
        self.color_button = ttk.Button(
            self.window,
            text="Select",
            command=self.pick_color,
            bootstyle="info-outline",
        )
        self.color_button.grid(
            row=6,
            column=6,
            columnspan=2,
            sticky="W",
            padx=WIDGET_PADDING,
        )
        self.location_label = ttk.Label(
            self.window,
            text="Location",
            bootstyle="primary",
            font=UI_FONT,
        )
        self.location_label.grid(
            row=7,
            column=6,
            sticky="W",
            padx=WIDGET_PADDING,
        )
        self.location_option = ttk.Combobox(self.window, bootstyle="primary")
        self.location_option.configure(state="readonly")
        self.location_dict = {
            "center": {
                "alignment": "mm",
                "coords": (self.orig_w / 2, self.orig_h / 2),
            },
            "top left": {
                "alignment": "la",
                "coords": (20, 20),
            },
            "top center": {
                "alignment": "ma",
                "coords": (self.orig_w / 2, 20),
            },
            "top right": {
                "alignment": "ra",
                "coords": (self.orig_w - 20, 20),
            },
            "bottom left": {
                "alignment": "ld",
                "coords": (20, self.orig_h),
            },
            "bottom center": {
                "alignment": "md",
                "coords": (self.orig_w / 2, self.orig_h),
            },
            "bottom right": {
                "alignment": "rd",
                "coords": (self.orig_w - 20, self.orig_h),
            },
            "middle left": {
                "alignment": "lm",
                "coords": (20, self.orig_h / 2),
            },
            "middle right": {
                "alignment": "rm",
                "coords": (self.orig_w - 20, self.orig_h / 2),
            },
        }
        loc_opts = list(self.location_dict.keys())
        self.location_option["values"] = loc_opts
        # Set default to Arial
        self.location_option.current(0)
        self.location_option.grid(
            row=8,
            column=6,
            sticky="W",
            padx=WIDGET_PADDING,
        )

    def config_watermark_menu(self):
        self.watermark_text_input = ttk.Entry(
            self.window,
            width=30,
            bootstyle="info",
            font=UI_FONT,
        )
        self.watermark_text_input.insert(tk.END, "WATERMARK TEXT")
        self.watermark_text_input.grid(
            row=2,
            column=6,
            columnspan=2,
            sticky="W",
            padx=WIDGET_PADDING,
        )
        self.create_font_selection()

        self.submit_text_button = ttk.Button(
            self.window,
            text="Apply",
            command=self.apply_settings,
            bootstyle="info-outline",
        )
        self.submit_text_button.grid(
            row=10,
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
            row=10,
            column=7,
            sticky="W",
            padx=WIDGET_PADDING,
        )

    def config_watermark_text(self):
        self.watermark_text = self.watermark_text_input.get()
        self.selected_font = self.font_dict.get(self.font_name_option.get())
        self.selected_font_size = self.font_size_slider.get()
        self.selected_fnt = ImageFont.truetype(
            self.selected_font, int(self.selected_font_size)
        )
        self.selected_alpha = int(self.alpha_slider.get())
        self.selected_location = self.location_dict.get(self.location_option.get())
        print(self.selected_location)

    def add_watermark_text(self):
        self.open_image_file()
        self.show_scaled_img(self.original_img)

        # Option 1 Too pale
        self.watermark = Image.new("RGBA", self.original_img.size, (255, 255, 255, 0))
        d = ImageDraw.Draw(self.watermark)

        # Option 2 Not really transparent, just gets more white
        # d = ImageDraw.Draw(self.original_img)

        d.text(
            self.selected_location.get("coords"),
            text=self.watermark_text,
            font=self.selected_fnt,
            fill=(*self.selected_color, self.selected_alpha),
            anchor=self.selected_location.get("alignment"),
        )

        # For option 1
        self.final_img = Image.alpha_composite(self.original_img, self.watermark)
        self.show_scaled_img(self.final_img)

        # For option 2
        # self.show_scaled_img(self.original_img)

    def apply_settings(self):
        self.config_watermark_text()
        self.add_watermark_text()
