# Interface design system

InsightPulse is a customer listening workspace. The overview pairs a wide temporal view with a compact sentiment composition; complaint categories link into the explorer, and urgent feedback has its own quieter rose surface. Existing React, Tailwind, Recharts and Lucide dependencies are retained.

## Tokens
- Canvas #14151b; navigation #191a21; surface #1b1c24; raised #23242e; border #30313c.
- Text #eeeef4; secondary #adafbd; muted #8d909f.
- Action lavender #b4a7fa, hover #c8baff, dark action text #242032.
- Positive mint #65c9ab; neutral amber #d6b773; negative rose #e18f9d. High/medium/low priority use rose/amber/mint with explicit text labels.
- Type: locally available Segoe UI Variable, Segoe UI, sans-serif. Page title 27px/600; panel title 14px/550; body 14px; metadata 10–12px. Tabular figures for metrics.
- Spacing: 4, 8, 12, 16, 20, 24, 32, 36px. Main width capped at 1500px; two unequal content columns, collapsing to one on tablets. Navigation becomes an icon rail at 800px.
- Corners: controls 6px, panels 9px. Borders define surfaces; no decorative shadows.
- Motion: 160–200ms cubic-bezier(.2,.8,.2,1); response to user actions only; reduced motion honored. Charts do not animate on mount.
- Interaction: visible 2px lavender focus ring; differentiated hover and pressed surfaces; disabled controls at 50% opacity. Indeterminate loading, actionable empty states, announced errors. No invented model readiness or progress percentages.

## Data integrity
Health reports configuration and API reachability, not whether transformer inference was used for a particular record. The API does not return per-record inference provenance; the interface must not infer it. Analytics remain server-generated; samples are only available through an explicit sample CSV download. No new backend contracts are required.
