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
    premiered_date = get_datetime_str(json_dict['upload_date'])
    root = Element("episodedetails")
    title = SubElement(root, "title")
    episode = SubElement(root, "episode")
    premiered = SubElement(root, "premiered")
    plot = SubElement(root, "plot")

    title.text = json_dict['fulltitle']
    episode.text = json_dict['playlist_index']
    premiered.text = premiered_date
    plot.text = json_dict['description']

    return root


def prettify(elem: Element) -> str:
    xml_string = tostring(elem, ENC)
    minidom_parsed = minidom.parseString(xml_string)
    return minidom_parsed.toprettyxml(indent=INDENT)


def get_datetime_str(date: str, out_fmt=KODI_DATE) -> str:
    return datetime.strptime(date, YTD_DATE).strftime(out_fmt)


if __name__ == "__main__":
    filename = sys.argv[1:][0]
    main(filename)
