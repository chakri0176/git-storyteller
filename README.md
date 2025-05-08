## Git history check CLI using GitPython+Rich
## Day 1 — Initial Commit History CLI
* Added `storyteller/git_dag.py`
* Prints last N commits in pretty table (uses GitPython + Rich)
graph TD
  subgraph Front-end
    R[React Timeline UI]
  end

  subgraph Backend
    F[FastAPI /commits & /ast]
    TS[Tree-sitter parser]
    LLM[llama.cpp local LLM]
  end

  Repo[(Local Git repo)]

  Repo -->|GitPython| F
  F -->|JSON| R
  F --> TS
  F --> LLM
  TS --> F
  LLM --> F
