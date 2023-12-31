# ticketlog

### Planning database:
<img width="1280" alt="image" src="https://github.com/rgulza01/ticketlog/assets/56838325/96180406-9ca6-430c-9204-7d18e479b3cb">

### Planning user stories:
<img width="1114" alt="image" src="https://github.com/rgulza01/ticketlog/assets/56838325/0bf089df-e059-4ab4-af8f-2e6aa9722f56">

### Feature branching workflow
The key aspects of a feature branching workflow:

- Each new user story/feature is implemented on its own feature branch, branched off of the main development branch.
- Feature branches are usually named after the feature identifier or user story number, e.g. feature/breakdown-ticket.
- Once the feature is complete on the branch, it is merged back into the main development branch for integration testing.
- After sufficient testing on the development branch, it is merged into the production ('main') branch and deployed.
- This keeps development isolated on branches and main branches stable.
I have isolated the changes by creating multiple feature branches (feature/assign-ticket, feature/breakdown-ticket, feature/check-ticket-status, feature/close-ticket, feature/service-station, feature/ticket-cancellation, feature/ticket-confirmation) and a tests branch. I’ve tested my changes in the tests branch and then merged them into main while keeping the README.md in main unchanged.
