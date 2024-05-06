import tkinter
from tkinter import messagebox
import call_Myotally as MT


class this_GUI:

    def __init__(self):

        def run():
            if cbvar7.get() == 0:
                MT.main(entry1.get(), entry2.get(), entry3.get(), entry4.get(), \
                        self.image_quality_var.get(), float(entry6_2.get()), float(entry6_3.get()),\
                        float(entry8_1.get()))
            elif cbvar7.get() == 1:
                MT.main(entry1.get(), entry2.get(), entry3.get(), entry4.get(), \
                        self.image_quality_var.get(), 200, 3000, float(entry8_1.get()))
            tkinter.messagebox.showinfo('', 'Finished')
            self.main_window.destroy()

            
        self.main_window = tkinter.Tk() 
        self.main_window.title('Myotally')
        

        frame1 = tkinter.Frame(self.main_window)
        label1 = tkinter.Label(frame1, text = 'Folder Path: ')
        entry1 = tkinter.Entry(frame1)
        frame1.pack()
        label1.pack(side = 'left')
        entry1.pack(side = 'left')

        frame2 = tkinter.Frame(self.main_window)
        label2 = tkinter.Label(frame2, text = '\n\nDAPI image name: ')
        entry2 = tkinter.Entry(frame2)
        frame2.pack()
        label2.pack()
        entry2.pack()
        
        frame3 = tkinter.Frame(self.main_window)
        label3 = tkinter.Label(frame3, text = 'Laminin image name: ')
        entry3 = tkinter.Entry(frame3)
        frame3.pack()
        label3.pack()
        entry3.pack()

        frame4 = tkinter.Frame(self.main_window)
        label4 = tkinter.Label(frame4, text = 'MFI image name(s) \n(separate by commas, leave blank if none):')
        entry4 = tkinter.Entry(frame4)
        frame4.pack()
        label4.pack()
        entry4.pack()

        frame5 = tkinter.Frame(self.main_window)
        label5 = tkinter.Label(frame5, text = 'Image quality:')
        self.image_quality_var = tkinter.IntVar()
        self.image_quality_var.set(2)
        rb5_1 = tkinter.Radiobutton(frame5, text = 'low', variable = self.image_quality_var, value = 1)
        rb5_2 = tkinter.Radiobutton(frame5, text = 'high', variable = self.image_quality_var, value = 2)
        frame5.pack()
        label5.pack(side = 'left')
        rb5_1.pack(side = 'left')
        rb5_2.pack(side = 'left')
        
        frame6 = tkinter.Frame(self.main_window)
        label6_1 = tkinter.Label(frame6, text = '\n\nFiber size range (µm^2)')
        label6_2 = tkinter.Label(frame6, text = 'Min: ')
        entry6_2 = tkinter.Entry(frame6)
        label6_3 = tkinter.Label(frame6, text = '- Max:')
        entry6_3 = tkinter.Entry(frame6)
        frame6.pack()
        label6_1.pack()
        label6_2.pack(side = 'left')
        entry6_2.pack(side = 'left')
        label6_3.pack(side = 'left')
        entry6_3.pack(side = 'left')

        frame7 = tkinter.Frame(self.main_window)
        label7 = tkinter.Label(frame7, text = 'OR')
        cbvar7 = tkinter.IntVar()
        cbvar7.set(0)
        cb7 = tkinter.Checkbutton(frame7, text = \
                                         'Default size for 10X 7DPI (200-3000)', \
                                         variable = cbvar7)
        frame7.pack()
        label7.pack()
        cb7.pack()

        frame8 = tkinter.Frame(self.main_window)
        label8_1 = tkinter.Label(frame8, text = '\n\npixel : µm^2 ratio')
        entry8_1 = tkinter.Entry(frame8)
        entry8_1.insert(-1,'1')

        frame8.pack()
        label8_1.pack()
        entry8_1.pack()

        frame_last = tkinter.Frame(self.main_window)
        run_button = tkinter.Button(frame_last, text = 'Run Myotally', command = run)
        quit_button = tkinter.Button(frame_last, text = 'Quit', command = self.main_window.destroy)
        frame_last.pack()
        run_button.pack(side = 'left')
        quit_button.pack(side = 'left')

        tkinter.mainloop()

this_GUI()



