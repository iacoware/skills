# Evaluation instructions

- External provider runs may consume quota or generate costs. Run the dry-run first, report the
  exact external-call count, and obtain explicit user authorization for that run before passing
  `--confirm-send` or sending provider requests. Approval of implementation or run strategy is not
  authorization to send.
- Authentication probes inside the agent sandbox may be false negatives because credentials or the
  system keychain are isolated. If an in-sandbox probe reports unauthenticated, rerun only the
  provider's read-only authentication-status command outside the sandbox with approval before
  reporting a blocker. Never expose account identifiers or credentials.
