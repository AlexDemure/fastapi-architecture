import typer as typer
import uvicorn as uvicorn

from src.framework import settings

app = typer.Typer()


@app.command()
def run(workers: int = 1):
    print("\n".join("%s: %s" % item for item in vars(settings).items()))
    uvicorn.run(
        "src.framework.application:app",
        port=settings.SERVER_PORT,
        host="127.0.0.1",
        workers=workers,
        app_dir="src",
    )


if __name__ == "__main__":
    app()
