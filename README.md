# PIT - Git but in Python

**PIT** is a lightweight, distributed source control system inspired by Git. It enables you to initialize repositories, stage files, commit changes, create branches, merge them, and view differences between file versions—all within a single directory.

This project was created as part of the Pesapal Junior Programmer Challenge '24 to demonstrate problem-solving, design thinking, and technical skills.

---

## Features
- **Repository Initialization:** Create a `.pit` directory for managing source control.
- **File Staging:** Add files to a staging area for tracking changes.
- **Committing Changes:** Save versions of files with descriptive commit messages.
- **Branching:** Create and switch between branches for independent development paths.
- **Merging:** Combine branches with support for conflict detection.
- **Status:** View Untracked, Modified and Staged Files.
- **Diffing:** View differences between commits or files in the working directory.
- **Cloning:** Clone a repository within the local file system.
- **Ignore Files:** Specify files or patterns to exclude from tracking via a `.pitignore` file.

---

## Project Structure

```
src/
├── branch.py          # Handles branch creation and checkout
├── cli.py             # Passes cli args to pit functions
├── clone.py           # Handles repository cloning
├── commit.py          # Manages commit operations
├── constants.py       # Re-usable string constants
├── diff.py            # Displays file differences
├── merge.py           # Handles branch merging
├── repository.py      # Manages repository initialization
├── staging.py         # Manages file staging
├── status.py          # Displays current repo status
├── utils.py           # Provides helper functions
tests/
├── test_repository.py # Tests for repository initialization
├── test_staging.py    # Tests for staging functionality
├── test_commit.py     # Tests for committing functionality
├── test_diff.py       # Tests for file diffs
```

---

## Installation

### Prerequisites
- Python 3.8 or higher installed on your system.

### Steps
1. Clone this repository:
   ```bash
   git clone https://github.com/zedjarvis/pit.git
   cd pit
   ```
2. Install dependencies (if any). For example:
   ```bash
   pip install -r requirements.txt
   ```
3. Make the tool executable:
   ```bash
   chmod +x pit.py
   ```

---

## Usage

### Initialize a Repository
```bash
python pit.py init
```

### Stage Files
```bash
python pit.py add file1.txt file2.txt
```

### Commit Changes
```bash
python pit.py commit -m "Commit message"
```

### Create a Branch
```bash
python pit.py branch branch_name
```

### Switch to a Branch
```bash
python pit.py checkout branch_name
```

### Merge Branches
```bash
python pit.py merge branch_name
```

### Check Branch Status
```bash
python pit.py status
```

### View Differences
```bash
python pit.py diff
```

### Clone a Repository
```bash
python pit.py clone /path/to/source /path/to/destination
```

### Ignore Files
Create a `.pitignore` file in the root of your repository with file names or patterns to exclude:
```
*.log
temp/
```

---

## Testing
To run the unit tests, execute:
```bash
python -m unittest discover -s tests
```

---

## Design Choices
1. **SHA1 Hashing:** Used to uniquely identify files and commits for simplicity.
2. **File-Based System:** A `.pit` directory stores all metadata and objects, mimicking Git's design.
3. **Command-Based Interface:** Similar to Git for familiarity.

---

## Challenges and Future Improvements
- Adding conflict resolution for merges.
- Supporting remote repositories over a network.
- Implementing additional features like rebase and cherry-pick.

---

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Feel free to customize it further based on your specific approach or additional features you've implemented!