# How to Contribute

We welcome contributions from everyone. There are many ways to contribute, from writing tutorials or blog posts, improving the documentation, submitting bug reports and feature requests, or writing code which can be incorporated into the project itself.

## Table of Contents

- [Getting Started](#getting-started)
- [Issues Conventions](#issues-conventions)
- [Commit Messages convention](#commit-messages-convention)
- [Branching convention](#branching-convention)
- [Merging convention](#merging-convention)
- [Documentation](#documentation)

## Getting Started

You can contribute to this project by following the steps below:

- [You are a part of the linear organization](#you-are-a-part-of-the-linear-organization)
- [You aren't a part of the linear organization](#you-arent-a-part-of-the-linear-organization)

### You are a part of Github organization

1. On GitHub, create a new issue or pick an existing issue you want to work on.
2. Create a new branch from the `main` branch while naming it following the [branching convention](#branching-convention).
3. Work on the issue you picked.
4. Commit your changes following the [commit messages convention](#commit-messages-convention).
5. Push your changes to the remote repository.
6. Create a pull request to merge your branch into the `main` branch.
7. Wait for the code review and address the comments if needed.
8. Once the code review is approved, the pull request will be merged into the `main` branch.

### You aren't a part of the linear organization

1. Fork the repository.
2. Clone the forked repository to your local machine.
3. Create a new branch from the `main` branch while naming it following the [branching convention](#branching-convention).
4. Work on the issue you picked.
5. Commit your changes following the [commit messages convention](#commit-messages-convention).
6. Push your changes to your forked repository.
7. Create a pull request to merge your branch into the `main` branch of the original repository.
8. Wait for the code review and address the comments if needed.
9. Once the code review is approved, the pull request will be merged into the `main` branch.


## Issues Conventions

For each issue, we precise the following information:

- **Type**: The type of the issue (e.g., bug, feature, documentation, etc.).
- **Priority**: The priority of the issue (e.g., Low, Medium, High, Urgent).
- **Status**: The status of the issue (e.g., open, in progress, resolved, closed).
- **Assignee**: The person who is responsible for the issue.
- **Milestone**: The milestone the issue is associated with.
- **Size**: The size of the issue (e.g., XS, S, M, L, XL).

*Note : You can use the [Issue Templates](.github/ISSUE_TEMPLATE) to create new issues*

### Types

- **Bug**: A bug is a problem that prevents the software from working as expected.
- **Feature**: A feature is a new functionality that is added to the software.
- **Documentation**: Documentation is the information that describes the software.
- **Benchmark**: Benchmark is the process of comparing the performance of the software.
- **DevOps**: DevOps is the practice of combining software development and IT operations.
- **Imrovement**: Improvement is the process of making the software better.

### Priorities

- **Low**: Low priority issues are minor issues that do not affect the software.
- **Medium**: Medium priority issues are issues that affect the software but are not critical.
- **High**: High priority issues are critical issues that affect the software.
- **Urgent**: Urgent priority issues are critical issues that need to be fixed immediately.

### Sizes

- **XS**: Extra Small issues are minor issues that can be fixed quickly (between some minutes and an hour).
- **S**: Small issues are issues that can be fixed in a short amount of time (few hours).
- **M**: Medium issues are issues that require more time to fix (one day).
- **L**: Large issues are issues that require a significant amount of time to fix (few days).
- **XL**: Extra Large issues are issues that require a lot of time to fix (more than a week).

## Commit Messages convention

We use the GitMoji convention for our commit messages. Each commit message should start with an emoji, followed by a verb in the present tense, and a brief description of what was done. You will find the list of emojis we use and their meanings on the following [link](https://gitmoji.dev/).

### Sorting the gitmojis

|Action (related to)            | Gitmojis                                                                  |
|:------------------------------|:--------------------------------------------------------------------------|
|The code                       | 🎨, ⚡, 🐛, 🚑, ✨, 🚨, ♻️, 🔧, 👽,💡, 💬,👥, 🚸, 🏗️,🤡, 📸, 🏷️, 🥅, 🗑️  |
|Git / Version Control System   | 🎉, 🔖, ⏪, 🔀                                                            |
|The project strucure           | 🔥, 📝, 🚀, 🔒, 💚, 👷, 📈, ➕, ➖, 📦, 🚚, 📄, 🍱, 🙈                   |

### Translating the Angular convention

|Angular types 	| Possible Gitmoji(s)                   |
|:--------------|:--------------------------------------|
|feat           | ✨, ♿, 🚸, ...                       |
|fix            | 🐛                                    |
|docs           | 📝                                    |
|style          | 🚨, 🎨                                |
|refactor       | ♻️                                    |
|test           | ✅                                    |
|chore          | 🚚, 🔥, 📦, ⬇️, ⬆️, 👽, 📌, 🔖, ... |

### Examples of commit messages

✨ Add new feature to improve user experience
🐛 Fix crash in the game engine component
📝 Update benchmark documentation
🚨 Remove unused imports


## Branching convention

We use the following branching convention:

- `main`: The main branch, always stable and deployable. We use this branch for production releases.
- `develop`: The development branch, where we merge all feature branches. We use this branch for testing and pre-production releases.
- `feature/feature-name`: The feature branch, where we develop new features. We use this branch for developing new features.
- `fix/fix-name`: The fix branch, where we fix bugs. We use this branch for fixing bugs.

## Merging convention

We use the following merging convention:

- `main`: We merge the `develop` branch into the `main` branch when we are ready to release a new version.
- `develop`: We merge the feature branches into the `develop` branch when we are ready to test the new features.
- `feature/feature-name`: We merge the `feature/feature-name` branch into the `develop` branch when we finish developing the new feature.
- `fix/fix-name`: We merge the `fix/fix-name` branch into the `develop` branch when we finish fixing the bug.

## Documentation

All contributions should include documentation. You can find the documentation in the `docs` folder. Please update the documentation when you add new features or fix bugs. If you are not sure how to document your contribution, please ask for help.
