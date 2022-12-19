#!/usr/bin/env python3

import codecs
import json
import os
import sys
from datetime import datetime
from typing import Dict, Any
from xml.dom import minidom
from xml.etree.ElementTree import Element, SubElement, tostring

INDENT = '  '
ENC = 'utf-8'
KODI_DATE = '%Y-%m-%d'
YTD_DATE = '%Y%m%d'


def main(json_file: str):
    base_file = os.path.splitext(json_file)[0]
    with open(f"{base_file}.info.json") as data_file:
        data = json.load(data_file)

    xml_data = get_xml_data(data)

    with codecs.open(filename=f"{base_file}.nfo", mode="w", encoding=ENC) as file:
        file.write(prettify(xml_data))


def get_xml_data(json_dict: Dict[str, Any]) -> Element:
    root = Element("episodedetails")
    title = SubElement(root, "title")
    show = SubElement(root, "showtitle")
    season = SubElement(root, "season")
    episode = SubElement(root, "episode")
    dseason = SubElement(root, "displayseason")
    depisode = SubElement(root, "displayepisode")
    plot = SubElement(root, "plot")
    runtime = SubElement(root, "runtime")
    uuid = SubElement(root, "uniqueid")
    premiered = SubElement(root, "premiered")
    year = SubElement(root, "year")
    aired = SubElement(root, "aired")

    title.text = json_dict['fulltitle']
    show.text = json_dict['channel']
    season.text = dseason.text = "1"
    episode.text = depisode.text = f"{json_dict['n_entries'] - json_dict['playlist_index'] + 1}"
    plot.text = json_dict['description']
    runtime.text = get_minutes_from_sec(json_dict['duration'])
    uuid.text = json_dict['id']
    uuid.set("type", json_dict['extractor'])
    uuid.set("default", "true")
    premiered.text = aired.text = get_datetime_str(json_dict['upload_date'])
    year.text = get_datetime_str(json_dict['upload_date'], '%Y')

    return root


def get_minutes_from_sec(secs) -> int:
    minutes = secs // 60
    remainder = secs % 60
    return minutes if remainder == 0 else minutes + 1


def prettify(elem: Element) -> str:
    xml_string = tostring(elem, ENC)
    minidom_parsed = minidom.parseString(xml_string)
    return minidom_parsed.toprettyxml(indent=INDENT)


def get_datetime_str(date: str, out_fmt=KODI_DATE) -> str:
    return datetime.strptime(date, YTD_DATE).strftime(out_fmt)


if __name__ == "__main__":
    filename = sys.argv[1:][0]
    main(filename)
