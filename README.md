# GitHub CSV Viewer

A Streamlit app that connects to GitHub, retrieves CSV files from a private repository, udilizing [github personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens).

## Features

- Data filtering
- Ease of use
- Quick setup
- 


## Installation 

1. Clone the repository

    ```bash
    git clone https://github.com/zvdy/py-git-csv-analysis

    cd py-git-csv-analysis
    ```

2. Install dependencies

    ```bash
    pip install -e .
    ```

3. Run the `streamlit` project

    ```bash
    streamlit run main.py
    ```

4. Insert your `github_PAT` and repository `username/repo` and navigate through all `.csv` files.
