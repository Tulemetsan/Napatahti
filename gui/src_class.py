# -------------------------------------------------------------------------------------------------------------------- #

import tkinter as tk
import tkinter.ttk as ttk

# @formatter:off


class GuiSmartCell:
    mf_w, mf_h = 0, 0
    _ex, _ey = 0, 0
    _sw, _sh = 0, 0
    flag = 0

    def __init__(self):
        self.cell = {}
        self.geo = {}
        self.wch_var = {}

    def on_cell_move(self, event, ind, set_geo):
        if event.type == '4':
            self.flag |= 1
            self._ex = event.x_root
            self._ey = event.y_root
            self.cell[ind].configure(highlightthickness=3)
            if 1 in self.wch_var:
                self.wch_var[1].set(' x%s, y%s ' % (self.geo[ind]['x'], self.geo[ind]['y']))
        elif self.flag & 1 and event.type == '6':
            x = self.normalize(
                self.geo[ind]['x'] + event.x_root - self._ex, self.geo[ind]['mnx'], self.mf_w - self.geo[ind]['w'])
            y = self.normalize(
                self.geo[ind]['y'] + event.y_root - self._ey, self.geo[ind]['mny'], self.mf_h - self.geo[ind]['h'])
            self.cell[ind].place(x=x, y=y)
            if 1 in self.wch_var:
                self.wch_var[1].set(' x%s, y%s ' % (x, y))
        elif self.flag & 1 and event.type == '5':
            self.cell[ind].configure(highlightthickness=0)

            x = self.normalize(
                self.geo[ind]['x'] + event.x_root - self._ex, self.geo[ind]['mnx'], self.mf_w - self.geo[ind]['w'])
            y = self.normalize(
                self.geo[ind]['y'] + event.y_root - self._ey, self.geo[ind]['mny'], self.mf_h - self.geo[ind]['h'])
            set_geo(ind, x=x, y=y)

            self.flag ^= 1
            if 1 in self.wch_var:
                self.wch_var[1].set('')

    def on_cell_resize(self, event, ind, set_geo, render=lambda: None):
        if event.type == '4':
            self.flag |= 2
            self._ex, self._ey = event.x, event.y
            self._sw, self._sh = 0, 0
            self.cell[ind].configure(highlightthickness=3)
            if 1 in self.wch_var:
                self.wch_var[1].set(' w%s, h%s ' % (self.geo[ind]['w'], self.geo[ind]['h']))
        elif self.flag & 2 and event.type == '6':
            if event.x > self._ex:
                self._sw += 1
            elif event.x < self._ex:
                self._sw -= 1
            if event.y > self._ey:
                self._sh += 1
            elif event.y < self._ey:
                self._sh -= 1
            self._ex, self._ey = event.x, event.y

            rw = self.normalize(self.geo[ind]['w'] + self._sw, self.geo[ind]['mnw'], self.geo[ind]['mxw'])
            rh = self.normalize(self.geo[ind]['h'] + self._sh, self.geo[ind]['mnh'], self.geo[ind]['mxh'])
            if self.geo[ind]['x'] + rw > self.mf_w:
                rw = self.mf_w - self.geo[ind]['x']
            if self.geo[ind]['y'] + rh > self.mf_h:
                rh = self.mf_h - self.geo[ind]['y']

            self.cell[ind].place(width=rw, height=rh)
            if 1 in self.wch_var:
                self.wch_var[1].set(' w%s, h%s ' % (rw, rh))
        elif self.flag & 2 and event.type == '5':
            self.cell[ind].configure(highlightthickness=0)

            rw = self.normalize(self.geo[ind]['w'] + self._sw, self.geo[ind]['mnw'], self.geo[ind]['mxw'])
            rh = self.normalize(self.geo[ind]['h'] + self._sh, self.geo[ind]['mnh'], self.geo[ind]['mxh'])
            if self.geo[ind]['x'] + rw > self.mf_w:
                rw = self.mf_w - self.geo[ind]['x']
            if self.geo[ind]['y'] + rh > self.mf_h:
                rh = self.mf_h - self.geo[ind]['y']
            set_geo(ind, w=rw, h=rh)

            self.flag ^= 2
            render()
            if 1 in self.wch_var:
                self.wch_var[1].set('')

    @staticmethod
    def normalize(arg, mn, mx): return arg if mn <= arg <= mx else mn if arg < mn else mx

    @staticmethod
    def bind_pack_mov_res(obj, cb):
        obj.bind('<Control-Button-1>', cb[0])
        obj.bind('<B1-Motion>', cb[0])
        obj.bind('<ButtonRelease-1>', cb[0])
        obj.bind('<Control-Button-3>', cb[1])
        obj.bind('<B3-Motion>', cb[1])
        obj.bind('<ButtonRelease-3>', cb[1])


