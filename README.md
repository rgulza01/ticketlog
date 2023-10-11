# ticketlog

### Planning database:
<img width="1280" alt="image" src="https://github.com/rgulza01/ticketlog/assets/56838325/96180406-9ca6-430c-9204-7d18e479b3cb">

### Planning user stories:
<img width="1064" alt="image" src="https://github.com/rgulza01/ticketlog/assets/56838325/a8b7f2cd-01e1-4cb0-8fed-ce79279b5cec">

### Feature branching workflow
The key aspects of a feature branching workflow:

- Each new user story/feature is implemented on its own feature branch, branched off of the main development branch.
- Feature branches are usually named after the feature identifier or user story number, e.g. feature/breakdown-ticket.
- Once the feature is complete on the branch, it is merged back into the main development branch for integration testing.
- The main development branch (often called 'develop') contains all completed features integrated together.
- After sufficient testing on the development branch, it is merged into the production ('main') branch and deployed.
- This keeps development isolated on branches and main branches stable.
- The relatively short-lived feature branches help minimize merge conflicts.
- Well suited for continuous integration and deployment environments.
