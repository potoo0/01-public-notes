# 命令行参数处理工具, repo: https://github.com/tiangolo/typer
import typer


def main(name: str):
    print(f"Hello {name}")


if __name__ == "__main__":
    typer.run(main)
