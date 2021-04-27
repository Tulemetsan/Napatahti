# -------------------------------------------------------------------------------------------------------------------- #

import tkinter as tk
import core.utilities as ut
from math import sin, cos, radians
from .src_class import GuiSmartCell
from core.local import LocalKeywords
from core.config import ConfigKeys
from core.dbase import DataBaseSQLite
from core.astro_base import AstroBaseObject
from core.prim_stat import AstroRefBook, PrimStat
from core.asha_stat import AshaStat
from core.cosm_stat import CosmicStat
from core.asp_page import AspectPage
from core.asp_table import AspectTable

# @formatter:off


class DataMng(GuiSmartCell):
    cs_name = {
        0: 'AC', 1: 'I I', 2: 'I I I', 3: 'I C', 4: 'V', 5: 'V I',
        6: 'DC', 7: 'VIII', 8: 'I X', 9: 'MC', 10: 'X I', 11: 'XII'
    }
    esd_key = {
        0: {'InHeart': 6, 'InBurn': 7, 'SunZone': 8, 'FreeZone': 9},
        1: {'Antaeus': 2, 'Icarus': 3, 'Atlas': 0, 'Sisyphus': 1}, 2: {'RexAsp': 0, 'InPit': 1},
        3: {'Doriph': 4, 'Auriga': 5}, 4: {'Anareta': 1, 'Alcocoden': 0, 'DGenitura': 3}
    }
    msc = 0
    edc_flg = 1
    acf_row = -1
    acf_mrk = None
    md_tip = None
    cel_enb_var = {}
    tool_gui = {}
    tool_bt = {}
    app = None
    dim_lb, dbs_lb, evt_lb = None, None, None

    def __init__(self):
        GuiSmartCell.__init__(self)
        self.fic_st = {}
        self.fic_pr = {}
        self.pr_crd = {}
        self.acf_pl = {}

        self.conf = ConfigKeys()
        self.pth = self.conf.get_app_pth()
        self.var = self.conf.get_act_var()
        self.child = self.conf.get_app_chd()
        self.chd_ord = self.conf.get_ord_list()

        self.font = self.conf.get_src_font()
        self.app_col = self.conf.get_c_col(0)
        self.map_col = self.conf.get_c_col(1)
        self.crd_col = self.conf.get_c_col(3)
        self.stb_col = self.conf.get_c_col(4)
        self.cor_col = self.conf.get_c_col(5)
        self.asc_col = self.conf.get_c_col(6)

        self.app_dim = self.conf.get_c_dim(0)
        self.map_dim = self.conf.get_c_dim(1)
        self.dtc_dim = self.conf.get_c_dim(2)
        self.edt_dim = self.conf.get_c_dim(10)
        self.crd_dim = self.conf.get_c_dim(3)
        self.stb_dim = self.conf.get_c_dim(4)
        self.cor_dim = self.conf.get_c_dim(5)
        self.asc_dim = self.conf.get_c_dim(6)
        self.acf_dim = self.conf.get_c_dim(7)
        self.esd_dim = self.conf.get_c_dim(8)
        self.rec_dim = self.conf.get_c_dim(9)

        self.loc = LocalKeywords(self.conf)
        self.ckw = self.loc.get_sample_cell()
        self.tkw = self.loc.get_sample_tkw()
        self.mkw = self.loc.get_sample_mkw()
        self.fkw = self.loc.get_sample_fkw()
        self.month = self.loc.get_month()
        self.w_day = self.loc.get_week_day()
        self.h_sys = self.loc.get_sample_hss()
        self.acf_nm = self.loc.get_acf_name()

        self.dbs = DataBaseSQLite(self.conf)
        self.data = self.dbs.get_data_buf()

        self.abo = AstroBaseObject(self.pth[0], self.data)
        self.base_pl = self.abo.get_base_pl()
        self.cat_pl = self.abo.get_cat_pl()
        self.show_pl = self.abo.get_show_pl()
        self.pl_crd_enb = self.abo.get_pl_crd_enb()
        self.pl_enb = self.abo.get_pl_enb()
        self.pl_crd = self.abo.get_pl_crd()
        self.cs_crd = self.abo.get_cs_crd()
        self.pl_sgn = self.abo.get_pl_sgn()
        self.cs_sgn = self.abo.get_cs_sgn()
        self.pl_str = self.abo.get_pl_str()
        self.cs_str = self.abo.get_cs_str()

        self.moon_d = self.abo.get_moon_d()
        self.moon_c = self.abo.get_moon_c()
        self.zp = self.cs_crd[0] if self.var[5] & 1 else 0
        self.sg_sym = self.abo.get_sg_sym()
        self.cs_sym = self.abo.get_cs_sym()
        self.sp_sym = self.abo.get_sp_sym()

        self.arb = AstroRefBook(self.abo)
        self.kad_deg = self.arb.get_kd_deg()
        self.ess_sym = self.arb.get_ess_sym()

        self.pr_cos = PrimStat(self.abo, self.arb, self.var[11])
        self.pr_hor = PrimStat(self.abo, self.arb, self.var[11] | 1)
        self.cos_st = self.pr_cos.get_src_st()
        self.hor_st = self.pr_hor.get_src_st()
        self.el_4ce = {0: self.pr_cos.get_el4ce(), 1: self.pr_hor.get_el4ce()}
        self.cr_4ce = {0: self.pr_cos.get_cr4ce(), 1: self.pr_hor.get_cr4ce()}
        self.qu_4ce = {0: self.pr_cos.get_qu4ce(), 1: self.pr_hor.get_qu4ce()}
        self.zo_4ce = {0: self.pr_cos.get_zo4ce(), 1: self.pr_hor.get_zo4ce()}
        self.ns_4ce = {0: self.pr_cos.get_ns4ce(), 1: self.pr_hor.get_ns4ce()}
        self.ew_4ce = {0: self.pr_cos.get_ew4ce(), 1: self.pr_hor.get_ew4ce()}
        self.bs_4ce = {0: self.pr_cos.get_bs4ce(), 1: self.pr_hor.get_bs4ce()}

        self.ash = AshaStat(self.abo, self.arb)
        self.ash_pw = self.ash.get_asha_pw()
        self.ash_cr = self.ash.get_asha_cr()
        self.ash_st = self.ash.get_asha_st()
        self.ash_pl = self.ash.get_asha_pl()

        self.apg = AspectPage(self.conf, self.pr_cos.get_pln_st())
        self.asp_src = self.apg.get_asp_src()
        self.asp_enb = self.apg.get_asp_enb()
        self.asp_sym = self.apg.get_asp_prop(mode=1)
        self.asp_col = self.apg.get_asp_prop(mode=2)
        self.asp_ftp = self.apg.get_asp_prop(mode=3)
        self.asp_dsh = self.apg.get_asp_prop(mode=4)

        self.atb = AspectTable(self.abo, self.apg, self.conf, self.data)
        self.tab_4pl = self.atb.get_tab_4pl()
        self.tab_4mx = self.atb.get_tab_4mx()
        self.asp_fld = self.atb.get_asp_fld()
        self.asp_cfg = self.atb.get_asp_cfg()
        self.acf_bnd = self.atb.get_acf_bnd()
        self.fic_src = self.atb.get_fic_src()
        self.rex_pit = self.atb.get_rex_pit()

        self.cst = CosmicStat(self.abo, self.arb, self.atb)
        self.pl_rec = self.cst.get_pl_rec()
        self.cst_pl = self.cst.get_ess_pl()
        self.map_vw = self.cst.get_map_vw()
        self.csm_st = self.cst.get_csm_st()

        self.t_frame = tk.Frame(bg=self.app_col['ToolBkg'])
        self.m_frame = tk.Frame(bg=self.app_col['CellBkg'])
        self.b_frame = tk.Frame(bg=self.app_col['FootBkg'])

        self.cell[1] = tk.Canvas(self.m_frame, bg=self.app_col['CellBkg'], highlightthickness=0)
        self.cell[2] = tk.Canvas(self.m_frame, bg=self.app_col['CellBkg'], highlightthickness=0)
        self.cell[4] = tk.Canvas(self.m_frame, bg=self.app_col['CellBkg'], highlightthickness=0)
        self.cell[8] = tk.Canvas(self.m_frame, bg=self.app_col['CellBkg'], highlightthickness=0)
        self.cell[16] = tk.Canvas(self.m_frame, bg=self.app_col['CellBkg'], highlightthickness=0)
        self.cell[32] = tk.Canvas(self.m_frame, bg=self.app_col['CellBkg'], highlightthickness=0)
        self.cell[256] = tk.Canvas(self.m_frame, bg=self.app_col['CellBkg'], highlightthickness=0)
        self.cell[512] = tk.Canvas(self.m_frame, bg=self.app_col['CellBkg'], highlightthickness=0)
        self.cell[1024] = tk.Canvas(self.m_frame, bg=self.app_col['CellBkg'], highlightthickness=0)
        self.cell[2048] = tk.Canvas(self.m_frame, bg=self.app_col['CellBkg'], highlightthickness=0)

        for i in self.cell:
            self.geo[i] = self.conf.get_c_geo(i)

        self.calc_fic_st()
        self.calc_pr_crd()
        self.conf.set_act_var(1, self.abo.get_eph_rng())

        self.bind_pack_mov_res(self.cell[1], self.get_move_res_cb(1))
        self.bind_pack_mov_res(self.cell[2], self.get_move_res_cb(2))
        self.bind_pack_mov_res(self.cell[4], self.get_move_res_cb(4))
        self.bind_pack_mov_res(self.cell[8], self.get_move_res_cb(8))
        self.bind_pack_mov_res(self.cell[16], self.get_move_res_cb(16))
        self.bind_pack_mov_res(self.cell[32], self.get_move_res_cb(32))
        self.bind_pack_mov_res(self.cell[256], self.get_move_res_cb(256))
        self.bind_pack_mov_res(self.cell[512], self.get_move_res_cb(512))
        self.bind_pack_mov_res(self.cell[1024], self.get_move_res_cb(1024))
        self.bind_pack_mov_res(self.cell[2048], self.get_move_res_cb(2048))
        self.cell[32].bind('<Double-Button-1>', lambda *args: self.stb_invert())
        self.cell[32].bind('<Double-Button-2>', lambda *args: self.stb_sync())
        self.cell[256].bind('<Motion>', self.on_acf_mark)
        self.cell[256].bind('<Leave>', self.on_acf_mark)

    def get_move_res_cb(self, mode):
        if mode == 1:
            return (
                lambda event: self.on_cell_move(event, 1, self.conf.set_c_geo),
                lambda event: self.on_cell_resize(event, 1, self.conf.set_c_geo, self.map_render)
            )
        elif mode == 2:
            return (
                lambda event: self.on_cell_move(event, 2, self.conf.set_c_geo),
                lambda event: self.on_cell_resize(event, 2, self.conf.set_c_geo)
            )
        elif mode == 4:
            return (
                lambda event: self.edt_mov_res(event, mode=0),
                lambda event: self.edt_mov_res(event, mode=1)
            )
        elif mode == 8:
            return (
                lambda event: self.on_cell_move(event, 8, self.conf.set_c_geo),
                lambda event: self.on_cell_resize(event, 8, self.conf.set_c_geo)
            )
        elif mode == 16:
            return (
                lambda event: self.on_cell_move(event, 16, self.conf.set_c_geo),
                lambda event: self.on_cell_resize(event, 16, self.conf.set_c_geo)
            )
        elif mode == 32:
            return (
                lambda event: self.on_cell_move(event, 32, self.conf.set_c_geo),
                lambda event: self.on_cell_resize(event, 32, self.conf.set_c_geo, self.stb_render)
            )
        elif mode == 256:
            return (
                lambda event: self.acf_mov_res(event, mode=0),
                lambda event: self.acf_mov_res(event, mode=1)
            )
        elif mode == 512:
            return (
                lambda event: self.on_cell_move(event, 512, self.conf.set_c_geo),
                lambda event: self.on_cell_resize(event, 512, self.conf.set_c_geo)
            )
        elif mode == 1024:
            return (
                lambda event: self.on_cell_move(event, 1024, self.conf.set_c_geo),
                lambda event: self.on_cell_resize(event, 1024, self.conf.set_c_geo)
            )
        elif mode == 2048:
            return (
                lambda event: self.on_cell_move(event, 2048, self.conf.set_c_geo),
                lambda event: self.on_cell_resize(event, 2048, self.conf.set_c_geo)
            )

    def edt_mov_res(self, event, mode=0):
        self.app.config(cursor='arrow')
        self.edc_flg = 1
        self.md_tip.hidecontents()
        if mode:
            self.on_cell_resize(event, 4, self.conf.set_c_geo)
        else:
            self.on_cell_move(event, 4, self.conf.set_c_geo)

    def acf_mov_res(self, event, mode=0):
        self.acf_row = -1
        self.acf_mrk = None
        self.app.config(cursor='arrow')
        self.cell[1].delete('mrk')
        if mode:
            self.on_cell_resize(event, 256, self.conf.set_c_geo)
        else:
            self.on_cell_move(event, 256, self.conf.set_c_geo)

    def stb_invert(self):
        self.conf.set_act_var(12, self.var[12] ^ 1)
        self.stb_render()

    def stb_sync(self):
        self.conf.set_c_geo(32, y=self.geo[16]['y'])
        self.cell_set_pos(32)

    def on_acf_mark(self, event):
        if event.type == '6':
            fs = self.font['CellText'][1]
            sc = self.acf_dim['SnsZnScl']
            x1 = self.acf_dim['ZeroPnt'] - sc*fs
            x2 = self.acf_dim['ZeroPnt'] + 2*sc*fs
            y1 = self.acf_dim['PadY'] - 0.6*fs
            y2 = self.acf_dim['PadY'] + 0.6*fs
            st = self.acf_dim['Step']
            rw = -1

            for i in self.acf_pl:
                if y1 < event.y - i*st < y2 and x1 < event.x < x2:
                    rw = i
                    break
            if rw > -1:
                if rw != self.acf_row:
                    self.acf_row = rw
                    self.acf_mrk = self.acf_pl[rw]
                    self.app.config(cursor='hand2')
                    self.cont_render(rend=32)
            else:
                if rw != self.acf_row:
                    self.acf_row = -1
                    self.acf_mrk = None
                    self.app.config(cursor='arrow')
                    self.cont_render(rend=32)
        else:
            self.acf_row = -1
            self.acf_mrk = None
            self.app.config(cursor='arrow')
            self.cell[1].delete('mrk')

    def calc_fic_st(self):
        self.fic_st.clear()
        self.fic_pr.clear()

        if self.var[11] & 2:
            fic_src = self.fic_src[1]
        else:
            fic_src = self.fic_src[0]

        for i in fic_src:
            self.fic_st[i] = fic_src[i] + self.cos_st[i][0] + self.cos_st[i][1]
            self.fic_pr[i] = self.fic_st[i]

        self.scale_st(11, 23, self.fic_st, 7)
        self.scale_st(12, 56, self.fic_st, 7)

        self.fic_st[11] = [self.fic_st[11], ut.check(self.fic_pr[11], self.fic_pr[23])]
        self.fic_st[23] = [self.fic_st[23], ut.check(self.fic_pr[23], self.fic_pr[11])]
        self.fic_st[12] = [self.fic_st[12], ut.check(self.fic_pr[12], self.fic_pr[56])]
        self.fic_st[56] = [self.fic_st[56], ut.check(self.fic_pr[56], self.fic_pr[12])]

    @staticmethod
    def scale_st(ia, ib, seq, mx):
        sa = abs(seq[ia])
        sb = abs(seq[ib])
        if sa > mx or sb > mx:
            if sa != 0 and sb != 0:
                k = min(sa, sb)/max(sa, sb)
                if sa > sb:
                    seq[ia] = mx*seq[ia]/sa
                    seq[ib] = mx*k*seq[ib]/sb
                else:
                    seq[ia] = mx*k*seq[ia]/sa
                    seq[ib] = mx*seq[ib]/sb
            else:
                if sa == 0:
                    seq[ib] = mx
                else:
                    seq[ia] = mx

    def calc_pr_crd(self):
        bps = self.map_dim['BtwPnSpc']
        max_ind = int(360/bps) - 1

        crd, buf = [], []
        for i in self.show_pl:
            if i in self.pl_crd:
                crd.append([int(self.pl_crd[i]/bps), i])
                buf.append([self.pl_crd[i], i])
        buf = sorted(buf)

        k = len(crd)
        while k != len(dict(crd)):
            crd = sorted(crd)
            for i in range(k):
                if i < k - 1:
                    if crd[i][0] == crd[i+1][0]:
                        if crd[i+1][0] == max_ind:
                            crd[i+1][0] = 0
                            buf.insert(0, buf.pop(k - 1))
                        else:
                            crd[i+1][0] += 1
                else:
                    if crd[i][0] == crd[0][0]:
                        crd[0][0] += 1

        self.pr_crd.clear()
        crd = sorted(crd)
        for i in range(k):
            self.pr_crd[buf[i][1]] = bps * (crd[i][0] + 0.5)

    def cont_render(self, calc=0, rend=0):
        if self.var[13]:
            self.conf.set_act_var(13, 0)
        else:
            if calc & 1:
                self.abo.reload()
                self.zp = self.cs_crd[0] if self.var[5] & 1 else 0
                if self.child[6]:
                    self.tool_gui[6].set_reset()
            if calc & 2:
                self.arb.reload()
                self.pr_cos.reload(self.var[11])
                self.pr_hor.reload(self.var[11] | 1)
                self.ash.reload()
                if self.var[3] == '' and self.apg.get_st_flag():
                    self.apg.calc_blt_page()
                    if self.child[3]:
                        self.tool_gui[3].tab_render()
            if calc & 4:
                self.atb.reload()
                self.calc_fic_st()
                if self.child[5]:
                    self.tool_gui[5].update()
                self.cst.reload()
            if calc & 8:
                self.atb.calc_all_cfg()
            if calc & 16:
                self.calc_pr_crd()

        if rend & 1:
            self.dtc_render()
        if rend & 2:
            self.edt_render()
        if rend & 4:
            self.rec_render()
        if rend & 8:
            self.ess_data_render()
        if rend & 16:
            self.map_render()
        if rend & 32:
            self.map_render(1)
        if rend & 64:
            self.crd_render()
        if rend & 128:
            self.stb_render()
        if rend & 256:
            self.asp_cfg_render()
        if rend & 512:
            self.asp_stc_render()
        if rend & 1024:
            self.core_render(0)
            self.core_render(3)
        if rend & 2048:
            self.m_frame.configure(bg=self.app_col['CellBkg'])
            for i in self.cell:
                self.cell[i].configure(bg=self.app_col['CellBkg'])
        if rend & 4096:
            for i in [2, 3, 4, 5]:
                if self.child[i]:
                    self.tool_gui[i].apply_cfg()

            tbg = self.app_col['ToolBkg']
            tfg = self.app_col['ToolFrg']
            fbg = self.app_col['FootBkg']
            ffg = self.app_col['FootFrg']
            fnt = self.font['AppSpc']

            self.t_frame.configure(bg=tbg)
            for i in range(9):
                self.tool_bt[i].configure(bg=tbg, fg=tfg, font=fnt)

            self.b_frame.configure(bg=fbg)
            self.dim_lb.configure(bg=fbg, fg=ffg, font=fnt)
            self.dbs_lb.configure(bg=fbg, fg=ffg, font=fnt)
            self.evt_lb.configure(bg=fbg, fg=ffg, font=fnt)

    def repos_map(self, mode=0):
        if not mode:
            self.acf_row = -1
            self.acf_mrk = None
            self.app.config(cursor='arrow')
            self.conf.calc_repos(self.mf_w, self.mf_h)
        mask = 0
        for i in self.cel_enb_var:
            if self.var[9] & i:
                mask |= i
        self.cont_render(rend=2015)
        self.cell_set_pos(mask)

    def cell_set_pos(self, mask, mode=1):
        if mode:
            if mask & 1:
                self.cell[1].place(
                    width=self.geo[1]['w'], height=self.geo[1]['h'], x=self.geo[1]['x'], y=self.geo[1]['y'])
            if mask & 2:
                self.cell[2].place(
                    width=self.geo[2]['w'], height=self.geo[2]['h'], x=self.geo[2]['x'], y=self.geo[2]['y'])
            if mask & 4:
                self.cell[4].place(
                    width=self.geo[4]['w'], height=self.geo[4]['h'], x=self.geo[4]['x'], y=self.geo[4]['y'])
            if mask & 8:
                self.cell[8].place(
                    width=self.geo[8]['w'], height=self.geo[8]['h'], x=self.geo[8]['x'], y=self.geo[8]['y'])
            if mask & 16:
                self.cell[16].place(
                    width=self.geo[16]['w'], height=self.geo[16]['h'], x=self.geo[16]['x'], y=self.geo[16]['y'])
            if mask & 32:
                self.cell[32].place(
                    width=self.geo[32]['w'], height=self.geo[32]['h'], x=self.geo[32]['x'], y=self.geo[32]['y'])
            if mask & 64:
                self.m_frame.pack_forget()
                self.t_frame.pack(side=tk.TOP, fill=tk.X, expand=0)
                self.m_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            if mask & 128:
                self.b_frame.pack(side=tk.BOTTOM, fill=tk.X, expand=0)
            if mask & 256:
                self.cell[256].place(
                    width=self.geo[256]['w'], height=self.geo[256]['h'], x=self.geo[256]['x'], y=self.geo[256]['y'])
            if mask & 512:
                self.cell[512].place(
                    width=self.geo[512]['w'], height=self.geo[512]['h'], x=self.geo[512]['x'], y=self.geo[512]['y'])
            if mask & 1024:
                self.cell[1024].place(
                    width=self.geo[1024]['w'], height=self.geo[1024]['h'], x=self.geo[1024]['x'], y=self.geo[1024]['y'])
            if mask & 2048:
                self.cell[2048].place(
                    width=self.geo[2048]['w'], height=self.geo[2048]['h'], x=self.geo[2048]['x'], y=self.geo[2048]['y'])
        else:
            if mask & 1:
                self.cell[1].place_forget()
            if mask & 2:
                self.cell[2].place_forget()
            if mask & 4:
                self.cell[4].place_forget()
            if mask & 8:
                self.cell[8].place_forget()
            if mask & 16:
                self.cell[16].place_forget()
            if mask & 32:
                self.cell[32].place_forget()
            if mask & 64:
                self.t_frame.pack_forget()
            if mask & 128:
                self.b_frame.pack_forget()
            if mask & 256:
                self.cell[256].place_forget()
            if mask & 512:
                self.cell[512].place_forget()
            if mask & 1024:
                self.cell[1024].place_forget()
            if mask & 2048:
                self.cell[2048].place_forget()

    def dtc_render(self):
        col = self.app_col['CellFont']
        fnt = self.font['CellText']

        sam = self.data[1]
        mth = self.month[sam['date'][1]]
        wkd = self.w_day[self.abo.get_week_d()]
        sec = ':%02d' % sam['time'][2] if sam['time'][2] else ''
        utc = sam['time'][3]
        utc = '%+.1f' % utc if utc % 1 else '%+d' % utc if utc else ' %d' % utc

        txt = '%s\n' % (sam['name']) if sam['name'] else ''
        txt += '%d %s %d %s %d:%02d%s (UTC%s) %d%s%02d %d%s%02d' % (
            sam['date'][2], mth, sam['date'][0], wkd,
            sam['time'][0], sam['time'][1], sec, utc,
            sam['lat'][0], sam['lat'][3].lower(), sam['lat'][1],
            sam['lon'][0], sam['lon'][3].lower(), sam['lon'][1])
        txt += '\n%s' % (sam['place'])

        self.cell[2].delete('all')

        px = self.dtc_dim['PadX']
        py = self.dtc_dim['PadY']

        self.cell[2].create_text(px, py, text=txt, font=fnt, fill=col, anchor=tk.W)

    def edt_render(self):
        col = self.app_col['CellFont']
        fnt = {1: [self.font['CellText'][0], int(0.8*self.font['CellText'][1])], 2: self.font['CellText']}

        h_sys = self.h_sys[self.data[1]['sysHouse']]
        m_day = '%s %s' % (self.moon_d[self.var[19]][0], self.ckw['md'])

        self.cell[4].delete('all')

        x1 = self.edt_dim['PadX']
        y1 = self.edt_dim['PadY']
        y2 = y1 + 2*self.font['CellText'][1]

        self.cell[4].create_text(x1, y1, text=h_sys, font=fnt[1], fill=col, anchor=tk.W)
        self.cell[4].create_text(x1, y2, text=m_day, font=fnt[2], fill=col, anchor=tk.W)

    def rec_render(self):
        col = self.app_col['CellFont']
        fnt = self.font['CellSym']
        sym = '=÷+-×'

        self.cell[2048].delete('all')

        px = self.rec_dim['PadX']
        sy = self.rec_dim['PadY']
        mx = self.rec_dim['Count']
        st = self.rec_dim['Step']
        rec = ''
        cnt = 0

        for i in range(5):
            for j in self.pl_rec[i]:
                if cnt == mx:
                    self.cell[2048].create_text(px, sy, text=rec[:-2], font=fnt, fill=col, anchor=tk.W)
                    rec = ''
                    cnt = 0
                    sy += st
                rec += '%s%s%s, ' % (self.cat_pl[j[0]], sym[i], self.cat_pl[j[1]])
                cnt += 1
        if rec:
            self.cell[2048].create_text(px, sy, text=rec[:-2], font=fnt, fill=col, anchor=tk.W)

    def ess_data_render(self):
        dim = self.esd_dim
        key = self.esd_key
        col = self.app_col['CellFont']
        fnt = {0: self.font['CellText'], 1: self.font['CellSym']}
        cnd = {0: self.var[17] & 8, 1: self.var[17] & 1, 2: self.var[17] & 2, 3: self.var[17] & 4, 4: self.var[16] == 2}

        st = dim['Step']
        px = dim['PadX']
        sy = dim['PadY'] + st
        des, val, pad = [], [], []

        for i in key:
            if cnd[i]:
                for j in key[i]:
                    ind = key[i][j]
                    if i == 2:
                        seq = self.rex_pit
                    elif i == 4:
                        seq = self.ash_pl
                    else:
                        seq = self.cst_pl

                    if seq[ind]:
                        des.append(self.ckw[j])
                        buf = ''
                        for k in seq[ind]:
                            buf += self.cat_pl[k]
                        val.append(buf)
                        pad.append(dim[j])
                    else:
                        sy += st

                if i == 0 and (cnd[1] or cnd[3] or cnd[4] or (cnd[2] and (self.rex_pit[0] or self.rex_pit[1]))):
                    sy -= st
                    des.append('')
                    val.append('')
                    pad.append(0)
            else:
                sy += st * len(key[i])

        self.cell[1024].delete('all')

        for i in range(len(des)):
            self.cell[1024].create_text(px, sy, text=des[i], font=fnt[0], fill=col, anchor=tk.W)
            self.cell[1024].create_text(px + pad[i], sy, text=val[i], font=fnt[1], fill=col, anchor=tk.W)
            sy += st

    def map_render(self, mode=0):
        dim = self.map_dim
        col = self.map_col
        fnt = {
            0: self.font['AsMrk1'], 1: self.font['AsMrk2'], 2: self.font['SgSym'], 3: self.font['CsSym'],
            4: self.font['PnSym']
        }

        zx = 0.5*self.geo[1]['w']
        zy = 0.5*self.geo[1]['h']
        self.msc = int(1.1764*min(zx, zy) - 558.8235)

        tag = 'all'
        enb = {1: self.pl_enb}
        if mode:
            if self.acf_mrk:
                enb[1] = self.acf_mrk[1]
                enb[2] = self.acf_mrk[2]
                tag = 'mrk'
            else:
                tag = 'asp'

        self.cell[1].delete(tag)

        if not mode:
            dgb = self.var[5] & 2
            spb = self.var[5] & 4
            emb = self.var[5] & 16
            fnt[5] = [fnt[3][0], int(0.75*fnt[3][1])]
            fnt[6] = [fnt[4][0], int(0.55*fnt[4][1])]
            fnt[7] = [fnt[4][0], int(0.76*fnt[4][1])]
            sgn = [col['SgFire'], col['SgLand'], col['SgAir'], col['SgWater']] * 4
            emk = {
                0: self.crd_col['Ruler'], 1: self.crd_col['Detriment'], 2: self.crd_col['Exaltation'],
                3: self.crd_col['Fall'], -1: self.crd_col['Neutral']
            }

            # map base
            r1 = dim['BkgOval'] + self.msc
            r2 = dim['SgRad'] - 0.5*dim['SgWid'] + self.msc
            r3 = dim['SgWid']
            r4 = dim['InsOval'] + self.msc
            x1 = zx - dim['SgRad'] - self.msc
            y1 = zy - dim['SgRad'] - self.msc
            x2 = zx + dim['SgRad'] + self.msc
            y2 = zy + dim['SgRad'] + self.msc
            c1 = col['Border']
            c2 = col['BkgOval']
            c3 = col['SgSym']
            c4 = self.app_col['CellBkg']

            self.cell[1].create_oval(zx - r1, zy - r1, zx + r1, zy + r1, outline=c1, fill=c2, width=1)

            for i in range(12):
                a1 = self.zp - i*30
                a2 = radians(a1 - 15)
                self.cell[1].create_arc(x1, y1, x2, y2, start=a1, outline=c1, fill=sgn[i], width=1, extent=-30)
                self.cell[1].create_text(zx + r2*cos(a2), zy - r2*sin(a2), text=self.sg_sym[i], font=fnt[2], fill=c3)

            self.cell[1].create_oval(x1 + r3, y1 + r3, x2 - r3, y2 - r3, outline=c1, fill=c2, width=1)
            self.cell[1].create_oval(zx - r4, zy - r4, zx + r4, zy + r4, outline=c1, fill=c4, width=1)

            # cuspids
            if self.var[5] & 8:
                r1 = dim['InsOval'] + self.msc
                r2 = dim['InsOval'] + dim['CsSymExt'] + self.msc
                r3 = r1 + dim['CsLineExt']
                dx = dim['CsDegPx']
                dy = dim['CsDegPy']
                c1 = col['CsLine']
                c2 = col['CsSym']
                da = radians(dim['CsSymRot'])
                if self.var[5] & 1:
                    sh = {1, 2, 3, 4, 5, 6}
                else:
                    sh = set()
                    for i in self.cs_crd:
                        if 10 < self.cs_crd[i] < 190:
                            sh.add(i)

                for i in range(12):
                    a1 = radians(self.zp - self.cs_crd[i])
                    if i in sh:
                        a2 = a1 + da
                    else:
                        a2 = a1 - da
                    aw = tk.LAST if i in {0, 9} else None
                    wd = 2 if i in {0, 3, 6, 9} else 1
                    x2 = zx + r2*cos(a2)
                    y2 = zy - r2*sin(a2)

                    self.cell[1].create_line(
                        zx + r1*cos(a1), zy - r1*sin(a1), zx + r3*cos(a1), zy - r3*sin(a1), fill=c1, width=wd, arrow=aw)

                    self.cell[1].create_text(x2, y2, text=self.cs_name[i], font=fnt[3], fill=c2)
                    if dgb:
                        dg = int(self.cs_crd[i] - 30*self.cs_sgn[i] + 1)
                        self.cell[1].create_text(x2 + dx, y2 - dy, text=dg, font=fnt[5], fill=c2)

            # planets
            r1 = dim['InsOval'] + self.msc
            r2 = dim['PnCirRad'] + self.msc
            r3 = r2 - dim['PnLineExt']
            r4 = dim['PnMrkRad']
            dx = dim['PnDegPx']
            dy = dim['PnDegPy']
            sx = dim['PnSpdPx']
            sy = dim['PnSpdPy']
            c1 = col['Border']
            c2 = col['PnSym']
            c3 = col['PnLine']
            c4 = self.app_col['CellBkg']

            for i in self.pr_crd:
                a1 = radians(self.zp - self.pl_crd[i])
                a2 = radians(self.zp - self.pr_crd[i])
                x1 = zx + r1*cos(a1)
                y1 = zy - r1*sin(a1)
                x2 = zx + r2*cos(a2)
                y2 = zy - r2*sin(a2)
                if emb:
                    c2 = emk[self.ess_sym[0][i]] if i in self.ess_sym[0] else emk[-1]

                self.cell[1].create_text(x2, y2, text=self.cat_pl[i], font=fnt[4], fill=c2)
                if dgb:
                    dg = int(self.pl_crd[i] - 30*self.pl_sgn[i] + 1)
                    self.cell[1].create_text(x2 + dx, y2 - dy, text=dg, font=fnt[6], fill=c2)
                if spb:
                    self.cell[1].create_text(x2 + sx, y2 + sy, text=self.sp_sym[i], font=fnt[7], fill=c2)

                self.cell[1].create_line(x1, y1, zx + r3*cos(a2), zy - r3*sin(a2), fill=c3, width=1)
                self.cell[1].create_oval(x1 - r4, y1 - r4, x1 + r4, y1 + r4, fill=c4, outline=c1, width=1)

        # aspects
        r1 = dim['InsOval'] - dim['PnMrkRad'] + self.msc
        r2 = 0.2*dim['AsUniRad']
        dm = dim['AsMrkRad']
        sn = dim['PnMrkRad']/dim['InsOval']
        c1 = self.app_col['AcfMrk']
        cm = self.app_col['CellBkg']

        for j in self.tab_4pl:
            sam = self.tab_4pl[j]
            asp = sam[1]
            if asp not in self.asp_enb or j[0] not in enb[1] or j[1] not in enb[1]:
                continue
            if self.var[4] != 2 and self.var[4] != sam[3]:
                continue
            if self.acf_mrk:
                if asp > 0 and (j[0] not in enb[2] or j[1] not in enb[2]):
                    continue

            cr1 = self.pl_crd[j[0]]
            cr2 = self.pl_crd[j[1]]
            if self.acf_mrk:
                tag = (sam[4], 'asp', 'mrk', 'a%.2f' % sam[1])
                clr = c1
                dsh = None
                cwd = 3
            else:
                tag = (sam[4], 'asp', 'a%.2f' % sam[1])
                clr = self.asp_col[asp]
                dsh = self.asp_dsh[asp]
                cwd = 1
            a1 = radians(self.zp - cr1)
            a2 = radians(self.zp - cr2)
            ah = 0.5*sam[0]

            if sin(radians(ah)) <= sn:
                a3 = 0
                if cr1 < cr2:
                    if abs(cr1 - cr2) < 15:
                        a3 = cr1 + ah
                    else:
                        a3 = cr2 + ah
                elif cr2 < cr1:
                    if abs(cr1 - cr2) < 15:
                        a3 = cr2 + ah
                    else:
                        a3 = cr1 + ah
                a3 = radians(self.zp - a3)
                x3 = zx + r1*cos(a3)
                y3 = zy - r1*sin(a3)
                self.cell[1].create_oval(x3 - r2, y3 - r2, x3 + r2, y3 + r2, fill=clr, width=0, tag=tag)
            else:
                wid = r2 if asp == 0 else cwd
                self.cell[1].create_line(
                    zx + r1*cos(a1), zy - r1*sin(a1), zx + r1*cos(a2), zy - r1*sin(a2),
                    fill=clr, width=wid, dash=dsh, tag=tag)

            if asp not in {0, 180}:
                dc = cr1 - cr2
                da = 0
                if cr1 > cr2 and dc < 180:
                    da = -dc/2
                elif cr1 < cr2 and abs(dc) < 180:
                    da = -dc/2
                elif cr1 < cr2 and abs(dc) > 180:
                    da = -(360 + dc)/2
                elif cr1 > cr2 and dc > 180:
                    da = -(360 + dc)/2
                am = radians(self.zp - cr1 - da)
                rm = r1*cos(radians(0.5*sam[0]))
                xm = zx + rm*cos(am)
                ym = zy - rm*sin(am)

                self.cell[1].create_oval(xm - dm, ym - dm, xm + dm, ym + dm, fill=cm, width=0, tag=tag)
                self.cell[1].create_text(xm, ym, text=self.asp_sym[asp], fill=clr, font=fnt[self.asp_ftp[asp]], tag=tag)

    def stb_render(self):
        dim = self.stb_dim
        col = self.stb_col
        fnt = {0: self.font['StbMrk'], 1: [self.font['StbMrk'][0], 2*dim['StLineW']]}

        if self.var[16] == 2:
            up = self.ash_pw
            dw = self.ash_st
            if self.var[21] == 2:
                dw = self.ash_cr
            elif self.var[21] == 1:
                up = self.ash_st
        elif self.var[16] == 1:
            up = self.csm_st
            dw = self.csm_st
        else:
            up = self.hor_st
            dw = self.cos_st

        self.cell[32].delete('all')

        if self.var[12]:
            x1 = self.geo[32]['w'] - dim['PadX']
            m1 = -dim['StatMul']
        else:
            x1 = dim['PadX']
            m1 = dim['StatMul']

        st = self.crd_dim['Step']
        py = self.crd_dim['PadY']
        dy = dim['StLineDy']
        yu = py - dy - st
        yd = py + dy - st
        m2 = dim['AshMul']/100
        ws = dim['StLineW']
        wm = dim['MrkLineW']
        c1 = col['PosStat']
        c2 = col['NegStat']
        c3 = col['AshPow']
        c4 = col['AshCre']
        c5 = col['MrkLine']

        for i in self.show_pl:
            if i not in up:
                yu += st
                yd += st
                continue

            mrk = ''
            if self.var[16] == 2:
                if self.var[21] == 2:
                    vu = m2 * up[i]
                    vd = m2 * dw[i]
                    cu = c3
                    cd = c4
                elif self.var[21] == 1:
                    vu = 1.5 * m2 * up[i][0]
                    vd = 1.5 * m2 * dw[i][1]
                    cu = c1
                    cd = c2
                else:
                    vu = m2 * up[i]
                    vd = m2 * (dw[i][0] + dw[i][1])
                    cu = c3
                    cd = c1 if vd > 0 else c2
            elif self.var[16] == 1:
                if self.var[20]:
                    vu = 0.7 * up[i][0]
                    vd = 0.7 * dw[i][1]
                    cu = c1
                    cd = c2
                else:
                    vu = 0
                    vd = 0.7 * (dw[i][0] + dw[i][1])
                    cu = ''
                    cd = c1 if vd > 0 else c2
            else:
                if self.var[15] == 2:
                    vu = up[i][0] + up[i][1]
                    vd = dw[i][0] + dw[i][1]
                elif self.var[15] == 1:
                    vu = up[i][0]
                    vd = up[i][1]
                else:
                    vu = dw[i][0]
                    vd = dw[i][1]
                if i in self.fic_st:
                    vu = 0
                    vd = self.fic_st[i][0]
                    if self.fic_st[i][1] == 1:
                        mrk = '●'
                cu = c1 if vu > 0 else c2
                cd = c1 if vd > 0 else c2

            xu = x1 + m1 * abs(vu)
            xd = x1 + m1 * abs(vd)
            yu += st
            yd += st

            self.cell[32].create_line(x1, yu, xu, yu, fill=cu, width=ws)
            self.cell[32].create_line(x1, yd, xd, yd, fill=cd, width=ws)
            if mrk:
                self.cell[32].create_text(xd + 0.1*m1*ws, yd - 1, text=mrk, fill=cd, font=fnt[1])

        if self.var[16] in {0, 1}:
            vu = 10 if self.var[16] else 7
            xm = x1 + 7*m1
            yu = py - 2*dy + 1
            yd = yu + dy + st * (len(self.base_pl & self.pl_crd_enb) - 0.5)

            self.cell[32].create_line(xm, yu, xm, yd, fill=c5, width=wm, dash=1)
            self.cell[32].create_text(xm, yu - 8, text=vu, font=fnt[0], fill=c5)
            if self.var[16]:
                vd = '%s %s' % (self.ckw['sum'], self.cst.get_sum_st())
                self.cell[32].create_text(xm, yd + 8, text=vd, font=fnt[0], fill=c5)

    def crd_render(self):
        dim = self.crd_dim
        col = self.crd_col
        emk = {0: col['Ruler'], 1: col['Detriment'], 2: col['Exaltation'], 3: col['Fall'], -1: col['Neutral']}
        fnt = {0: self.font['CellSym'], 1: [self.font['CellText'][0], int(0.92*self.font['CellText'][1])]}

        self.cell[16].delete('all')

        px = dim['PadX']
        x1 = px + dim['PnSymPx']
        x2 = px + dim['PnCrdPx']
        x3 = px + dim['KdMrkPx']
        x4 = px + dim['StarPx']
        sy = dim['PadY']
        dy = dim['StarDy']
        st = dim['Step']
        c1 = col['Neutral']
        ck = col['KngDgMrk']
        cd = col['DesDgMrk']

        for i in self.show_pl:
            sym = self.cat_pl[i] + self.sp_sym[i] if self.sp_sym[i] else self.cat_pl[i] + '  '
            mxs = self.tab_4mx[0][i] if self.var[22] and i in self.tab_4mx[0] else ''

            c2 = emk[self.ess_sym[0][i]] if i in self.ess_sym[0] else emk[-1]
            dg = int(self.pl_crd[i])

            if dg in self.kad_deg[0]:
                mrk = '+'
                c3 = ck
            elif dg in self.kad_deg[1]:
                mrk = '×'
                c3 = cd
            else:
                mrk = ''
                c3 = ''

            self.cell[16].create_text(x1, sy, text=sym, font=fnt[0], fill=c2)
            self.cell[16].create_text(x2, sy, text=self.pl_str[i], font=fnt[0], anchor=tk.E, fill=c2)
            if mrk:
                self.cell[16].create_text(x3, sy, text=mrk, font=fnt[0], anchor=tk.E, fill=c3)
            if mxs:
                self.cell[16].create_text(x4, sy + dy, text=mxs, font=fnt[1], anchor=tk.W, fill=c1)
            sy += st

        for i in range(12):
            sym = self.cs_sym[i] + '  '
            mxs = self.tab_4mx[1][i] if self.var[22] and i in self.tab_4mx[1] else ''

            dg = int(self.cs_crd[i])
            sy += st

            if dg in self.kad_deg[0]:
                mrk = '+'
                c3 = ck
            elif dg in self.kad_deg[1]:
                mrk = '×'
                c3 = cd
            else:
                mrk = ''
                c3 = ''

            self.cell[16].create_text(x1, sy, text=sym, font=fnt[0], fill=c1)
            self.cell[16].create_text(x2, sy, text=self.cs_str[i], font=fnt[0], fill=c1, anchor=tk.E)
            if mrk:
                self.cell[16].create_text(x3, sy, text=mrk, font=fnt[0], anchor=tk.E, fill=c3)
            if mxs:
                self.cell[16].create_text(x4, sy + dy, text=mxs, font=fnt[1], anchor=tk.W, fill=c1)

    def core_render(self, mode):
        col = {0: self.cor_col['Neutral'], 1: self.cor_col['Dominant'], -1: self.cor_col['Weak']}
        swi = mode & 1

        if swi:
            prm = self.pr_hor
            tit = self.ckw['horTit']
        else:
            prm = self.pr_cos
            tit = self.ckw['cosTit']

        if mode & 2:
            px = self.cor_dim['PxHor']
            tag = 'HOR'
        else:
            px = self.cor_dim['PxCos']
            tag = 'COS'

        self.cell[8].delete(tag)

        if not self.var[14] & (swi + 1):
            return None

        el_4ce = self.el_4ce[swi]
        cr_4ce = self.cr_4ce[swi]
        qu_4ce = self.qu_4ce[swi]
        zo_4ce = self.zo_4ce[swi]
        ns_4ce = self.ns_4ce[swi]
        ew_4ce = self.ew_4ce[swi]
        bs_4ce = self.bs_4ce[swi]

        mtp = prm.get_map_tp()
        mtp = ',  %s' % mtp if mtp else ''
        end = '%s :  %s %+d%s' % (self.ckw['coreTit'], self.ckw[prm.get_core_st()], prm.get_sum_st(), mtp)

        m1 = 100 / (ns_4ce[0][0] + ns_4ce[1][0])
        m2 = 100 / (bs_4ce[0][0] + bs_4ce[1][0] + bs_4ce[2][0])

        ft = self.font['CellText']
        py = self.cor_dim['PadY']
        st = self.cor_dim['Step']
        sx = px - st + 6
        sy = py + st
        hs = round(0.6 * ft[1])
        dy = round(2.9 * hs)
        dx = self.cor_dim['TitleDx']
        cb = self.app_col['CellBkg']

        self.cell[8].create_text(px + dx, py, font=ft, text=tit, fill=col[0], anchor=tk.W, tag=tag)

        for i in range(21):
            sx += st
            if i == 4:
                sx += 0.6*st
            elif i == 7:
                sy += 1.8*st
                sx = px + 6
            elif i == 11:
                sx += 0.6*st
            elif i == 14:
                sy += 1.8*st
                sx = px + 6
            elif i == 18:
                sx += 0.6*st

            if i in {0, 1, 2, 3}:
                ic = i
                cs = col[el_4ce[ic][1]]
                ds = round(m1 * el_4ce[ic][0])
            elif i in {4, 5, 6}:
                ic = i - 4
                cs = col[cr_4ce[ic][1]]
                ds = round(m1 * cr_4ce[ic][0])
            elif i in {7, 8, 9, 10}:
                ic = i - 7
                cs = col[qu_4ce[ic][1]]
                ds = round(m1 * qu_4ce[ic][0])
            elif i in {11, 12, 13}:
                ic = i - 11
                cs = col[zo_4ce[ic][1]]
                ds = round(m1 * zo_4ce[ic][0])
            elif i in {14, 15}:
                ic = i - 14
                cs = col[ns_4ce[ic][1]]
                ds = round(m1 * ns_4ce[ic][0])
            elif i in {16, 17}:
                ic = i - 16
                cs = col[ew_4ce[ic][1]]
                ds = round(m1 * ew_4ce[ic][0])
            else:
                ic = i - 18
                cs = col[bs_4ce[ic][1]]
                ds = round(m2 * bs_4ce[ic][0])

            self.create_sym(i, sx, sy, hs, self.cell[8], cs, cb, tag)
            self.cell[8].create_text(sx, sy + dy, text=ds, font=ft, fill=col[0], tag=tag)

        self.cell[8].create_text(px + dx, py + 6.4*st, text=end, font=ft, fill=col[0], anchor=tk.W, tag=tag)

    @staticmethod
    def create_sym(ind, x, y, h, cnv, col, fill, tag=''):
        if ind in {0, 1, 2, 3}:  # elements
            if ind == 0:
                point = [x - h, y + h, x, y - h, x + h, y + h]
            elif ind == 1:
                point = [x - h, y - h, x + h, y - h, x, y + h]
            elif ind == 2:
                point = [x - 0.7*h, y + 0.4*h, x, y - h, x + h, y + h, x - h,
                         y + h, x - 0.7*h, y + 0.4*h, x + 0.7*h, y + 0.4*h]
            else:
                point = [x + 0.7*h, y - 0.4*h, x, y + h, x - h, y - h, x + h,
                         y - h, x + 0.7*h, y - 0.4*h, x - 0.7*h, y - 0.4*h]
            cnv.create_polygon(point, outline=col, fill=fill, tag=tag)
        elif ind in {4, 5, 6}:  # crosses
            cnv.create_rectangle(x - h, y - h, x + h, y + h, outline=col, fill=fill, tag=tag)
            if ind == 4:
                cnv.create_oval(x - 1, y - 1, x + 1, y + 1, outline=col, fill=col, tag=tag)
            elif ind == 5:
                cnv.create_line(x - h, y, x + h, y, fill=col, tag=tag)
                cnv.create_line(x, y - h, x, y + h, fill=col, tag=tag)
            else:
                point = [x - h + 1, y, x, y - h + 1, x + h - 1, y, x, y + h - 1]
                cnv.create_polygon(point, outline=col, fill=fill, tag=tag)
        elif ind in {7, 8, 9, 10}:  # quadrants
            cnv.create_rectangle(x - h, y - h, x + h, y + h, outline=col, fill=fill, tag=tag)
            if ind == 7:
                ax, ay = x, y
                bx, by = x + h, y + h
            elif ind == 8:
                ax, ay = x - h, y
                bx, by = x, y + h
            elif ind == 9:
                ax, ay = x - h, y - h
                bx, by = x, y
            else:
                ax, ay = x, y - h
                bx, by = x + h, y
            cnv.create_rectangle(ax, ay, bx, by, outline=col, fill=col, tag=tag)
        elif ind in {11, 12, 13}:  # zones
            cnv.create_oval(x - h, y - h, x + h, y + h, outline=col, fill=fill, tag=tag)
            if ind == 11:
                a = 0
            elif ind == 12:
                a = 240
            else:
                a = 120
            cnv.create_arc(x - h, y - h, x + h, y + h, outline=col, fill=col, tag=tag, start=a, extent=-120)
        elif ind in {14, 15, 16, 17}:  # hemispheres
            cnv.create_oval(x - h, y - h, x + h, y + h, outline=col, fill=fill, tag=tag)
            if ind == 14:
                a = 180
            elif ind == 15:
                a = 0
            elif ind == 16:
                a = 90
            else:
                a = 270
            cnv.create_arc(x - h, y - h, x + h, y + h, outline=col, fill=col, tag=tag, start=a, extent=-180)
        elif ind in {18, 19, 20}:  # bases
            cnv.create_oval(x - h, y - h, x + h, y + h, outline=col, fill=fill, tag=tag)
            if ind == 18:
                cnv.create_oval(x - 1, y - 1, x + 1, y + 1, outline=col, fill=col, tag=tag)
            elif ind == 19:
                cnv.create_line(x - h, y, x + h, y, fill=col, tag=tag)
                cnv.create_line(x, y - h, x, y + h, fill=col, tag=tag)
            else:
                point = [x - h + 1, y, x, y - h + 1, x + h - 1, y, x, y + h - 1]
                cnv.create_polygon(point, outline=col, fill=fill, tag=tag)
        elif ind in {21, 22, 23, 24, 25, 26}:  # aspect statistic
            sym = 'qweQN+'
            if ind == 26:
                font = ('Serif', h + 4)
            elif ind in {24, 25}:
                font = ('Serif', h)
            else:
                font = ('HamburgSymbols', h)
            dy = 1 if ind in {21, 22, 23} else 0
            cnv.create_rectangle(x - h, y - h, x + h, y + h, outline=col, fill=fill, tag=tag)
            cnv.create_text(x, y + dy, text=sym[ind-21], font=font, fill=col, tag=tag)

    def asp_cfg_render(self):
        self.acf_pl.clear()
        fnt = {0: self.font['CellText'], 1: self.font['CellSym']}

        self.cell[256].delete('all')

        x1 = self.acf_dim['PadX'] + self.acf_dim['ZeroPnt']
        x2 = x1 + self.acf_dim['PnPadX']
        sy = self.acf_dim['PadY']
        st = self.acf_dim['Step']
        c1 = self.app_col['CellFont']
        vw = self.var[8] & 4
        rw = 0

        for i in self.asp_cfg:
            if self.asp_cfg[i]:
                des = self.acf_nm[i] if i in self.acf_nm else i
                for j in self.asp_cfg[i]:
                    val = ''
                    bnd = self.acf_bnd[tuple(j)]
                    if vw:
                        self.acf_pl[rw] = {1: bnd, 2: bnd}
                        cfg = self.atb.sort_by_crd(bnd)
                    else:
                        self.acf_pl[rw] = {1: set(j), 2: bnd}
                        cfg = j
                    for k in cfg:
                        val += '%s' % self.cat_pl[k]

                    self.cell[256].create_text(x1, sy, text=des, font=fnt[0], fill=c1, anchor=tk.E)
                    self.cell[256].create_text(x2, sy, text=val, font=fnt[1], fill=c1, anchor=tk.W)

                    sy += st
                    rw += 1

    def asp_stc_render(self):
        col = {0: self.asc_col['Neutral'], 1: self.asc_col['Dominant'], -1: self.asc_col['Weak']}

        self.cell[512].delete('all')

        ft = self.font['CellText']
        st = self.asc_dim['Step']
        sx = self.asc_dim['PadX'] - st
        ys = self.asc_dim['PadY']
        hs = round(0.7 * ft[1])
        dy = 2.8 * hs
        cb = self.app_col['CellBkg']

        for i in range(6):
            sx += st
            cs = col[0] if i in {0, 5} else col[self.asp_fld[i][1]]
            ds = round(self.asp_fld[i][0]) if i < 5 else self.atb.get_asp_num()

            self.create_sym(i + 21, sx, ys, hs, self.cell[512], cs, cb)
            self.cell[512].create_text(sx, ys + dy, text=ds, font=ft, fill=col[0])

# -------------------------------------------------------------------------------------------------------------------- #
