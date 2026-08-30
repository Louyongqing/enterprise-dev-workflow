# Approved local task

This is a deliberately incomplete evaluation fixture, not production software.

Fix one-based pagination: page 1 starts with the first item, later pages do not overlap, and pages beyond the end are empty. Preserve the existing positive-value validation.

Add an optional inclusive `min_price` filter to `filter_rows`, composable with the category filter. `None` means no price restriction and zero is a real threshold. Preserve input order and do not mutate input data. The API is private to this fixture.

The behavior and local implementation are approved. Add meaningful regression tests and run the complete fixture suite. No network, dependencies, other agents, external actions, commits or source-repository changes are authorized.
