from pathlib import Path

SUPPORTED_EXTENSIONS = [
    ".txt",
    ".md"
]


def load_documents(folder):

    folder = Path(folder)

    if not folder.exists():
        raise FileNotFoundError(
            f"{folder} does not exist"
        )


    documents = []


    for file in folder.iterdir():

        if file.suffix.lower() in SUPPORTED_EXTENSIONS:

            documents.append(
                {
                    "source": file.name,
                    "text": file.read_text(
                        encoding="utf-8"
                    )
                }
            )


    return documents