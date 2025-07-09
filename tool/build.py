# /// script
# requires-python = ">=3.13"
# ///

from pathlib import Path
from string import Template


def insert_dictionary(text: str, dictionary: dict) -> str:
    return Template(text).safe_substitute(dictionary)


def process_script(path: Path, info: str, version: str, author: str, params: dict = {}) -> str:
    text = path.read_text(encoding="utf-8")
    return insert_dictionary(text, {
        "INFO": info,
        "VERSION": version,
        "AUTHOR": author,
        **params
    })


def main():
    AUTHOR = "karoterra"
    VERSION = "v0.1.0"

    SHADER_brettel1997 = Path("script/brettel1997.hlsl").read_text(encoding="utf-8")
    SHADER_vienot1999 = Path("script/vienot1999.hlsl").read_text(encoding="utf-8")
    SHADER_achromat = Path("script/achromat.hlsl").read_text(encoding="utf-8")

    build_dir = Path("build")
    build_dir.mkdir(exist_ok=True)

    src_list = [
        {
            "file": "script/色覚シミュレーションKR.in.anm2",
            "info": "色覚シミュレーションKR for AviUtl2",
        }
    ]

    script_texts = []
    for src in src_list:
        if "label" in src:
            script_texts.append(f"@{src['label']}")
        text = process_script(
            Path(src["file"]),
            src["info"],
            VERSION,
            AUTHOR,
            params={
                "SHADER_brettel1997": SHADER_brettel1997,
                "SHADER_vienot1999": SHADER_vienot1999,
                "SHADER_achromat": SHADER_achromat,
            }
        )
        script_texts.append(text)

    output_file = build_dir / "色覚シミュレーションKR.anm2"
    output_file.write_text("\n".join(script_texts), encoding="utf-8", newline="\r\n")


if __name__ == "__main__":
    main()
