# 🤝 Contributing to AI Magic Invisibility Portal

First off — thank you for even *opening* this file. ✨ Whether you're fixing a typo, squashing a bug, or adding a whole new gesture, every contribution helps this portal get a little more magical. This guide will walk you through everything you need to start contributing with confidence.

---

## 📜 Table of Contents

1. [Code of Conduct](#-code-of-conduct)
2. [Ways to Contribute](#-ways-to-contribute)
3. [Project Setup](#️-project-setup)
4. [Project Structure](#-project-structure)
5. [Branch Naming Conventions](#-branch-naming-conventions)
6. [Commit Message Guidelines](#-commit-message-guidelines)
7. [Coding Standards](#-coding-standards)
8. [Reporting Issues](#-reporting-issues)
9. [Pull Request Workflow](#-pull-request-workflow)
10. [Contributor Checklist](#-contributor-checklist-before-you-submit)
11. [Getting Help](#-getting-help)

---

## 📖 Code of Conduct

This project doesn't yet have a dedicated `CODE_OF_CONDUCT.md`, but the expectation is simple:

> Be kind, be respectful, and assume good intent. 🌱

Harassment, discrimination, or disrespectful behavior of any kind will not be tolerated. If a formal Code of Conduct is added later, it will be linked here and will take precedence over this note.

---

## 💡 Ways to Contribute

You don't need to be a computer-vision wizard to help out. Contributions of *every* size are welcome:

| Type | Examples |
|------|----------|
| 🐛 **Bug fixes** | Portal glitches, gesture misfires, crashes |
| ✨ **Features** | New gestures, portal color themes, particle effects |
| 📝 **Documentation** | README fixes, tutorials, code comments |
| 🎨 **UI/UX polish** | Smoother portal animations, glow effects |
| 🧪 **Testing** | Manual test reports, edge-case discovery |
| 🌍 **Accessibility** | Improving detection under different lighting/hand types |

Check the [Issues tab](../../issues) for `good first issue` or `help wanted` labels if you're not sure where to start.

---

## ⚙️ Project Setup

### 1. Fork & Clone

```bash
# Fork the repo on GitHub first, then:
git clone https://github.com/YOUR_GITHUB_USERNAME/AI-Magic-Invisibility-Portal.git
cd AI-Magic-Invisibility-Portal
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it:

```bash
# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the App

```bash
python main.py
```

If your webcam feed opens and the portal follows your finger — you're all set! 🪄

---

## 📂 Project Structure

```
AI-Magic-Invisibility-Portal/
│
├── main.py                 # Entry point — runs the app loop
├── portal.py                # Portal rendering & positioning logic
├── gesture_recognizer.py    # MediaPipe-based hand gesture detection
├── requirements.txt          # Python dependencies
├── README.md
├── CONTRIBUTING.md           # You are here 📍
└── screenshots/              # Demo images
```

Keep new files organized within this structure — e.g., new gesture logic belongs in `gesture_recognizer.py`, not scattered across `main.py`.

---

## 🌿 Branch Naming Conventions

Create a new branch for every change — never commit directly to `main`.

```bash
git checkout -b <type>/<short-description>
```

| Type | Use For | Example |
|------|---------|---------|
| `feature/` | New functionality | `feature/portal-color-themes` |
| `fix/` | Bug fixes | `fix/gesture-detection-lag` |
| `docs/` | Documentation only | `docs/update-readme-controls` |
| `refactor/` | Code cleanup, no behavior change | `refactor/portal-class-cleanup` |
| `test/` | Adding/improving tests | `test/gesture-edge-cases` |

---

## ✍️ Commit Message Guidelines

Write clear, present-tense commit messages that explain **what** and **why**.

```
<type>: <short summary>

[optional longer description]
```

**Examples:**

```
feat: add peace-sign gesture to toggle portal visibility
fix: resolve portal flicker when hand leaves frame
docs: add gesture control table to README
refactor: extract distance calculation into helper function
```

**Types:** `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

🚫 Avoid vague messages like `update`, `fix stuff`, or `wip`.

---

## 🧑‍💻 Coding Standards

To keep the codebase consistent and readable:

- Follow **[PEP 8](https://peps.python.org/pep-0008/)** style conventions.
- Use descriptive variable and function names (`portal_radius`, not `pr`).
- Add docstrings to new functions/classes explaining their purpose.
- Keep functions focused — one responsibility per function.
- Avoid hardcoding values (e.g., colors, thresholds); use named constants where possible.
- Comment non-obvious logic, especially around MediaPipe landmark math.
- Test your changes manually with your webcam before submitting — this is a real-time vision app, so behavior matters more than it might appear in a code diff.
- Do not commit unrelated files (`venv/`, `__pycache__/`, personal screenshots, IDE configs).

---

## 🐞 Reporting Issues

Before opening a new issue:

1. **Search existing issues** to avoid duplicates.
2. If none exist, open a new one with:
   - A clear, descriptive title
   - Steps to reproduce (if it's a bug)
   - Expected vs. actual behavior
   - Screenshots/GIFs if visual (very helpful for a portal app! 👻)
   - Your OS, Python version, and webcam setup if relevant

If you'd like to work on an issue, **comment on it and wait to be assigned** before starting work — this avoids duplicate effort.

---

## 🔃 Pull Request Workflow

1. **Sync your fork** with the latest `main` branch.
2. **Create a branch** following the [naming convention](#-branch-naming-conventions) above.
3. **Make your changes**, committing in logical, well-described chunks.
4. **Test locally** — run `python main.py` and confirm nothing is broken.
5. **Push your branch:**
   ```bash
   git push origin <your-branch-name>
   ```
6. **Open a Pull Request** against the `main` branch with:
   - A descriptive title
   - A summary of what changed and why
   - Reference to the related issue (e.g., `Closes #6`)
   - Before/after screenshots or a short clip if the change is visual
7. **Respond to review feedback** — maintainers may request changes before merging.
8. Once approved, your PR will be merged. 🎉

---

## ✅ Contributor Checklist (Before You Submit)

- [ ] My branch follows the naming convention
- [ ] My commits follow the message guidelines
- [ ] I tested the app locally and it runs without errors
- [ ] I did not commit `venv/`, `__pycache__/`, or unrelated files
- [ ] My code follows PEP 8 and existing project style
- [ ] I added comments/docstrings where needed
- [ ] I updated the README/docs if my change affects usage
- [ ] My PR description clearly explains the change and links the related issue
- [ ] I've linked screenshots/clips for any visual changes

---

## 🙋 Getting Help

Stuck, confused, or just want to bounce an idea around? Open a [Discussion](../../discussions) or comment on the relevant issue — maintainers and fellow contributors are happy to help.

---

### 🌟 Thank You

Every PR, issue, and suggestion makes this portal a little more magical. We're excited to see what you build! 🪄✨