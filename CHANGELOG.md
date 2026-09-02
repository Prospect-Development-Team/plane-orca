# Changelog

## [1.4.1-plane.1.4.1](https://github.com/Prospect-Development-Team/plane-orca/compare/v1.4.0-plane.1.4.1...v1.4.1-plane.1.4.1) (2026-09-02)


### 🔧 Chores & Maintenance

* **orca:** include upstream version in sync PR title ([e4394ce](https://github.com/Prospect-Development-Team/plane-orca/commit/e4394cec5003699e7ff117c077de59e6dd6caf22))
* **orca:** sync upstream master v1.4.2 into stage ([0c7052b](https://github.com/Prospect-Development-Team/plane-orca/commit/0c7052b23cee363daaea39cf5196cebbd2d17f56))


### ⚙️ Continuous Integration

* **orca:** add automated workflow to sync upstream master and manage PRs to stage ([25db999](https://github.com/Prospect-Development-Team/plane-orca/commit/25db99971d535a375ceba90dfe80260f18cca016))
* **orca:** grant write permissions for contents and packages in production workflow ([1f624a8](https://github.com/Prospect-Development-Team/plane-orca/commit/1f624a8f76d3607eed7636353210665960678e60))
* **orca:** restrict stage docker builds and deployments to pushes only ([37a73f4](https://github.com/Prospect-Development-Team/plane-orca/commit/37a73f48be785b2b53ab368ea3d3c5c04f0bf5a8))
* **orca:** update sync PR title format to sync upstream &lt;version&gt; ([63339cb](https://github.com/Prospect-Development-Team/plane-orca/commit/63339cba98f5f54e80ce768101a58b733ab0b458))

## [1.4.0-plane.1.4.1](https://github.com/Prospect-Development-Team/plane-orca/compare/v1.3.0-plane.1.4.1...v1.4.0-plane.1.4.1) (2026-08-22)


### ✨ Features

* **orca:** add automated conventional commit label tagging based on issue title prefixes ([ceaba4d](https://github.com/Prospect-Development-Team/plane-orca/commit/ceaba4d804e9f0c55ac2d4746919c022a39bb032))


### 🐛 Bug Fixes

* **orca:** ensure soft-deleted labels are excluded from issue and draft queries and update serializer validation to use UUIDField ([b920dfb](https://github.com/Prospect-Development-Team/plane-orca/commit/b920dfb80196f66c425a017b0c0bdb2e59e98ccc))
* **orca:** improve intake issue error handling, fallback state resolution, and store exception propagation ([b2834e8](https://github.com/Prospect-Development-Team/plane-orca/commit/b2834e810736d55794969863f3c5053be3f8dcd7))


### 📝 Documentation

* **orca:** add conventional commits auto-labeling documentation and update quick copy details description ([52a561d](https://github.com/Prospect-Development-Team/plane-orca/commit/52a561d917c43f427ab3b7d152b027387f0f7cd2))
* **orca:** convert feature list in README.md to a table for improved readability ([b54705f](https://github.com/Prospect-Development-Team/plane-orca/commit/b54705fc4c84249a8abf899732bd08400c2dae3c))
* **orca:** streamline and condense README deployment and workflow documentation ([3aa9554](https://github.com/Prospect-Development-Team/plane-orca/commit/3aa955485dc9f1e7a366f0acd0442340926e812b))


### ♻️ Refactoring

* **orca:** default project features to disabled and implement workspace-level sync for new projects ([3ef3e18](https://github.com/Prospect-Development-Team/plane-orca/commit/3ef3e187e625e0d0825d25c877cc562d20d28c79))
* **orca:** replace sanitizeHTML with htmlToPlainText for Copy Details formatted issue description ([3be52b4](https://github.com/Prospect-Development-Team/plane-orca/commit/3be52b4e06e031d699ef2fd59e6f867a6b85a223))
* **orca:** simplify issue copy functionality by replacing the details submenu with a single smart copy action ([ca69f53](https://github.com/Prospect-Development-Team/plane-orca/commit/ca69f5380b14889445442e6bbb1ea90f16b8ad59))


### ⚙️ Continuous Integration

* **orca:** add versioned image tagging and update GitHub releases with container artifact details ([c66f3cb](https://github.com/Prospect-Development-Team/plane-orca/commit/c66f3cb3b06dd841c977567b569da0c29f6be21e))
* **orca:** disable concurrency cancellation in stage and prod workflows ([1e7e5f8](https://github.com/Prospect-Development-Team/plane-orca/commit/1e7e5f85de3ef66f87faa6d62bd12c10733076c8))
* **orca:** remove unused React Doctor and i18n sync check GitHub workflows ([502d2b7](https://github.com/Prospect-Development-Team/plane-orca/commit/502d2b79d75ef5720320836ee2dccd92cceba013))

## [1.3.0-plane.1.4.1](https://github.com/Prospect-Development-Team/plane-orca/compare/v1.2.0-plane.1.4.1...v1.3.0-plane.1.4.1) (2026-08-20)


### ✨ Features

* **api:** add lite list endpoints for projects, members, cycles, and modules ([#9410](https://github.com/Prospect-Development-Team/plane-orca/issues/9410)) ([7cef741](https://github.com/Prospect-Development-Team/plane-orca/commit/7cef741c29cf61d3bca18dc892e6af11a1e7becc))
* **api:** add workspace_slug to webhook delivery payload ([#9232](https://github.com/Prospect-Development-Team/plane-orca/issues/9232)) ([f2feca6](https://github.com/Prospect-Development-Team/plane-orca/commit/f2feca61e838b011d3bb51cf76ee3c03cacf3f54))
* **api:** enhance workspace module query to include member IDs ([#9541](https://github.com/Prospect-Development-Team/plane-orca/issues/9541)) ([a18177c](https://github.com/Prospect-Development-Team/plane-orca/commit/a18177ce5e01bff5f2d66b2345d7da5d8a20c4d5))
* **orca:** add cycle auto-complete configuration to project settings and database models ([780232e](https://github.com/Prospect-Development-Team/plane-orca/commit/780232e1dc9603e8c2cbfab86c40e5d7b37d68f2))
* **orca:** add detailed error logging for API request failures and exceptions in migration script ([a2da0c9](https://github.com/Prospect-Development-Team/plane-orca/commit/a2da0c964948dd16fbfdb5dec14785af06e38606))
* **orca:** add inline cycle creation support to CycleDropdown component ([31e623f](https://github.com/Prospect-Development-Team/plane-orca/commit/31e623fadd974d951776e3afa4a37a5039320b06))
* **orca:** add migration tools to sync projects, issues, and users from Plane to Plane Orca ([5b36f6a](https://github.com/Prospect-Development-Team/plane-orca/commit/5b36f6a99a42351f0b6514749111adc3cb768cc4))
* **orca:** add option to automatically move incomplete cycle issues to Completed state when ending a cycle ([f9c20d1](https://github.com/Prospect-Development-Team/plane-orca/commit/f9c20d149839ad41165712746f1b5edb1a47ac2c))
* **orca:** add optional move-to-in-progress state functionality for cycles upon start ([7b95441](https://github.com/Prospect-Development-Team/plane-orca/commit/7b954416029d8dbfdcffd51460ca2acf1671b65e))
* **orca:** sync upstream plane v1.4.1 release updates ([1856d2f](https://github.com/Prospect-Development-Team/plane-orca/commit/1856d2f91b1cba64f67f54b348c6a8dcd991e5de))
* **orca:** update issue creation to default assignees from user's previous project issue ([56e9d43](https://github.com/Prospect-Development-Team/plane-orca/commit/56e9d43baf9d0075e6bae9608f9393024a2942b7))


### 🐛 Bug Fixes

* Add docker pytest runner and fix bugs the suite surfaced ([#9138](https://github.com/Prospect-Development-Team/plane-orca/issues/9138)) ([9f77ea5](https://github.com/Prospect-Development-Team/plane-orca/commit/9f77ea5ebb033a3554fcb1e1509a769c3c6510b0))
* add model_activity.delay() to API issue update/create paths for webhook dispatch ([#8792](https://github.com/Prospect-Development-Team/plane-orca/issues/8792)) ([d94a269](https://github.com/Prospect-Development-Team/plane-orca/commit/d94a26945198a5f5a026420fe4ff6ac2acc7ba46))
* add WEBHOOK_ALLOWED_HOSTS allowlist for internal webhook targets ([#9078](https://github.com/Prospect-Development-Team/plane-orca/issues/9078)) ([761c999](https://github.com/Prospect-Development-Team/plane-orca/commit/761c999e0c2911132b23746a6c2c5225430cb216))
* added workspace member check in allow permission for creator [#8778](https://github.com/Prospect-Development-Team/plane-orca/issues/8778) ([9d3b5d9](https://github.com/Prospect-Development-Team/plane-orca/commit/9d3b5d9da7c2320cf6e60e2e17c85cadf68b7a78))
* **aio:** use JSON array double quotes in VOLUME instruction ([#9099](https://github.com/Prospect-Development-Team/plane-orca/issues/9099)) ([039d582](https://github.com/Prospect-Development-Team/plane-orca/commit/039d582fbb904ef0d1d3d6b6e1c9fef9696beb13))
* alpha colors ([#8418](https://github.com/Prospect-Development-Team/plane-orca/issues/8418)) ([7a3cebd](https://github.com/Prospect-Development-Team/plane-orca/commit/7a3cebdb6b62a3631631b0abf499217ca25642bf))
* **api:** enforce workspace membership on GenericAssetEndpoint ([#9212](https://github.com/Prospect-Development-Team/plane-orca/issues/9212)) ([9a30a07](https://github.com/Prospect-Development-Team/plane-orca/commit/9a30a07cf5e42a7a5434768ba34fe18840aff92c))
* **api:** pass project_lead_id (not User instance) when creating ProjectMember ([#8966](https://github.com/Prospect-Development-Team/plane-orca/issues/8966)) ([50a7b47](https://github.com/Prospect-Development-Team/plane-orca/commit/50a7b47b31d46b8525a680bc778b420802c14bce))
* **api:** rate-limit magic-code verify, bound per-token attempts (GHSA-9pvm-fcf6-9234) ([#9130](https://github.com/Prospect-Development-Team/plane-orca/issues/9130)) ([b1c78fe](https://github.com/Prospect-Development-Team/plane-orca/commit/b1c78fe4c832e188454840eb38fd20cd05ef8b0a))
* **api:** reject API key auth for deactivated user accounts ([#9225](https://github.com/Prospect-Development-Team/plane-orca/issues/9225)) ([fd16d03](https://github.com/Prospect-Development-Team/plane-orca/commit/fd16d033fccb37f18e8794df739c8c24ba9d7939))
* **api:** require at least one alphanumeric char in workspace name ([#9278](https://github.com/Prospect-Development-Team/plane-orca/issues/9278)) ([7b0704d](https://github.com/Prospect-Development-Team/plane-orca/commit/7b0704d9cc0fa7d5f16fc269705beffeb2496eb5))
* **api:** sanitize XLSX export cells to prevent formula injection ([#9224](https://github.com/Prospect-Development-Team/plane-orca/issues/9224)) ([2f7941a](https://github.com/Prospect-Development-Team/plane-orca/commit/2f7941a17c8bc2dd401ff08a6d6062653b0dc554))
* **api:** scope cross-workspace resource lookups to prevent IDOR ([#9008](https://github.com/Prospect-Development-Team/plane-orca/issues/9008)) ([9491bdb](https://github.com/Prospect-Development-Team/plane-orca/commit/9491bdbe46e269611f9dad9cfb5182c2da8ca65a))
* **api:** use requester's workspace role for project member role updates (GHSA-x63v-p7wc-47x4) ([#9014](https://github.com/Prospect-Development-Team/plane-orca/issues/9014)) ([4c1bdd1](https://github.com/Prospect-Development-Team/plane-orca/commit/4c1bdd1d625fa3f1141e8af9c15423946472069e))
* broken lockfile ([54b80e9](https://github.com/Prospect-Development-Team/plane-orca/commit/54b80e91eb600fd1628fb536d6173e57cb04ab2a))
* bump npm deps to resolve Dependabot advisories ([#9191](https://github.com/Prospect-Development-Team/plane-orca/issues/9191)) ([7ec8d49](https://github.com/Prospect-Development-Team/plane-orca/commit/7ec8d4990fc7929d54619dc462d5a0fe45282ff6))
* bump react-router and vitest to resolve Dependabot advisories ([#9215](https://github.com/Prospect-Development-Team/plane-orca/issues/9215)) ([0bbfe95](https://github.com/Prospect-Development-Team/plane-orca/commit/0bbfe95cc74c9c958d66b156df2783fdbc180f8e))
* cast avatar_asset to CharField to resolve mixed type errors in URL concatenation ([#9512](https://github.com/Prospect-Development-Team/plane-orca/issues/9512)) ([027a5a0](https://github.com/Prospect-Development-Team/plane-orca/commit/027a5a03300ce2cf0a72077701c7b47d88edd8e8))
* correct spelling error in database.ts log message ([#8452](https://github.com/Prospect-Development-Team/plane-orca/issues/8452)) ([a976bea](https://github.com/Prospect-Development-Team/plane-orca/commit/a976bea5afb24b4688142a3dd8a00c6de76bb390))
* **cover-image:** return absolute URLs for cover images ([18ea715](https://github.com/Prospect-Development-Team/plane-orca/commit/18ea715960b2697cf3980c493c44e894683c8f98))
* custom z-index classNames ([#8395](https://github.com/Prospect-Development-Team/plane-orca/issues/8395)) ([1e35145](https://github.com/Prospect-Development-Team/plane-orca/commit/1e3514575f1e5b02646aee84f7e53afa3a29e83b))
* declare @tailwindcss/postcss in admin/space/web for Docker builds ([#9189](https://github.com/Prospect-Development-Team/plane-orca/issues/9189)) ([e388cb9](https://github.com/Prospect-Development-Team/plane-orca/commit/e388cb9125533c029c33ee62916a81f398886e0e))
* dependabot and codeql CI ([2578c53](https://github.com/Prospect-Development-Team/plane-orca/commit/2578c5311bdf988dcaebe3bcd10f505888e1d75d))
* disable react-in-jsx-scope rule in oxlint config ([#8682](https://github.com/Prospect-Development-Team/plane-orca/issues/8682)) ([be88366](https://github.com/Prospect-Development-Team/plane-orca/commit/be8836642a654207c9e0ac2a813403ca716ea754)), closes [#8681](https://github.com/Prospect-Development-Team/plane-orca/issues/8681)
* dropdown shadow on the work item more options ([#9154](https://github.com/Prospect-Development-Team/plane-orca/issues/9154)) ([b6e47cc](https://github.com/Prospect-Development-Team/plane-orca/commit/b6e47ccdae76358ec55fc605dcc3cfa8d746d3f7))
* enforce FILE_SIZE_LIMIT on published Space asset upload ([#9242](https://github.com/Prospect-Development-Team/plane-orca/issues/9242)) ([25c6843](https://github.com/Prospect-Development-Team/plane-orca/commit/25c6843fceede6400eae38145458041c6acefb79))
* enforce workspace membership on V2 asset endpoints ([#8885](https://github.com/Prospect-Development-Team/plane-orca/issues/8885)) ([ac11c3e](https://github.com/Prospect-Development-Team/plane-orca/commit/ac11c3ef7939e31201fa92a17de106906025590f))
* file fomatting ([587cb3e](https://github.com/Prospect-Development-Team/plane-orca/commit/587cb3ecfec3197b02657b66b5cbdabc04d13221))
* filter out soft-deleted states from API endpoints ([#8840](https://github.com/Prospect-Development-Team/plane-orca/issues/8840)) ([db1c5b9](https://github.com/Prospect-Development-Team/plane-orca/commit/db1c5b95138e8bf641208bfae00e9e07e1cc0295))
* font imports ([#8387](https://github.com/Prospect-Development-Team/plane-orca/issues/8387)) ([5e0091e](https://github.com/Prospect-Development-Team/plane-orca/commit/5e0091e32e5d448484e0b91d6ae25aeb2951a9a5))
* **GIT-235:** add styles to onboarding tour close button for contrast ([#9188](https://github.com/Prospect-Development-Team/plane-orca/issues/9188)) ([bd0d164](https://github.com/Prospect-Development-Team/plane-orca/commit/bd0d164e0b343ac8f9df141d74d20716fe8a7bce))
* handle error message for special characters in Identifier of Project ([#9059](https://github.com/Prospect-Development-Team/plane-orca/issues/9059)) ([4280c4d](https://github.com/Prospect-Development-Team/plane-orca/commit/4280c4d1b131c209f9fc60b2f43276d32ce39064))
* harden webhook/link/OAuth-avatar SSRF (advisory clusters A/B/C/E) ([#9163](https://github.com/Prospect-Development-Team/plane-orca/issues/9163)) ([04622ce](https://github.com/Prospect-Development-Team/plane-orca/commit/04622ce1188c4680951f0001e35efb342fe51615))
* IDOR Vulnerabilities in Asset & Attachment Endpoints ([#8644](https://github.com/Prospect-Development-Team/plane-orca/issues/8644)) ([1548288](https://github.com/Prospect-Development-Team/plane-orca/commit/1548288e95722ccfa310046079ab3fe9c323282d))
* IDOR Vulnerabilities in Asset & Attachment Endpoints ([#8644](https://github.com/Prospect-Development-Team/plane-orca/issues/8644)) ([9070acb](https://github.com/Prospect-Development-Team/plane-orca/commit/9070acbbe81bc02db5c169789da6862d5fc35d96))
* image uploader bg in light mode ([#8385](https://github.com/Prospect-Development-Team/plane-orca/issues/8385)) ([cb56fbe](https://github.com/Prospect-Development-Team/plane-orca/commit/cb56fbe3cac49b0b87ae287803703f352b244d4f))
* input fields bg ([#8389](https://github.com/Prospect-Development-Team/plane-orca/issues/8389)) ([465c99f](https://github.com/Prospect-Development-Team/plane-orca/commit/465c99f742a5c08254dc308325c043105b94c634))
* Issues created or updated via REST API send no notifications or emails ([#9307](https://github.com/Prospect-Development-Team/plane-orca/issues/9307)) ([d5dda5d](https://github.com/Prospect-Development-Team/plane-orca/commit/d5dda5d41cd1d7425e8bea1a372d0f520bbafaf2))
* material icons font file ([#8366](https://github.com/Prospect-Development-Team/plane-orca/issues/8366)) ([b906d42](https://github.com/Prospect-Development-Team/plane-orca/commit/b906d42e1d7b5b37879f055644340b513d268f86))
* Member Information Disclosure via Public Endpoint [#8646](https://github.com/Prospect-Development-Team/plane-orca/issues/8646) ([8c23fdd](https://github.com/Prospect-Development-Team/plane-orca/commit/8c23fdd1d865f9bf3fd7edc7c7f2a60828523216))
* Member Information Disclosure via Public Endpoint [#8646](https://github.com/Prospect-Development-Team/plane-orca/issues/8646) ([f534463](https://github.com/Prospect-Development-Team/plane-orca/commit/f53446340b9021c6916259aa9cf772920309415d))
* merge lists in editor ([#8639](https://github.com/Prospect-Development-Team/plane-orca/issues/8639)) ([9ee73d5](https://github.com/Prospect-Development-Team/plane-orca/commit/9ee73d57efd9a9937e25022eda57fdfc07e8602b))
* migrate page navigation pane tabs from headless ui to propel ([#8805](https://github.com/Prospect-Development-Team/plane-orca/issues/8805)) ([113bba4](https://github.com/Prospect-Development-Team/plane-orca/commit/113bba46ea04309fa584d09084c6aaf36814d720))
* module percentage calculation ([#8595](https://github.com/Prospect-Development-Team/plane-orca/issues/8595)) ([b8d3b3c](https://github.com/Prospect-Development-Team/plane-orca/commit/b8d3b3c5eb63b5241e3d75460b16f1e22cff758d))
* nested context menu UI ([#8367](https://github.com/Prospect-Development-Team/plane-orca/issues/8367)) ([4cac953](https://github.com/Prospect-Development-Team/plane-orca/commit/4cac953cd1bd7e4b5eea933231257726fe02b0b0))
* **nginx:** correct real_ip_header typo X-Forward-For → X-Forwarded-For ([#8935](https://github.com/Prospect-Development-Team/plane-orca/issues/8935)) ([ff21e53](https://github.com/Prospect-Development-Team/plane-orca/commit/ff21e53f5a75fbe4686d5974f9f4840ef5d3deb1))
* node view renders ([#8559](https://github.com/Prospect-Development-Team/plane-orca/issues/8559)) ([20e266c](https://github.com/Prospect-Development-Team/plane-orca/commit/20e266c9bbfab7bf077778d065fe68c9c1b61c3d))
* **orca:** add copy options for details, title, and description to common locale file ([a9652ae](https://github.com/Prospect-Development-Team/plane-orca/commit/a9652aede7c0404a741e42c2e28a298510793292))
* **orca:** add i18n localization strings for project features configuration ([8e6e505](https://github.com/Prospect-Development-Team/plane-orca/commit/8e6e505b635675a1a8a26fcc486db4f7c3714548))
* **orca:** add project labels localization and improve fallback label rendering across settings pages ([c36dadb](https://github.com/Prospect-Development-Team/plane-orca/commit/c36dadb448bab255f1597e0048c2ad878cd66236))
* **orca:** improve assignee inference logic by resolving current user from request and deduplicating assigned IDs ([ef1cc59](https://github.com/Prospect-Development-Team/plane-orca/commit/ef1cc59ba0fb7a3642387c6cb7fbe4c32297cdd1))
* **orca:** prevent hydration mismatch by delaying theme-dependent UI rendering until component mount ([ca51a2a](https://github.com/Prospect-Development-Team/plane-orca/commit/ca51a2a11a7e19bff1f6939ee49a5e91e3e1a5eb))
* package updates ([c3c7c72](https://github.com/Prospect-Development-Team/plane-orca/commit/c3c7c72affcf4eff93dc21f8192d5b3fe23f3598))
* pdf export ([#8564](https://github.com/Prospect-Development-Team/plane-orca/issues/8564)) ([b31c019](https://github.com/Prospect-Development-Team/plane-orca/commit/b31c0195bc04deaed776c42b170d4b4fc60b742c))
* pnpm path for Docker builds ([#9079](https://github.com/Prospect-Development-Team/plane-orca/issues/9079)) ([1dabc63](https://github.com/Prospect-Development-Team/plane-orca/commit/1dabc632bf79ef860a8d6e6d3b48bfdea67875e5))
* prevent ORM field injection via segment parameter in analytics (GHSA-93x3-ghh7-72j3) ([#8864](https://github.com/Prospect-Development-Team/plane-orca/issues/8864)) ([8a2579c](https://github.com/Prospect-Development-Team/plane-orca/commit/8a2579ce9ba5675873d9aa10e84a7d02a53e6150))
* prevent privilege escalation in project member role updates (GHSA-494h-3rcq-5g3c) ([#8833](https://github.com/Prospect-Development-Team/plane-orca/issues/8833)) ([587fe76](https://github.com/Prospect-Development-Team/plane-orca/commit/587fe76032fb69275866fdeb655699a70a83c521))
* remove ee folder from web ([#8622](https://github.com/Prospect-Development-Team/plane-orca/issues/8622)) ([06e4a16](https://github.com/Prospect-Development-Team/plane-orca/commit/06e4a1624c52e5e58b3ed19ef37b090cf269eab7))
* remove unused imports and variables (part 1 — packages & non-web-core) ([#8751](https://github.com/Prospect-Development-Team/plane-orca/issues/8751)) ([d9695af](https://github.com/Prospect-Development-Team/plane-orca/commit/d9695afcdcb31697fc1831d87997913ac6cadc9c))
* remove unused imports and variables (part 2 — web/core non-issues) ([#8752](https://github.com/Prospect-Development-Team/plane-orca/issues/8752)) ([04d4490](https://github.com/Prospect-Development-Team/plane-orca/commit/04d4490293b5a49996dcc93c72977fb4766295f9))
* remove unused imports and variables (part 3) ([#8753](https://github.com/Prospect-Development-Team/plane-orca/issues/8753)) ([5a7d1eb](https://github.com/Prospect-Development-Team/plane-orca/commit/5a7d1ebd65c9283ec97a155bc5dd3c914431206d))
* removed unused files ([d91b5a2](https://github.com/Prospect-Development-Team/plane-orca/commit/d91b5a274b4f8ad9d9eea10eb3a250150957b887))
* replace eslint with oxlint ([#8677](https://github.com/Prospect-Development-Team/plane-orca/issues/8677)) ([c554243](https://github.com/Prospect-Development-Team/plane-orca/commit/c5542438a146298362262db245aecaf7c4729e72))
* replace IS_SELF_MANAGED with WEBHOOK_ALLOWED_IPS allowlist ([#8884](https://github.com/Prospect-Development-Team/plane-orca/issues/8884)) ([a8a16c8](https://github.com/Prospect-Development-Team/plane-orca/commit/a8a16c8ba0b555438c0fe50e5217cc6ac5eda328))
* Require at least one alphanumeric char in workspace name ([#9263](https://github.com/Prospect-Development-Team/plane-orca/issues/9263)) ([0f1f4d5](https://github.com/Prospect-Development-Team/plane-orca/commit/0f1f4d5c253afef64492bcaa74880b597184b27b))
* resolve esbuild advisory and bump turbo to 2.9.18 ([#9236](https://github.com/Prospect-Development-Team/plane-orca/issues/9236)) ([498f857](https://github.com/Prospect-Development-Team/plane-orca/commit/498f857be45da47e1385c25a0b4184dfcec824ab))
* resolve open CodeQL security alerts ([#9505](https://github.com/Prospect-Development-Team/plane-orca/issues/9505)) ([08a7d12](https://github.com/Prospect-Development-Team/plane-orca/commit/08a7d12b9ddc719180270f78b693b764a9132002))
* resolve React Doctor errors and restore its PR baseline ([#9488](https://github.com/Prospect-Development-Team/plane-orca/issues/9488)) ([7564480](https://github.com/Prospect-Development-Team/plane-orca/commit/7564480cf73c7ea8b037c002f3fe6cfd2267367e))
* sanitize filenames in upload paths to prevent path traversal ([#8879](https://github.com/Prospect-Development-Team/plane-orca/issues/8879)) ([aea66f5](https://github.com/Prospect-Development-Team/plane-orca/commit/aea66f53f4022bd51cbc829bc03baa048c03e011))
* scope IssueBulkUpdateDateEndpoint query to workspace and project ([#8834](https://github.com/Prospect-Development-Team/plane-orca/issues/8834)) ([a01b51f](https://github.com/Prospect-Development-Team/plane-orca/commit/a01b51fca5adff16923ad8148de0d0563f8cd738))
* scope workspace user preference filter to current user ([#9279](https://github.com/Prospect-Development-Team/plane-orca/issues/9279)) ([4a0746b](https://github.com/Prospect-Development-Team/plane-orca/commit/4a0746b45eb7c6737209822dd8e91f5d777ba28b))
* security vulnerabilities for plane docker images ([#9140](https://github.com/Prospect-Development-Team/plane-orca/issues/9140)) ([13a3ea2](https://github.com/Prospect-Development-Team/plane-orca/commit/13a3ea27fb1c22d3f657b07e3f9c5c5afc2f0a0b))
* **security:** block bot user logins ([#9368](https://github.com/Prospect-Development-Team/plane-orca/issues/9368)) ([4fc79a2](https://github.com/Prospect-Development-Team/plane-orca/commit/4fc79a2d7e93e769f2e6251cb4e0436b8ae4d2e7))
* space app default background ([#8384](https://github.com/Prospect-Development-Team/plane-orca/issues/8384)) ([ba7b2a3](https://github.com/Prospect-Development-Team/plane-orca/commit/ba7b2a3e27df5677631bff042ed65299056e1246))
* strip control characters from sanitized filenames ([#9151](https://github.com/Prospect-Development-Team/plane-orca/issues/9151)) ([49c4da6](https://github.com/Prospect-Development-Team/plane-orca/commit/49c4da6d4b1f32e07131d6ed49958f9fce2ff4fa)), closes [#9127](https://github.com/Prospect-Development-Team/plane-orca/issues/9127)
* strip whitespace and handle null values in instance configuration ([#8744](https://github.com/Prospect-Development-Team/plane-orca/issues/8744)) ([77c4b9c](https://github.com/Prospect-Development-Team/plane-orca/commit/77c4b9c77462d15d5a105a55ae1ad438bfb0e5c0))
* tooltip imports ([#8379](https://github.com/Prospect-Development-Team/plane-orca/issues/8379)) ([3df5839](https://github.com/Prospect-Development-Team/plane-orca/commit/3df58397b58ad97679dfb42ec834b6aa4f1a23e7))
* tsdown watch ([#8813](https://github.com/Prospect-Development-Team/plane-orca/issues/8813)) ([97b4abd](https://github.com/Prospect-Development-Team/plane-orca/commit/97b4abd69313d3f7d2f3cf63cf69139a917557cd)), closes [#8791](https://github.com/Prospect-Development-Team/plane-orca/issues/8791)
* type fix for description payload ([#8619](https://github.com/Prospect-Development-Team/plane-orca/issues/8619)) ([e1227f0](https://github.com/Prospect-Development-Team/plane-orca/commit/e1227f0b58b92b2d4b97d22387b7960d249a58fe))
* Update healthcheck endpoint in Dockerfile to target /spaces/ path ([#8674](https://github.com/Prospect-Development-Team/plane-orca/issues/8674)) ([5c9f2a1](https://github.com/Prospect-Development-Team/plane-orca/commit/5c9f2a17c21b41e1d20203756a3a437ff2026304))
* update Twitter icon and links to X ([#8785](https://github.com/Prospect-Development-Team/plane-orca/issues/8785)) ([#8790](https://github.com/Prospect-Development-Team/plane-orca/issues/8790)) ([7c2fc2d](https://github.com/Prospect-Development-Team/plane-orca/commit/7c2fc2dd7f8f02ce16cac3f126871c98b614773f))
* Use APP_DOMAIN env var for bot user email ([#9262](https://github.com/Prospect-Development-Team/plane-orca/issues/9262)) ([64da8dc](https://github.com/Prospect-Development-Team/plane-orca/commit/64da8dc9312fc454ed01e5c98703376b2638c501))
* **user:** clone user data before updates to prevent mutations ([#9285](https://github.com/Prospect-Development-Team/plane-orca/issues/9285)) ([18ea715](https://github.com/Prospect-Development-Team/plane-orca/commit/18ea715960b2697cf3980c493c44e894683c8f98))
* validate redirects in favicon fetching to prevent SSRF ([#8858](https://github.com/Prospect-Development-Team/plane-orca/issues/8858)) ([63fac3b](https://github.com/Prospect-Development-Team/plane-orca/commit/63fac3b8c488eb0afb8ec7d6731688c77ed72e24))
* **web:** add requestIdleCallback fallback for Safari/iOS ([#9094](https://github.com/Prospect-Development-Team/plane-orca/issues/9094)) ([fd613dc](https://github.com/Prospect-Development-Team/plane-orca/commit/fd613dc7388e39b0991f6600b06be8b69cd211cf))
* **web:** add Safari fallback for requestIdleCallback ([#9137](https://github.com/Prospect-Development-Team/plane-orca/issues/9137)) ([f14451a](https://github.com/Prospect-Development-Team/plane-orca/commit/f14451a5de3b8e4283d35ff11190d79292491a7c))
* **web:** add trailing slash to notification list API call ([#9521](https://github.com/Prospect-Development-Team/plane-orca/issues/9521)) ([1942665](https://github.com/Prospect-Development-Team/plane-orca/commit/194266581c7fd6f0807c4565ffa651702789febe))
* **web:** guard unguarded data derefs causing work-item and layout crashes ([#9546](https://github.com/Prospect-Development-Team/plane-orca/issues/9546)) ([fa02716](https://github.com/Prospect-Development-Team/plane-orca/commit/fa027167f62638166dd1b43dff0c9bd2e559aa7b))
* work item property icon renderer ([#8363](https://github.com/Prospect-Development-Team/plane-orca/issues/8363)) ([b7621c6](https://github.com/Prospect-Development-Team/plane-orca/commit/b7621c62ebf46beecfff9d8ed263c5a815940e46))
* workitem description input inital load ([#8617](https://github.com/Prospect-Development-Team/plane-orca/issues/8617)) ([dbe059b](https://github.com/Prospect-Development-Team/plane-orca/commit/dbe059b7b526f9a1cea926ec7edd31d7fa98bf41))


### 🎨 Styles & UI

* update ASCII art in install script header ([#8628](https://github.com/Prospect-Development-Team/plane-orca/issues/8628)) ([bcc8fb4](https://github.com/Prospect-Development-Team/plane-orca/commit/bcc8fb4d1d48131638b9bd381456a51ac35acec6))


### 📝 Documentation

* add Zenith Hosting deploy option ([#9529](https://github.com/Prospect-Development-Team/plane-orca/issues/9529)) ([65f4a99](https://github.com/Prospect-Development-Team/plane-orca/commit/65f4a99657deb2d7c40e94ee4c63001d76ea1cc5))
* **orca:** add documentation for Plane Orca feature set and fork enhancements to README ([e3d75b4](https://github.com/Prospect-Development-Team/plane-orca/commit/e3d75b49b056e20560261ea4ed82b483c09a26e9))
* **orca:** rename main branch to upstream to clarify its role as the official upstream mirror ([4587a5a](https://github.com/Prospect-Development-Team/plane-orca/commit/4587a5aac672d9e307105f2e6634414c597af44f))
* **orca:** update upstream synchronization instructions to track master branch instead of main ([e8ce574](https://github.com/Prospect-Development-Team/plane-orca/commit/e8ce57453c400f635d0d1fa181f101aa3d66a68b))
* update readme with react router badge ([#8424](https://github.com/Prospect-Development-Team/plane-orca/issues/8424)) ([dbf84bf](https://github.com/Prospect-Development-Team/plane-orca/commit/dbf84bf6bb5d343f98342aae20e1517a761cea52))


### ♻️ Refactoring

* actions icon migration ([#8219](https://github.com/Prospect-Development-Team/plane-orca/issues/8219)) ([2980c2d](https://github.com/Prospect-Development-Team/plane-orca/commit/2980c2d76bee848198d756f609d16e71dd173ba4))
* **api:** source API_KEY_RATE_LIMIT from settings, drop service token throttle ([#9161](https://github.com/Prospect-Development-Team/plane-orca/issues/9161)) ([248f5d6](https://github.com/Prospect-Development-Team/plane-orca/commit/248f5d66e69fa99b64de27aa454819158d19872a))
* **i18n:** migrate packages/i18n from MobX to react-i18next ([#8898](https://github.com/Prospect-Development-Team/plane-orca/issues/8898)) ([65d6a94](https://github.com/Prospect-Development-Team/plane-orca/commit/65d6a94b0a7763df62701a2f94200765b3b165a1))
* logging with retention + API token hardening ([#9148](https://github.com/Prospect-Development-Team/plane-orca/issues/9148)) ([edf2475](https://github.com/Prospect-Development-Team/plane-orca/commit/edf247541301e482f2688c63481464b671ec579d))
* **orca:** apply consistent indentation and formatting to UI components and helper functions ([953fbae](https://github.com/Prospect-Development-Team/plane-orca/commit/953fbae4a878dcf5aa849ef207ec6923ea51f42f))
* **orca:** implement project estimate synchronization and optimize API requests using persistent session connection pooling ([54a5607](https://github.com/Prospect-Development-Team/plane-orca/commit/54a56074d4b2f1d1d711fb71f51d4cb090d5cf75))
* **orca:** improve cycle creation logic with exact match detection ([5f7c01b](https://github.com/Prospect-Development-Team/plane-orca/commit/5f7c01b6d7ce4651533bef3146065a79750027d9))
* **orca:** improve project, label, cycle, and module migration logic with better error handling and duplication checks ([1d08e5d](https://github.com/Prospect-Development-Team/plane-orca/commit/1d08e5dfffea71d1cf67c9b9ede21c3e7bc0faf1))
* **orca:** migrate gantt and bulk operation imports to core components directory ([acde60c](https://github.com/Prospect-Development-Team/plane-orca/commit/acde60c6755bcc7d8668e6cb9ca6c84ec6115994))
* **orca:** remove CycleAdditionalActions component from cycle list item actions ([7c37c40](https://github.com/Prospect-Development-Team/plane-orca/commit/7c37c4033a2dbcf830ee29755b312f40c95f02e8))
* **orca:** replace asset migration with generic pagination handling and workspace wiping capabilities ([09b5487](https://github.com/Prospect-Development-Team/plane-orca/commit/09b5487d667a4f1efad83e62ba77aa05e9183eb0))
* table drag preview using decorations ([#8597](https://github.com/Prospect-Development-Team/plane-orca/issues/8597)) ([d497304](https://github.com/Prospect-Development-Team/plane-orca/commit/d497304de5a018303a605c70d35d7b3583a1242f))


### 🔧 Chores & Maintenance

* add Claude Code skills for PR descriptions and release notes ([#8920](https://github.com/Prospect-Development-Team/plane-orca/issues/8920)) ([f1d567a](https://github.com/Prospect-Development-Team/plane-orca/commit/f1d567accc5e6dbfb56265de850cb1cac4188cb5))
* add copyright ([#8584](https://github.com/Prospect-Development-Team/plane-orca/issues/8584)) ([02d0ee3](https://github.com/Prospect-Development-Team/plane-orca/commit/02d0ee3e0fe2606a6b3470e093b39bf90f1b3faa))
* Add forum link and remove discord link on readme ([#8655](https://github.com/Prospect-Development-Team/plane-orca/issues/8655)) ([9425c66](https://github.com/Prospect-Development-Team/plane-orca/commit/9425c66eb57f71507b89cd3c2e2e452949da6878))
* adding traget commit sha for the github release ([799b9cb](https://github.com/Prospect-Development-Team/plane-orca/commit/799b9cbfc5deed97f6de13698194e023821bc818))
* admin folder structure ([#8632](https://github.com/Prospect-Development-Team/plane-orca/issues/8632)) ([dfce8c6](https://github.com/Prospect-Development-Team/plane-orca/commit/dfce8c627839b54800fa306bac68c59f3b88e8d4))
* bump turbo to 2.9.14, migrate pnpm config to workspace yaml ([#9147](https://github.com/Prospect-Development-Team/plane-orca/issues/9147)) ([0acb32e](https://github.com/Prospect-Development-Team/plane-orca/commit/0acb32e65e8c3880a32d7b73a40cae52d3960ab0))
* bump up the package version ([c62930e](https://github.com/Prospect-Development-Team/plane-orca/commit/c62930ebcfab1a9591379289d505effbe92dcf32))
* **ci:** suppress CodeQL file coverage deprecation warning ([#8916](https://github.com/Prospect-Development-Team/plane-orca/issues/8916)) ([da41f14](https://github.com/Prospect-Development-Team/plane-orca/commit/da41f14a057e04f7c19e6cf380e755deab98dbcf))
* clean up React Doctor warnings in admin app ([#9418](https://github.com/Prospect-Development-Team/plane-orca/issues/9418)) ([bed58d9](https://github.com/Prospect-Development-Team/plane-orca/commit/bed58d9b17dbc8b221af9cde0cec9cec299d183b))
* **deps:** bump axios, uuid and add security overrides ([#8930](https://github.com/Prospect-Development-Team/plane-orca/issues/8930)) ([32fb88a](https://github.com/Prospect-Development-Team/plane-orca/commit/32fb88ab2480d9f7d1a37282739df920cef921b0))
* **deps:** bump cryptography ([#8625](https://github.com/Prospect-Development-Team/plane-orca/issues/8625)) ([6c984e1](https://github.com/Prospect-Development-Team/plane-orca/commit/6c984e18ae8d63617ad51836a88fd397b9b2d31f))
* **deps:** bump cryptography ([#8625](https://github.com/Prospect-Development-Team/plane-orca/issues/8625)) ([b59e541](https://github.com/Prospect-Development-Team/plane-orca/commit/b59e541b3577f40808306642413e13022273c383))
* **deps:** bump cryptography ([#8819](https://github.com/Prospect-Development-Team/plane-orca/issues/8819)) ([9851fe0](https://github.com/Prospect-Development-Team/plane-orca/commit/9851fe0b8fad33cb683d4b5b928670d31185685b))
* **deps:** bump cryptography ([#9243](https://github.com/Prospect-Development-Team/plane-orca/issues/9243)) ([2541a8c](https://github.com/Prospect-Development-Team/plane-orca/commit/2541a8c9cc819aecf29835d5024ae9bb5e71ee9c))
* **deps:** bump lodash-es in the npm_and_yarn group across 1 directory ([#8573](https://github.com/Prospect-Development-Team/plane-orca/issues/8573)) ([6c8779c](https://github.com/Prospect-Development-Team/plane-orca/commit/6c8779c8d30dac97f2ff72617b27da9af1e3bc98))
* **deps:** bump lxml ([#8925](https://github.com/Prospect-Development-Team/plane-orca/issues/8925)) ([03a2be8](https://github.com/Prospect-Development-Team/plane-orca/commit/03a2be84b76ae12c88a6565b5fb3836397d18bce))
* **deps:** bump postcss ([#8931](https://github.com/Prospect-Development-Team/plane-orca/issues/8931)) ([a40e064](https://github.com/Prospect-Development-Team/plane-orca/commit/a40e064448e5d5e185b01f87b44300ea14553735))
* **deps:** bump pyjwt ([#9241](https://github.com/Prospect-Development-Team/plane-orca/issues/9241)) ([7db4d8e](https://github.com/Prospect-Development-Team/plane-orca/commit/7db4d8ec9a00c37388765fc6a0d982fc1e190c70))
* **deps:** bump pytest ([#8891](https://github.com/Prospect-Development-Team/plane-orca/issues/8891)) ([bbf14fb](https://github.com/Prospect-Development-Team/plane-orca/commit/bbf14fba31c0d8be9435eb32eedad9673ff1ed98))
* **deps:** bump pytest from 7.4.0 to 9.0.2 in /apps/api ([#8693](https://github.com/Prospect-Development-Team/plane-orca/issues/8693)) ([6627282](https://github.com/Prospect-Development-Team/plane-orca/commit/6627282bc5854dddb006ff0fe8c8c83264a0f067))
* **deps:** bump python-json-logger from 3.3.0 to 4.0.0 in /apps/api ([#8692](https://github.com/Prospect-Development-Team/plane-orca/issues/8692)) ([d7c12f9](https://github.com/Prospect-Development-Team/plane-orca/commit/d7c12f9730203ede20b841f1dd3c8d2abb893d20))
* **deps:** bump requests ([#8804](https://github.com/Prospect-Development-Team/plane-orca/issues/8804)) ([130ba5e](https://github.com/Prospect-Development-Team/plane-orca/commit/130ba5ee6cf90217ddf5fa52189cdf3711e40796))
* **deps:** bump the actions group across 1 directory with 11 updates ([#8741](https://github.com/Prospect-Development-Team/plane-orca/issues/8741)) ([72b6453](https://github.com/Prospect-Development-Team/plane-orca/commit/72b6453f6f6aa3a3bd72df5d79808d509cba426e))
* **deps:** bump the npm_and_yarn group across 1 directory with 3 updates ([#9244](https://github.com/Prospect-Development-Team/plane-orca/issues/9244)) ([53a323d](https://github.com/Prospect-Development-Team/plane-orca/commit/53a323d559cb27d87f7440b2fc8514147cf7e542))
* **deps:** bump vite in the npm_and_yarn group across 1 directory ([#8863](https://github.com/Prospect-Development-Team/plane-orca/issues/8863)) ([d1db13c](https://github.com/Prospect-Development-Team/plane-orca/commit/d1db13c3a7cc9a341286af4558e4f0383488db0b))
* **deps:** django version upgrade ([d20247e](https://github.com/Prospect-Development-Team/plane-orca/commit/d20247e9760fee250f468a9efb2b1f763392c045))
* **deps:** minimatch and rollup package vulnerabilities ([#8675](https://github.com/Prospect-Development-Team/plane-orca/issues/8675)) ([da870a1](https://github.com/Prospect-Development-Team/plane-orca/commit/da870a1513c56f1b8917c20d836d98070c271d0c))
* **deps:** react router upgraded ([8399f64](https://github.com/Prospect-Development-Team/plane-orca/commit/8399f64beef3f7c2d2a83dedab8d219355558195))
* **deps:** remove unused pnpm overrides ([#8973](https://github.com/Prospect-Development-Team/plane-orca/issues/8973)) ([a62fe8a](https://github.com/Prospect-Development-Team/plane-orca/commit/a62fe8a781286ba4c15593f70035c482dbc3c5a6))
* **deps:** replace dotenvx with dotenv and update overrides ([#8832](https://github.com/Prospect-Development-Team/plane-orca/issues/8832)) ([b73d634](https://github.com/Prospect-Development-Team/plane-orca/commit/b73d6344adee8fa77cb202009067f3f6c295d33a))
* **deps:** resolve open Dependabot security alerts ([#9456](https://github.com/Prospect-Development-Team/plane-orca/issues/9456)) ([a8e53b6](https://github.com/Prospect-Development-Team/plane-orca/commit/a8e53b6ac7b87bd8e3e931d21188f7679c7ab6c4))
* **deps:** update axios dependency ([efc600a](https://github.com/Prospect-Development-Team/plane-orca/commit/efc600ad8cde635719128f0c18671197f3502c42))
* **deps:** update dependency overrides ([#8831](https://github.com/Prospect-Development-Team/plane-orca/issues/8831)) ([f0ec846](https://github.com/Prospect-Development-Team/plane-orca/commit/f0ec84661ddb2430275b10a7538b1e3043014f3c))
* **deps:** update lodash package ([0887cbb](https://github.com/Prospect-Development-Team/plane-orca/commit/0887cbbda8f030eff833323e1f9522dfd21571d9))
* **deps:** update the node pacakges ([ea7b30b](https://github.com/Prospect-Development-Team/plane-orca/commit/ea7b30bc9cf5f4ff71d01b3b261cb9b0c950a2cd))
* **deps:** upgrade django version ([95d121c](https://github.com/Prospect-Development-Team/plane-orca/commit/95d121ce3867f1edc61b627a840c37cbd7a36be5))
* **deps:** upgrade django version ([13a6794](https://github.com/Prospect-Development-Team/plane-orca/commit/13a679437d39b8f889896aa5457ac02d98c5606d))
* **deps:** upgrade Storybook to v10 and fix security advisories ([#9277](https://github.com/Prospect-Development-Team/plane-orca/issues/9277)) ([ad32dc7](https://github.com/Prospect-Development-Team/plane-orca/commit/ad32dc7f709f62ecc1e88bd1c4276be2583372ca))
* **deps:** upgrade the undici and flatted versions ([e972989](https://github.com/Prospect-Development-Team/plane-orca/commit/e97298952249a691b3d8f51760a85af5d6bfb53a))
* fix typos in comments ([#8553](https://github.com/Prospect-Development-Team/plane-orca/issues/8553)) ([bb4f172](https://github.com/Prospect-Development-Team/plane-orca/commit/bb4f172e26243c3d6ba83359f4321c3ffd11f5b4))
* Intake snooze modal width ([5747dc6](https://github.com/Prospect-Development-Team/plane-orca/commit/5747dc6fd818d14ddc3d568ee8237b3444928985))
* integrate react-doctor scanning ([#9223](https://github.com/Prospect-Development-Team/plane-orca/issues/9223)) ([a153531](https://github.com/Prospect-Development-Team/plane-orca/commit/a1535319e6eade1e51dff858dee9ba57a62573bb))
* merge constants and services ([#8623](https://github.com/Prospect-Development-Team/plane-orca/issues/8623)) ([7793feb](https://github.com/Prospect-Development-Team/plane-orca/commit/7793febcf80af36759b6bab137efb5121c887229))
* merge helpers and layouts ([#8624](https://github.com/Prospect-Development-Team/plane-orca/issues/8624)) ([2b6e24d](https://github.com/Prospect-Development-Team/plane-orca/commit/2b6e24d5268300eba6a29e2e21f2b41463dc1759))
* move all dependencies into pnpm catalog ([#9153](https://github.com/Prospect-Development-Team/plane-orca/issues/9153)) ([3f57fef](https://github.com/Prospect-Development-Team/plane-orca/commit/3f57fefdb4dd0ccf102b7ea8700225f0f46b1907))
* navigation preference enhancements ([#8468](https://github.com/Prospect-Development-Team/plane-orca/issues/8468)) ([8663382](https://github.com/Prospect-Development-Team/plane-orca/commit/866338289ed23033190989789b7bd6a680f88445))
* **orca:** add global HTTP 429 retry logic and support for syncing/updating existing projects during migration ([414ac5c](https://github.com/Prospect-Development-Team/plane-orca/commit/414ac5c70d18ba96fc499bfff0987690b7ee5aa1))
* **orca:** add migration file to merge divergent database branches ([d4a2487](https://github.com/Prospect-Development-Team/plane-orca/commit/d4a2487145ce1dcc1faeb112b3cb0bd3dedcedaf))
* **orca:** bump version to 1.2.0-plane.1.4.1 ([63aa568](https://github.com/Prospect-Development-Team/plane-orca/commit/63aa56854cb2479a9dfb024eaa0c940c30cb6faa))
* **orca:** clean up duplicate entries in CHANGELOG.md ([582fae8](https://github.com/Prospect-Development-Team/plane-orca/commit/582fae881a9f4a4dc91acbe88f64364c4a2ca45b))
* **orca:** enable visibility for test, ci, and build in release-please changelog ([5c28123](https://github.com/Prospect-Development-Team/plane-orca/commit/5c28123f062e522ace204dfa2427a06c48e6c833))
* **orca:** ensure required release labels exist in labeler workflow ([403118c](https://github.com/Prospect-Development-Team/plane-orca/commit/403118c2ed87a7b879a753455474e323fab9585e))
* **orca:** remove release-as override on stage branch ([9c9bd60](https://github.com/Prospect-Development-Team/plane-orca/commit/9c9bd60f400b63a48bf4e7f8647e5666e7a0fa5d))
* **orca:** restrict labeler workflow to prod/stage branches and secure package version retrieval ([9b31b2b](https://github.com/Prospect-Development-Team/plane-orca/commit/9b31b2b55a9fa78a5946e5f43543026ea7d03bc0))
* **orca:** set pull_policy to always for all services in docker-compose-orca.yml ([b6d3504](https://github.com/Prospect-Development-Team/plane-orca/commit/b6d350407289003bc1fbe8fba684e32fb20a40d4))
* **orca:** skip labeler workflow for release-please and bot-initiated pull requests ([8a47f12](https://github.com/Prospect-Development-Team/plane-orca/commit/8a47f1220caf3edaa35dcb1a9d7267a270563342))
* **orca:** sync prod back to stage [skip ci] ([6a41de4](https://github.com/Prospect-Development-Team/plane-orca/commit/6a41de42d60169b9d3a716440155532c4552c451))
* **orca:** sync prod back to stage [skip ci] ([3f23d2b](https://github.com/Prospect-Development-Team/plane-orca/commit/3f23d2b65d5856343bd213ff21b8c5a4c0841c5a))
* **orca:** update commit prefixes to standard conventional commit format in documentation ([159ba35](https://github.com/Prospect-Development-Team/plane-orca/commit/159ba3505986f74aade18a731dc0a446ede42bdc))
* **orca:** update release candidate PR template and refine automation title formatting ([80a1067](https://github.com/Prospect-Development-Team/plane-orca/commit/80a1067b933d009a1f003fa42d19a101db38f320))
* **orca:** update templates to use scoped conventional commit naming ([b1316d0](https://github.com/Prospect-Development-Team/plane-orca/commit/b1316d073038254facbfb8bf2d0c5edac691b9cb))
* pacakge version ([ec44b63](https://github.com/Prospect-Development-Team/plane-orca/commit/ec44b63027cfd96974c1c964aa3ca615ebbc52fd))
* pacakge version bump ([6a061ac](https://github.com/Prospect-Development-Team/plane-orca/commit/6a061acc69768d837acd2d5884e06e0de9ebf3f7))
* platform layout enhancements ([#8386](https://github.com/Prospect-Development-Team/plane-orca/issues/8386)) ([80acecb](https://github.com/Prospect-Development-Team/plane-orca/commit/80acecb77a9e756111accaf860a4c5ee8665296e))
* **prod:** release 1.0.0-plane.1.3.1 ([e5e3b6d](https://github.com/Prospect-Development-Team/plane-orca/commit/e5e3b6d0b231915bf565a28295c226dd4ba47ff5))
* **prod:** release 1.0.0-plane.1.3.1 ([f1b9b88](https://github.com/Prospect-Development-Team/plane-orca/commit/f1b9b88a789416cd9b9ab79af755949470860580))
* **prod:** release 1.0.0-plane.1.3.1 ([3a4c171](https://github.com/Prospect-Development-Team/plane-orca/commit/3a4c1715a0a0b335fd4fb829d1f410ea3f3cb44f))
* **prod:** release 1.0.0-plane.1.3.1 ([d47b4ae](https://github.com/Prospect-Development-Team/plane-orca/commit/d47b4ae3f227ebbad605cdcdfbafa55c52697c67))
* **prod:** release 1.1.0-plane.1.3.1 ([fbe93a8](https://github.com/Prospect-Development-Team/plane-orca/commit/fbe93a8b987db683ca7a8b336f1a2409b8be981d))
* **prod:** release 1.1.0-plane.1.3.1 ([ebbcb13](https://github.com/Prospect-Development-Team/plane-orca/commit/ebbcb13afe5eebe6e8ca291ad8df3320cd48e3ae))
* **prod:** release 1.2.0-plane.1.3.1 ([9b4738b](https://github.com/Prospect-Development-Team/plane-orca/commit/9b4738b94289e5155f831b63bc9066f3eaadebb5))
* **prod:** release 1.2.0-plane.1.3.1 ([9b0fed6](https://github.com/Prospect-Development-Team/plane-orca/commit/9b0fed6c1a90cf115048ecbe713624ab89e54194))
* remove chat support component ([1faf06c](https://github.com/Prospect-Development-Team/plane-orca/commit/1faf06c7553d2bbce59634ae96fb498495c46d62))
* remove Intercom integration and chat support components ([#8875](https://github.com/Prospect-Development-Team/plane-orca/issues/8875)) ([c21d2c6](https://github.com/Prospect-Development-Team/plane-orca/commit/c21d2c6fb35fd93b2ddab5edf20a017bd12fef4a))
* remove posthog events ([#8465](https://github.com/Prospect-Development-Team/plane-orca/issues/8465)) ([d61b157](https://github.com/Prospect-Development-Team/plane-orca/commit/d61b157929d76daced61881189f71b5b87797030))
* remove service token endpoint which is unused ([#8797](https://github.com/Prospect-Development-Team/plane-orca/issues/8797)) ([f3c7c05](https://github.com/Prospect-Development-Team/plane-orca/commit/f3c7c057b44902bb89c087c3adcaa2394a79b6dc))
* remove unused get_client_ip import ([#8453](https://github.com/Prospect-Development-Team/plane-orca/issues/8453)) ([94d5779](https://github.com/Prospect-Development-Team/plane-orca/commit/94d5779f3a87b863024b186457796f3558cc14e1))
* remove unused right sidebar component and clean up workspace member settings ([#8477](https://github.com/Prospect-Development-Team/plane-orca/issues/8477)) ([3d5e427](https://github.com/Prospect-Development-Team/plane-orca/commit/3d5e427894d35185d7cf23da29bc75677d48f93d))
* replace old classNames ([#8372](https://github.com/Prospect-Development-Team/plane-orca/issues/8372)) ([88f4d82](https://github.com/Prospect-Development-Team/plane-orca/commit/88f4d8253de0e0e33eea45ea3031b427e73d6436))
* replace prettier with oxfmt ([#8676](https://github.com/Prospect-Development-Team/plane-orca/issues/8676)) ([41abaff](https://github.com/Prospect-Development-Team/plane-orca/commit/41abaffc6e39fb35f633c39cfc67d1a3c47f1b97))
* resolve dependabot security alerts (pnpm + pip) ([#9549](https://github.com/Prospect-Development-Team/plane-orca/issues/9549)) ([31853ab](https://github.com/Prospect-Development-Team/plane-orca/commit/31853ab2b8b7810c59dc30d22e52c8f4b5a71a47))
* restructure .claude/skills into per-skill directories ([#9146](https://github.com/Prospect-Development-Team/plane-orca/issues/9146)) ([310d2ed](https://github.com/Prospect-Development-Team/plane-orca/commit/310d2eda215a8e7a8bb116b7b450ab3a0289ac07))
* retire departed code owners (apps/live, ox configs) ([#9504](https://github.com/Prospect-Development-Team/plane-orca/issues/9504)) ([55610f4](https://github.com/Prospect-Development-Team/plane-orca/commit/55610f40686b7b78bccb3cc238be9ee7de903919))
* space folders ([#8707](https://github.com/Prospect-Development-Team/plane-orca/issues/8707)) ([7fb6696](https://github.com/Prospect-Development-Team/plane-orca/commit/7fb6696c67aafd7d471a88a89b52cb67fdf30606))
* update CODEOWNERS for apps and deployments ([#8919](https://github.com/Prospect-Development-Team/plane-orca/issues/8919)) ([62b2d1b](https://github.com/Prospect-Development-Team/plane-orca/commit/62b2d1b20729284b425e69c734b3a414cfe6a7e1))
* update component styles and class names for consistency across the application ([#8376](https://github.com/Prospect-Development-Team/plane-orca/issues/8376)) ([c56bb06](https://github.com/Prospect-Development-Team/plane-orca/commit/c56bb06957686b304ac46a74d77b78383f8895f2))
* update dependencies (Django, cryptography, axios, lodash) ([#8880](https://github.com/Prospect-Development-Team/plane-orca/issues/8880)) ([39325d2](https://github.com/Prospect-Development-Team/plane-orca/commit/39325d28a68c4b5abd8bbe42116dc1d2c57eebdc))
* update package version ([ed61f99](https://github.com/Prospect-Development-Team/plane-orca/commit/ed61f9925b7334a6c2e5d57db9e5c9b4e0dec3b2))
* update storybook dependency ([4908211](https://github.com/Prospect-Development-Team/plane-orca/commit/4908211fe6ebf6150cb8516a4036366f44221185))
* updated migration file name ([#8515](https://github.com/Prospect-Development-Team/plane-orca/issues/8515)) ([5f3f9d2](https://github.com/Prospect-Development-Team/plane-orca/commit/5f3f9d2623b09899002a7b6841fc6f45f8a2d7eb))
* upgrade Django 4.2 → 5.2 ([#9325](https://github.com/Prospect-Development-Team/plane-orca/issues/9325)) ([ca3b48e](https://github.com/Prospect-Development-Team/plane-orca/commit/ca3b48ef8718095d8572afb3aaa3a9b411335ab9))
* upgrade turbo from v2.8.12 to v2.9.4 ([#8859](https://github.com/Prospect-Development-Team/plane-orca/issues/8859)) ([bb128e3](https://github.com/Prospect-Development-Team/plane-orca/commit/bb128e3e1630707bceaed747d52d42a8c4966227))
* version bump ([00a51f5](https://github.com/Prospect-Development-Team/plane-orca/commit/00a51f5e6a703b0475cca3568c35f1e2acbab42a))
* version upgrade ([9a7696a](https://github.com/Prospect-Development-Team/plane-orca/commit/9a7696acac92c68280f6efc2173e2ea9a4e1bb14))
* workspace events ([#8439](https://github.com/Prospect-Development-Team/plane-orca/issues/8439)) ([777200d](https://github.com/Prospect-Development-Team/plane-orca/commit/777200db7b95c1a9a13dafe6a9041ac9eb9ff8e0))


### ⚙️ Continuous Integration

* **orca:** add workflow job to automatically manage stage-to-prod release candidate pull requests ([3c845a3](https://github.com/Prospect-Development-Team/plane-orca/commit/3c845a3c1f1f9dbda87ea78c5abac2b661d37484))
* **orca:** migrate PR labeler and template logic into the staging workflow and remove redundant labeler action ([12f8fef](https://github.com/Prospect-Development-Team/plane-orca/commit/12f8fefa75c9c1ae83ad8e3c2f9441b72d2b435a))


### 📦 Build System & Dependencies

* **orca:** add service healthchecks, update redis to valkey-cli, and correct healthcheck exclusion keys in docker-compose ([d204d65](https://github.com/Prospect-Development-Team/plane-orca/commit/d204d65ff2d431d656b004b4b18034c93a2e1830))
* **orca:** use exec for service process execution in docker entrypoints to ensure proper signal handling ([4a65056](https://github.com/Prospect-Development-Team/plane-orca/commit/4a65056a5e1408f9b95003b078203f9cad5ac7b1))

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
