#!/usr/bin/python3

import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
from tkinter import ttk
from tkinter import *
import pyautogui
import datetime
import os

window = tk.Tk()

widget_standard_width = 50
widget_standard_height = 50
widget_x_padding = 20
widget_y_padding = 20
widget_font = {"font": ("Calibri", 12)}

screen_width, screen_height = pyautogui.size()
screen_center_x = str(int(screen_width / 3.3))
screen_center_y = str(int(screen_height / 10))
print("Center width: " + screen_center_x)
print("Center height: " + screen_center_y)

value_catalog = None
value_template = None
value_title = None
value_url = None


def close_window():
    print("Shutting down program...........Thank you using the program")
    window.after(200, window.quit())


def set_catalog_option(option_value):
    global value_catalog
    value_catalog = option_value


def set_template_option(template_option_value):
    global value_template
    value_template = template_option_value


def get_current_date() -> str:
    today = datetime.date.today()
    return today.strftime("%Y%m%d%H%S")


def get_company(catalog) -> str:
    return catalog.replace("ContentCatalog", "")


def show_alert_dialog_after_file_save():
    message = "File has been saved"
    title = "File"
    tkinter.messagebox.showinfo(title=title, message=message)


def reset_widget_text(widget):
    widget.delete(0, END)


def generate_impex():
    global value_title
    value_title = titleText.get()

    global value_url
    if len(urlText.get()) == "":
        value_url = value_title.replace(" ", "-").lower()
    else:
        value_url = urlText.get()

    company = get_company(str(value_catalog))
    current_date = get_current_date()
    lowercase_title = value_title.replace(" ", "").lower()
    lowercase_page_id = lowercase_title + "page"
    paragraph_component = lowercase_title + "paragraph"

    # automatically generated output file
    output_filename = (
        str(current_date)
        + "-"
        + str(value_template)
        + "-"
        + str(company)
        + "-"
        + str(value_title).replace(" ", "")
        + ".impex"
    )

    # open and read from template file
    with open("impex-template.txt", "r") as input:
        filedata = input.read()

        filedata = filedata.replace("[contentCatalog]", str(value_catalog))
        filedata = filedata.replace("[pageID]", str(lowercase_page_id))
        filedata = filedata.replace("[pageTitle]", str(value_title))
        filedata = filedata.replace("[pageTemplate]", str(value_template))
        filedata = filedata.replace("[pageAlias]", str(value_url))
        filedata = filedata.replace("[paragraphcomponent]", str(paragraph_component))
        filedata = filedata.replace("[paragraphcomponentTitle]", str(value_title))
        filedata = filedata.replace("[miscTitle]", str(value_title.replace(" ", "")))

        user_filename = tkinter.filedialog.asksaveasfilename(
            initialdir="/",
            title="Save File",
            filetypes=[("All files", "*.impex")],
            defaultextension=".impex",
        )

        if user_filename:
            # write and create a new output file
            with open(user_filename, "w") as output:
                output.write(filedata)
                show_alert_dialog_after_file_save()
                # clear title and url fields
                titleText.delete(0, END)
                urlText.delete(0, END)
                # reset_widget_text(titleText)
                # reset_widget_text(urlText)


window.title("Page Builder")
window.geometry("+" + screen_center_x + "+" + screen_center_y)

# Add storefront drop-down select (OptionMenu)
catalogs = [
    "",
    "cnwContentCatalog",
    "samiosContentCatalog",
    "sherriffContentCatalog",
    "bgwtechContentCatalog",
]

pageTemplates = ["", "ContentPage1Template", "SingleColumnTemplate"]

"""
 TOP SECTION
"""
topFrame = tk.Frame(window, pady=widget_y_padding)

optionsLabel = tk.Label(
    topFrame, text="Catalog", width=widget_standard_width, **widget_font
)
optionsLabel.grid(row=1, column=0)

options = ttk.Combobox(
    topFrame, values=catalogs, width=widget_standard_width, **widget_font
)
options.bind("<<ComboboxSelected>>", lambda event: set_catalog_option(options.get()))
options.grid(row=1, column=1)
options.set(catalogs[0])

templateOptionsLabel = tk.Label(
    topFrame, text="Page Template", width=widget_standard_width, **widget_font
)
templateOptionsLabel.grid(row=2, column=0, pady=widget_y_padding)

template_options = ttk.Combobox(
    topFrame, values=pageTemplates, width=widget_standard_width, **widget_font
)
template_options.bind(
    "<<ComboboxSelected>>", lambda event: set_template_option(template_options.get())
)
template_options.grid(row=2, column=1, pady=widget_y_padding)
template_options.set(pageTemplates[0])

"""
    MIDDLE SECTION
"""
middleFrame = tk.Frame(window, pady=widget_y_padding)

# Page Title
titleLabel = tk.Label(
    middleFrame, text="Page Title", width=widget_standard_width, **widget_font
)
titleLabel.grid(row=1, column=0, pady=widget_y_padding)

titleText = tk.Entry(middleFrame, width=widget_standard_width, **widget_font)
titleText.grid(row=1, column=1, pady=widget_y_padding)

# Page URL
urlLabel = tk.Label(
    middleFrame, text="Page URL", width=widget_standard_width, **widget_font
)
urlLabel.grid(row=2, column=0, pady=widget_y_padding)

urlText = tk.Entry(middleFrame, width=widget_standard_width, **widget_font)
urlText.grid(row=2, column=1, pady=widget_y_padding)

"""
    BOTTOM SECTION
"""
bottomFrame = tk.Frame(window, pady=widget_y_padding)


# Generate Button
generateButton = tk.Button(
    bottomFrame,
    text="Generate",
    command=generate_impex,
    width=widget_standard_width,
    **widget_font,
)
generateButton.grid(row=1, column=0, padx=widget_x_padding, pady=widget_y_padding)
# Close Button
closeButton = tk.Button(
    bottomFrame,
    text="Close",
    command=close_window,
    width=widget_standard_height,
    **widget_font,
)
closeButton.grid(row=1, column=1, padx=widget_x_padding, pady=widget_y_padding)

# pack frames
topFrame.pack()
middleFrame.pack()
bottomFrame.pack()


# main loop to run
window.mainloop()