class ModalBoxAskEntry:
    app, act_wdg, pos_bt = None, None, None
    parent = None

    def __init__(self, font=None, kwd=None):
        self.act_var = tk.StringVar()
        self.font = font if font else {'AppBsc': ('Arial', 12)}
        self.kwd = kwd if kwd else {'ok': 'Ok', 'cancel': 'Cancel', 'qws': 'Do you want to confirm?'}

    def mb(self, title='', alter='', proc_func=None, valid_func=None, cx=None, cy=None, ent_font='AppBsc'):
        self.create_app()
        if cx is None:
            cx = 0.5*self.app.winfo_screenwidth() - 200
        if cy is None:
            cy = 0.5*self.app.winfo_screenheight() - 100
        self.app.geometry('+%d+%d' % (cx, cy))
        self.app.resizable(width=False, height=False)
        self.app.title(title)

        ttk.Style().configure('mbs.TButton', font=self.font['AppBsc'])

        if valid_func:
            mode = 1
            self.act_wdg = ttk.Entry(
                self.app, font=self.font[ent_font], width=24, justify=tk.CENTER, textvariable=self.act_var)
            self.act_wdg.focus_set()
        else:
            mode = 0
            self.act_wdg = tk.Label(
                self.app, font=self.font['AppBsc'], width=24, text=self.kwd[alter], anchor=tk.CENTER)

        self.pos_bt = ttk.Button(
            self.app, style='mbs.TButton', width=9, text=self.kwd['ok'], state=tk.NORMAL,
            command=lambda: self.processing(proc_func, mode))
        neg_bt = ttk.Button(
            self.app, style='mbs.TButton', width=9, text=self.kwd['cancel'], command=lambda: self.app.destroy())

        self.act_wdg.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky=tk.N+tk.S+tk.E+tk.W)
        self.pos_bt.grid(row=2, column=0, padx=5, pady=10, sticky=tk.E)
        neg_bt.grid(row=2, column=1, padx=5, pady=10, sticky=tk.W)

        if valid_func:
            self.act_var.trace_add('write', lambda *args: self.validate(valid_func))
            self.act_var.set(alter)

        self.app.bind('<Escape>', lambda *args: self.app.destroy())
        self.app.bind('<Return>', lambda *args: self.on_return(proc_func, mode))

    def configure(self, **kwargs):
        if 'parent' in kwargs:
            self.parent = kwargs['parent']

    def create_app(self):
        self.app = tk.Toplevel(self.parent)
        self.app.attributes('-topmost', 1)
        self.app.transient(self.parent)
        self.app.grab_set()
        self.app.focus_set()

    def on_return(self, proc_func, mode):
        if str(self.pos_bt.cget('state')) == tk.NORMAL:
            self.processing(proc_func, mode)

    def processing(self, proc_func, mode):
        if not proc_func:
            self.app.destroy()
        proc_func(self.act_var.get()) if mode else proc_func()
        self.app.destroy()

    def validate(self, valid_func):
        if valid_func(self.act_var.get()):
            self.pos_bt.configure(state=tk.NORMAL)
        else:
            self.pos_bt.configure(state=tk.DISABLED)


