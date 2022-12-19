#!/usr/bin/env python3

import codecs
import json
import os
import sys
from datetime import datetime
from xml.dom import minidom
from xml.etree.ElementTree import Element, SubElement, tostring


def main(filename):
    base_file = os.path.splitext(filename)[0]
    filejson = f"{base_file}.info.json"
    with open(filejson) as data_file:
        data = json.load(data_file)

    premiered_date = datetime.strptime(data['upload_date'], '%Y%m%d').strftime('%Y-%m-%d')
    root = Element("episodedetails")
    title = SubElement(root, "title")
    episode = SubElement(root, "episode")
    premiered = SubElement(root, "premiered")
    plot = SubElement(root, "plot")

    title.text = f"{data['fulltitle']}"
    episode.text = f"{data['playlist_index']}"
    premiered.text = f"{premiered_date}"
    plot.text = f"{data['uploader_url']}\n{data['description']}\n{data['playlist_title']}"

    with codecs.open(filename=f"{base_file}.nfo", mode="w", encoding="utf-8") as file:
        file.write(prettify(root))


def prettify(elem):
    xml_string = tostring(elem, "utf-8")
    minidom_parsed = minidom.parseString(xml_string)
    return minidom_parsed.toprettyxml(indent="  ")


if __name__ == "__main__":
    filename = sys.argv[1:][0]
    main(filename)
