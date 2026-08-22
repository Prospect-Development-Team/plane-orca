# 🐋 Plane Orca (Custom Fork)

> [!IMPORTANT]
> **Plane Orca** is our customized team fork of upstream [Plane Community Edition](https://github.com/makeplane/plane).

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

### 📝 Custom Fork Changelog

All custom changes, new features, and bug fixes are automatically tracked and compiled by Release Please in [CHANGELOG.md](./CHANGELOG.md). Refer to it for the complete release history of this fork.

### ✨ What Makes Plane Orca Different? (Fork Features)

Plane Orca builds on top of official Plane Community Edition with extra features, workflow improvements, and simpler self-hosting:

#### 🔄 Parallel Cycles (Sprints)

- **Run Multiple Active Cycles**: Run more than one cycle at the same time in a single project.
- **Manual Cycle Controls**: Manually start, pause, complete, or edit active and finished cycles anytime.
- **Auto-Complete & Transfer**: Automatically finish cycles when their end date arrives, and easily transfer issues between active cycles.

#### 🏷️ Shared Workspace Labels & States

- **Global Workspace Labels**: Create issue labels at the workspace level so all projects share the same labels.
- **Global Workflow States**: Use standardized issue states (e.g., In Progress, Done) across all team projects.

#### ⚡ Productivity Quick Actions

- **Quick Copy Details**: Right-click or open the issue menu to copy work item details (title and description) in one smart action.
- **Form Value Retention**: Keeps what you typed in creation forms even if you toggle "Create More".
- **Enhanced Bulk Operations**: Select and edit multiple work items faster with clearer multi-value dropdowns.

#### 🛠️ Data Migration Tool

- **Import from Another Plane**: Built-in Python migration tool ([tools/migration](./tools/migration/README.md)) to copy projects, issues, cycles, users, and labels from another Plane instance.

#### 🎨 Clean & Distraction-Free UI

- **Custom Branding**: Cleaned up logos and edition badges.
- **No Promotional Ads**: Removed telemetry tracking and promotional popups for a faster, distraction-free interface.

#### 🐳 Simple Self-Hosting (Coolify Ready)

- **Low Memory Footprint**: Includes [docker-compose-orca.yml](./docker-compose-orca.yml), pre-configured to run smoothly on small VPS servers (<3GB RAM).
- **Automated CI/CD**: Seamless deployment to Coolify with auto-versioning and changelog tracking ([CHANGELOG.md](./CHANGELOG.md)).

### 🐳 Self-Hosted Deployment (docker-compose-orca.yml)

To deploy **Plane Orca** on your VPS via Coolify, we recommend using [docker-compose-orca.yml](./docker-compose-orca.yml).

#### 1. Why use `docker-compose-orca.yml`?

- **Pre-Built Images**: It references pre-compiled images from GHCR (e.g. `ghcr.io/.../web:stage`) built on GitHub's free Actions runners. Running a compile/build step directly on a 4GB VPS (which Next.js frontends require) will crash the server due to high compile-time RAM usage.
- **Resource Constraints**: It defines strict memory limits (`mem_limit`) for all containers, ensuring the entire 11-service stack stays safe and stable under 3GB of runtime memory.

#### 2. Environment Variables & Automated Routing

Most configuration variables are fully automated or pre-filled:

- **Automatic Domain Injection**: The compose file binds `DOMAIN_NAME` to `${SERVICE_FQDN_PROXY:-localhost}`. Coolify automatically generates this variable based on the domain you assign to the `proxy` service in the dashboard UI.
- **Required Secrets**: `SECRET_KEY` and `LIVE_SERVER_SECRET_KEY` must be manually generated and configured in Coolify's **Environment Variables** tab.
  - **Linux / macOS (Terminal)**:
    ```bash
    openssl rand -hex 32
    ```
  - **Windows (PowerShell)**:
    ```powershell
    -join ((0..63) | ForEach-Object { Get-Random -InputObject ('a'..'z' + 'A'..'Z' + '0'..'9') })
    ```

##### Customizable Variables

For convenience, database credentials, RabbitMQ settings, and local MinIO storage keys are **pre-filled with safe defaults**. If you wish to customize them (e.g. changing database credentials or pointing to an external S3 store like Cloudflare R2), define them in Coolify's **Environment Variables** tab:

| Variable                 | Description                               | Default                       |
| ------------------------ | ----------------------------------------- | ----------------------------- |
| `SECRET_KEY`             | Secure session cryptography key (django). | _User-provided (64-char key)_ |
| `LIVE_SERVER_SECRET_KEY` | Websockets server encryption key.         | _User-provided (64-char key)_ |
| `POSTGRES_USER`          | PostgreSQL database user.                 | `plane`                       |
| `POSTGRES_PASSWORD`      | PostgreSQL database password.             | `plane123`                    |
| `POSTGRES_DB`            | PostgreSQL database schema name.          | `plane`                       |
| `RABBITMQ_USER`          | RabbitMQ connection user.                 | `plane`                       |
| `RABBITMQ_PASSWORD`      | RabbitMQ connection password.             | `plane123`                    |
| `AWS_ACCESS_KEY_ID`      | Storage access key.                       | `plane-access-key`            |
| `AWS_SECRET_ACCESS_KEY`  | Storage secret key.                       | `plane-secret-key`            |
| `AWS_S3_BUCKET_NAME`     | Storage bucket name.                      | `uploads`                     |

#### 3. Coolify-Specific Deployment Steps

1. Create a new **Docker Compose** application resource in Coolify.
2. Select your repository, branch (`stage` or `prod`), and specify the file path as `docker-compose-orca.yml`.
3. Go to **Settings** -> **Domains** in Coolify, assign your domain (e.g., `https://plane.yourdomain.com`), and select the target service as `proxy` on port `80`.
4. **Proxy Note**: To avoid port collisions on the host, `docker-compose-orca.yml` binds the proxy container's HTTP port to a non-standard port (`8000` by default). Do not bind host ports `80` or `443` manually in the compose file; Coolify's Traefik/Caddy proxy automatically routes the external domain traffic directly to the `proxy` service on container port `80`.

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
