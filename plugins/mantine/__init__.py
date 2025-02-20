# -*- coding: utf-8 -*-
# Copyright (c) 2024 Manuel Schneider

"""
Search for components from Mantine and open their URLs via browser.
"""

import json
import typing
from pathlib import Path
from shutil import which

import albert

md_iid = "2.3"
md_version = "0.01"
md_name = "Mantine Components"
md_description = "Open and search for Mantine components"
md_license = "MIT"
md_url = "None"
md_authors = "Nic"

EXEC = "xdg-open"
DEFAULT_TRIGGER = "mantine"


class MantineLink(typing.TypedDict):
    name: str
    url: str


class Plugin(albert.PluginInstance, albert.TriggerQueryHandler):
    data: dict[str, list[MantineLink]] = None

    def __init__(self):
        albert.PluginInstance.__init__(self)
        albert.TriggerQueryHandler.__init__(
            self, self.id, self.name, self.description, defaultTrigger=DEFAULT_TRIGGER
        )
        self.iconUrls = [f"file:{Path(__file__).parent}/mantine.svg"]

        with open(Path(__file__).parent / "data.json", "r") as f:
            self.data = json.load(f)

        if not which(EXEC):
            albert.info("No browser found")
            return

    def configWidget(self):
        return [{"type": "label", "text": __doc__.strip()}]

    def handleTriggerQuery(self, query):
        striped_query = query.string.strip().lower()
        if striped_query:
            keywords = striped_query.split()

            for key, value in self.data.items():
                filtered_value = [
                    link
                    for link in value
                    if any(k in link["name"].lower() for k in keywords)
                ]
                for link in filtered_value:
                    cmd = [EXEC] + [link["url"]]
                    query.add(
                        albert.StandardItem(
                            id=self.id,
                            text=f"Mantine {key} - {link['name']}",
                            subtext=link["url"],
                            iconUrls=self.iconUrls,
                            actions=[
                                albert.Action(
                                    "Open in browser",
                                    "Open in browser",
                                    lambda c=cmd: albert.runDetachedProcess(c),
                                )
                            ],
                        )
                    )
        else:
            core = self.data["Inputs"]
            for link in core:
                cmd = [EXEC] + [link["url"]]
                query.add(
                    albert.StandardItem(
                        id=self.id,
                        text=f"Mantine {link['name']}",
                        subtext=link["url"],
                        iconUrls=self.iconUrls,
                        actions=[
                            albert.Action(
                                "Open in browser",
                                "Open in browser",
                                lambda c=cmd: albert.runDetachedProcess(c),
                            )
                        ],
                    )
                )
