# Resume Maker Pro

Windows 11 desktop resume builder. Includes 100 selectable combinations (10 design families × 10 color themes), English/Hindi labels, local resume saving, heuristic ATS readiness checks, live preview, PDF and DOCX export.

## Run locally
1. Install Python 3.11+ from python.org (only if running from source).
2. Open this folder in Command Prompt.
3. Run `pip install -r requirements.txt`
4. Run `python app.py`

## Build Windows EXE on GitHub (no local Python required)
1. Create a new GitHub repository.
2. Upload all files and folders from this project, including `.github/workflows/build-windows.yml`.
3. Open the repository's **Actions** tab.
4. Select **Build Resume Maker Pro Windows EXE** and click **Run workflow**, or push to `main`.
5. Open the completed workflow run, scroll to **Artifacts**, and download `ResumeMakerPro-Windows`.
6. Extract the ZIP and run `ResumeMakerPro.exe`.

## Data and privacy
Resume data is saved locally at `%USERPROFILE%\\ResumeMakerPro\\resumes.json`. It is not uploaded to a server.

## Important notes
- The ATS checker is a local checklist-based estimate, not a guarantee of passing any employer's ATS.
- Smart suggestions are rule-based and work offline. No external AI model or API is included; genuine generative AI requires a local model or an external service.
- 100 templates are currently represented by selectable design-family/color combinations. This starter version exports a clean ATS-friendly layout; additional visual layouts can be added in future versions.
