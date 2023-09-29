# ticketlog

### Planning database:
<img width="729" alt="image" src="https://github.com/rgulza01/ticketlog/assets/56838325/0956f1c7-5537-46fd-b49d-999241fe77d8">

In this schema:

- The User Table contains user information and serves as the parent table.
- The Vehicle Table is related to the User Table through the UserID field. This relationship connects each vehicle to a specific user. It's a one-to-many relationship, indicating that one user can have multiple vehicles, but each vehicle belongs to only one user.
- The ServiceTicket Table is related to the User Table through the UserID field. This relationship connects each service ticket to a specific user. Again, it's a one-to-many relationship, meaning one user can log multiple service tickets, but each ticket belongs to only one user.

### Planning user stories:
<img width="1099" alt="image" src="https://github.com/rgulza01/ticketlog/assets/56838325/88f93cf0-52fd-4292-bb14-f542347e7a95">

### Feature branching workflow
The key aspects of a feature branching workflow:

- Each new user story/feature is implemented on its own feature branch, branched off of the main development branch.
- Feature branches are usually named after the feature identifier or user story number, e.g. feature/authentication or story/456.
- Once the feature is complete on the branch, it is merged back into the main development branch for integration testing.
- The main development branch (often called 'develop') contains all completed features integrated together.
- After sufficient testing on the development branch, it is merged into the production ('main') branch and deployed.
- This keeps development isolated on branches and main branches stable.
- The relatively short-lived feature branches help minimize merge conflicts.
- Well suited for continuous integration and deployment environments.

  
