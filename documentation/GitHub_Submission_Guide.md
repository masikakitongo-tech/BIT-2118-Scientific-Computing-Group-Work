# GitHub Submission Guide

The assignment requires an **individual** GitHub repository (not a group repository). The repository link and the documentation are uploaded on VLMS.

The project folder is a **local Git repository** on the branch `main` with a `.gitignore` and a clean commit history. It is published to a **new** repository using the existing GitHub account, so no other repository is touched.

## Suggested repository

| Item | Value |
|---|---|
| Repository name | `BIT-2118-Scientific-Computing-Group-Work` |
| Visibility | Public (so the lecturer can open it) |
| Description | BIT 2118 Scientific Computing group work: Tasks 2-20 in Python (NumPy, SciPy, Matplotlib) |

## Before publishing

1. Open `README.md` and write your name, registration number and group in the table at the top, then save.
2. Check that everything works and that no file is waiting to be saved:

```bash
python run_all.py
git status
```

`run_all.py` must end with *"All selected tasks ran successfully."* If it re-creates the files in `results/`, `git status` will show them as changed because the timings in Tasks 3 and 7 differ slightly each run; commit them with `git add results` and `git commit -m "chore: refresh saved results"`.

## Publish with GitHub Desktop (uses your existing login)

1. Open **GitHub Desktop** and check that you are signed in as the correct account (**File → Options → Accounts**).
2. **File → Add local repository…**, choose the project folder and click **Add repository**.
3. Click **Publish repository** (top bar).
4. Check the form:
   - **Name:** `BIT-2118-Scientific-Computing-Group-Work`
   - **Description:** as in the table above
   - **Keep this code private:** **untick** it (public)
   - **Organization:** *None* (your own account)
5. Click **Publish repository**.

## After publishing

The repository address will be

```
https://github.com/<your-username>/BIT-2118-Scientific-Computing-Group-Work
```

Open it in a browser (preferably in a private window, where you are not signed in) to confirm that the lecturer can see it, then upload that link and the documentation on VLMS.

## Notes

- The lecturer's assignment PDF is listed in `.gitignore`, so it is not uploaded. Delete that line in `.gitignore` if the lecturer wants it in the repository.
- Later changes: save them with `git add` and `git commit`, then click **Push origin** in GitHub Desktop.
