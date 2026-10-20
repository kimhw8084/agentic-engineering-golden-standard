# Interview defense bank — practice with evidence, not memorized slogans

## Backend/CS
1. What is the asymptotic cost of filtering then ranking N documents with V vocabulary terms? How would you profile it?
2. Design a parser that never accepts unknown recipe fields. Why reject boolean as integer in Python?
3. Explain uniqueness and idempotency with concurrent writers and retries.
4. When should a DB transaction replace an in-memory state machine?
5. What happens to latency and consistency when a cache uses revision-blind keys?
6. Explain indices, query plans, cardinality estimates and partitioning on time-series data.
7. How do you handle DST and event time vs processing time in briefing scheduling?
8. Show a resource leak/deadlock/race you fixed. What proof demonstrates correctness?

## Agent/retrieval
9. How do BM25, vector similarity and reranking differ? Which fails on exact IDs?
10. Define Recall@k, MRR and nDCG with a concrete numerical example.
11. Why is a citation ID not proof that a specific generated claim is supported?
12. How do you distinguish no evidence from no record and from access denied?
13. Design version-aware retrieval for changed recipes and code commits.
14. When does multi-agent decomposition help, and when does it increase latency/errors?
15. How do you impose reliable limits on retries, tools, context and model budget?
16. How would you design an eval that reveals a model's unsupported root-cause claims?
17. How can you compare models fairly across variable answer quality and stochasticity?
18. What is the operational impact when embeddings lag deleted messages?

## Security/SRE
19. Why must authorization occur after the user prompt and before data access?
20. How can retrieved email lead to prompt injection even if email is "read only"?
21. What tests would prove that cache keys do not leak another employee's messages?
22. Design hash-bound approval and expiry; what about concurrent revisions?
23. Explain idempotency keys and exactly-once semantics limits.
24. How would you safely degrade when a model or embedding API is down?
25. What is your error budget and how would an SLO influence releases?
26. What fields may you log without exposing sensitive recipe/email content?

## Staff/leadership
27. Why did you choose a modular monolith over microservices or a graph database?
28. What were the rejected alternatives and observable tradeoffs?
29. Describe an incident where your initial model was wrong. How did evidence change it?
30. How did you show net engineering hours saved without double-counting review time?
31. How did you get owners of two independent systems to trust an integration?
32. Which API contract makes a project reusable outside metrology?
33. What did you implement *without* AI and how was it independently verified?
34. If you leave the company, how can the system be operated and improved safely?

## Answer rubric
A persuasive answer has mechanism → failure case → implementation tradeoff → measured evidence → limitations, ideally tied to code/tests you personally wrote. If any section is missing, mark the gap rather than improvising.
