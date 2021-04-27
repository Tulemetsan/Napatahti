# -------------------------------------------------------------------------------------------------------------------- #

import time
import tkinter as tk
import tkinter.filedialog as fd
import idlelib.tooltip as ttp
import pyscreenshot as ps
from .sb_sub_menu import SubMenu

# @formatter:off


class MainGui(SubMenu):
    img_type = [('Image PNG', '*.png'), ('Image GIF', '*.gif'), ('All Files', '*.*')]
    mf_y = 0

    def __init__(self):
        self.app = tk.Tk()
        SubMenu.__init__(self)
        self.scw = self.app.winfo_screenwidth()
        self.sch = self.app.winfo_screenheight()

        self.app.wm_state(self.var[24])
        self.app.title('Napatähti')
        self.app.geometry('%sx%s+-8+%d' % (self.scw, self.sch - self.app_dim['OsFootHgt'], self.app_dim['PyFrmTop']))

        self.app_state = {}
        self.wch_var[0] = tk.IntVar()
        self.wch_var[1] = tk.StringVar()

        self.md_tip = MoonDayToolTip(self.moon_d, self.conf, self.loc, self.app)

        fnt = self.font['AppSpc']
        tbg = self.app_col['ToolBkg']
        tfg = self.app_col['ToolFrg']
        fbg = self.app_col['FootBkg']
        ffg = self.app_col['FootFrg']

        self.tool_bt[0] = tk.Button(
            self.t_frame, text='NEW', width=4, font=fnt, command=lambda: self.tool_gui_trig(1, 0))
        self.tool_bt[1] = tk.Button(
            self.t_frame, text='SRC', width=4, font=fnt, command=lambda: self.tool_gui_trig(1, 1))
        self.tool_bt[2] = tk.Button(self.t_frame, text='DBS', width=4, font=fnt, command=lambda: self.tool_gui_trig(2))
        self.tool_bt[3] = tk.Button(self.t_frame, text='APG', width=4, font=fnt, command=lambda: self.tool_gui_trig(3))
        self.tool_bt[4] = tk.Button(self.t_frame, text='PLC', width=4, font=fnt, command=lambda: self.tool_gui_trig(4))
        self.tool_bt[5] = tk.Button(self.t_frame, text='ATB', width=4, font=fnt, command=lambda: self.tool_gui_trig(5))
        self.tool_bt[6] = tk.Button(self.t_frame, text='TMC', width=4, font=fnt, command=lambda: self.tool_gui_trig(6))

        self.tool_bt[7] = tk.Button(self.t_frame, text='˄', width=2, font=fnt, command=lambda: self.swi_chd_state(1))
        self.tool_bt[8] = tk.Button(self.t_frame, text='˅', width=2, font=fnt, command=self.swi_chd_state)

        self.dim_lb = tk.Label(self.b_frame, bg=fbg, fg=ffg, font=fnt, relief=tk.RIDGE)
        self.dbs_lb = tk.Label(self.b_frame, bg=fbg, fg=ffg, font=fnt, relief=tk.RIDGE)
        self.evt_lb = tk.Label(self.b_frame, textvariable=self.wch_var[1], bg=fbg, fg=ffg, font=fnt)

        self.t_frame.pack(side=tk.TOP, fill=tk.X, expand=0)
        self.m_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.b_frame.pack(side=tk.BOTTOM, fill=tk.X, expand=0)

        self.cell_set_pos(64, self.var[9] & 64)
        for i in range(9):
            self.tool_bt[i].configure(bg=tbg, fg=tfg)
            if i < 7:
                self.tool_bt[i].pack(side=tk.LEFT)
            else:
                self.tool_bt[i].pack(side=tk.RIGHT)

        self.cell_set_pos(128, self.var[9] & 128)
        self.dim_lb.pack(side=tk.LEFT)
        self.dbs_lb.pack(side=tk.LEFT)
        self.evt_lb.pack(side=tk.LEFT)

        app_menu = tk.Menu()
        app_menu.add_cascade(label=self.mkw['file'], menu=self.file_menu)
        app_menu.add_cascade(label=self.mkw['view'], menu=self.view_menu)
        app_menu.add_cascade(label=self.mkw['options'], menu=self.opt_menu)
        app_menu.add_cascade(label=self.mkw['tools'], menu=self.tool_menu)
        app_menu.add_cascade(label=self.tkw['set'], menu=self.set_menu)
        app_menu.add_command(label=self.tkw['about'], command=self.about_msg)
        self.app.config(menu=app_menu)

        if not self.var[13]:
            self.repos_map(1)

        self.wch_var[0].trace_add('write', lambda *args: self.dbs_watch())
        self.wch_var[0].set(self.var[6])
        self.conf.lnk_wch_dbs(self.wch_var[0])

        self.app.bind('<Escape>', lambda *args: self.app.destroy())
        self.app.bind('<Configure>', self.on_config)
        self.app.bind('<FocusIn>', lambda *args: self.on_focus_in())
        self.app.bind('<FocusOut>', lambda *args: self.on_focus_out())
        self.app.bind('<Control-Key>', self.on_key_press)
        self.m_frame.bind('<Destroy>', lambda *args: self.on_destroy())
        self.cell[4].bind('<Motion>', self.moon_day_tip)
        self.cell[4].bind('<Leave>', self.moon_day_tip)

        self.app.mainloop()

    def on_config(self, event):
        widget = str(event.widget).split('.!')[-1]
        if widget == '.':
            self.conf.set_act_var(24, self.app.state())
            self._rs[1] = event.x
            self._rs[2] = event.y
            self._rs[3] = event.width
            self._rs[4] = event.height
            if self._rs[1] + self._rs[3] < self.scw and self._rs[2] + self._rs[4] < self.sch:
                self._rs[0] = 1
            if self._rs[0] and self.app.attributes('-topmost') == 1:
                self.app.attributes('-topmost', 0)
                if self._rs[5]:
                    time.sleep(0.2)
                self._rs[0] = 0
                if self.app.state() == 'zoomed':
                    x = 0
                    y = self.mf_y + self.app_dim['TopHgtZm'] + self.app_dim['PyFrmTop']
                else:
                    x = self._rs[1] + 8
                    y = self._rs[2] + self.mf_y + self.app_dim['TopHgtNr'] + self.app_dim['PyFrmTop']
                img = ps.grab(bbox=(x, y, x + self.mf_w, y + self.mf_h))
                img_name = fd.asksaveasfilename(
                    initialfile=self.data[1]['name'], filetypes=self.img_type, defaultextension='*.png')
                if img_name:
                    img.save(img_name)
            for i in self.chd_ord:
                if self.child[i]:
                    self.child[i].attributes('-topmost', 1)
                    self.child[i].attributes('-topmost', 0)
        if widget == 'frame2':
            self.mf_y = event.y
            self.mf_w = event.width
            self.mf_h = event.height
            self.dim_lb.configure(text='%d x %d' % (self.mf_w, self.mf_h))
            if self.var[13]:
                self.repos_map()

    def on_destroy(self):
        self.conf.set_act_var(23, 0)
        for i in self.child:
            if self.child[i]:
                self.child[i].destroy()
        self.conf.dump()

    def on_key_press(self, event):
        if event.keycode == 82:
            self.repos_map()
        elif event.keycode == 83:
            self.save_img_task()

    def on_focus_in(self):
        self.ask_ent.configure(parent=self.app)
        state = self.app.wm_state()
        for i in self.chd_ord:
            if self.child[i]:
                self.child[i].attributes('-topmost', 1)
                self.child[i].attributes('-topmost', 0)
                if state in {'normal', 'zoomed'} and self.app_state[0] == 'iconic':
                    self.child[i].wm_state(self.app_state[i])

    def on_focus_out(self):
        self.app_state[0] = self.app.wm_state()
        for i in self.chd_ord:
            if self.child[i]:
                self.app_state[i] = self.child[i].wm_state()
                if self.app_state[0] == 'iconic':
                    self.child[i].wm_state('iconic')

    def moon_day_tip(self, event):
        hide = 0
        if event.type == '6':
            fs = self.font['CellText'][1]
            x1 = self.edt_dim['PadX']
            x2 = self.edt_dim['PadX'] + fs * 3.5
            y1 = self.edt_dim['PadY'] + fs
            y2 = self.edt_dim['PadY'] + fs * 3

            if x1 < event.x < x2 and y1 < event.y < y2:
                if self.edc_flg:
                    self.app.config(cursor='hand2')
                    self.edc_flg = 0
                    self.md_tip.showcontents(self.geo[4]['x'] + x2 + 10, self.geo[4]['y'] + y1 + fs)
            else:
                if not self.edc_flg:
                    hide = 1
        else:
            hide = 1
        if hide:
            self.app.config(cursor='arrow')
            self.edc_flg = 1
            self.md_tip.hidecontents()

    def dbs_watch(self):
        ind = self.dbs.get_cur_ind(self.data)
        if ind:
            self.wch_var[0].set(ind)
            txt = self.fkw['dbsRec']
        else:
            self.wch_var[0].set(self.var[6])
            txt = self.fkw['dbsNew']
        patch = '&' if self.data[2] else ''
        self.dbs_lb.configure(text='%s %s%s' % (txt, self.wch_var[0].get(), patch))

    def swi_chd_state(self, mode=0):
        state = 'normal' if mode else 'iconic'
        for i in self.chd_ord:
            self.child[i].wm_state(state)

    @staticmethod
    def about_msg():
        app = tk.Toplevel()
        app.focus_set()
        app.title('About')
        app.attributes('-topmost', 1)
        cx = 0.5*app.winfo_screenwidth() - 200
        cy = 0.5*app.winfo_screenheight() - 75
        app.geometry('400x150+%d+%d' % (cx, cy))
        app.resizable(width=False, height=False)

        tit = tk.Label(app, text='Napatähti version pre-alpha', font=('', 14, 'italic'))
        bld = tk.Label(app, text='Built on  April 27, 2021', font=('', 12))
        lng = tk.Label(app, text='Python 3.8.9 stdlib, pyswisseph, pyscreenshot, pillow', font=('', 12))
        dev = tk.Label(app, text='Tulemetsan, e-mail: sagenwind@gmail.com', font=('', 12))

        tit.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        bld.grid(row=1, column=0, padx=10, sticky=tk.W)
        lng.grid(row=2, column=0, padx=10, sticky=tk.W)
        dev.grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)

        app.bind('<FocusOut>', lambda *args: app.destroy())


