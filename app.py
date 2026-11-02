
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json, os, re, webbrowser
from datetime import datetime

APP_DIR=os.path.join(os.path.expanduser("~"), "ResumeMakerPro")
DATA_FILE=os.path.join(APP_DIR,"resumes.json")
os.makedirs(APP_DIR,exist_ok=True)

TEMPLATES=[]
styles=["Modern","Minimal","Corporate","Creative","Executive","Elegant","Tech","Academic","Fresher","Professional"]
colors=["Navy","Blue","Teal","Green","Purple","Burgundy","Charcoal","Orange","Indigo","Black"]
for s in styles:
    for c in colors:
        TEMPLATES.append(f"{s} {c} - {len(TEMPLATES)+1:03d}")

LABELS={
"English":{"title":"Resume Maker Pro","personal":"Personal Details","name":"Full name","role":"Target job title","email":"Email","phone":"Phone","location":"City / Address","summary":"Professional summary","education":"Education","skills":"Skills (comma separated)","experience":"Work experience","projects":"Projects","languages":"Languages","template":"Choose template","score":"Check ATS Score","pdf":"Export PDF","docx":"Export DOCX","save":"Save Resume","load":"Open Saved Resume","new":"New Resume","assistant":"Smart Suggestions","photo":"Photo path (optional)"},
"Hindi":{"title":"Resume Maker Pro","personal":"व्यक्तिगत जानकारी","name":"पूरा नाम","role":"लक्षित नौकरी","email":"ईमेल","phone":"मोबाइल","location":"शहर / पता","summary":"प्रोफाइल सारांश","education":"शिक्षा","skills":"कौशल (कॉमा से अलग)","experience":"कार्य अनुभव","projects":"प्रोजेक्ट","languages":"भाषाएँ","template":"टेम्पलेट चुनें","score":"ATS स्कोर जाँचें","pdf":"PDF डाउनलोड","docx":"DOCX डाउनलोड","save":"रिज्यूमे सेव करें","load":"सेव रिज्यूमे खोलें","new":"नया रिज्यूमे","assistant":"स्मार्ट सुझाव","photo":"फोटो पथ (वैकल्पिक)"}
}
FIELDS=["name","role","email","phone","location","summary","education","skills","experience","projects","languages"]
def read_all():
    try:
        with open(DATA_FILE,encoding="utf-8") as f: return json.load(f)
    except: return []
def write_all(items):
    with open(DATA_FILE,"w",encoding="utf-8") as f: json.dump(items,f,ensure_ascii=False,indent=2)

