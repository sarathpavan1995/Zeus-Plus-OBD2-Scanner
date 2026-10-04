#!/usr/bin/env python3
"""
ZEUS+ OBD2 SCANNER — FULL MERGED VERSION
Includes ALL features from Karthika Diesel Service Scanner
ZEUS+ Design Style | python-obd + Bluetooth | Tkinter UI
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import threading, time, math, random, json, os
from datetime import datetime

# ── PIL for PNG icons ─────────────────────────────────────────
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

# ── python-obd ────────────────────────────────────────────────
try:
    import obd
    OBD_AVAILABLE = True
except ImportError:
    OBD_AVAILABLE = False

# ── Bluetooth ─────────────────────────────────────────────────
try:
    import bluetooth
    BT_AVAILABLE = True
except ImportError:
    BT_AVAILABLE = False

# ═════════════════════════════════════════════════════════════
#  ZEUS+ THEME
# ═════════════════════════════════════════════════════════════
BG_DARK   = "#F0F4F8"
BG_CARD   = "#2C3E50"
BG_CARD2  = "#2C3E51"
BG_ROW    = "#3E648D"
RED       = "#9b0013"
RED_DARK  = "#BB4242"
TEAL      = "#C55151"
WHITE     = "#f0f0f0"
GRAY      = "#888888"
GRAY_L    = "#F8FAFC"
GREEN     = "#C55151"
YELLOW    = "#ff6d00"
ORANGE    = "#CD4D4D"
BLUE      = "#793131"
CYAN      = "#F8FAFC"
PURPLE    = "#07FBD2"

FT        = ("Consolas", 11)
FT_HD     = ("Consolas", 13, "bold")
FT_SM     = ("Consolas", 9)
FT_TT     = ("Consolas", 22, "bold")
FT_BIG    = ("Consolas", 18, "bold")
FT_MED    = ("Consolas", 15, "bold")

# ═════════════════════════════════════════════════════════════
#  SENSOR / DTC DATA (from Karthika Scanner)
# ═════════════════════════════════════════════════════════════
LIVE_SENSORS = [
    ("Crankshaft Sensor",                        "GET_CRANK",       "750 RPM"),
    ("Camshaft Sensor",                          "GET_CAM",         "375 RPM"),
    ("MAF (Mass Air Flow) Sensor",               "GET_MAF",         "3.5 g/s"),
    ("MAP (Manifold Absolute Pressure) Sensor",  "GET_MAP",         "101 kPa"),
    ("ECT (Engine Coolant Temp) Sensor",         "GET_ECT",         "85 °C"),
    ("Throttle Position Sensor",                 "GET_TPS",         "15 %"),
    ("Knock Sensor",                             "GET_KNOCK",       "Normal"),
    ("IAT (Intake Air Temp) Sensor",             "GET_IAT",         "32 °C"),
    ("Turbo Boost Sensor",                       "GET_BOOST",       "1.1 bar"),
    ("Fuel Rail Pressure Sensor",                "GET_FUEL_PRESS",  "320 bar"),
    ("Fuel Composition Sensor",                  "GET_FUEL_TYPE",   "Diesel"),
    ("Fuel Temp Sensor",                         "GET_FUEL_TEMP",   "38 °C"),
    ("Fuel Level Sensor",                        "GET_FUEL_LEVEL",  "48 %"),
    ("Injector 1 Monitor",                       "GET_INJ1",        "2.4 ms"),
    ("Injector 2 Monitor",                       "GET_INJ2",        "2.4 ms"),
    ("Injector 3 Monitor",                       "GET_INJ3",        "2.4 ms"),
    ("Injector 4 Monitor",                       "GET_INJ4",        "2.4 ms"),
    ("O2 Upstream Sensor",                       "GET_O2_UP",       "0.45 V"),
    ("O2 Downstream Sensor",                     "GET_O2_DN",       "0.70 V"),
    ("EGR Temp Sensor",                          "GET_EGR",         "121 °C"),
    ("Exhaust Back Pressure Sensor",             "GET_EXH_BACK",    "18 kPa"),
    ("NOx Sensor",                               "GET_NOX",         "120 ppm"),
    ("PM (Particulate Matter) Sensor",           "GET_PM",          "Normal"),
    ("DPF Pressure Sensor",                      "GET_DPF",         "6 kPa"),
    ("DEF (AdBlue) Level Sensor",                "GET_DEF_LEVEL",   "65 %"),
    ("EVAP Pressure Sensor",                     "GET_EVAP",        "OK"),
    ("Oil Level Sensor",                         "GET_OIL_LEVEL",   "OK"),
    ("Oil Pressure Sensor",                      "GET_OIL_PRESS",   "3.2 bar"),
    ("Transmission Input Speed Sensor",          "GET_GEAR_IN",     "1800 RPM"),
    ("Transmission Output Speed Sensor",         "GET_GEAR_OUT",    "900 RPM"),
    ("Gear Position Sensor",                     "GET_GEAR_POS",    "3"),
    ("Clutch Status Sensor",                     "GET_CLUTCH",      "Released"),
    ("Wheel Speed Sensor FL",                    "GET_ABS_FL",      "42 km/h"),
    ("Wheel Speed Sensor FR",                    "GET_ABS_FR",      "41 km/h"),
    ("Brake Pedal Sensor",                       "GET_BRAKE",       "Pressed"),
    ("Steering Angle Sensor",                    "GET_STEER",       "5 deg"),
    ("Impact/Crash Sensor",                      "GET_IMPACT",      "No Crash"),
    ("Seat Occupancy Sensor",                    "GET_SEAT",        "Detected"),
    ("Yaw Rate Sensor",                          "GET_YAW",         "0.3 deg/s"),
    ("Lateral Accel (G) Sensor",                 "GET_LAT_G",       "0.02 g"),
    ("TPMS (Tire Pressure Sensor)",              "GET_TPMS",        "32 PSI"),
    ("Ambient Temp Sensor",                      "GET_AMB_TEMP",    "30 °C"),
    ("Cabin Temp Sensor",                        "GET_CABIN_TEMP",  "24 °C"),
    ("Sunlight/Solar Sensor",                    "GET_SUN",         "High"),
    ("Rain Sensor",                              "GET_RAIN",        "No Rain"),
    ("Light/LDR Sensor",                         "GET_LIGHT",       "Night"),
    ("Door Status Sensor",                       "GET_DOOR",        "Closed"),
    ("Seatbelt Sensor",                          "GET_SEATBELT",    "Fastened"),
    ("Long Range Radar",                         "GET_RADAR_LR",    "Active"),
    ("Short Range Radar",                        "GET_RADAR_SR",    "Active"),
    ("Front Camera / Vision Sensor",             "GET_CAMERA",      "OK"),
    ("LiDAR Sensor",                             "GET_LIDAR",       "Active"),
]

DTC_LIST = [
    ("P0335", "Crankshaft Position Sensor Circuit",         "Active"),
    ("P0340", "Camshaft Position Sensor Circuit",           "Active"),
    ("P0100", "MAF Sensor Malfunction",                     "Pending"),
    ("P0105", "MAP Sensor Range Problem",                   "Stored"),
    ("P0115", "Coolant Temp Sensor Circuit",                "Stored"),
    ("P0120", "Throttle Position Sensor",                   "Pending"),
    ("P0130", "O2 Sensor Circuit",                          "Active"),
    ("P0325", "Knock Sensor Circuit",                       "Stored"),
    ("P0201", "Injector 1 Circuit",                         "Active"),
    ("P0202", "Injector 2 Circuit",                         "Pending"),
    ("P0203", "Injector 3 Circuit",                         "Stored"),
    ("P0204", "Injector 4 Circuit",                         "Stored"),
    ("P0700", "Transmission Control System",                "Active"),
    ("C0035", "Front Left Wheel Speed Sensor",              "Stored"),
    ("P0401", "EGR Flow Insufficient",                      "Active"),
    ("P2463", "DPF Soot Accumulation",                      "Active"),
    ("B1325", "Battery Voltage Low",                        "Pending"),
]

WARNING_CODES = [
    ("Injector Coding (IMA/ISA Coding)",         "INJ_CODING"),
    ("Throttle Body Alignment",                  "TBA"),
    ("Battery Management System (BMS) Reset",    "BMS_RESET"),
    ("Steering Angle Sensor (SAS) Calibration",  "SAS_CAL"),
    ("Transmission Adaptation",                  "TRANS_ADAPT"),
    ("Key Fob Programming",                      "KEY_FOB"),
    ("Cloud Backup & Restore",                   "CLOUD_BACKUP"),
    ("Hard Reset",                               "HARD_RESET"),
    ("Clear Learned Values",                     "CLEAR_LEARN"),
    ("DTC (Diagnostic Trouble Codes) Clear",     "ERASE_FAULT"),
    ("Service Interval Reset",                   "SVC_RESET"),
    ("Initialization (Learning Process)",        "INIT_LEARN"),
    ("Lighting Settings",                        "LIGHT_SET"),
    ("Instrument Cluster",                       "INST_CLUSTER"),
    ("Locking & Alarms",                         "LOCK_ALARM"),
    ("Safety & Comfort",                         "SAFETY"),
    ("SCN Coding (Software Calibration Number)", "SCN_CODE"),
    ("Firmware Over-The-Air (FOTA) Management",  "FOTA"),
]

LIBRARY_ITEMS = [
    ("", "DTC Code Reference Book"),
    ("", "Sensor Wiring Diagrams"),
    ("", "Diesel Engine Service Manual"),
    ("", "CAN Bus Protocol Guide"),
    ("", "ESP32 Pin Reference"),
    ("", "OBD2 PID List"),
    ("", "Injector Coding Guide"),
    ("", "Coolant System Diagram"),
    ("", "Turbo System Reference"),
    ("", "ABS/ESP System Guide"),
]

CHART_ITEMS = [
    (" Engine Health Radar Chart",   "engine_health"),
    (" Cylinder Balance Chart",      "cylinder_balance"),
    (" Injector Performance Chart",  "injector_perf"),
    (" Fuel Rail Pressure Chart",    "fuel_rail"),
    ("O2 Sensor Live Test",         "o2_test"),
    ("Injector Full Test",          "inj_test"),
    (" VIN Reader",                  "vin_reader"),
    ("ECU Information",             "ecu_info"),
    ("AI Fault Diagnosis",          "ai_fault"),
    ("Freeze Frame Data",           "freeze_frame"),
]

# ═════════════════════════════════════════════════════════════
#  BLUETOOTH MANAGER
# ═════════════════════════════════════════════════════════════
class BTManager:
    def __init__(self):
        self.sock        = None
        self.connected   = False
        self.device_name = "Not Connected"

    def scan(self):
        demo = [("Karthika Diesel Scanner", "AA:BB:CC:DD:EE:FF"),
                ("OBD_ESP32_BT",            "11:22:33:44:55:66"),
                ("ELM327 Bluetooth",        "00:1D:A5:00:00:00")]
        if BT_AVAILABLE:
            try:
                found = bluetooth.discover_devices(lookup_names=True, duration=4)
                if found:
                    return found
            except:
                pass
        return demo

    def connect(self, addr, name):
        if BT_AVAILABLE:
            try:
                self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
                self.sock.connect((addr, 1))
                self.connected   = True
                self.device_name = name
                return True
            except:
                pass
        # Demo mode
        self.connected   = True
        self.device_name = name + " (Demo)"
        return True

    def disconnect(self):
        if self.sock:
            try: self.sock.close()
            except: pass
        self.sock        = None
        self.connected   = False
        self.device_name = "Not Connected"

    def send(self, cmd):
        if self.sock and self.connected:
            try:
                self.sock.send((cmd + "\n").encode())
                time.sleep(0.12)
                return self.sock.recv(256).decode().strip()
            except:
                self.connected = False
        # Demo responses
        demo_map = {
            "GET_VIN":      "VIN:1HGCM82633A123456",
            "GET_ECU_INFO": json.dumps({"make":"Toyota","model":"Hilux","year":"2019",
                                        "dtc":3,"can":"CAN 2.0B","vin":"1HGCM82633A123456",
                                        "status":"FAULT DETECTED","advice":"Check injectors",
                                        "confidence":"87%"}),
            "ANALYZE_AI":   json.dumps({"status":"FAULT DETECTED","advice":"Check fuel injector #2 pulse width",
                                        "confidence":"87%","rpm":1850,"temp":92,"fuel":320,"o2":0.45}),
            "GET_FREEZE":   json.dumps({"dtc":"P0201","rpm":2200,"temp":88,"throttle":52.3,
                                        "maf":14.2,"speed":45,"fuel":310}),
            "O2_TEST":      json.dumps({"upstream_v":0.45+math.sin(time.time()*3)*0.35,
                                        "downstream_v":0.65+random.uniform(-0.05,0.05),
                                        "catalyst_ok":True,"result":"UP:NORMAL DN:CAT_OK"}),
        }
        for key in demo_map:
            if cmd.startswith(key):
                return demo_map[key]
        # Generic sensor
        for name, cmd2, val in LIVE_SENSORS:
            if cmd == cmd2:
                try:
                    parts = val.split()
                    num = float(parts[0])
                    unit = parts[1] if len(parts)>1 else ""
                    noise = random.uniform(-2, 2)
                    return f"{num+noise:.1f} {unit}"
                except:
                    return val
        return f"OK:{cmd}"


bt = BTManager()

# ═════════════════════════════════════════════════════════════
#  OBD MANAGER
# ═════════════════════════════════════════════════════════════
class OBDManager:
    def __init__(self):
        self.connection = None
        self.connected  = False
        self.mock       = True

    def connect(self, port=None):
        if not OBD_AVAILABLE:
            self.mock = True; self.connected = True
            return True, "Demo Mode (install python-obd for real data)"
        try:
            self.connection = obd.OBD(port) if port else obd.OBD()
            if self.connection.is_connected():
                self.mock = False; self.connected = True
                return True, "Connected to OBD2 port"
            self.mock = True; self.connected = True
            return True, "Demo Mode (no OBD device)"
        except Exception as e:
            self.mock = True; self.connected = True
            return True, f"Demo Mode ({str(e)[:40]})"

    def disconnect(self):
        if self.connection:
            try: self.connection.close()
            except: pass
        self.connected = False; self.mock = True

    def get_live(self):
        if self.mock:
            data = {}
            for name, cmd, val in LIVE_SENSORS[:12]:
                try:
                    parts = val.split()
                    num = float(parts[0]) + random.uniform(-2,2)
                    unit = parts[1] if len(parts)>1 else ""
                    data[name] = f"{num:.1f} {unit}"
                except:
                    data[name] = val
            return data
        cmds = {
            "RPM":          obd.commands.RPM,
            "Speed":        obd.commands.SPEED,
            "Coolant Temp": obd.commands.COOLANT_TEMP,
            "Engine Load":  obd.commands.ENGINE_LOAD,
            "Throttle Pos": obd.commands.THROTTLE_POS,
            "MAF Rate":     obd.commands.MAF,
            "Intake Temp":  obd.commands.INTAKE_TEMP,
        }
        result = {}
        for name, cmd in cmds.items():
            try:
                r = self.connection.query(cmd)
                if not r.is_null():
                    v = str(r.value.magnitude) if hasattr(r.value,'magnitude') else str(r.value)
                    u = str(r.value.units) if hasattr(r.value,'units') else ""
                    result[name] = f"{v} {u}"
            except: pass
        return result

    def get_dtcs(self):
        if self.mock:
            return DTC_LIST
        try:
            r = self.connection.query(obd.commands.GET_DTC)
            if not r.is_null():
                return [(str(c), str(d), "Active") for c,d in r.value]
        except: pass
        return []

    def clear_dtcs(self):
        if self.mock: return True
        try:
            self.connection.query(obd.commands.CLEAR_DTC); return True
        except: return False


obd_mgr = OBDManager()

# ═════════════════════════════════════════════════════════════
#  ANIMATED CANVAS WIDGETS (Radar, Cylinder, Fuel, O2)
# ═════════════════════════════════════════════════════════════
class RadarCanvas(tk.Canvas):
    """Engine Health Radar Chart"""
    def __init__(self, parent):
        super().__init__(parent, bg=BG_CARD, highlightthickness=0)
        self.t = 0
        self._animate()

    def _animate(self):
        self._draw()
        self.t += 0.03
        self.after(50, self._animate)

    def _draw(self):
        self.delete("all")
        w, h   = self.winfo_width(), self.winfo_height()
        if w < 10: return
        cx, cy = w//2, h//2
        r      = min(w, h) * 0.38
        n      = 6
        labels = ["RPM","Temp","Fuel","O2","Load","EGR"]
        angles = [math.pi/2 + 2*math.pi*i/n for i in range(n)]
        ideal  = [48,45,38,10,20,30]
        curr   = [40+8*math.sin(self.t), 40+5*math.cos(self.t*0.7),
                  30+4*math.sin(self.t*1.2), 8+3*math.cos(self.t*0.5),
                  15+5*math.sin(self.t*0.9), 25+6*math.cos(self.t*1.1)]
        mx = 60
        # Grid rings
        for lvl in [0.25, 0.5, 0.75, 1.0]:
            pts = []
            for ang in angles:
                pts.append(cx + r*lvl*math.cos(ang))
                pts.append(cy - r*lvl*math.sin(ang))
            pts += pts[:2]
            self.create_line(pts, fill="#334466", width=1)
        # Spokes + labels
        for i, ang in enumerate(angles):
            ex = cx + r*math.cos(ang); ey = cy - r*math.sin(ang)
            self.create_line(cx, cy, ex, ey, fill="#334466")
            lx = cx + (r+22)*math.cos(ang); ly = cy - (r+22)*math.sin(ang)
            self.create_text(lx, ly, text=labels[i], font=FT_SM, fill=TEAL)
        # Ideal polygon (red)
        ip = []
        for i, ang in enumerate(angles):
            f = ideal[i]/mx
            ip.append(cx + r*f*math.cos(ang)); ip.append(cy - r*f*math.sin(ang))
        ip_closed = ip + ip[:2]
        self.create_line(ip_closed, fill=RED, width=2)
        for i in range(0, len(ip), 2):
            self.create_oval(ip[i]-5, ip[i+1]-5, ip[i]+5, ip[i+1]+5, fill=RED, outline="")
        # Current polygon (cyan)
        cp = []
        for i, ang in enumerate(angles):
            f = curr[i]/mx
            cp.append(cx + r*f*math.cos(ang)); cp.append(cy - r*f*math.sin(ang))
        cp_closed = cp + cp[:2]
        self.create_line(cp_closed, fill=TEAL, width=2)
        for i in range(0, len(cp), 2):
            self.create_oval(cp[i]-6, cp[i+1]-6, cp[i]+6, cp[i+1]+6, fill=TEAL, outline="")
        # Legend
        self.create_rectangle(10,10,30,20, fill=RED, outline="")
        self.create_text(35,15, text="Ideal", font=FT_SM, fill=WHITE, anchor="w")
        self.create_rectangle(80,10,100,20, fill=TEAL, outline="")
        self.create_text(105,15, text="Current", font=FT_SM, fill=WHITE, anchor="w")


class CylCanvas(tk.Canvas):
    """Cylinder Balance / Injector Performance"""
    def __init__(self, parent, title=""):
        super().__init__(parent, bg=BG_CARD, highlightthickness=0)
        self.t = 0; self.title = title
        self._animate()

    def _animate(self):
        self._draw(); self.t += 0.04
        self.after(50, self._animate)

    def _draw(self):
        self.delete("all")
        w, h = self.winfo_width(), self.winfo_height()
        if w < 10: return
        cx, cy = 50, h-30
        aw, ah = w-70, h-60
        n, mx  = 12, 80
        colors = [TEAL, GREEN, PURPLE, ORANGE]
        series = [
            (colors[0], lambda i: 16+48*max(0,math.sin(i*0.5-1))+2*math.sin(self.t+i)),
            (colors[1], lambda i: 12+50*max(0,math.sin(i*0.5-1.5))+2*math.sin(self.t+i+1)),
            (colors[2], lambda i: 9+3*math.cos(self.t*0.9+i*0.4)),
            (colors[3], lambda i: 5+2*math.sin(self.t*1.2+i*0.2)),
        ]
        # Grid
        for lvl in [20,40,60,80]:
            yy = cy - lvl/mx*ah
            self.create_line(cx, yy, cx+aw, yy, fill="#334466", dash=(4,4))
        # Axes
        self.create_line(cx, cy-ah, cx, cy, fill=GRAY_L, width=1)
        self.create_line(cx, cy, cx+aw, cy, fill=GRAY_L, width=1)
        # Series lines
        for col, fn in series:
            pts = []
            for i in range(n):
                px = cx + i/(n-1)*aw
                py = cy - fn(i)/mx*ah
                pts += [px, py]
            self.create_line(pts, fill=col, width=2)
            for i in range(n):
                px = cx + i/(n-1)*aw; py = cy - fn(i)/mx*ah
                self.create_oval(px-4, py-4, px+4, py+4, fill=col, outline="")
        # Legend
        for k, (col, _) in enumerate(series):
            self.create_rectangle(10+k*70, 8, 28+k*70, 18, fill=col, outline="")
            self.create_text(32+k*70, 13, text=f"Cyl {k+1}", font=FT_SM,
                             fill=WHITE, anchor="w")


class FuelCanvas(tk.Canvas):
    """Fuel Rail Pressure Chart"""
    def __init__(self, parent):
        super().__init__(parent, bg=BG_CARD, highlightthickness=0)
        self.t = 0
        self._animate()

    def _animate(self):
        self._draw(); self.t += 0.04
        self.after(50, self._animate)

    def _draw(self):
        self.delete("all")
        w, h = self.winfo_width(), self.winfo_height()
        if w < 10: return
        cx, cy = 50, h-30
        aw, ah = w-70, h-60
        n, mx  = 18, 1400
        def tgt(i): return 550*max(0,math.sin(math.pi*i/(n-1)))
        def act(i): return 750*max(0,math.sin(math.pi*(i-2.5)/(n-4)))*max(0,(i-1)/n)
        # Grid
        for lvl in [200,400,600,800,1000,1200,1400]:
            yy = cy - lvl/mx*ah
            self.create_line(cx, yy, cx+aw, yy, fill="#334466", dash=(6,4))
            self.create_text(cx-4, yy, text=str(lvl), font=FT_SM,
                             fill=GRAY, anchor="e")
        # Axes
        self.create_line(cx, cy-ah, cx, cy, fill=GRAY_L, width=1)
        self.create_line(cx, cy, cx+aw, cy, fill=GRAY_L, width=1)
        # Target (blue)
        tp = []
        for i in range(n):
            tp += [cx+i/(n-1)*aw, cy-(tgt(i)+5*math.sin(self.t+i))/mx*ah]
        self.create_line(tp, fill=TEAL, width=2)
        # Actual (red)
        ap = []
        for i in range(n):
            ap += [cx+i/(n-1)*aw, cy-(act(i)+8*math.sin(self.t*1.2+i))/mx*ah]
        self.create_line(ap, fill=RED, width=2)
        # Legend
        self.create_rectangle(10,8,30,18, fill=TEAL, outline="")
        self.create_text(34,13, text="Target", font=FT_SM, fill=WHITE, anchor="w")
        self.create_rectangle(90,8,110,18, fill=RED, outline="")
        self.create_text(114,13, text="Actual", font=FT_SM, fill=WHITE, anchor="w")


class O2Canvas(tk.Canvas):
    """O2 Sensor Live Chart"""
    def __init__(self, parent):
        super().__init__(parent, bg=BG_CARD, highlightthickness=0, height=180)
        self._up_vals = [0.45]*20
        self._dn_vals = [0.65]*20

    def update_vals(self, up, dn):
        self._up_vals.append(up); self._up_vals = self._up_vals[-20:]
        self._dn_vals.append(dn); self._dn_vals = self._dn_vals[-20:]
        self._draw()

    def _draw(self):
        self.delete("all")
        w, h = self.winfo_width(), self.winfo_height()
        if w < 10: return
        x0, y0 = 10, 10
        aw, ah = w-20, h-20
        n = len(self._up_vals)
        # BG
        self.create_rectangle(0,0,w,h, fill=BG_CARD, outline="")
        # Grid
        for i in range(5):
            yy = y0 + i/4*ah
            self.create_line(x0, yy, x0+aw, yy, fill="#334466", dash=(4,4))
        # Upstream (cyan)
        pts = []
        for i, v in enumerate(self._up_vals):
            pts += [x0+i/(n-1)*aw, y0+(1-v)*ah]
        if len(pts) >= 4: self.create_line(pts, fill=TEAL, width=2)
        # Downstream (yellow)
        pts2 = []
        for i, v in enumerate(self._dn_vals):
            pts2 += [x0+i/(n-1)*aw, y0+(1-v)*ah]
        if len(pts2) >= 4: self.create_line(pts2, fill=YELLOW, width=2)
        # Legend
        self.create_rectangle(10,5,30,12, fill=TEAL, outline="")
        self.create_text(34,9, text="Upstream", font=FT_SM, fill=WHITE, anchor="w")
        self.create_rectangle(100,5,120,12, fill=YELLOW, outline="")
        self.create_text(124,9, text="Downstream", font=FT_SM, fill=WHITE, anchor="w")


# ═════════════════════════════════════════════════════════════
#  MAIN APPLICATION
# ═════════════════════════════════════════════════════════════
class ZeusApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ZEUS+ OBD2 Scanner — Karthika Diesel Service")
        self.geometry("1200x760")
        self.minsize(900, 600)
        self.configure(bg=BG_DARK)

        self.live_running = False
        self.o2_running   = False
        self.vehicle      = {"make":"—","model":"—","year":"—","vin":"—"}
        self.status_msg   = tk.StringVar(value="Disconnected")
        self._active      = "home"

        self._build_ui()
        self._show("home")

    # ── UI BUILD ──────────────────────────────────────────────
    def _build_ui(self):
        # TOP BAR
        top = tk.Frame(self, bg=BG_DARK, height=56)
        top.pack(fill="x"); top.pack_propagate(False)
        tk.Label(top, text="⚡ ZEUS+", font=FT_TT, bg=BG_DARK, fg=RED).pack(side="left", padx=18)
        tk.Label(top, text="Karthika Diesel Service Scanner", font=FT_SM, bg=BG_DARK, fg=GRAY).pack(side="left")
        self.conn_dot = tk.Label(top, text="●", font=("Consolas",14), bg=BG_DARK, fg=RED)
        self.conn_dot.pack(side="right", padx=4)
        self.status_lbl = tk.Label(top, textvariable=self.status_msg, font=FT_SM, bg=BG_DARK, fg=RED)
        self.status_lbl.pack(side="right", padx=8)
        tk.Frame(self, bg=RED, height=2).pack(fill="x")

        # BODY
        body = tk.Frame(self, bg=BG_DARK)
        body.pack(fill="both", expand=True)

        # SIDEBAR
        self.sidebar = tk.Frame(body, bg=BG_CARD, width=290)
        self.sidebar.pack(fill="y", side="left"); self.sidebar.pack_propagate(False)

        # CONTENT
        self.content = tk.Frame(body, bg=BG_DARK)
        self.content.pack(fill="both", expand=True)

        self._build_sidebar()

        # BOTTOM BAR
        bot = tk.Frame(self, bg=BG_CARD, height=32)
        bot.pack(fill="x", side="bottom"); bot.pack_propagate(False)
        tk.Label(bot, text="© ZEUS+ | Karthika Diesel Service | ESP32 CAN Bus OBD2",
                 font=FT_SM, bg=BG_CARD, fg=GRAY).pack(side="left", padx=12)
        self.volt_lbl = tk.Label(bot, text="🔋 14.2 V", font=FT_SM, bg=BG_CARD, fg=GREEN)
        self.volt_lbl.pack(side="right", padx=12)

    def _build_sidebar(self):
        menus = [
            ("", "Home",           "home"),
            ("", "Scanner",        "scanner"),
            ("", "OBD Direct",     "obd_direct"),
            ("", "Live Data",      "live_data"),
            ("", "Multimeter",     "multimeter"),
            ("", "Warning Coding", "warning_coding"),
            ("", "Engine Diag",    "engine_diag"),
            ("", "Live Charts",    "charts_menu"),
            ("", "VIN Reader",     "vin_reader"),
            ("", "ECU Info",       "ecu_info"),
            ("", "AI Diagnosis",   "ai_fault"),
            ("", "O2 Test",        "o2_test"),
            ("", "Injector Test",  "inj_test"),
            ("", "Freeze Frame",   "freeze"),
            ("", "Library",        "library"),
            ("", "Veh. History",   "history"),
            ("", "Data Manager",   "data_mgr"),
            ("", "Settings",       "settings"),
        ]
        tk.Label(self.sidebar, text="MENU", font=FT_SM, bg=BG_CARD, fg=GRAY).pack(pady=(10,4))
        self.menu_btns = {}

        canvas = tk.Canvas(self.sidebar, bg=BG_CARD, highlightthickness=0)
        scrollbar = tk.Scrollbar(self.sidebar, orient="vertical", command=canvas.yview)
        inner = tk.Frame(canvas, bg=BG_CARD)
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0,0), window=inner, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for icon, label, key in menus:
            f = tk.Frame(inner, bg=BG_CARD, cursor="hand2")
            f.pack(fill="x", pady=1)
            lbl = tk.Label(f, text=f"  {icon}  {label}", font=FT, bg=BG_CARD,
                           fg=GRAY_L, anchor="w", pady=7)
            lbl.pack(fill="x", padx=4)
            for w in (f, lbl):
                w.bind("<Button-1>", lambda e, k=key: self._show(k))
                w.bind("<Enter>",    lambda e, ff=f, ll=lbl: (ff.config(bg=BG_CARD2), ll.config(bg=BG_CARD2, fg=WHITE)))
                w.bind("<Leave>",    lambda e, ff=f, ll=lbl, kk=key: self._reset_btn(ff, ll, kk))
            self.menu_btns[key] = (f, lbl)

        tk.Frame(inner, bg=RED, height=1).pack(fill="x", pady=8)
        # Bluetooth connect
        self.bt_btn = tk.Button(inner, text="BLUETOOTH", font=FT, bg=BLUE, fg=WHITE,
                                relief="flat", cursor="hand2", command=self._bt_popup)
        self.bt_btn.pack(fill="x", padx=10, pady=2)
        # OBD connect
        self.conn_btn = tk.Button(inner, text="OBD CONNECT", font=FT, bg=RED, fg=WHITE,
                                  relief="flat", cursor="hand2", command=self._obd_connect)
        self.conn_btn.pack(fill="x", padx=10, pady=2)

    def _reset_btn(self, f, lbl, key):
        if key == self._active:
            f.config(bg=RED_DARK); lbl.config(bg=RED_DARK, fg=WHITE)
        else:
            f.config(bg=BG_CARD); lbl.config(bg=BG_CARD, fg=GRAY_L)

    def _highlight(self, key):
        for k, (f, lbl) in self.menu_btns.items():
            if k == key: f.config(bg=RED_DARK); lbl.config(bg=RED_DARK, fg=WHITE)
            else:        f.config(bg=BG_CARD);  lbl.config(bg=BG_CARD,  fg=GRAY_L)

    # ── SCREEN ROUTER ─────────────────────────────────────────
    def _show(self, name):
        self._active = name
        self._highlight(name)
        self.live_running = False
        self.o2_running   = False
        for w in self.content.winfo_children(): w.destroy()
        {
            "home":          self._s_home,
            "scanner":       self._s_scanner,
            "obd_direct":    self._s_obd_direct,
            "live_data":     self._s_live_data,
            "multimeter":    self._s_multimeter,
            "warning_coding":self._s_warning_coding,
            "engine_diag":   self._s_engine_diag,
            "charts_menu":   self._s_charts_menu,
            "engine_health": self._s_engine_health,
            "cylinder_balance":self._s_cyl_balance,
            "injector_perf": self._s_inj_perf,
            "fuel_rail":     self._s_fuel_rail,
            "vin_reader":    self._s_vin,
            "ecu_info":      self._s_ecu,
            "ai_fault":      self._s_ai_fault,
            "o2_test":       self._s_o2_test,
            "inj_test":      self._s_inj_test,
            "freeze":        self._s_freeze,
            "library":       self._s_library,
            "history":       self._s_history,
            "data_mgr":      self._s_data_mgr,
            "settings":      self._s_settings,
        }.get(name, self._s_home)()

    # ── HELPERS ───────────────────────────────────────────────
    def _frame(self):
        f = tk.Frame(self.content, bg=BG_DARK)
        f.pack(fill="both", expand=True, padx=16, pady=16)
        return f

    def _title(self, parent, text):
        tk.Label(parent, text=text, font=FT_HD, bg=BG_DARK, fg=WHITE).pack(anchor="w", pady=(0,4))
        tk.Frame(parent, bg=RED, height=2).pack(fill="x", pady=(0,10))

    def _redbtn(self, parent, text, cmd, **kw):
        return tk.Button(parent, text=text, font=FT, bg=RED, fg=WHITE,
                         relief="flat", cursor="hand2", command=cmd, **kw)

    def _card(self, parent, **kw):
        f = tk.Frame(parent, bg=BG_CARD, **kw)
        return f

    def _row_lbl(self, parent, label, value, lc=GRAY, vc=TEAL):
        r = tk.Frame(parent, bg=BG_CARD)
        r.pack(fill="x", padx=14, pady=3)
        tk.Label(r, text=label, font=FT, bg=BG_CARD, fg=lc, width=26, anchor="w").pack(side="left")
        v = tk.Label(r, text=value, font=FT_HD, bg=BG_CARD, fg=vc)
        v.pack(side="left")
        return v

    def _scrollable(self, parent):
        outer = tk.Frame(parent, bg=BG_DARK)
        outer.pack(fill="both", expand=True)
        cv = tk.Canvas(outer, bg=BG_DARK, highlightthickness=0)
        sb = tk.Scrollbar(outer, orient="vertical", command=cv.yview)
        inner = tk.Frame(cv, bg=BG_DARK)
        inner.bind("<Configure>", lambda e: cv.configure(scrollregion=cv.bbox("all")))
        cv.create_window((0,0), window=inner, anchor="nw")
        cv.configure(yscrollcommand=sb.set)
        cv.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        cv.bind("<MouseWheel>", lambda e: cv.yview_scroll(-1*(1 if e.delta>0 else -1),"units"))
        return inner

    def _treeview(self, parent, cols, widths):
        style = ttk.Style(); style.theme_use("clam")
        style.configure("Treeview", background=BG_CARD2, foreground=WHITE,
                        fieldbackground=BG_CARD2, rowheight=28, font=FT)
        style.configure("Treeview.Heading", background=BG_CARD, foreground=TEAL, font=FT_HD)
        style.map("Treeview", background=[("selected", RED_DARK)])
        tree = ttk.Treeview(parent, columns=cols, show="headings")
        for col, w in zip(cols, widths):
            tree.heading(col, text=col); tree.column(col, width=w, anchor="center" if w<150 else "w")
        vsb = ttk.Scrollbar(parent, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")
        return tree

    def _popup_result(self, title, msg, color=GREEN):
        pw = tk.Toplevel(self); pw.title(title)
        pw.configure(bg=BG_CARD); pw.geometry("420x180")
        tk.Label(pw, text=title, font=FT_HD, bg=BG_CARD, fg=TEAL).pack(pady=(16,4))
        tk.Label(pw, text=msg, font=FT, bg=BG_CARD, fg=color, wraplength=380).pack(pady=8)
        tk.Button(pw, text="OK", font=FT, bg=RED, fg=WHITE, relief="flat",
                  command=pw.destroy).pack(pady=8, ipadx=20)
        pw.after(3000, pw.destroy)

    # ════════════════════════════════════════════════════════
    #  SCREENS
    # ════════════════════════════════════════════════════════

    # ── HOME ──
    def _s_home(self):
        f = self._frame()
        tk.Label(f, text="⚡ZEUS+  KARTHIKA DIESEL SERVICE SCANNER",
                 font=FT_TT, bg=BG_DARK, fg=RED).pack(pady=(4,2))
        tk.Label(f, text="ESP32 · CAN Bus · Bluetooth · OBD2",
                 font=FT_SM, bg=BG_DARK, fg=GRAY).pack(pady=(0,14))

        # Vehicle card
        vc = self._card(f, pady=12); vc.pack(fill="x", pady=(0,14))
        tk.Label(vc, text="VEHICLE INFO", font=FT_HD, bg=BG_CARD, fg=TEAL).pack(anchor="w", padx=14)
        row = tk.Frame(vc, bg=BG_CARD); row.pack(fill="x", padx=14, pady=6)
        for k, v in [("Make",self.vehicle["make"]),("Model",self.vehicle["model"]),
                     ("Year",self.vehicle["year"]),("VIN",self.vehicle["vin"])]:
            col = tk.Frame(row, bg=BG_CARD); col.pack(side="left", expand=True)
            tk.Label(col, text=k, font=FT_SM, bg=BG_CARD, fg=GRAY).pack()
            tk.Label(col, text=v, font=FT_HD, bg=BG_CARD, fg=WHITE).pack()

        # Grid of tiles
        tk.Label(f, text="QUICK LAUNCH", font=FT_SM, bg=BG_DARK, fg=GRAY).pack(anchor="w", pady=(4,4))
        grid = tk.Frame(f, bg=BG_DARK); grid.pack(fill="both", expand=True)
        tiles = [
            ("🔍","Scanner",      "scanner"),   ("📊","Live Data",   "live_data"),
            ("⚠️","Warning Codes","warning_coding"),("⚙️","Engine Diag","engine_diag"),
            ("📈","Live Charts",  "charts_menu"),("🧠","AI Diagnosis","ai_fault"),
            ("💉","Injector Test","inj_test"),  ("🔬","O2 Test",     "o2_test"),
            ("🔑","VIN Reader",   "vin_reader"),("🖥️","ECU Info",    "ecu_info"),
            ("🧊","Freeze Frame", "freeze"),    ("📚","Library",     "library"),
        ]
        # ── Load PNG icons (64x64) from icons/ folder ───────
        self._tile_icons = {}
        ICON_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons")
        if PIL_AVAILABLE and os.path.isdir(ICON_DIR):
            for _, _, key in tiles:
                path = os.path.join(ICON_DIR, f"{key}.png")
                if os.path.exists(path):
                    try:
                        img = Image.open(path).resize((64, 64), Image.LANCZOS)
                        self._tile_icons[key] = ImageTk.PhotoImage(img)
                    except Exception:
                        pass

        for i, (emoji, label, key) in enumerate(tiles):
            r, c = divmod(i, 4)
            btn = tk.Frame(grid, bg=BG_CARD, cursor="hand2")
            btn.grid(row=r, column=c, padx=5, pady=5, sticky="nsew")
            grid.columnconfigure(c, weight=1); grid.rowconfigure(r, weight=1)
            # PNG icon if available, else emoji fallback
            if key in self._tile_icons:
                tk.Label(btn, image=self._tile_icons[key],
                         bg=BG_CARD).pack(pady=(10,2))
            else:
                tk.Label(btn, text=emoji, font=("Segoe UI Emoji",18),
                         bg=BG_CARD, fg=TEAL).pack(pady=(12,2))
            tk.Label(btn, text=label, font=FT, bg=BG_CARD, fg=WHITE).pack(pady=(0,10))
            for w in btn.winfo_children()+[btn]:
                w.bind("<Button-1>", lambda e,k=key: self._show(k))
                w.bind("<Enter>",    lambda e,b=btn: b.config(bg=BG_CARD2))
                w.bind("<Leave>",    lambda e,b=btn: b.config(bg=BG_CARD))

    # ── SCANNER ──
    def _s_scanner(self):
        f = self._frame(); self._title(f, "SCANNER — Full System Scan")
        card = self._card(f, pady=14); card.pack(fill="x")
        tk.Label(card, text="Select System:", font=FT_HD, bg=BG_CARD, fg=WHITE).pack(anchor="w", padx=14)
        systems = ["Engine (PCM/ECM)","Transmission (TCM)","ABS / Brake",
                   "Airbag (SRS)","Body Control (BCM)","All Systems"]
        self.scan_var = tk.StringVar(value=systems[0])
        for s in systems:
            tk.Radiobutton(card, text=s, variable=self.scan_var, value=s,
                           font=FT, bg=BG_CARD, fg=GRAY_L, selectcolor=BG_CARD,
                           activebackground=BG_CARD).pack(anchor="w", padx=30, pady=1)
        ctrl = tk.Frame(f, bg=BG_DARK); ctrl.pack(fill="x", pady=8)
        self._redbtn(ctrl, "▶  START SCAN", self._run_scan).pack(side="left", ipadx=14, ipady=5)
        tk.Button(ctrl, text=" CLEAR ALL", font=FT, bg=ORANGE, fg=WHITE,
                  relief="flat", cursor="hand2", command=self._clear_dtcs
                  ).pack(side="left", padx=8, ipadx=10, ipady=5)
        self.scan_out = scrolledtext.ScrolledText(f, bg=BG_CARD2, fg=GRAY_L, font=FT_SM,
                                                   relief="flat", height=14, wrap="word")
        self.scan_out.pack(fill="both", expand=True)
        self.scan_out.insert("end", "Ready. Select system and press START SCAN.\n")

    def _run_scan(self):
        self.scan_out.config(state="normal")
        self.scan_out.delete("1.0","end")
        self.scan_out.insert("end", f"Scanning {self.scan_var.get()}...\n\n")
        def do():
            time.sleep(0.8)
            dtcs = obd_mgr.get_dtcs()
            if dtcs:
                self.scan_out.insert("end", f"Found {len(dtcs)} Fault Code(s):\n\n")
                for code, desc, status in dtcs:
                    c = RED if status=="Active" else (YELLOW if status=="Pending" else GRAY_L)
                    self.scan_out.insert("end", f"  [{status}]  {code} — {desc}\n",)
            else:
                self.scan_out.insert("end", "No faults found. System OK.\n")
            self.scan_out.insert("end", f"\nScan complete: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        threading.Thread(target=do, daemon=True).start()

    def _clear_dtcs(self):
        if messagebox.askyesno("Clear DTCs", "Clear all fault codes from ECU?"):
            obd_mgr.clear_dtcs()
            self._popup_result("Cleared", "All DTC fault codes cleared successfully.", GREEN)

    # ── OBD DIRECT ──
    def _s_obd_direct(self):
        f = self._frame(); self._title(f, "OBD DIRECT — Generic PID Mode")
        card = self._card(f, pady=12); card.pack(fill="x")
        tk.Label(card, text="Send OBD2 PID Command:", font=FT_HD, bg=BG_CARD, fg=WHITE).pack(anchor="w", padx=14, pady=(0,6))
        row = tk.Frame(card, bg=BG_CARD); row.pack(fill="x", padx=14)
        self.obd_cmd = tk.Entry(row, bg=BG_CARD2, fg=WHITE, font=FT, insertbackground=WHITE,
                                relief="flat", width=28)
        self.obd_cmd.pack(side="left", ipady=6, padx=(0,8))
        self.obd_cmd.insert(0, "0100")
        self._redbtn(row, "SEND ▶", self._send_pid).pack(side="left", ipadx=10, ipady=5)

        # Quick PID buttons
        pids = tk.Frame(f, bg=BG_DARK); pids.pack(fill="x", pady=6)
        tk.Label(pids, text="Common PIDs:", font=FT_SM, bg=BG_DARK, fg=GRAY).pack(side="left", padx=(0,8))
        for pid, name in [("010C","RPM"),("010D","Speed"),("0105","Coolant"),
                          ("0111","Throttle"),("0104","Engine Load"),("012F","Fuel Level")]:
            tk.Button(pids, text=f"{pid}\n{name}", font=FT_SM, bg=BG_CARD, fg=TEAL,
                      relief="flat", cursor="hand2",
                      command=lambda p=pid: self._quick_pid(p)).pack(side="left", padx=3, ipady=2)

        self.obd_out = tk.Text(f, bg=BG_CARD2, fg=GREEN, font=("Consolas",11),
                               relief="flat", wrap="word")
        sb = tk.Scrollbar(f, command=self.obd_out.yview)
        self.obd_out.configure(yscrollcommand=sb.set)
        self.obd_out.pack(fill="both", expand=True, pady=(6,0))
        sb.pack(side="right", fill="y")
        self.obd_out.insert("end", "ZEUS+ OBD2 Terminal Ready\n> \n")

    def _quick_pid(self, pid):
        self.obd_cmd.delete(0,"end"); self.obd_cmd.insert(0,pid); self._send_pid()

    def _send_pid(self):
        cmd = self.obd_cmd.get().strip()
        resp = bt.send(cmd) if bt.connected else f"41 {cmd[2:] if len(cmd)>2 else 'XX'} 00 (Demo)"
        self.obd_out.insert("end", f"> {cmd}\n  {resp}\n")
        self.obd_out.see("end")

    # ── LIVE DATA (Karthika style — all 52 sensors) ──
    def _s_live_data(self):
        self._s_sensor_list("LIVE DATA — All Sensors", "live_data")

    def _s_multimeter(self):
        self._s_sensor_list("MULTIMETER — Sensor Readings", "multimeter")

    def _s_sensor_list(self, title, mode):
        f = self._frame(); self._title(f, title)
        ctrl = tk.Frame(f, bg=BG_DARK); ctrl.pack(fill="x", pady=(0,8))
        self.live_btn = tk.Button(ctrl, text="▶  START LIVE", font=FT,
                                  bg=GREEN, fg=BG_DARK, relief="flat", cursor="hand2",
                                  command=self._toggle_live)
        self.live_btn.pack(side="left", ipadx=10, ipady=4)

        inner = self._scrollable(f)
        self._sensor_vals = {}

        for i, (name, cmd, val) in enumerate(LIVE_SENSORS):
            bg = BG_ROW if i%2==0 else BG_CARD
            row = tk.Frame(inner, bg=bg); row.pack(fill="x")
            tk.Label(row, text="●", font=FT_SM, bg=bg, fg=GREEN,
                     width=3).pack(side="left", padx=(6,0))
            tk.Label(row, text=name, font=FT_SM, bg=bg, fg=WHITE,
                     width=40, anchor="w").pack(side="left", pady=6)
            v = tk.Label(row, text=val, font=FT_SM, bg=bg, fg=CYAN,
                         width=18, anchor="e")
            v.pack(side="right", padx=10)
            self._sensor_vals[cmd] = v

    def _toggle_live(self):
        self.live_running = not self.live_running
        if self.live_running:
            self.live_btn.config(text="⏹  STOP LIVE", bg=RED, fg=WHITE)
            threading.Thread(target=self._live_loop, daemon=True).start()
        else:
            self.live_btn.config(text="▶  START LIVE", bg=GREEN, fg=BG_DARK)

    def _live_loop(self):
        while self.live_running:
            for name, cmd, val in LIVE_SENSORS:
                if not self.live_running: break
                resp = bt.send(cmd)
                if resp and cmd in self._sensor_vals:
                    try: self._sensor_vals[cmd].config(text=resp)
                    except: pass
                time.sleep(0.02)
            time.sleep(0.5)

    # ── WARNING CODING ──
    def _s_warning_coding(self):
        f = self._frame(); self._title(f, "⚠️ WARNING CODING — Service Functions")
        tk.Label(f, text="⚠  These functions modify ECU settings. Use with caution!",
                 font=FT_SM, bg=BG_DARK, fg=YELLOW).pack(anchor="w", pady=(0,10))
        inner = self._scrollable(f)
        for i in range(0, len(WARNING_CODES), 2):
            row = tk.Frame(inner, bg=BG_DARK); row.pack(fill="x", pady=4, padx=4)
            for j in range(2):
                if i+j >= len(WARNING_CODES): break
                name, cmd = WARNING_CODES[i+j]
                btn = tk.Button(row, text=name, font=FT_SM, bg=BLUE, fg=WHITE,
                                relief="flat", cursor="hand2", anchor="w",
                                command=lambda c=cmd, n=name: self._run_warning(c,n))
                btn.pack(side="left", fill="x", expand=True, padx=4, ipady=8)

    def _run_warning(self, cmd, name):
        if not messagebox.askyesno("Confirm", f"Run function:\n{name}?"):
            return
        resp = bt.send(cmd)
        msg = resp if resp else f"Command sent: {cmd}\n(Demo Mode — No response)"
        self._popup_result(name, msg, TEAL)

    # ── ENGINE DIAGNOSTICS ──
    def _s_engine_diag(self):
        f = self._frame(); self._title(f, "⚙ ENGINE DIAGNOSTICS — DTC Status")
        ctrl = tk.Frame(f, bg=BG_DARK); ctrl.pack(fill="x", pady=(0,8))
        self._redbtn(ctrl, "READ CODES", self._load_engine_dtcs).pack(side="left", ipadx=10, ipady=4)
        tk.Button(ctrl, text="CLEAR", font=FT, bg=ORANGE, fg=WHITE, relief="flat",
                  cursor="hand2", command=self._clear_engine).pack(side="left", padx=8, ipadx=10, ipady=4)

        cols = ("Code","Description","Status")
        frame = tk.Frame(f, bg=BG_DARK); frame.pack(fill="both", expand=True)
        self.eng_tree = self._treeview(frame, cols, [90,450,110])
        self._load_engine_dtcs()

    def _load_engine_dtcs(self):
        for r in self.eng_tree.get_children(): self.eng_tree.delete(r)
        for code, desc, status in DTC_LIST:
            self.eng_tree.insert("", "end", values=(code, desc, status))

    def _clear_engine(self):
        if messagebox.askyesno("Clear", "Clear all engine fault codes?"):
            for r in self.eng_tree.get_children(): self.eng_tree.delete(r)
            resp = bt.send("ERASE_FAULT")
            self._popup_result("Cleared", "All engine DTCs cleared.", GREEN)

    # ── CHARTS MENU ──
    def _s_charts_menu(self):
        f = self._frame(); self._title(f, "LIVE CHARTS — Select Chart")
        inner = self._scrollable(f)
        for name, key in CHART_ITEMS:
            row = tk.Frame(inner, bg=BG_CARD, cursor="hand2", pady=2)
            row.pack(fill="x", pady=4, padx=4)
            tk.Label(row, text=name, font=FT_HD, bg=BG_CARD, fg=WHITE).pack(side="left", padx=16, pady=10)
            tk.Button(row, text="OPEN ▶", font=FT_SM, bg=RED, fg=WHITE,
                      relief="flat", cursor="hand2",
                      command=lambda k=key: self._show(k)).pack(side="right", padx=16, ipady=4, ipadx=8)
            row.bind("<Enter>", lambda e, r=row: r.config(bg=BG_CARD2))
            row.bind("<Leave>", lambda e, r=row: r.config(bg=BG_CARD))

    # ── ENGINE HEALTH RADAR ──
    def _s_engine_health(self):
        f = self._frame(); self._title(f, " ENGINE HEALTH RADAR CHART")
        tk.Button(f, text="◀ Back to Charts", font=FT_SM, bg=BG_CARD, fg=TEAL,
                  relief="flat", cursor="hand2",
                  command=lambda: self._show("charts_menu")).pack(anchor="w", pady=(0,8))
        c = RadarCanvas(f)
        c.pack(fill="both", expand=True, pady=4)

    # ── CYLINDER BALANCE ──
    def _s_cyl_balance(self):
        f = self._frame(); self._title(f, "CYLINDER BALANCE CHART")
        tk.Button(f, text="◀ Back to Charts", font=FT_SM, bg=BG_CARD, fg=TEAL,
                  relief="flat", cursor="hand2",
                  command=lambda: self._show("charts_menu")).pack(anchor="w", pady=(0,8))
        c = CylCanvas(f, "Cylinder Balance")
        c.pack(fill="both", expand=True, pady=4)

    # ── INJECTOR PERFORMANCE ──
    def _s_inj_perf(self):
        f = self._frame(); self._title(f, " INJECTOR PERFORMANCE CHART")
        tk.Button(f, text="◀ Back to Charts", font=FT_SM, bg=BG_CARD, fg=TEAL,
                  relief="flat", cursor="hand2",
                  command=lambda: self._show("charts_menu")).pack(anchor="w", pady=(0,8))
        c = CylCanvas(f, "Injector Performance")
        c.pack(fill="both", expand=True, pady=4)

    # ── FUEL RAIL ──
    def _s_fuel_rail(self):
        f = self._frame(); self._title(f, "FUEL RAIL PRESSURE CHART")
        tk.Button(f, text="◀ Back to Charts", font=FT_SM, bg=BG_CARD, fg=TEAL,
                  relief="flat", cursor="hand2",
                  command=lambda: self._show("charts_menu")).pack(anchor="w", pady=(0,8))
        c = FuelCanvas(f)
        c.pack(fill="both", expand=True, pady=4)

    # ── VIN READER ──
    def _s_vin(self):
        f = self._frame(); self._title(f, "VIN READER — Vehicle Identification")
        card = self._card(f, pady=14); card.pack(fill="x", pady=(0,10))
        tk.Label(card, text="VIN NUMBER", font=FT_SM, bg=BG_CARD, fg=TEAL).pack(anchor="w", padx=14)
        self.vin_lbl = tk.Label(card, text="--- Press READ VIN ---", font=FT_BIG,
                                bg=BG_CARD, fg=WHITE)
        self.vin_lbl.pack(pady=12)

        info_card = self._card(f, pady=12); info_card.pack(fill="x", pady=(0,10))
        self._vin_rows = {}
        for lbl in ["Make","Model","Year","ECU Status","DTC Count","CAN Bus"]:
            self._vin_rows[lbl] = self._row_lbl(info_card, lbl, "---")

        self._redbtn(f, " READ VIN FROM ECU", self._read_vin).pack(pady=8, ipadx=16, ipady=6)

    def _read_vin(self):
        self.vin_lbl.config(text="Reading VIN from ECU...", fg=YELLOW)
        def do():
            resp = bt.send("GET_VIN")
            if resp and "VIN:" in resp:
                vin = resp.split("VIN:")[-1].strip()
                self.vin_lbl.config(text=vin[:17], fg=GREEN)
                self.vehicle["vin"] = vin[:17]
                ecu_resp = bt.send("GET_ECU_INFO")
                if ecu_resp:
                    try:
                        d = json.loads(ecu_resp)
                        self.vehicle["make"]  = d.get("make","?")
                        self.vehicle["model"] = d.get("model","?")
                        self.vehicle["year"]  = str(d.get("year","?"))
                        self._vin_rows["Make"].config(text=d.get("make","?"))
                        self._vin_rows["Model"].config(text=d.get("model","?"))
                        self._vin_rows["Year"].config(text=str(d.get("year","?")))
                        self._vin_rows["DTC Count"].config(text=str(d.get("dtc",0)))
                        self._vin_rows["CAN Bus"].config(text=d.get("can","?"))
                        self._vin_rows["ECU Status"].config(text="CONNECTED", fg=GREEN)
                    except: pass
            else:
                self.vin_lbl.config(text="NO RESPONSE — Check Bluetooth", fg=RED)
        threading.Thread(target=do, daemon=True).start()

    # ── ECU INFO ──
    def _s_ecu(self):
        f = self._frame(); self._title(f, "ECU INFORMATION")
        card = self._card(f, pady=12); card.pack(fill="x", pady=(0,10))
        self._ecu_fields = {}
        fields = [("ECU Make",GREEN),("ECU Model",GREEN),("Year",WHITE),
                  ("VIN",TEAL),("Software Ver",WHITE),("Hardware Ver",WHITE),
                  ("Calibration ID",WHITE),("DTC Count",YELLOW),
                  ("CAN Bus",TEAL),("AI Diagnosis",ORANGE)]
        for name, color in fields:
            self._ecu_fields[name] = self._row_lbl(card, name, "---", vc=color)
        self._redbtn(f, " READ ECU INFO", self._read_ecu).pack(pady=8, ipadx=16, ipady=6)

    def _read_ecu(self):
        def do():
            resp = bt.send("GET_ECU_INFO")
            if resp:
                try:
                    d = json.loads(resp)
                    m = {"ECU Make":d.get("make","?"),"ECU Model":d.get("model","?"),
                         "Year":str(d.get("year","?")),"VIN":d.get("vin","?")[:17],
                         "DTC Count":str(d.get("dtc",0)),"CAN Bus":d.get("can","?"),
                         "Software Ver":"ECU_V2.3","Hardware Ver":"HW_1.0","Calibration ID":"K19_023"}
                    for k,v in m.items():
                        if k in self._ecu_fields:
                            self._ecu_fields[k].config(text=v)
                except: pass
            ai = bt.send("ANALYZE_AI")
            if ai:
                try:
                    d = json.loads(ai)
                    self._ecu_fields["AI Diagnosis"].config(text=d.get("status","?"))
                except: pass
        threading.Thread(target=do, daemon=True).start()

    # ── AI FAULT DIAGNOSIS ──
    def _s_ai_fault(self):
        f = self._frame(); self._title(f, " AI FAULT DIAGNOSIS")
        card = self._card(f, pady=20); card.pack(fill="x", pady=(0,12))
        self.ai_status = tk.Label(card, text="AI READY", font=FT_BIG,
                                  bg=BG_CARD, fg=TEAL)
        self.ai_status.pack(pady=(10,4))
        tk.Frame(card, bg=GRAY, height=1).pack(fill="x", padx=20, pady=8)
        self.ai_result = tk.Label(card, text="Press ANALYZE to start",
                                  font=FT_MED, bg=BG_CARD, fg=GREEN, wraplength=600)
        self.ai_result.pack(pady=4)
        self.ai_advice = tk.Label(card, text="", font=FT, bg=BG_CARD, fg=WHITE, wraplength=600)
        self.ai_advice.pack(pady=2)
        self.ai_conf = tk.Label(card, text="", font=FT_SM, bg=BG_CARD, fg=TEAL)
        self.ai_conf.pack(pady=2)
        self.ai_sensors = tk.Label(card, text="RPM: ---  |  Temp: ---  |  Fuel: ---  |  O2: ---",
                                   font=FT_SM, bg=BG_CARD, fg=GRAY_L)
        self.ai_sensors.pack(pady=(8,14))
        tk.Button(f, text=" RUN AI ANALYSIS", font=FT_MED, bg=BLUE, fg=WHITE,
                  relief="flat", cursor="hand2",
                  command=self._run_ai).pack(pady=8, ipadx=20, ipady=8)

    def _run_ai(self):
        self.ai_result.config(text="Analyzing engine data...", fg=YELLOW)
        self.ai_status.config(text="ANALYZING...", fg=YELLOW)
        def do():
            resp = bt.send("ANALYZE_AI")
            if resp:
                try:
                    d = json.loads(resp)
                    status = d.get("status","UNKNOWN")
                    col = GREEN if status=="NORMAL" else RED
                    self.ai_status.config(text=status, fg=col)
                    self.ai_result.config(text=status, fg=col)
                    self.ai_advice.config(text=f"⚠ {d.get('advice','')}")
                    self.ai_conf.config(text=f"Confidence: {d.get('confidence','')}")
                    self.ai_sensors.config(
                        text=(f"RPM:{d.get('rpm',0):.0f}  Temp:{d.get('temp',0):.0f}°C  "
                              f"Fuel:{d.get('fuel',0):.0f}bar  O2:{d.get('o2',0):.2f}V"))
                except:
                    self.ai_result.config(text="PARSE ERROR", fg=RED)
            else:
                self.ai_result.config(text="NO RESPONSE", fg=RED)
                self.ai_status.config(text="NO RESPONSE", fg=RED)
        threading.Thread(target=do, daemon=True).start()

    # ── O2 SENSOR TEST ──
    def _s_o2_test(self):
        f = self._frame(); self._title(f, " O2 SENSOR LIVE TEST")
        self.o2_canvas = O2Canvas(f); self.o2_canvas.pack(fill="x", pady=(0,8))
        card = self._card(f, pady=10); card.pack(fill="x", pady=(0,8))
        self._o2_rows = {}
        for name, col in [("Upstream Voltage",GREEN),("Downstream Voltage",TEAL),
                          ("Catalyst Status",YELLOW),("Heater Status",GREEN),
                          ("O2 Result",ORANGE)]:
            self._o2_rows[name] = self._row_lbl(card, name, "---", vc=col)
        tk.Button(f, text="  START O2 TEST", font=FT_HD, bg=GREEN, fg=BG_DARK,
                  relief="flat", cursor="hand2",
                  command=self._start_o2).pack(pady=8, ipadx=16, ipady=6)

    def _start_o2(self):
        self.o2_running = True
        threading.Thread(target=self._o2_loop, daemon=True).start()

    def _o2_loop(self):
        while self.o2_running:
            resp = bt.send("O2_TEST")
            if resp:
                try:
                    d = json.loads(resp)
                    up = float(d.get("upstream_v", 0.45))
                    dn = float(d.get("downstream_v", 0.65))
                    self.o2_canvas.update_vals(up, dn)
                    self._o2_rows["Upstream Voltage"].config(text=f"{up:.2f} V")
                    self._o2_rows["Downstream Voltage"].config(text=f"{dn:.2f} V")
                    cat = d.get("catalyst_ok", True)
                    self._o2_rows["Catalyst Status"].config(text="✓ OK" if cat else "✗ FAIL",
                                                            fg=GREEN if cat else RED)
                    self._o2_rows["Heater Status"].config(text="✓ OK")
                    self._o2_rows["O2 Result"].config(text=d.get("result","")[:30])
                except: pass
            time.sleep(0.4)

    # ── INJECTOR FULL TEST ──
    def _s_inj_test(self):
        f = self._frame(); self._title(f, "INJECTOR FULL TEST — 4 Cylinders")
        inner = self._scrollable(f)
        self._inj_cards = []
        PARAMS = ["Voltage","Resistance","Pulse","Signal","Short Ckt","Spray","Status"]
        for cyl in range(4):
            card = tk.Frame(inner, bg=BG_CARD, pady=10); card.pack(fill="x", pady=6, padx=4)
            # Header
            hdr = tk.Frame(card, bg=BG_CARD); hdr.pack(fill="x", padx=10)
            tk.Label(hdr, text=f" CYLINDER {cyl+1}", font=FT_HD, bg=BG_CARD, fg=TEAL).pack(side="left")
            status = tk.Label(hdr, text="● IDLE", font=FT_SM, bg=BG_CARD, fg=YELLOW)
            status.pack(side="right")
            tk.Frame(card, bg=GRAY, height=1).pack(fill="x", padx=10, pady=4)
            # Params
            pd = {}
            for param in PARAMS:
                row = tk.Frame(card, bg=BG_CARD); row.pack(fill="x", padx=14, pady=2)
                tk.Label(row, text=param, font=FT_SM, bg=BG_CARD, fg=GRAY_L,
                         width=16, anchor="w").pack(side="left")
                v = tk.Label(row, text="---", font=FT_SM, bg=BG_CARD, fg=WHITE,
                             anchor="e")
                v.pack(side="right", padx=10)
                pd[param] = v
            pd["_status"] = status
            # Test button
            tk.Button(card, text=f"▶ TEST CYL {cyl+1}", font=FT, bg=BLUE, fg=WHITE,
                      relief="flat", cursor="hand2",
                      command=lambda c=cyl, p=pd: self._test_cyl(c,p)).pack(pady=(6,4), ipadx=10, ipady=4)
            self._inj_cards.append(pd)
        # Injector Coding
        code_card = tk.Frame(inner, bg=BG_CARD, pady=12)
        code_card.pack(fill="x", pady=6, padx=4)
        tk.Label(code_card, text=" INJECTOR CODING (IMA/ISA)",
                 font=FT_HD, bg=BG_CARD, fg=TEAL).pack(anchor="w", padx=14)
        self.inj_code_result = tk.Label(code_card, text="Press button to run IMA coding...",
                                         font=FT_SM, bg=BG_CARD, fg=GRAY_L)
        self.inj_code_result.pack(pady=6)
        tk.Button(code_card, text="⚙  RUN INJECTOR CODING", font=FT_HD, bg=ORANGE, fg=WHITE,
                  relief="flat", cursor="hand2",
                  command=self._run_inj_coding).pack(pady=4, ipadx=14, ipady=6)

    def _test_cyl(self, cyl, params):
        params["_status"].config(text="● TESTING", fg=TEAL)
        def do():
            resp = bt.send(f"INJ_TEST_{cyl+1}")
            if resp:
                try:
                    d = json.loads(resp)
                    params["Voltage"].config(text=d.get("voltage","---"))
                    params["Resistance"].config(text=d.get("resistance","---"))
                    params["Pulse"].config(text=d.get("pulse","---"))
                    params["Signal"].config(text="✓ Active" if d.get("pulse_ok") else "✗ No Signal")
                    params["Short Ckt"].config(text="⚠ SHORT!" if d.get("short") else "✓ Normal")
                    params["Spray"].config(text=d.get("spray","---"))
                    s = d.get("status","?")
                    params["Status"].config(text=s, fg=GREEN if s=="OK" else RED)
                    params["_status"].config(text="● DONE", fg=GREEN if s=="OK" else ORANGE)
                    return
                except: pass
            # Demo
            v = round(random.uniform(11.8,13.9),2)
            r = round(random.uniform(13.0,15.5),1)
            p = round(random.uniform(1.8,2.8),2)
            params["Voltage"].config(text=f"{v} V")
            params["Resistance"].config(text=f"{r} ohm")
            params["Pulse"].config(text=f"{p} ms")
            params["Signal"].config(text="✓ Active")
            params["Short Ckt"].config(text="✓ Normal")
            sprays = ["EXCELLENT","GOOD","POOR - Clean","WEAK - Replace"]
            params["Spray"].config(text=random.choice(sprays[:2+cyl]))
            s = "OK" if cyl < 2 else "CHECK"
            params["Status"].config(text=s, fg=GREEN if s=="OK" else YELLOW)
            params["_status"].config(text=f"● {s}", fg=GREEN if s=="OK" else ORANGE)
        threading.Thread(target=do, daemon=True).start()

    def _run_inj_coding(self):
        resp = bt.send("INJ_CODING")
        self.inj_code_result.config(text=resp if resp else "IMA Coding command sent (Demo Mode)", fg=GREEN)

    # ── FREEZE FRAME ──
    def _s_freeze(self):
        f = self._frame(); self._title(f, "FREEZE FRAME DATA")
        dtc_card = tk.Frame(f, bg="#2a1010", pady=14); dtc_card.pack(fill="x", pady=(0,10))
        tk.Label(dtc_card, text="Triggered DTC:", font=FT_SM, bg="#2a1010", fg="#ff9999").pack(side="left", padx=14)
        self.dtc_lbl = tk.Label(dtc_card, text="---", font=FT_BIG, bg="#2a1010", fg=RED)
        self.dtc_lbl.pack(side="left", padx=8)

        card = self._card(f, pady=12); card.pack(fill="x", pady=(0,10))
        self._ff_rows = {}
        for name in ["RPM","Coolant Temp","Throttle","MAF","Speed","Fuel Pressure"]:
            self._ff_rows[name] = self._row_lbl(card, name, "---")

        self._redbtn(f, "  READ FREEZE FRAME", self._read_freeze).pack(pady=8, ipadx=16, ipady=6)

    def _read_freeze(self):
        resp = bt.send("GET_FREEZE")
        if resp:
            try:
                d = json.loads(resp)
                self.dtc_lbl.config(text=d.get("dtc","---"))
                self._ff_rows["RPM"].config(text=f"{d.get('rpm',0):.0f} RPM")
                self._ff_rows["Coolant Temp"].config(text=f"{d.get('temp',0):.1f} °C")
                self._ff_rows["Throttle"].config(text=f"{d.get('throttle',0):.1f} %")
                self._ff_rows["MAF"].config(text=f"{d.get('maf',0):.2f} g/s")
                self._ff_rows["Speed"].config(text=f"{d.get('speed',0):.0f} km/h")
                self._ff_rows["Fuel Pressure"].config(text=f"{d.get('fuel',0):.0f} bar")
                return
            except: pass
        self._popup_result("Freeze Frame", "No data received (Demo mode — connect BT)", YELLOW)

    # ── LIBRARY ──
    def _s_library(self):
        f = self._frame(); self._title(f, "LIBRARY — Reference Documents")
        inner = self._scrollable(f)
        for icon, item in LIBRARY_ITEMS:
            row = tk.Frame(inner, bg=BG_CARD, cursor="hand2"); row.pack(fill="x", pady=4, padx=4)
            tk.Label(row, text=icon, font=("Segoe UI Emoji",16), bg=BG_CARD).pack(side="left", padx=14, pady=14)
            tk.Label(row, text=item, font=FT_HD, bg=BG_CARD, fg=WHITE).pack(side="left", pady=14)
            tk.Label(row, text="▶", font=FT, bg=BG_CARD, fg=GRAY).pack(side="right", padx=14)
            row.bind("<Enter>", lambda e, r=row: r.config(bg=BG_CARD2))
            row.bind("<Leave>", lambda e, r=row: r.config(bg=BG_CARD))

    # ── VEHICLE HISTORY ──
    def _s_history(self):
        f = self._frame(); self._title(f, "VEHICLE HISTORY")
        sample = [
            ("2024-01-15","Toyota Hilux 2019","P0335, P0201","3 Active"),
            ("2024-01-10","Tata Yodha 2021","P0100","1 Active"),
            ("2024-01-08","Mahindra Bolero 2020","None","✅ OK"),
            ("2024-01-05","Ashok Leyland 2018","P2463, P0401","2 Active"),
            ("2024-01-02","Ford Ranger 2022","B1325","1 Pending"),
        ]
        frame = tk.Frame(f, bg=BG_DARK); frame.pack(fill="both", expand=True)
        cols = ("Date","Vehicle","Last DTCs","Status")
        tree = self._treeview(frame, cols, [120,250,200,130])
        for row in sample: tree.insert("","end",values=row)

    # ── DATA MANAGER ──
    def _s_data_mgr(self):
        f = self._frame(); self._title(f, "📁 DATA MANAGER")
        ctrl = tk.Frame(f, bg=BG_DARK); ctrl.pack(fill="x", pady=(0,8))
        self._redbtn(ctrl, "💾 Save Report", self._save_report).pack(side="left", ipadx=10, ipady=4)
        tk.Button(ctrl, text="📂 Open Folder", font=FT, bg=BG_CARD, fg=WHITE,
                  relief="flat", cursor="hand2",
                  command=lambda: os.startfile(".") if os.name=="nt" else None
                  ).pack(side="left", padx=8, ipadx=10, ipady=4)

        self.dm_text = scrolledtext.ScrolledText(f, bg=BG_CARD2, fg=GRAY_L, font=FT_SM,
                                                  relief="flat")
        self.dm_text.pack(fill="both", expand=True)
        self.dm_text.insert("end", "Saved Reports:\n\n")
        for fn in os.listdir("."):
            if fn.endswith((".json",".txt")):
                self.dm_text.insert("end", f"  📄 {fn}\n")

    def _save_report(self):
        path = filedialog.asksaveasfilename(defaultextension=".json",
                                            filetypes=[("JSON","*.json"),("Text","*.txt")])
        if path:
            report = {
                "timestamp": datetime.now().isoformat(),
                "vehicle":   self.vehicle,
                "dtcs":      DTC_LIST,
                "bt_device": bt.device_name,
            }
            with open(path,"w") as fp: json.dump(report,fp,indent=2)
            self._popup_result("Saved", f"Report saved:\n{os.path.basename(path)}", GREEN)

    # ── SETTINGS ──
    def _s_settings(self):
        f = self._frame(); self._title(f, "⚙️ SYSTEM SETTINGS")
        card = self._card(f, pady=16); card.pack(fill="x")
        settings = [
            ("OBD Port",        "AUTO / COM3 / /dev/ttyUSB0"),
            ("Bluetooth",       "ESP32 CAN Bus Scanner"),
            ("Protocol",        "CAN 2.0B / ISO 15765-4"),
            ("Units",           "Metric (km/h, °C, bar)"),
            ("Language",        "English / Malayalam"),
            ("Update Channel",  "Stable"),
            ("App Version",     "ZEUS+ v5.0 — Karthika Edition"),
            ("Build",           "ESP32 + SN65HVD230 + OBD2"),
        ]
        for k, v in settings:
            self._row_lbl(card, k, v)

        tk.Frame(f, bg=GRAY, height=1).pack(fill="x", pady=12)
        row = tk.Frame(f, bg=BG_DARK); row.pack(fill="x")
        self._redbtn(row, "🔄 Check Updates", lambda: self._popup_result("Updates","You are on the latest version.",GREEN)).pack(side="left",ipadx=10,ipady=5)
        tk.Button(row, text="🖨️ Print Report", font=FT, bg=BG_CARD, fg=WHITE,
                  relief="flat", cursor="hand2",
                  command=lambda: self._popup_result("Print","Sending to printer...",TEAL)
                  ).pack(side="left", padx=8, ipadx=10, ipady=5)

    # ════════════════════════════════════════════════════════
    #  BLUETOOTH POPUP
    # ════════════════════════════════════════════════════════
    def _bt_popup(self):
        pw = tk.Toplevel(self); pw.title("Bluetooth Device Selector")
        pw.configure(bg=BG_CARD); pw.geometry("760x800")
        tk.Label(pw, text="📶 BLUETOOTH DEVICES", font=FT_HD, bg=BG_CARD, fg=TEAL).pack(pady=(14,4))
        tk.Label(pw, text="Scanning...", font=FT_SM, bg=BG_CARD, fg=GRAY).pack()
        lbox = tk.Listbox(pw, bg=BG_CARD2, fg=WHITE, font=FT, selectbackground=RED_DARK,
                          height=12, relief="flat")
        lbox.pack(fill="both", expand=True, padx=16, pady=8)
        ctrl = tk.Frame(pw, bg=BG_CARD); ctrl.pack(pady=8)
        def connect_selected():
            sel = lbox.curselection()
            if not sel: return
            item = lbox.get(sel[0])
            parts = item.split(" — ")
            name = parts[0].strip(); addr = parts[1].strip() if len(parts)>1 else "00:00:00:00:00:00"
            ok = bt.connect(addr, name)
            if ok:
                self.status_msg.set(f"BT: {name[:30]}")
                self.status_lbl.config(fg=GREEN)
                self.conn_dot.config(fg=GREEN)
                pw.destroy()
        tk.Button(ctrl, text="CONNECT ▶", font=FT, bg=GREEN, fg=BG_DARK, relief="flat",
                  cursor="hand2", command=connect_selected).pack(side="left", ipadx=14, ipady=5)
        tk.Button(ctrl, text="Cancel", font=FT, bg=BG_CARD, fg=WHITE, relief="flat",
                  cursor="hand2", command=pw.destroy).pack(side="left", padx=8, ipadx=10, ipady=5)
        def scan():
            devices = bt.scan()
            lbox.delete(0,"end")
            for name, addr in devices:
                lbox.insert("end", f"{name} — {addr}")
        threading.Thread(target=scan, daemon=True).start()

    # ════════════════════════════════════════════════════════
    #  OBD CONNECT
    # ════════════════════════════════════════════════════════
    def _obd_connect(self):
        if not obd_mgr.connected:
            ok, msg = obd_mgr.connect()
            if ok:
                self.status_msg.set(msg[:40])
                self.status_lbl.config(fg=GREEN)
                self.conn_dot.config(fg=GREEN)
                self.conn_btn.config(text="OBD DISCONNECT", bg=GRAY)
        else:
            obd_mgr.disconnect()
            self.status_msg.set("OBD Disconnected")
            self.status_lbl.config(fg=RED)
            self.conn_dot.config(fg=RED)
            self.conn_btn.config(text="OBD CONNECT", bg=RED)


# ═════════════════════════════════════════════════════════════
#  ENTRY POINT
# ═════════════════════════════════════════════════════════════
if __name__ == "__main__":
    app = ZeusApp()
    app.mainloop()
