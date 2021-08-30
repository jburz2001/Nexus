try:
    import tkinter as tk
    import tkinter.ttk as ttk
    from tkinter import filedialog
except ImportError:
    import Tkinter as tk
    import ttk
    import tkFileDialog as filedialog

# https://pypi.org/project/tkfilebrowser/
from tkfilebrowser import askopendirname, askopenfilenames, asksaveasfilename

import numpy as np

# https://pythonguides.com/python-tkinter-canvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import *
import matplotlib.pyplot as plt

from functions import *


class App(tk.Tk):
    # self is root here
    def __init__(self):
        super().__init__()

        appTitle = "Image Nexus"
        self.title(appTitle)

        factor = 1.618
        rootWidth = 800
        rootHeight = int(rootWidth / factor)
        geo = "{}x{}".format(str(rootWidth), str(rootHeight))
        self.geometry(geo)

        self.create_menu()
        self.create_widgets()

    def create_menu(self):
        def command_close():
            self.quit()

        menu_main = tk.Menu(self)
        self.config(menu=menu_main)

        menu_dataTypes = tk.Menu(menu_main)
        menu_options = tk.Menu(menu_main)

        menu_main.add_cascade(label="Data Types", menu=menu_dataTypes)
        menu_main.add_cascade(label="Options", menu=menu_options)

        menu_options.add_command(label="Exit", command=command_close)

    def create_widgets(self):
        # ANCHOR layer attributes
        l1padx = 3
        l1pady = l1padx
        l1color = "gray"
        l1padding = {
            "padx": l1padx,
            "pady": l1pady,
            "ipadx": l1padx,
            "ipady": l1pady
        }
        # l1data = (l1color, l1padding)

        l2padx = 2
        l2pady = l2padx
        l2color = "white"
        l2padding = {
            "padx": l2padx,
            "pady": l2pady,
            "ipadx": l2padx,
            "ipady": l2pady
        }
        # l2data = (l2color, l2padding)

        # layerData = {
        #     "l1data": l1data,
        #     "l2data": l2data
        # }

        lColors = (l1color, l2color)
        lPaddings = (l1padding, l2padding)

        # self.create_topSection(lColors, lPaddings)
        self.create_transformationSection(lColors, lPaddings)
        self.create_contentSection(lColors, lPaddings)
        self.create_footerSection(lColors, lPaddings)

    # unused section
    """
    def create_topSection(self, lColors, lPaddings):
        # l1color = layerData.get("l1data")[0]
        # l1padding = layerData.get("l1data")[1]

        # l2color = layerData.get("l2data")[0]
        # l2padding = layerData.get("l2data")[1]

        l1color, l2color = lColors[0], lColors[1]
        l1padding, l2padding = lPaddings[0], lPaddings[1]

        # ANCHOR TOP BAR
        fLabel_topBar = "Links"
        labelFrame_topBar = tk.LabelFrame(
            self, bg=l1color,
            text=fLabel_topBar, height=50
        )
        labelFrame_topBar.pack(side=tk.TOP, fill=tk.X,
                               **l1padding
                               )
    """

    def create_transformationSection(self, lColors, lPaddings):
        l1color, l2color = lColors[0], lColors[1]
        l1padding, l2padding = lPaddings[0], lPaddings[1]

        # ANCHOR OPERATIONS
        frame_operations = tk.Frame(self,
                                    bg=l1color,
                                    height=50)
        frame_operations.pack(fill=tk.X,
                              **l1padding
                              )

        # ANCHOR TRANSFORMATIONS
        fLabel_transformations = "Transformations"
        labelFrame_transformations = tk.LabelFrame(frame_operations,
                                                   bg=l2color,
                                                   text=fLabel_transformations,
                                                   height=50
                                                   )
        labelFrame_transformations.pack(expand=True, side=tk.LEFT, fill=tk.X,
                                        **l2padding)

        # https://www.pythontutorial.net/tkinter/tkinter-optionmenu/
        listOfTransformations = (
            "Choose a transformation",
            "Compress",
            "Discretize",
            "Blur"
        )
        self.selectedTransformation = tk.StringVar()

        optionMenu_transformations = ttk.OptionMenu(labelFrame_transformations,
                                                    self.selectedTransformation,
                                                    listOfTransformations[0],
                                                    *listOfTransformations,
                                                    )

        menuWidth = len(max(listOfTransformations, key=len))
        optionMenu_transformations.config(width=int(menuWidth))
        optionMenu_transformations.pack()
        # s = "Selected transformation: {}".format(
        #     self.selectedTransformation.get())
        label_transformations = tk.Label(labelFrame_transformations,
                                         #  textvariable=self.selectedTransformation
                                         )
        # label_transformations.config(textvariable=s)
        label_transformations.pack()

        # ANCHOR FILE PATHS
        fLabel_filePaths = "File paths"
        labelFrame_filePaths = tk.LabelFrame(frame_operations,
                                             bg=l2color,
                                             text=fLabel_filePaths,
                                             height=50
                                             )
        labelFrame_filePaths.pack(expand=True, side=tk.RIGHT, fill=tk.X,
                                  **l2padding)

        def getSourcePath():
            self.sourcePath.set(filedialog.askopenfilename(
                initialdir="/",
                title="Select a file",
                filetypes=(
                    ("png files", "*.png"),
                    ("all files", "*.*")
                )
            )
            )

            # print(self.sourcePath.get())

        self.sourcePath = tk.StringVar()
        button_sourcePath = tk.Button(labelFrame_filePaths,
                                      text="Select source file",
                                      command=getSourcePath
                                      )
        button_sourcePath.pack()

        label_sourcePath = tk.Label(labelFrame_filePaths,
                                    textvariable=self.sourcePath
                                    )
        label_sourcePath.pack()

        def getSinkPath():
            self.sinkPath.set(filedialog.askopenfilename(
                initialdir="/",
                title="Select a file",
                filetypes=(
                    ("png files", "*.png"),
                    ("all files", "*.*")
                )
            )
            )

            # print(self.sinkPath.get())

        self.sinkPath = tk.StringVar()
        button_sinkPath = tk.Button(labelFrame_filePaths,
                                    text="Select sink file",
                                    command=getSinkPath
                                    )
        button_sinkPath.pack()

        label_sinkPath = tk.Label(labelFrame_filePaths,
                                  textvariable=self.sinkPath
                                  )
        label_sinkPath.pack()

        # give these variables to other methods
        #self.sinkPath = sinkPath
        # self.sourcePath = sourcePath
        # self.selectedTransformation = selectedTransformation.get()

    def create_contentSection(self, lColors, lPaddings):

        # # FIXME get to plot
        # def displayPlot(master):
        #     fig = Figure(1)
        #     y = [2, 10, 30, 10, 5, 8, 50, 44, 41]

        #     plot1 = fig.add_subplot(111)

        #     plot1.hist(y)

        #     canvas = FigureCanvasTkAgg(master,
        #                                fig
        #                                )
        #     canvas.draw()
        #     canvas.get_tk_widget().pack()

        #     toolbar = NavigationToolbar2Tk(
        #         canvas,
        #         master=master
        #     )

        #     toolbar.update()
        #     canvas.get_tk_widget().pack()

        l1color, l2color = lColors[0], lColors[1]
        l1padding, l2padding = lPaddings[0], lPaddings[1]

        # ANCHOR CONTENT
        fLabel_content = "Content"
        labelFrame_content = tk.LabelFrame(self,
                                           bg=l1color,
                                           text=fLabel_content,
                                           height=300
                                           )
        labelFrame_content.pack(expand=True, side=tk.TOP, fill=tk.BOTH,
                                **l1padding)

        # ANCHOR INSTRUCTIONS
        fLabel_instructions = "Instructions"
        labelFrame_instructions = tk.LabelFrame(labelFrame_content,
                                                bg=l2color,
                                                text=fLabel_instructions
                                                )
        labelFrame_instructions.pack(expand=True, side=tk.LEFT, fill=tk.BOTH,
                                     **l2padding
                                     )

        # ANCHOR DISPLAY
        fLabel_display = "Display"
        labelFrame_display = tk.LabelFrame(labelFrame_content,
                                           bg=l2color,
                                           text=fLabel_display
                                           )
        labelFrame_display.pack(expand=True, side=tk.RIGHT, fill=tk.BOTH,
                                **l2padding
                                )

        def displayImg():
            # fig = Figure(dpi=100)
            # subplt = fig.add_subplot(1, 1, 1)

            sourceImg = transform_discretize(self.sourcePath)
            print(sourceImg.shape)
            # sourceImg = sourceImg[:, :, 0]

            # #disp = plt.imshow(sourceImg)
            # subplt.plot(sourceImg)

            # # canvas_display = FigureCanvasTkAgg(fig, labelFrame_display)
            # canvas_display = FigureCanvasTkAgg(fig, labelFrame_display)
            # canvas_display.get_tk_widget().pack()

            fig = plt.figure(figsize=(4, 5))
            fig.clear()
            ax = fig.add_subplot(111)
            ax.imshow(sourceImg)
            #fig = plt.figure(figsize=(4, 5))
            canvas = FigureCanvasTkAgg(fig, labelFrame_display)
            canvas.get_tk_widget().pack()
            canvas.draw()
            # toolbar = NavigationToolbar2Tk(canvas, self.master)
            # toolbar.update()
            # canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=1)

        button_display = tk.Button(labelFrame_display,
                                   text="Display",
                                   command=displayImg
                                   )
        button_display.pack()

        # # FIXME get to show the plot
        # master = labelFrame_display
        # plot(master)

    def create_footerSection(self, lColors, lPaddings):
        l1color, l2color = lColors[0], lColors[1]
        l1padding, l2padding = lPaddings[0], lPaddings[1]

        # ANCHOR FOOTER
        frame_footer = tk.Frame(self,
                                bg=l1color,
                                height=30
                                )
        frame_footer.pack(side=tk.TOP, fill=tk.BOTH,
                          **l1padding
                          )

        # ANCHOR FOOTER LABEL
        footerText = "Created by Justin Burzachiello"
        label_footer = tk.Label(frame_footer,
                                text=footerText)
        label_footer.pack(side=tk.RIGHT,
                          **l2padding
                          )


if __name__ == "__main__":
    app = App()
    app.mainloop()