class App:
    def __init__(self,root):
        self.root=root; root.title("Resume Maker Pro"); root.geometry("1180x820"); root.minsize(980,700)
        self.lang=tk.StringVar(value="English"); self.template=tk.StringVar(value=TEMPLATES[0]); self.photo=tk.StringVar()
        self.entries={}; self.texts={}; self.current=None
        self.build()
    def build(self):
        self.root.configure(bg="#f3f5fa")
        top=tk.Frame(self.root,bg="#14213d",height=72); top.pack(fill="x")
        tk.Label(top,text="✦ RESUME MAKER PRO",font=("Segoe UI",20,"bold"),fg="white",bg="#14213d").pack(side="left",padx=22,pady=16)
        ttk.Combobox(top,textvariable=self.lang,values=["English","Hindi"],state="readonly",width=12).pack(side="right",padx=22)
        self.lang.trace_add("write",lambda *_: self.refresh_labels())
        body=tk.Frame(self.root,bg="#f3f5fa"); body.pack(fill="both",expand=True,padx=18,pady=14)
        left=tk.Frame(body,bg="white",width=560); left.pack(side="left",fill="both",expand=True,padx=(0,10))
        right=tk.Frame(body,bg="white",width=480); right.pack(side="right",fill="both",expand=True)
        self.form=left; self.preview=right
        self.heading=tk.Label(left,text="Personal Details",font=("Segoe UI",15,"bold"),bg="white",fg="#14213d"); self.heading.pack(anchor="w",padx=18,pady=(14,8))
        grid=tk.Frame(left,bg="white"); grid.pack(fill="x",padx=16)
        for i,key in enumerate(FIELDS):
            label=tk.Label(grid,text=LABELS["English"][key],bg="white",fg="#344054",font=("Segoe UI",9,"bold"))
            label.grid(row=i,column=0,sticky="w",pady=4)
            if key in ("summary","education","skills","experience","projects","languages"):
                w=tk.Text(grid,height=3 if key in ("summary","experience","education") else 2,width=42,font=("Segoe UI",9),wrap="word",relief="solid",bd=1)
                w.grid(row=i,column=1,sticky="ew",padx=8,pady=3); self.texts[key]=w
            else:
                w=tk.Entry(grid,font=("Segoe UI",10),relief="solid",bd=1); w.grid(row=i,column=1,sticky="ew",padx=8,pady=3,ipady=4); self.entries[key]=w
            setattr(self,key+"_label",label)
        grid.columnconfigure(1,weight=1)
        photo_row=tk.Frame(left,bg="white"); photo_row.pack(fill="x",padx=18,pady=6)
        self.photo_label=tk.Label(photo_row,text="Photo path (optional)",bg="white"); self.photo_label.pack(side="left")
        tk.Entry(photo_row,textvariable=self.photo,width=28).pack(side="left",padx=6)
        tk.Button(photo_row,text="Browse",command=self.pick_photo).pack(side="left")
        templ=tk.Frame(left,bg="white"); templ.pack(fill="x",padx=18,pady=8)
        self.template_label=tk.Label(templ,text="Choose template",bg="white",font=("Segoe UI",9,"bold")); self.template_label.pack(side="left")
        ttk.Combobox(templ,textvariable=self.template,values=TEMPLATES,state="readonly",width=34).pack(side="left",padx=8)
        buttons=tk.Frame(left,bg="white"); buttons.pack(fill="x",padx=16,pady=8)
        self.btn_save=tk.Button(buttons,text="Save Resume",command=self.save,bg="#176b55",fg="white",relief="flat",padx=10,pady=8); self.btn_save.pack(side="left",padx=3)
        self.btn_load=tk.Button(buttons,text="Open Saved Resume",command=self.load,bg="#e9eef8",relief="flat",padx=10,pady=8); self.btn_load.pack(side="left",padx=3)
        self.btn_new=tk.Button(buttons,text="New Resume",command=self.clear,bg="#e9eef8",relief="flat",padx=10,pady=8); self.btn_new.pack(side="left",padx=3)
        buttons2=tk.Frame(left,bg="white"); buttons2.pack(fill="x",padx=16,pady=4)
        self.btn_ats=tk.Button(buttons2,text="Check ATS Score",command=self.ats,bg="#14213d",fg="white",relief="flat",padx=12,pady=9); self.btn_ats.pack(side="left",padx=3)
        self.btn_pdf=tk.Button(buttons2,text="Export PDF",command=self.export_pdf,bg="#276ef1",fg="white",relief="flat",padx=12,pady=9); self.btn_pdf.pack(side="left",padx=3)
        self.btn_docx=tk.Button(buttons2,text="Export DOCX",command=self.export_docx,bg="#276ef1",fg="white",relief="flat",padx=12,pady=9); self.btn_docx.pack(side="left",padx=3)
        self.score=tk.Label(left,text="ATS score will appear here",bg="#eef3ff",fg="#14213d",font=("Segoe UI",11,"bold"),anchor="w",padx=12,pady=12); self.score.pack(fill="x",padx=18,pady=12)
        self.suggest=tk.Label(left,text="Smart Suggestions: Add clear sections, measurable achievements and keywords from the job description.",bg="white",fg="#667085",wraplength=510,justify="left"); self.suggest.pack(fill="x",padx=18,pady=4)
        tk.Label(right,text="LIVE RESUME PREVIEW",font=("Segoe UI",14,"bold"),bg="white",fg="#14213d").pack(anchor="w",padx=16,pady=14)
        self.preview_text=tk.Text(right,font=("Segoe UI",10),wrap="word",bg="#fbfcff",relief="solid",bd=1,padx=18,pady=16)
        self.preview_text.pack(fill="both",expand=True,padx=16,pady=(0,16))
        for widget in list(self.entries.values())+list(self.texts.values()):
            if isinstance(widget,tk.Entry): widget.bind("<KeyRelease>",lambda e:self.update_preview())
            else: widget.bind("<KeyRelease>",lambda e:self.update_preview())
        self.update_preview()
    def refresh_labels(self):
        d=LABELS[self.lang.get()]
        self.heading.config(text=d["personal"])
        for k in FIELDS: getattr(self,k+"_label").config(text=d[k])
        self.photo_label.config(text=d["photo"]); self.template_label.config(text=d["template"])
        self.btn_save.config(text=d["save"]); self.btn_load.config(text=d["load"]); self.btn_new.config(text=d["new"])
        self.btn_ats.config(text=d["score"]); self.btn_pdf.config(text=d["pdf"]); self.btn_docx.config(text=d["docx"])
    def pick_photo(self):
        p=filedialog.askopenfilename(filetypes=[("Images","*.png *.jpg *.jpeg")])
        if p:self.photo.set(p)
    def data(self):
        d={k:w.get().strip() for k,w in self.entries.items()}
        d.update({k:w.get("1.0","end").strip() for k,w in self.texts.items()})
        d["template"]=self.template.get(); d["photo"]=self.photo.get(); d["updated"]=datetime.now().isoformat()
        return d
    def set_data(self,d):
        for k,w in self.entries.items(): w.delete(0,"end"); w.insert(0,d.get(k,""))
        for k,w in self.texts.items(): w.delete("1.0","end"); w.insert("1.0",d.get(k,""))
        self.template.set(d.get("template",TEMPLATES[0])); self.photo.set(d.get("photo","")); self.update_preview()
    def update_preview(self):
        d=self.data()
        lines=[d.get("name") or "YOUR NAME",d.get("role") or "Target Job Title"," | ".join(x for x in [d.get("email"),d.get("phone"),d.get("location")] if x)]
        for key,title in [("summary","PROFILE"),("skills","SKILLS"),("experience","EXPERIENCE"),("education","EDUCATION"),("projects","PROJECTS"),("languages","LANGUAGES")]:
            if d.get(key): lines += ["",title,d[key]]
        self.preview_text.config(state="normal"); self.preview_text.delete("1.0","end"); self.preview_text.insert("1.0","\n".join(lines)); self.preview_text.config(state="disabled")
    def save(self):
        d=self.data()
        if not d["name"]: messagebox.showwarning("Required","Please enter your full name."); return
        allr=read_all()
        if self.current is not None and self.current<len(allr): allr[self.current]=d
        else: allr.append(d); self.current=len(allr)-1
        write_all(allr); messagebox.showinfo("Saved",f"Resume saved locally in {DATA_FILE}")
    def load(self):
        allr=read_all()
        if not allr: messagebox.showinfo("No resumes","No saved resumes found."); return
        win=tk.Toplevel(self.root); win.title("Saved Resumes"); win.geometry("420x360")
        lb=tk.Listbox(win,font=("Segoe UI",10)); lb.pack(fill="both",expand=True,padx=12,pady=12)
        for r in allr: lb.insert("end",f'{r.get("name","Unnamed")} — {r.get("role","")}')
        def open_selected():
            sel=lb.curselection()
            if sel:self.current=sel[0]; self.set_data(allr[sel[0]]); win.destroy()
        tk.Button(win,text="Open Selected",command=open_selected).pack(pady=8)
    def clear(self):
        self.current=None
        for w in self.entries.values(): w.delete(0,"end")
        for w in self.texts.values(): w.delete("1.0","end")
        self.template.set(TEMPLATES[0]); self.photo.set(""); self.score.config(text="ATS score will appear here"); self.update_preview()
    def ats(self):
        d=self.data(); score=0; checks=[]
        if d["name"]: score+=10
        if d["email"] and re.search(r"[^@]+@[^@]+\.[^@]+",d["email"]): score+=10
        if d["phone"]: score+=5
        if d["summary"]: score+=15
        if d["education"]: score+=10
        if d["skills"]: score+=15
        if d["experience"] or d["projects"]: score+=15
        if d["role"]: score+=10
        if len(d["summary"])+len(d["experience"])+len(d["projects"])>250: score+=10
        missing=[x for x in ["summary","education","skills","experience"] if not d[x]]
        self.score.config(text=f"Estimated ATS Readiness: {score}/100")
        tips=[]
        if missing: tips.append("Add: "+", ".join(missing))
        if not d["role"]: tips.append("Add a target job title.")
        tips.append("Match relevant keywords from the job description; quantify achievements where possible.")
        self.suggest.config(text="Smart Suggestions: "+" ".join(tips))
    def export_pdf(self):
        try: from reportlab.lib.pagesizes import A4; from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer; from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle; from reportlab.lib import colors
        except ImportError: messagebox.showerror("Missing package","Install requirements.txt first."); return
        p=filedialog.asksaveasfilename(defaultextension=".pdf",filetypes=[("PDF","*.pdf")])
        if not p:return
        d=self.data(); doc=SimpleDocTemplate(p,pagesize=A4,rightMargin=42,leftMargin=42,topMargin=42,bottomMargin=42); st=getSampleStyleSheet()
        story=[Paragraph(d["name"] or "Resume",st["Title"]),Paragraph(d["role"],st["Heading2"]),Paragraph(" | ".join(x for x in [d["email"],d["phone"],d["location"]] if x),st["Normal"]),Spacer(1,12)]
        for k,t in [("summary","PROFILE"),("skills","SKILLS"),("experience","EXPERIENCE"),("education","EDUCATION"),("projects","PROJECTS"),("languages","LANGUAGES")]:
            if d[k]:
                story += [Paragraph(t,st["Heading2"]),Paragraph(d[k].replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace("\n","<br/>"),st["BodyText"]),Spacer(1,8)]
        doc.build(story); messagebox.showinfo("Exported","PDF created successfully.")
    def export_docx(self):
        try: from docx import Document
        except ImportError: messagebox.showerror("Missing package","Install requirements.txt first."); return
        p=filedialog.asksaveasfilename(defaultextension=".docx",filetypes=[("Word document","*.docx")])
        if not p:return
        d=self.data(); doc=Document(); doc.add_heading(d["name"] or "Resume",0)
        if d["role"]: doc.add_heading(d["role"],2)
        doc.add_paragraph(" | ".join(x for x in [d["email"],d["phone"],d["location"]] if x))
        for k,t in [("summary","PROFILE"),("skills","SKILLS"),("experience","EXPERIENCE"),("education","EDUCATION"),("projects","PROJECTS"),("languages","LANGUAGES")]:
            if d[k]: doc.add_heading(t,2); doc.add_paragraph(d[k])
        doc.save(p); messagebox.showinfo("Exported","Word document created successfully.")

if __name__=="__main__":
    root=tk.Tk(); App(root); root.mainloop()
