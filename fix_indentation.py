import re

def clean_file(filename="app.py"):
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()
    # Inasafisha tabo na spaces zilizoharibika nyuma ya pazia
    cleaned = content.replace("\t", "    ")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(cleaned)
    print("Master Machine File App.py Imerekebishwa Spaces Zote Kikamilifu!")

if __name__ == "__main__":
    clean_file()
