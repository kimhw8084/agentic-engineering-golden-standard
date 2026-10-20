# Golden blueprint — fast mental model

```mermaid
flowchart TD
    A[Engineer request in OpenCode] --> B{Authorized engineering task?}
    B -- No --> X[Decline / seek approved access]
    B -- Yes --> C[Inspect existing repo and evidence]
    C --> D[Specify measurable acceptance and trust boundaries]
    D --> E[Choose smallest reversible design]
    E --> F[Implement one bounded change]
    F --> G{Tests + negatives + policy pass?}
    G -- No --> H[Fix or block with evidence]
    H --> F
    G -- Yes --> I[Measure quality, latency and labor impact]
    I --> J[Human code review + company release policy]
    J --> K[Independent mastery exercise + ADR]
    K --> L[Next high-impact backlog item]
```

For each independent application the production runtime follows a separate trust path:

```mermaid
flowchart TD
    U[Authenticated engineer] --> P[Trusted API / policy]
    P --> R[Permitted read-only adapters]
    R --> E[Versioned evidence + allowed retrieval]
    E --> M[Bounded model reasoning]
    M --> V[Typed deterministic validators]
    V --> H[Independent human review]
    H --> O[Reviewable output / existing controlled change system]
    M -. no direct write .-> Z[Production manufacturing systems]
```

The dashed line documents a *forbidden* link, not a permission. This starter cannot connect to the real endpoints shown. No enterprise service is implied by the diagrams.
