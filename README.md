# 🐋 Plane Orca (Custom Fork)

> [!IMPORTANT]
> **Plane Orca** is our customized team fork of upstream [Plane Community Edition](https://github.com/makeplane/plane).

### ✨ Fork Features

Plane Orca enhances official Plane Community Edition with extended workflow capabilities, automations, and streamlined self-hosting:

| Category               | Feature                            | Description                                                                                                                                              |
| :--------------------- | :--------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **🔄 Parallel Cycles** | Multi-Active Cycles                | Run multiple active cycles simultaneously in a single project with manual start, pause, and complete controls.                                           |
|                        | Auto-Complete & Transfer           | Automatically finish cycles on their end date and easily transfer unfinished work items between cycles.                                                  |
| **🏷️ Global Taxonomy** | Shared Workspace Labels & States   | Create and maintain standardized issue states and labels at the workspace level across all team projects.                                                |
| **⚡ Automations**     | Conventional Commits Auto-Labeling | Automatically assigns conventional labels (`feat`, `fix`, `docs`, `refactor`, `chore`, etc.) based on title prefixes, with on-activation backfill.       |
| **🚀 Productivity**    | Quick Copy Details                 | Copy work item title and clean, single-spaced formatted description from context menus in one action.                                                    |
|                        | Form Value Retention               | Preserves user input across creation forms when using "Create More".                                                                                     |
|                        | Enhanced Bulk Operations           | Multi-select and update work item properties with clear, streamlined multi-value dropdowns.                                                              |
| **🛠️ Data Migration**  | Plane-to-Plane Migration Tool      | Built-in CLI migration utility ([tools/migration](./tools/migration/README.md)) to migrate issues, cycles, labels, and projects between Plane instances. |
| **🎨 UI & Privacy**    | Clean & Distraction-Free UI        | Removed telemetry trackers and promotional ads for a faster, clutter-free workspace.                                                                     |
| **🐳 Self-Hosting**    | VPS & Coolify Ready                | Optimized low-memory footprint stack ([docker-compose-orca.yml](./docker-compose-orca.yml)) running smoothly under 3GB RAM.                              |

### 🐳 Self-Hosted Deployment (`docker-compose-orca.yml`)

Plane Orca is pre-configured for self-hosting on low-spec VPS instances (<3GB RAM) and PaaS platforms like **Coolify** using [docker-compose-orca.yml](./docker-compose-orca.yml).

#### ⚡ Quick Start (Coolify)

1. **Create Application**: Add a new **Docker Compose** resource in Coolify pointing to this repository (`stage` or `prod` branch) with file path `docker-compose-orca.yml`.
2. **Assign Domain**: In **Domains**, route your URL (e.g. `https://plane.example.com`) to the **`proxy`** service on container port `80`.
3. **Configure Secrets & Deploy**: Add required secrets in **Environment Variables** and click **Deploy**.

> [!TIP]
> **Generate Secret Keys**: Run `openssl rand -hex 32` in your terminal to generate 64-character secret keys.

#### ⚙️ Configuration Variables

| Variable                                      | Required | Description                     | Default                                    |
| :-------------------------------------------- | :------: | :------------------------------ | :----------------------------------------- |
| `SECRET_KEY`                                  | **Yes**  | Django session cryptography key | _User-provided (64-char hex)_              |
| `LIVE_SERVER_SECRET_KEY`                      | **Yes**  | WebSocket encryption key        | _User-provided (64-char hex)_              |
| `DOMAIN_NAME`                                 |    No    | Public application domain       | Auto-resolved from `${SERVICE_FQDN_PROXY}` |
| `POSTGRES_USER` / `POSTGRES_PASSWORD`         |    No    | PostgreSQL credentials          | `plane` / `plane123`                       |
| `POSTGRES_DB`                                 |    No    | PostgreSQL database schema      | `plane`                                    |
| `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` |    No    | MinIO / S3 storage credentials  | `plane-access-key` / `plane-secret-key`    |
| `AWS_S3_BUCKET_NAME`                          |    No    | File upload storage bucket      | `uploads`                                  |

### 🚀 Fork Workflow & Git Strategy

| Branch      | Purpose                                                                                             | Source Branch          | Merge Target       | Environment                       |
| :---------- | :-------------------------------------------------------------------------------------------------- | :--------------------- | :----------------- | :-------------------------------- |
| `upstream`  | **Upstream Mirror**: Tracks unmodified official Plane CE releases (`master` branch).                | _None (upstream sync)_ | _None (read-only)_ | N/A                               |
| `stage`     | **Staging/Integration**: Custom features, branding, and configs are integrated here.                | `stage`                | `stage`            | Staging / QA                      |
| `prod`      | **Production Releases**: Deployed directly to our self-hosted Plane instance for team-internal use. | `stage`                | `prod`             | Production (Internal Self-Hosted) |
| `feature/*` | **Feature Development**: Working branches for custom tasks and fixes.                               | `stage`                | `stage`            | Local Dev / Preview               |

- **Development Rules**: Please read and follow [FORK.md](./FORK.md) and [AGENTS.md](./AGENTS.md) closely.
  - Use the conventional commit format: `feat(orca):`, `fix(orca):`, `style(orca-ui):`, `style(orca):`, `docs(orca):`, `chore(orca):`, or `refactor(orca):`.
  - Do not edit database migration files or drop core tables directly.
  - All files must adhere to standard monorepo styling rules and preserve existing license headers.

---

<br /><br />

<p align="center">
<a href="https://plane.so">
  <img src="https://media.docs.plane.so/logo/plane_github_readme.png" alt="Plane Logo" width="400">
</a>
</p>
<p align="center"><b>Modern project management for all teams</b></p>

<p align="center">
    <a href="https://plane.so/"><b>Website</b></a> •
    <a href="https://forum.plane.so"><b>Forum</b></a> •
    <a href="https://x.com/planepowers"><b>X</b></a> •
    <a href="https://docs.plane.so/"><b>Documentation</b></a>
</p>

<p>
    <a href="https://app.plane.so/#gh-light-mode-only" target="_blank">
      <img
        src="https://media.docs.plane.so/GitHub-readme/github-top.webp"
        alt="Plane Screens"
        width="100%"
      />
    </a>
</p>

Meet [Plane](https://plane.so/), an open-source project management tool to track issues, run ~sprints~ cycles, and manage product roadmaps without the chaos of managing the tool itself. 🧘‍♀️

> Plane is evolving every day. Your suggestions, ideas, and reported bugs help us immensely. Do not hesitate to join in the conversation on [Forum](https://forum.plane.so) or raise a GitHub issue. We read everything and respond to most.

## 🚀 Installation

Getting started with Plane is simple. Choose the setup that works best for you:

- **Plane Cloud**
  Sign up for a free account on [Plane Cloud](https://app.plane.so)—it's the fastest way to get up and running without worrying about infrastructure.

- **Self-host Plane**
  Prefer full control over your data and infrastructure? Install and run Plane on your own servers. Follow our detailed [deployment guides](https://developers.plane.so/self-hosting/overview) to get started.

| Installation methods | Docs link                                                                                                                                                                               |
| -------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Docker               | [![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://developers.plane.so/self-hosting/methods/docker-compose)         |
| Kubernetes           | [![Kubernetes](https://img.shields.io/badge/kubernetes-%23326ce5.svg?style=for-the-badge&logo=kubernetes&logoColor=white)](https://developers.plane.so/self-hosting/methods/kubernetes) |
| Managed hosting      | [<img alt="Deploy with Zenith" src="https://cdn.zenith.hosting/buttons/deploy-with-zenith.svg" height="40">](https://zenith.hosting/host/plane)                                         |

`Instance admins` can configure instance settings with [God mode](https://developers.plane.so/self-hosting/govern/instance-admin).

## 🌟 Features

- **Work Items**
  Efficiently create and manage tasks with a robust rich text editor that supports file uploads. Enhance organization and tracking by adding sub-properties and referencing related issues.

- **Cycles**
  Maintain your team’s momentum with Cycles. Track progress effortlessly using burn-down charts and other insightful tools.

- **Modules**
  Simplify complex projects by dividing them into smaller, manageable modules.

- **Views**
  Customize your workflow by creating filters to display only the most relevant issues. Save and share these views with ease.

- **Pages**
  Capture and organize ideas using Plane Pages, complete with AI capabilities and a rich text editor. Format text, insert images, add hyperlinks, or convert your notes into actionable items.

- **Analytics**
  Access real-time insights across all your Plane data. Visualize trends, remove blockers, and keep your projects moving forward.

## 🛠️ Local development

See [CONTRIBUTING](./CONTRIBUTING.md)

## ⚙️ Built with

[![React Router](https://img.shields.io/badge/-React%20Router-CA4245?logo=react-router&style=for-the-badge&logoColor=white)](https://reactrouter.com/)
[![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)](https://www.djangoproject.com/)
[![Node JS](https://img.shields.io/badge/node.js-339933?style=for-the-badge&logo=Node.js&logoColor=white)](https://nodejs.org/en)

## 📸 Screenshots

  <p>
    <a href="https://plane.so" target="_blank">
      <img
        src="https://media.docs.plane.so/GitHub-readme/github-work-items.webp"
        alt="Plane Views"
        width="100%"
      />
    </a>
  </p>
  <p>
    <a href="https://plane.so" target="_blank">
      <img
        src="https://media.docs.plane.so/GitHub-readme/github-cycles.webp"
        width="100%"
      />
    </a>
  </p>
  <p>
    <a href="https://plane.so" target="_blank">
      <img
        src="https://media.docs.plane.so/GitHub-readme/github-modules.webp"
        alt="Plane Cycles and Modules"
        width="100%"
      />
    </a>
  </p>
  <p>
    <a href="https://plane.so" target="_blank">
      <img
        src="https://media.docs.plane.so/GitHub-readme/github-views.webp"
        alt="Plane Analytics"
        width="100%"
      />
    </a>
  </p>
   <p>
    <a href="https://plane.so" target="_blank">
      <img
        src="https://media.docs.plane.so/GitHub-readme/github-analytics.webp"
        alt="Plane Pages"
        width="100%"
      />
    </a>
  </p>
</p>

## 📝 Documentation

Explore Plane's [product documentation](https://docs.plane.so/) and [developer documentation](https://developers.plane.so/) to learn about features, setup, and usage.

## ❤️ Community

Join the Plane community on [GitHub Discussions](https://github.com/orgs/makeplane/discussions) and our [Forum](https://forum.plane.so). We follow a [Code of conduct](https://github.com/makeplane/plane/blob/master/CODE_OF_CONDUCT.md) in all our community channels.

Feel free to ask questions, report bugs, participate in discussions, share ideas, request features, or showcase your projects. We’d love to hear from you!

## 🛡️ Security

If you discover a security vulnerability in Plane, please report it responsibly instead of opening a public issue. We take all legitimate reports seriously and will investigate them promptly. See [Security policy](https://github.com/makeplane/plane/blob/master/SECURITY.md) for more info.

To disclose any security issues, please email us at security@plane.so.

## 🤝 Contributing

There are many ways you can contribute to Plane:

- Report [bugs](https://github.com/makeplane/plane/issues/new?assignees=srinivaspendem%2Cpushya22&labels=%F0%9F%90%9Bbug&projects=&template=--bug-report.yaml&title=%5Bbug%5D%3A+) or submit [feature requests](https://github.com/makeplane/plane/issues/new?assignees=srinivaspendem%2Cpushya22&labels=%E2%9C%A8feature&projects=&template=--feature-request.yaml&title=%5Bfeature%5D%3A+).
- Review the [documentation](https://docs.plane.so/) and submit [pull requests](https://github.com/makeplane/docs) to improve it—whether it's fixing typos or adding new content.
- Talk or write about Plane or any other ecosystem integration and [let us know](https://forum.plane.so)!
- Show your support by upvoting [popular feature requests](https://github.com/makeplane/plane/issues).

Please read [CONTRIBUTING.md](https://github.com/makeplane/plane/blob/master/CONTRIBUTING.md) for details on the process for submitting pull requests to us.

### Repo activity

![Plane Repo Activity](https://repobeats.axiom.co/api/embed/2523c6ed2f77c082b7908c33e2ab208981d76c39.svg "Repobeats analytics image")

### We couldn't have done this without you.

<a href="https://github.com/makeplane/plane/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=makeplane/plane" />
</a>

## License

This project is licensed under the [GNU Affero General Public License v3.0](https://github.com/makeplane/plane/blob/master/LICENSE.txt).