class MoonDayToolTip(ttp.TooltipBase):
    mth = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april', 5: 'may', 6: 'june', 7: 'july',
        8: 'august', 9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    ckw = {'mdFull': 'Moon day', 'beg': 'Begin', 'end': 'End'}
    box = None

    def __init__(self, items, conf=None, loc=None, parent=None):
        ttp.TooltipBase.__init__(self, parent)
        if conf:
            self.var = conf.get_act_var()
        else:
            self.var = {19: 0}
        if loc:
            self.ckw = loc.get_sample_cell()
            self.mth = loc.get_month()
        self.parent = parent
        self.items = items

    def showtip(self): pass
    def hidetip(self): pass
    def get_position(self): pass
    def position_window(self): pass

    def showcontents(self, x=100, y=100, w=200, h=55, bkg='#FFFFE0'):
        items = self.items[self.var[19]]

        self.box = tk.Listbox(self.parent, background=bkg)
        self.box.place(x=x, y=y, width=w, height=h)

        self.box.insert(tk.END, ' %s : %d' % (self.ckw['mdFull'], items[0]))
        self.box.insert(
            tk.END, ' %s : %d %s %d %d:%02d:%02d' % (
                self.ckw['beg'], items[1][2], self.mth[items[1][1]], items[1][0],
                items[1][3], items[1][4], items[1][5])
        )
        self.box.insert(
            tk.END, ' %s : %d %s %d %d:%02d:%02d' % (
                self.ckw['end'], items[2][2], self.mth[items[2][1]], items[2][0],
                items[2][3], items[2][4], items[2][5])
        )

    def hidecontents(self):
        if self.box:
            self.box.place_forget()

# -------------------------------------------------------------------------------------------------------------------- #
