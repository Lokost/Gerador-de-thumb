# coding: utf-8

from datetime import datetime, timedelta
from genericpath import exists
from io import TextIOWrapper
import os
from random import choice
import re
import unicodedata
from PIL import Image, ImageDraw, ImageFont
import json
import sqlite3
import sys

data = {
    "localdata": os.getenv("APPDATA") + "\\LokoThumb",
    "version": "1.0.0"
}

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def db_execute(command: str, *params) -> None:
    with sqlite3.connect(data["localdata"] + "/loko.db") as db:
        cursor = db.cursor()
        cursor.execute(command, params)
        db.commit()
        return cursor.fetchall()


def get_config():
    if not os.path.exists(data["localdata"]):
        os.mkdir(data["localdata"])

    try:
        with open(data["localdata"] + "/config.json", encoding="utf-8") as file:
            return json.load(file)

    except FileNotFoundError:
        with open(data["localdata"] + "/config.json", "w", encoding="utf-8") as file:
            json.dump({"outputFolder": "./"}, file, indent=4, separators=(",", ":"))

            return {"outputFolder": "./"}


def save_config(path):
    config = get_config()
    config["outputFolder"] = path

    with open(data["localdata"] + "/config.json", "w", encoding="utf-8") as file:
        json.dump(config, file, indent=4, separators=(",", ":"))


def add_alias(alias, file, x, y, stroke_color, stroke_weight):
    base = {
        "alias": alias,
        "title_max": 20,
        "source": file,
        "x": x,
        "y": y,
        "font": "AveriaSansLibre-Bold.ttf",
        "font_size": 100,
        "stroke_color": stroke_color,
        "stroke_weight": stroke_weight,
    }

    db_execute(
        "INSERT INTO bases (alias, title_max, path, x, y, font, font_size, stroke_color, stroke_weight) VALUES (?,?,?,?,?,?,?,?,?)",
        base["alias"],
        base["title_max"],
        base["source"],
        base["x"],
        base["y"],
        base["font"],
        base["font_size"],
        base["stroke_color"],
        base["stroke_weight"],
    )


def update_base(alias, source, x, y, stroke_color, stroke_weight):
    db_execute(
        "UPDATE bases SET path = ?, x = ?, y = ?, stroke_color = ?, stroke_weight = ? WHERE alias = ?",
        source,
        x,
        y,
        stroke_color,
        stroke_weight,
        alias,
    )


def get_bases():
    return db_execute("SELECT * FROM bases")


def get_base(alias: str):
    results = db_execute("SELECT * FROM bases WHERE alias = ?", alias)[0]

    return {
        "title_max": results[3],
        "source": results[2],
        "x": results[4],
        "y": results[5],
        "font": results[6],
        "font_size": results[7],
        "stroke_color": results[8],
        "stroke_weight": results[9],
    }


def get_alias():
    results = db_execute("SELECT alias FROM bases")
    return [res[0] for res in results]


def parse_filename(value):
    value = unicodedata.normalize("NFKC", value)
    value = re.sub(r"[^\w\s-]", "", value.lower())
    return re.sub(r"[-\s]+", "-", value).strip("-_")

def remove_base(alias):
    db_execute("DELETE FROM bases WHERE alias = ?", alias)

class Alert:
    path = f"{data['localdata']}/logs"
    filename = datetime.now().strftime("%d-%m-%y") + ".log"
    file: TextIOWrapper

    def __init__(self):
        if not exists(self.path):
            os.mkdir(self.path)

        if not exists(f"{self.path}/{self.filename}"):
            open(f"{self.path}/{self.filename}", "w").close()
        
        self.file = open(f"{self.path}/{self.filename}", "r+")

    def log(self, message):
        log = f"[{datetime.now().strftime('%H:%M:%S')}] - {message}"
        print(log)
        self.file.write(f"{log}\n")
        self.file.flush()

class ThumbGen:
    def __init__(self, auto_date, auto_hour, alias, title=""):
        self.auto_date = auto_date
        self.auto_hour = auto_hour
        self.title = title
        self.alias = alias
        self.config = get_config()

    def set_date(self, hour):
        self.hour = hour

    def set_hour(self, date):
        self.date = date

    def auto_day(self):
        self.date = (datetime.now() + timedelta(hours=1)).strftime("%d/%m/%y")

    def auto_time(self):
        self.hour = (datetime.now() + timedelta(hours=1)).strftime("%Hh")

    def generate(self):
        if self.auto_date:
            self.auto_day()

        if self.auto_hour:
            self.auto_time()

        text = str(
            f"{self.title}\n{self.date}\n{self.hour}"
            if self.title
            else f"{self.date}\n{self.hour}"
        )

        base = get_base(self.alias if self.alias != "*" else choice(get_alias()))
        img = Image.open(base["source"])
        edited = ImageDraw.Draw(img)
        myFont = ImageFont.truetype(base["font"], base["font_size"])

        edited.text(
            (base["x"], base["y"]),
            anchor="ma",
            text=text,
            font=myFont,
            align="center",
            fill="white",
            stroke_width=base["stroke_weight"],
            stroke_fill=tuple(
                int(base["stroke_color"].lstrip("#")[i : i + 2], 16) for i in (0, 2, 4)
            ),
        )

        save_path = (
            self.config["outputFolder"]
            + f"""/{parse_filename(f'{self.date}_{self.hour}{"_" + self.title if self.title else ""}')}.png"""
        )

        img.save(save_path, "PNG")
        if save_path.startswith("./"):
            print("relpath")
            path = os.path.realpath("./")
            print(path)
            os.system(f'"{path + "/" + save_path[2:]}"')
        else:
            os.system(f'"{save_path}"')


# Fim
