# -*- coding: utf-8 -*-
# Copyright (c) 2024 Manuel Schneider

"""
Search for workspaces from Visual Studio Code and open it in Visual Studio Code.
"""

import json
from dataclasses import dataclass
from pathlib import Path
from shutil import which

import albert

md_iid = "2.3"
md_version = "0.01"
md_name = "VSCode Projects"
md_description = "Open and search for Visual Studio Code projects"
md_license = "MIT"
md_url = "None"
md_authors = "Nic"

EXEC = "/usr/bin/code"
DEFAULT_TRIGGER = "code"


@dataclass
class Project:
    name: str
    path: str


class Plugin(albert.PluginInstance, albert.TriggerQueryHandler):
    config_path = Path.home() / ".config" / "Code" / "User" / "workspaceStorage"

    def __init__(self):
        albert.PluginInstance.__init__(self)
        albert.TriggerQueryHandler.__init__(
            self, self.id, self.name, self.description, defaultTrigger=DEFAULT_TRIGGER
        )
        self.iconUrls = [f"file:{Path(__file__).parent}/vscode.svg"]

        if not which("code"):
            albert.info("VSCode not found")
            return

    def configWidget(self):
        return [{"type": "label", "text": __doc__.strip()}]

    def handleTriggerQuery(self, query):
        projects = self.projects()

        striped_query = query.string.strip().lower()
        if striped_query:
            keywords = striped_query.split()
            projects = [
                p for p in projects if all(k in p.name.lower() for k in keywords)
            ]

            # projects = [
            #     p for p in projects if p.name.lower().find(striped_query.lower()) != -1
            # ]

        if not projects:
            query.add(
                albert.StandardItem(
                    id=self.id,
                    text="No results",
                    subtext="No projects found",
                    iconUrls=self.iconUrls,
                )
            )
            return

        for project in projects:
            project_path = f"/{project.path}"
            cmd = [EXEC] + [project_path]
            query.add(
                albert.StandardItem(
                    id=self.id,
                    text=project.name,
                    subtext="Open project located at " + project_path,
                    iconUrls=self.iconUrls,
                    actions=[
                        albert.Action(
                            "open-project",
                            "Open project",
                            lambda c=cmd: albert.runDetachedProcess(c),
                        )
                    ],
                )
            )

    def projects(self):
        workspaces = list(self.config_path.glob("**/workspace.json"))
        projects: list[Project] = []
        for workspace in workspaces:
            with open(workspace, "r") as f:
                try:
                    data = json.load(f)
                    workspace_folder_path = data.get(
                        "folder", data.get("workspace")
                    ).lstrip("file://")
                    project = Project(
                        name=workspace_folder_path.split("/")[-1],
                        path=workspace_folder_path,
                    )
                    projects.append(project)
                except Exception:
                    pass

        return projects
