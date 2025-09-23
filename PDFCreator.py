import re
import os

class PDFCreator:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def create_latex(self, name, geburtsdatum, befunde, path):

        bausteine = self.db_manager.get_bausteine()
        
        #get date in format dd.mm.yyyy
        from datetime import datetime
        now = datetime.now()
        date_str = now.strftime("%d.%m.%Y")

        with open(f"{os.path.expanduser("~/Library/Application Support/Befund-Tool")}/befund_template.tex", "r") as file:
            template = file.read()

        # for baustein in bausteine:
        #     id, kategorie, text, kuerzel = baustein
        #     if kuerzel in befunde:
        #         clean = re.sub(r'[\u00B2\u00B3\u2070-\u209F\u202F]', '', text)
        #         template = template.replace(f"%item%", "\item " + clean + f"\n %item%")
                
        # other way around in order to keep order
        for befund in befunde:
            for baustein in bausteine:
                id, kategorie, text, kuerzel = baustein
                if kuerzel == befund:
                    clean = re.sub(r'[\u00B2\u00B3\u2070-\u209F\u202F]', '', text)
                    template = template.replace(f"%item%", "\item " + clean + f"\n %item%")
                    break

        template = template.replace("%Patientenname%", name)
        template = template.replace("%Geburtsdatum%", geburtsdatum)
        
        #create directory if it doesn't exist
        if not os.path.exists(f"{path}/latex"):
            os.makedirs(f"{path}/latex")
        
        with open(f"{path}/latex/{name.replace(' ', '_')}_{geburtsdatum}_{date_str}.tex", "w") as file:
            file.write(template)
            
        #execute terminal command to compile the LaTeX file
        import subprocess

        create_cmd = [
            "/Library/TeX/texbin/pdflatex",       ### geändert
            f"{name.replace(' ', '_')}_{geburtsdatum}_{date_str}.tex"   ### geändert
        ]
        
        # copy files from library to latex directory
        for file in os.listdir(os.path.expanduser("~/Library/Application Support/Befund-Tool")):
            if file.endswith(".png") or file.endswith(".tex"):
                subprocess.run(["cp", os.path.join(os.path.expanduser("~/Library/Application Support/Befund-Tool"), file), f"{path}/latex/"])

        ### geändert: cwd ins latex-Verzeichnis
        result = subprocess.run(create_cmd, cwd=f"{path}/latex")
        
        #copy PDF to path
        subprocess.run(["cp", f"{path}/latex/{name.replace(' ', '_')}_{geburtsdatum}_{date_str}.pdf", f"{path}/{name.replace(' ', '_')}_{geburtsdatum}_{date_str}.pdf"])
        
        import shutil

        latex_dir = f"{path}/latex"
        if os.path.exists(latex_dir):
            shutil.rmtree(latex_dir)

        
        print("STDOUT:\n", result.stdout)
        print("STDERR:\n", result.stderr)


        print(f"Befund PDF für {name} erstellt.")


    def save_pdf(self, filename):
        # Implement PDF saving logic here
        pass