class GuiSmartTable:
    _ix, _iy = 0, 0
    _sx, _sy = 0, 0
    _nc, _nr = 0, 0
    _mx, _my = 0, 0
    _w, _h = 0, 0
    dim = {'CellWid': 60, 'CellHgt': 30}
    app, m_frame, cnv = None, None, None
    cnv_scr_ver, cnv_scr_hor, cnv_scr_cap = None, None, None

    def child_app(self):
        self.app = tk.Toplevel()

        self.m_frame = tk.Frame(self.app)
        self.cnv = tk.Canvas(self.m_frame, highlightthickness=0)
        self.cnv_scr_ver = ttk.Scrollbar(
            self.m_frame, orient=tk.VERTICAL, command=lambda *args: self.on_cnv_scroll(*args, mode=1))
        self.cnv_scr_hor = ttk.Scrollbar(
            self.m_frame, orient=tk.HORIZONTAL, command=lambda *args: self.on_cnv_scroll(*args, mode=0))
        self.cnv_scr_cap = tk.Label(self.m_frame, text='●')

    def tab_render(self): pass
    def ent_c_set(self): pass
    def ent_c_var_save(self): return None, None
    def ent_c_var_set(self): pass
    def next_ind(self): pass

    def on_click_src(self, event, pad_left, pad_top):
        self._ix = int(event.x/self.dim['CellWid'])
        self._iy = int(event.y/self.dim['CellHgt'])
        if self._ix >= pad_left:
            self._ix += self._sx
        if self._iy >= pad_top:
            self._iy += self._sy

    def on_motion_src(self, event, col='#FF0000'):
        cw = self.dim['CellWid']
        ch = self.dim['CellHgt']

        self._mx = int(event.x/cw)
        self._my = int(event.y/ch)

        self.cnv.delete('mark')

        if self._mx > 0:
            x1 = cw * self._mx + 2
            x2 = cw * (self._mx + 1) - 2
            y2 = ch - 2
            self.cnv.create_rectangle(x1, 2, x2, y2, width=3, fill=None, outline=col, tag='mark')
        if self._my > 0:
            y1 = ch * self._my + 2
            x2 = cw - 2
            y2 = ch * (self._my + 1) - 2
            self.cnv.create_rectangle(2, y1, x2, y2, width=3, fill=None, outline=col, tag='mark')

    def on_cnv_scroll(self, *args, mode):
        if mode:
            shift = self._sy
            num = self._nr
        else:
            shift = self._sx
            num = self._nc

        if args[0] == 'moveto':
            src_pos = float(args[1])
            max_pos = num/(num + 1)
            if src_pos < 0:
                src_pos = 0
            if src_pos > max_pos:
                src_pos = max_pos
            calc_shift = int(src_pos*(num + 1))
            if shift != calc_shift:
                if mode:
                    self._sy = calc_shift
                else:
                    self._sx = calc_shift
                self.tab_render()
            self.cnv_scr_repos(mode, src_pos)
        elif args[0] == 'scroll':
            flag = 0
            if args[1] == '1':
                if shift < num:
                    if mode:
                        self._sy += 1
                    else:
                        self._sx += 1
                    flag = 1
            elif args[1] == '-1':
                if shift > 0:
                    if mode:
                        self._sy -= 1
                    else:
                        self._sx -= 1
                    flag = 1

            if flag:
                self.tab_render()
            self.cnv_scr_repos(mode)

    def cnv_scr_repos(self, mode=1, pos=None):
        if mode:
            scroll = self.cnv_scr_ver
            shift = self._sy
            num = self._nr
        else:
            scroll = self.cnv_scr_hor
            shift = self._sx
            num = self._nc

        if pos is None:
            pos = shift/(num + 1)

        scroll.set(pos, pos + 1/(num + 1))

    def cnv_scr_upd_src(self, num_cell_v, num_cell_h, left_pad):
        cw = self.dim['CellWid']
        ch = self.dim['CellHgt']

        self._nr = int((num_cell_v*ch - self._h + 21)/ch)
        self._nc = int((num_cell_h*cw - self._w + left_pad + 21)/cw)

        if self._nr <= 0:
            self.cnv_scr_ver.set(0, 1)
        else:
            self.cnv_scr_repos(1)
        if self._nc <= 0:
            self.cnv_scr_hor.set(0, 1)
        else:
            self.cnv_scr_repos(0)

    def on_cnv_mouse_wheel(self, event):
        flag = 0
        key = str(event).split(' ')
        key = key[2].split('=')
        key = key[1].split('|')
        if key[0] == 'Shift':
            mode = 0
            shift = self._sx
            num = self._nc
        else:
            mode = 1
            shift = self._sy
            num = self._nr

        if event.delta < 0:
            if shift < num:
                if mode:
                    self._sy += 1
                else:
                    self._sx += 1
                flag = 1
        elif event.delta > 0:
            if shift > 0:
                if mode:
                    self._sy -= 1
                else:
                    self._sx -= 1
                flag = 1

        self.cnv_scr_repos(mode)
        if flag:
            self.tab_render()

    def next_ind_src(self, max_num_cell_v, max_num_cell_h, l_pass_cell=0, break_num=0, af_break_num=0, break_exc=True):
        if l_pass_cell <= self._ix < (max_num_cell_h - 1):
            k = self._sx + 1 if break_exc or self._ix != break_num else self._nc
            self._ix = self._ix + 1 if break_exc or self._ix != break_num else af_break_num
            if self._nc > 0 and (self._ix - self._sx) >= (max_num_cell_h - self._nc):
                self._sx = k
                self.cnv_scr_repos(0)
                self.tab_render()
        elif self._ix == (max_num_cell_h - 1):
            self._ix = l_pass_cell
            self._sx = 0
            if self._nc > 0:
                self.cnv_scr_repos(0)
                self.tab_render()
            k = self._sy + 1 if self._iy < (max_num_cell_v - 1) else 0
            self._iy = self._iy + 1 if self._iy < (max_num_cell_v - 1) else 1
            if (self._nr > 0 and k == 0) or (
                    self._nr > 0 and (self._iy - self._sy) >= (max_num_cell_v - self._nr)):
                self._sy = k
                self.cnv_scr_repos(1)
                self.tab_render()

    def tab_upd_src(self, num_cell_v, num_cell_h, left_pad, mode=0):
        rd = 0
        cw = self.dim['CellWid']
        ch = self.dim['CellHgt']

        if self._sy > 0 and (num_cell_v - self._sy + 1.5)*ch < self._h:
            self._sy -= 1
            rd = 1
        if self._sx > 0 and (num_cell_h - self._sx + 1.5)*cw < (self._w - left_pad + 11):
            self._sx -= 1
            rd = 1
        if rd or mode:
            self.tab_render()

# -------------------------------------------------------------------------------------------------------------------- #
