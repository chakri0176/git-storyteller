from pathlib import Path
from git import Repo
from rich.table import Table
from rich.console import Console
from rich import box


def last_commits(repo_path: Path, n: int = 10)->None:
    "This will prints the last *n* commits as a table"
    repo = Repo(repo_path)
    commits = list(repo.iter_commits("HEAD",max_count=n))
    table = Table(title=f"Last {n} commits", box=box.MINIMAL)
    table.add_column("Hash",style="cyan",no_wrap=True)
    table.add_column("Author")
    table.add_column("Message")
    
    for c in commits:
        table.add_row(c.hexsha[:7],c.author.name,c.message.split("\n")[0])
    console = Console()
    console.print(table)
    
if __name__ == "__main__":
    import sys
    path_arg = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    last_commits(path_arg)