#!/usr/bin/env -S uv run --script
#
# "File Upload" pattern — htmx v4 docs:
# https://four.htmx.org/patterns/file-upload
#
# The form sets hx-encoding="multipart/form-data" (sends FormData, required
# for files) and hx-post submits to /upload. The server responds with a
# success or error message. To preserve the file selection when the form is
# re-rendered with errors, the file input carries hx-preserve — select a
# file, then submit with an empty title: the form comes back with errors
# but your selection stays. (Upload progress: htmx 4 uses native fetch and
# does not report it; for full-featured uploads see Uppy/FilePond/Dropzone.)
#
# /// script
# requires-python = ">=3.14"
# dependencies = ["heflex", "uvicorn", "python-multipart"]
#
# [tool.uv.sources]
# heflex = { path = "../", editable = true }
# ///

import uvicorn
from fastapi import FastAPI, File, Form as FastAPIForm, UploadFile
from heflex import Button, Component, Div, Form, Heflex, Input, Style
from heflex.component import H1, P


def upload_form(errors: str | None) -> Div:
    return Div(
        Form(
            P("Title:"),
            Input(type="text", name="title"),
            P("File:"),
            Input(type="file", name="file", hx_preserve="this"),
            Button("Submit", type="submit"),
            hx_post="/upload",
            hx_encoding="multipart/form-data",
            hx_target="#result",
            hx_swap="innerHTML",
        ),
        *( [P(errors, class_="error")] if errors else [] ),
    )


hx = Heflex(FastAPI(debug=True, title="File Upload"))


@hx.route("/", methods=["GET"])
async def index() -> Component:
    return Div(
        H1("Upload"),
        upload_form(None),
        Div(id="result", min_height="2rem"),
        Style(".error { color: oklch(57.7% 0.245 27.325); } .ok { color: green; }"),
    )


@hx.route("/upload", methods=["POST"])
async def upload(title: str = FastAPIForm(""), file: UploadFile | None = File(None)) -> Component:
    """Success message — or the re-rendered form (with hx-preserve) on error."""
    if not title.strip():
        return upload_form("Title is required.")
    if file is None:
        return upload_form("A file is required.")
    data = await file.read()
    return Div(
        P("File uploaded successfully.", class_="ok"),
        P(f"{file.filename} ({len(data)} bytes) titled “{title.strip()}”."),
    )


app = hx.app

if __name__ == "__main__":
    uvicorn.run(app, port=8000)
