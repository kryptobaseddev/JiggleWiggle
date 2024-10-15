# Developer Instructions for JiggleWiggle

This document provides step-by-step instructions on setting up the development environment, compiling the app, and updating the version and changelog.

---

## 1. Setting Up the Development Environment

### Step 1: Clone the Repository

If you haven't cloned the repository yet, do so using the following command:

```bash
git clone https://github.com/kryptobaseddev/JiggleWiggle.git
cd JiggleWiggle
```

---

### Step 2: Create and Activate a Virtual Environment

Create a virtual environment in the project directory to isolate your project dependencies:

```bash
# On Windows:
python -m venv venv
.\venv\Scripts\activate

# On macOS/Linux:
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

Install the required packages by running:

```bash
pip install -r requirements.txt
```

---

## 2. Compiling the App into an `.exe`

To compile the app into a standalone .exe file for distribution, follow these steps:

### Step 1: Install PyInstaller

If you don’t have PyInstaller installed, install it by running:

```bash
pip install pyinstaller
```

### Step 2: Compile the App

Use PyInstaller to package the app:

```bash
pyinstaller --onefile --windowed --icon=assets/icon.ico app.py
```


`--onefile`: Combines everything into a single `.exe` file.
`--windowed`: Prevents the console window from appearing when the app runs.
`--icon`: Uses the specified icon for the `.exe`.
After compilation, the .exe will be located in the `dist/` folder.

### Step 3: Verify the Compilation

Navigate to the `dist/` folder and run the newly created `.exe` to ensure it works as expected.

---

## 3. Updating the Version and Changelog

Before each new release, it's essential to update both the version.txt file and CHANGELOG.md.

Here’s how to continue using it to maintain your changelog effectively:

### 1. **Commit Changes Regularly with Conventional Commit Messages**

Make sure to follow conventional commit message formats, as mentioned earlier. Here are a few examples:

- For a new feature:

     ```bash
     git commit -m "feat(gui): added settings panel for advanced options"
     ```

- For fixing a bug:

    ```bash
     git commit -m "fix(jiggler): resolve delay issue in mouse movement"
     ```

### 2. **Generate the Changelog After Committing Changes**

After making several commits, run `git-changelog` again to update your `CHANGELOG.md` file.

   ```bash
   git-changelog
   ```

   The `<!-- insertion marker -->` ensures that each time you run the command, new changes are added under the **Unreleased** section.

### 3. **Update the Version in `version.txt`**

Before releasing a new version:

- Manually update the `version.txt` file with the new version (e.g., `1.1.0`).
- Add and commit the version change:

     ```bash
     echo "1.1.0" > version.txt
     git add version.txt
     git commit -m "chore(release): bump version to 1.1.0"
     ```

### 4. **Move Changes from "Unreleased" to the New Version Section**

Once you are ready to release, move the items under **Unreleased** to a new section named after the new version (e.g., `## [1.1.0]`).

   Example:

   ```markdown
   ## [1.1.0] - 2024-10-10

   ### Added
   - Added settings panel for advanced options ([commit-hash](link))

   ## Unreleased
   ```

   This makes it clear what changes have been included in each version.

### 5. **Tag the New Release in Git**

After finalizing your changes and updating the changelog, create a Git tag for the new version:

   ```bash
   git tag v1.1.0
   git push --tags
   ```

### 6. **Push the Updated Changelog**

Commit and push your updated `CHANGELOG.md` file along with other files:

   ```bash
   git add CHANGELOG.md
   git commit -m "chore: update changelog for v1.1.0"
   git push origin main
   ```

### **Automating the Process (Optional)**

If you want to automate the process of moving changes from **Unreleased** to a new version section when releasing, you could create a small script to:

1. Run `git-changelog`.
2. Update the `version.txt`.
3. Tag the release and commit the changelog.

### Step 3: Commit and Push Changes

After updating the version.txt and CHANGELOG.md, commit and push your changes:

```bash
git add version.txt CHANGELOG.md
git commit -m "Bumped version to X.X.X and updated changelog"
git push origin main
```

---

## 4. Releasing the `.exe`

Once you've compiled a new `.exe`, upload it to your GitHub repository under a new release.

### Step 1: Create a New Release

1. Go to your repository on GitHub.
2. Click on Releases and then Draft a new release.
3. Tag the release with the updated version number (e.g., v1.0.1).
4. Upload the compiled .exe from the dist/ folder.
5. Add release notes summarizing the changes (copy from the CHANGELOG.md).

---

## 5. Testing Update Feature

Once the new release is live on GitHub:

- Make sure the app can check for updates by running the existing version.
- The app should notify you of the new version (based on the update logic in updater.py).
- Test the "Download Update" button to ensure it links to the latest .exe on GitHub.

---
