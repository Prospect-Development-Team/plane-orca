# Changelog

## [1.2.0-plane.1.3.1](https://github.com/Prospect-Development-Team/plane-orca/compare/v1.1.0-plane.1.3.1...v1.2.0-plane.1.3.1) (2026-07-22)


### ✨ Features

* **orca:** add cycle auto-complete configuration to project settings and database models ([780232e](https://github.com/Prospect-Development-Team/plane-orca/commit/780232e1dc9603e8c2cbfab86c40e5d7b37d68f2))
* **orca:** add detailed error logging for API request failures and exceptions in migration script ([a2da0c9](https://github.com/Prospect-Development-Team/plane-orca/commit/a2da0c964948dd16fbfdb5dec14785af06e38606))


### 🔧 Chores & Maintenance

* **orca:** add global HTTP 429 retry logic and support for syncing/updating existing projects during migration ([414ac5c](https://github.com/Prospect-Development-Team/plane-orca/commit/414ac5c70d18ba96fc499bfff0987690b7ee5aa1))
* **orca:** set pull_policy to always for all services in docker-compose-orca.yml ([b6d3504](https://github.com/Prospect-Development-Team/plane-orca/commit/b6d350407289003bc1fbe8fba684e32fb20a40d4))

## [1.1.0-plane.1.3.1](https://github.com/Prospect-Development-Team/plane-orca/compare/v1.0.0-plane.1.3.1...v1.1.0-plane.1.3.1) (2026-07-20)


### ✨ Features

* **orca:** add migration tools to sync projects, issues, and users from Plane to Plane Orca ([5b36f6a](https://github.com/Prospect-Development-Team/plane-orca/commit/5b36f6a99a42351f0b6514749111adc3cb768cc4))


### 🐛 Bug Fixes

* **orca:** prevent hydration mismatch by delaying theme-dependent UI rendering until component mount ([ca51a2a](https://github.com/Prospect-Development-Team/plane-orca/commit/ca51a2a11a7e19bff1f6939ee49a5e91e3e1a5eb))


### ♻️ Refactoring

* **orca:** implement project estimate synchronization and optimize API requests using persistent session connection pooling ([54a5607](https://github.com/Prospect-Development-Team/plane-orca/commit/54a56074d4b2f1d1d711fb71f51d4cb090d5cf75))
* **orca:** improve project, label, cycle, and module migration logic with better error handling and duplication checks ([1d08e5d](https://github.com/Prospect-Development-Team/plane-orca/commit/1d08e5dfffea71d1cf67c9b9ede21c3e7bc0faf1))
* **orca:** replace asset migration with generic pagination handling and workspace wiping capabilities ([09b5487](https://github.com/Prospect-Development-Team/plane-orca/commit/09b5487d667a4f1efad83e62ba77aa05e9183eb0))


### 🔧 Chores & Maintenance

* **orca:** clean up duplicate entries in CHANGELOG.md ([582fae8](https://github.com/Prospect-Development-Team/plane-orca/commit/582fae881a9f4a4dc91acbe88f64364c4a2ca45b))
* **orca:** enable visibility for test, ci, and build in release-please changelog ([5c28123](https://github.com/Prospect-Development-Team/plane-orca/commit/5c28123f062e522ace204dfa2427a06c48e6c833))
* **orca:** ensure required release labels exist in labeler workflow ([403118c](https://github.com/Prospect-Development-Team/plane-orca/commit/403118c2ed87a7b879a753455474e323fab9585e))
* **orca:** restrict labeler workflow to prod/stage branches and secure package version retrieval ([9b31b2b](https://github.com/Prospect-Development-Team/plane-orca/commit/9b31b2b55a9fa78a5946e5f43543026ea7d03bc0))
* **orca:** skip labeler workflow for release-please and bot-initiated pull requests ([8a47f12](https://github.com/Prospect-Development-Team/plane-orca/commit/8a47f1220caf3edaa35dcb1a9d7267a270563342))
* **orca:** sync prod back to stage [skip ci] ([6a41de4](https://github.com/Prospect-Development-Team/plane-orca/commit/6a41de42d60169b9d3a716440155532c4552c451))
* **orca:** update commit prefixes to standard conventional commit format in documentation ([159ba35](https://github.com/Prospect-Development-Team/plane-orca/commit/159ba3505986f74aade18a731dc0a446ede42bdc))
* **orca:** update release candidate PR template and refine automation title formatting ([80a1067](https://github.com/Prospect-Development-Team/plane-orca/commit/80a1067b933d009a1f003fa42d19a101db38f320))
* **orca:** update templates to use scoped conventional commit naming ([b1316d0](https://github.com/Prospect-Development-Team/plane-orca/commit/b1316d073038254facbfb8bf2d0c5edac691b9cb))

## [1.0.0-plane.1.3.1](https://github.com/Prospect-Development-Team/plane-orca/compare/v0.0.0-plane.1.3.1...v1.0.0-plane.1.3.1) (2026-07-18)

### Features (Orca)

- add bulk operations and enhance multi-value dropdown displays ([c9bb42f](https://github.com/Prospect-Development-Team/plane-orca/commit/c9bb42f15b264a87190f0a7ec3bb8dde07cc13a1))
- add Coolify-compatible docker-compose orchestration and deployment documentation ([fc357e2](https://github.com/Prospect-Development-Team/plane-orca/commit/fc357e2d773009256414af5b67561ceb28fbbc7e))
- add copy issue details submenu with options to copy title, description, and both ([1eb5ada](https://github.com/Prospect-Development-Team/plane-orca/commit/1eb5ada23e7bda5a6196e72d43981796527659f1))
- add functionality to manually start and end cycles with dynamic status support ([3265153](https://github.com/Prospect-Development-Team/plane-orca/commit/32651539ed4ccf3a4eb86adb0b1dc9585f50c307))
- add PDT logo and update edition badge component ([99d53f3](https://github.com/Prospect-Development-Team/plane-orca/commit/99d53f392e5039866108bb74e51ffadf5e807d50))
- allow editing completed cycles and fix active status reversion on edit ([e9a9802](https://github.com/Prospect-Development-Team/plane-orca/commit/e9a980224968e3cac1c28ce6b0a88bb95ec2546b))
- document active parallel cycles exclusion and getters ([4561148](https://github.com/Prospect-Development-Team/plane-orca/commit/456114859173b3d45972a065c0f0e34191c58ac2))
- implement workspace-level project labels ([8b18a48](https://github.com/Prospect-Development-Team/plane-orca/commit/8b18a489d30c7f7ad6aea801f3734032f9b30efd))
- implement workspace-level project states ([9e95dd0](https://github.com/Prospect-Development-Team/plane-orca/commit/9e95dd0f745d3f9b1e9062be58b879acda138455))
- include active cycles in transfer modal and update cycle status visualization ([3ace9f9](https://github.com/Prospect-Development-Team/plane-orca/commit/3ace9f9b13d13223f277a0f3363edf8c3490782f))
- introduce parallel cycles project configuration with custom settings model and migration ([0f569ad](https://github.com/Prospect-Development-Team/plane-orca/commit/0f569adaf902dd415ae2e2bac7c387a4bc012e87))
- persist form values when create-more is toggled in issue and inbox modals ([92dba66](https://github.com/Prospect-Development-Team/plane-orca/commit/92dba661058456219b63aa3487ef99cc78e3d9fd))

### Bug Fixes (Orca)

- add WEB_URL configuration to core services in docker-compose-orca.yml ([7fedf09](https://github.com/Prospect-Development-Team/plane-orca/commit/7fedf090070b06502f1677c8d2583f225dc7e2cc))
- disable default state display in bulk operation issue action bar ([146ad91](https://github.com/Prospect-Development-Team/plane-orca/commit/146ad9170677e76ed47dee8bb52e532c610c3665))
- project onboarding internationalize project feature toggle toasts and update submission handler logic ([e72f29b](https://github.com/Prospect-Development-Team/plane-orca/commit/e72f29ba6d00ee1753732bcc43a5371425057584))
- remove redundant WEB_URL fallback variable in docker-compose-orca.yml ([db97d0f](https://github.com/Prospect-Development-Team/plane-orca/commit/db97d0fb38833bca54faa46cf696170961af52fb))
- update SITE_ADDRESS configuration to use default port 80 explicitly ([9f77538](https://github.com/Prospect-Development-Team/plane-orca/commit/9f775383048c8cadae350cadc51d93dc30cb6073))

### Styles (Orca)

- center edition badge and update font weight in workspace component ([3fd0079](https://github.com/Prospect-Development-Team/plane-orca/commit/3fd00797c8298c116e78e5e9e7aed70186c3a53f))

### Documentation (Orca)

- add design cohesion guidelines to AGENTS.md and FORK.md for consistent component and style usage ([fb7b610](https://github.com/Prospect-Development-Team/plane-orca/commit/fb7b610d6f1b4c41cdbd41ab20b24a698f99358b))
- add fork customization guide and update agent coding standards for upstream compatibility ([8774057](https://github.com/Prospect-Development-Team/plane-orca/commit/877405728b44b430ee7ec83d526567c4e243897f))
- clarify guidelines for linting suppressions and root cause resolution in AGENTS.md ([ac87ee7](https://github.com/Prospect-Development-Team/plane-orca/commit/ac87ee75149261e8394aef848a5f5ccd9119620c))
- document agent token efficiency guidelines ([bbb9f99](https://github.com/Prospect-Development-Team/plane-orca/commit/bbb9f999db30f077f38cada343c69c4b2c3303f0))
- document bulk operations store methods and multi-value display dropdowns ([6dbcc28](https://github.com/Prospect-Development-Team/plane-orca/commit/6dbcc288ebb619531cfc73e54d395f77400c90f3))
- document copy issue title and description quick-action handlers ([fb93799](https://github.com/Prospect-Development-Team/plane-orca/commit/fb937994f13026ae5dbac05ef327374daf2b94e1))
- document create-more toggle form values preservation ([57bd326](https://github.com/Prospect-Development-Team/plane-orca/commit/57bd326a2e3adf7047c002f7553b3154176201d6))
- document disabled telemetry settings overrides ([019e165](https://github.com/Prospect-Development-Team/plane-orca/commit/019e16545bc0a438243cf1f915f45281f222611a))
- document parallel cycles override logic and store getters ([b59febb](https://github.com/Prospect-Development-Team/plane-orca/commit/b59febb9a5506cd7f41a81d8a7cebc36af93941a))
- format Conventional Commit prefixes as a table in fork guide ([e8ce54e](https://github.com/Prospect-Development-Team/plane-orca/commit/e8ce54e67b371ab0375ee3daec6958e48315478b))
- update agent contribution guidelines to mandate documentation standards and restrict heavy local command execution ([8a6a4ff](https://github.com/Prospect-Development-Team/plane-orca/commit/8a6a4ff74e6bf1c86a08000d0a810e8472bbea01))
- update commit prefix formatting and release-please mapping in fork guide ([4e3bf67](https://github.com/Prospect-Development-Team/plane-orca/commit/4e3bf675c87fc8aaf495405423dd1f1aa41e582e))
- update database migration instructions to include makemigrations step ([03ebcc9](https://github.com/Prospect-Development-Team/plane-orca/commit/03ebcc9afab3f7dd35f748a1052f4a5b2f0ce9a3))
- update pull request template and Git workflow documentation to reflect automated CI/CD processes ([11a6cf2](https://github.com/Prospect-Development-Team/plane-orca/commit/11a6cf25c9f883e98a688a8e815db730f7cc5792))

### Chores (Orca)

- add code_changes filter to stage workflow to refine CI trigger conditions ([1f54fc5](https://github.com/Prospect-Development-Team/plane-orca/commit/1f54fc5acd39b4b2001f99b194cd0a00657a8d94))
- add healthcheck configurations to service containers and disable migrator healthcheck in docker-compose ([1e0468d](https://github.com/Prospect-Development-Team/plane-orca/commit/1e0468dababd93458cd63f013b26c0b680d612af))
- add package.json alias to vite configurations in admin and web apps ([6c27252](https://github.com/Prospect-Development-Team/plane-orca/commit/6c2725259f63b9ebc285f22fd3fce9ae0ab07442))
- automate Release PR title/description templates and add warnings to default template ([1598f93](https://github.com/Prospect-Development-Team/plane-orca/commit/1598f93473e67b82f465b6e18f3d206b764ae6a2))
- change release-please trigger branch to prod ([5bbb17c](https://github.com/Prospect-Development-Team/plane-orca/commit/5bbb17c72eae1d4a9c37d2220e144ea004a779e7))
- configure release automation and versioning for Orca ([8aaef8e](https://github.com/Prospect-Development-Team/plane-orca/commit/8aaef8e0f90f002335363275cc93e330b4d1cd7e))
- disable go module caching in copyright-check workflow ([07d1fa7](https://github.com/Prospect-Development-Team/plane-orca/commit/07d1fa7656a0171c4eed7b67e9008a99cb00b76d))
- downgrade checkout action to v6 and update pnpm/node setup versions in workflows ([56b59b8](https://github.com/Prospect-Development-Team/plane-orca/commit/56b59b85c4f941179191077b0c72601109f14cad))
- expose proxy container port internally instead of binding to host port ([41b49ac](https://github.com/Prospect-Development-Team/plane-orca/commit/41b49aca8ceb6c871a9de214be627b1b7075baf5))
- implement matrix-based docker builds for stage workflow and enforce lowercase image naming for prod and stage ([3c7900d](https://github.com/Prospect-Development-Team/plane-orca/commit/3c7900d752b88cf8bc884f6848439d24f9d50ba7))
- implement path-based change detection to skip unnecessary CI and deployment jobs ([fa40106](https://github.com/Prospect-Development-Team/plane-orca/commit/fa4010628adbdd1a413499379e7332db6388ad5b))
- implement pull request templates and automatic PR labeling workflow ([3cc8635](https://github.com/Prospect-Development-Team/plane-orca/commit/3cc86353d06df726c00f3de0edfcccf6a932ee69))
- implement release automation with Release Please and reorganize CI/CD workflows for the Orca fork ([fefb7fd](https://github.com/Prospect-Development-Team/plane-orca/commit/fefb7fd8f2ff2095bd35b700a470167fe2277baa))
- improve job and step naming for path-based change detection ([bfafaaf](https://github.com/Prospect-Development-Team/plane-orca/commit/bfafaafcc89b00102b04aad1e08d42632fd0a0bf))
- inject missing API_BASE_URL environment variable into live service container ([9009ea7](https://github.com/Prospect-Development-Team/plane-orca/commit/9009ea7a83390573051cbe38a2d71df4d115cd89))
- inject root workspace version into web and api containers at build time for consistent versioning ([a5fe728](https://github.com/Prospect-Development-Team/plane-orca/commit/a5fe728b4c48eed5b882ce8148fbef625806eeca))
- isolate concurrency groups dynamically using github.ref in workflows ([8997ffe](https://github.com/Prospect-Development-Team/plane-orca/commit/8997ffea4307d19f208651109be64952ebbd3a4f))
- load template dynamically for all PRs and simplify default template ([f447768](https://github.com/Prospect-Development-Team/plane-orca/commit/f4477683cd19fa17ef10be9d70372d4a5508977d))
- move matrix-based change checks from job to step level in stage workflow ([a08ad00](https://github.com/Prospect-Development-Team/plane-orca/commit/a08ad00bcc3f1817ea6720df82be83c068dd635d))
- prevent overwriting customized PR bodies during automated labeler updates ([b2d3ce5](https://github.com/Prospect-Development-Team/plane-orca/commit/b2d3ce5174d9fe5e6286710226ad551f7950407a))
- revert version display overrides for web and god mode ([8539292](https://github.com/Prospect-Development-Team/plane-orca/commit/853929255e9d601e5414b1ffc469d2a85b559c58))
- set default value for is_telemetry_enabled to False in instance model ([82fe212](https://github.com/Prospect-Development-Team/plane-orca/commit/82fe21219ae19e0dee5bbd9583edbc1aa733c21c))
- simplify and consolidate QA verification checklist in release candidate PR template ([f648c85](https://github.com/Prospect-Development-Team/plane-orca/commit/f648c850a6f5ac68edb98d1fe3882f7071248768))
- skip CI job on commits with no code changes ([51612bd](https://github.com/Prospect-Development-Team/plane-orca/commit/51612bd57529b87b4c41963d4a98eb95be7b7e8d))
- standardize environment variables and add default values in docker-compose configuration ([cbc77de](https://github.com/Prospect-Development-Team/plane-orca/commit/cbc77de9664d26196da29c93973d3d08f48513ee))
- tag and push production images with version from package.json in CI workflow ([57db74e](https://github.com/Prospect-Development-Team/plane-orca/commit/57db74ecce168841acc0f82902c1d4fbec47e4fc))
- update actions/checkout to version 7 in production workflow ([c111b2c](https://github.com/Prospect-Development-Team/plane-orca/commit/c111b2ccf7215418a0dc4392f9db3a1e93aad4ae))
- update docker-compose healthcheck configurations, environment variables, and workflow action versions ([f99abe6](https://github.com/Prospect-Development-Team/plane-orca/commit/f99abe6fc758d24b7793be6c4c7ba7126fc06810))
- update GitHub Actions versions and refine stage deployment trigger conditions ([51b0884](https://github.com/Prospect-Development-Team/plane-orca/commit/51b08842dd98cd276c4bd004535175e28eb4b7a8))
- update image registry paths to use lowercase organization name ([5f19a14](https://github.com/Prospect-Development-Team/plane-orca/commit/5f19a147f41ef3bf3e507a451197590ebe72f704))
- update package.json path alias in tsconfig to reference root directory ([b4e0c0a](https://github.com/Prospect-Development-Team/plane-orca/commit/b4e0c0a6473980c972fcca2a3a8f2ee6bb0fd355))
- update trigger branch to prod and add automated sync to stage workflow ([3d88104](https://github.com/Prospect-Development-Team/plane-orca/commit/3d8810423d5396892b0c17ac703a0cb1d711bff0))
- update versioning ([5ffc828](https://github.com/Prospect-Development-Team/plane-orca/commit/5ffc8281bae532ee0f72277e3ff590d9f9e7803c))
- update workflow names and restrict license check triggers to specific file extensions ([f2d9a89](https://github.com/Prospect-Development-Team/plane-orca/commit/f2d9a89be0511d66d05a18049a82bf01fcc421be))

### Code Refactoring (Orca)

- move global server configuration block to the top of Caddyfile.ce ([866754f](https://github.com/Prospect-Development-Team/plane-orca/commit/866754f5d6358b1e6f0e17df1bbfa6bbb467fcf0))
- remove promotional links, telemetry defaults, and unused UI components across the application ([dcec1a3](https://github.com/Prospect-Development-Team/plane-orca/commit/dcec1a39b38207467262de4c07ee9ffade99cd30))
- standardize environment variable naming for database, message queue, and minio configurations ([6657e61](https://github.com/Prospect-Development-Team/plane-orca/commit/6657e610582f471898e2ea6d66f8ef0a67be0bf4))
- update Coolify configuration to require manual secret generation and use standard FQDN environment variables ([2513420](https://github.com/Prospect-Development-Team/plane-orca/commit/2513420bf90bc24ea2b9f9be78a7d10eed4a9cf0))
- update docker-compose environment variables to use standardized service-specific configuration naming conventions ([5a6d88f](https://github.com/Prospect-Development-Team/plane-orca/commit/5a6d88f26657419da3f1fc4c8bebbd4e1c0c91a6))
- update secret environment variable references to remove \_SECRET suffix ([2253160](https://github.com/Prospect-Development-Team/plane-orca/commit/2253160047a09b1f142f871af1b4cb66744f029c))
- update stage workflow to use pnpm scripts for formatting and linting ([e533145](https://github.com/Prospect-Development-Team/plane-orca/commit/e533145de23b4fc798276c7160f31dfb023eb076))
