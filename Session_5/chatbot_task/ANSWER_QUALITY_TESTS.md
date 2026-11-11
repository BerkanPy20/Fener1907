# Answer quality tests – Issue #18

Configuration:
- Model: llama3.2:3b
- Temperature: 0
- Embeddings: bge-m3
- Retrieval: 12 candidates, up to 3 unique excerpts
- Prompt: separate system instruction and context; request context-based sentence extraction

Manual test results:
1. "What is supervised learning?"
   Correctly describes labeled training data, without the previous
   incorrect claim about learning without a teacher.

2. "What is unsupervised learning?"
   Correctly describes unlabeled data and learning without a teacher.
   The response repeats a statement.

3. "What did I eat for breakfast today?"
   Responds: "I don't know based on the provided context."

Sources were displayed for all three responses.

Limitations:
These three tests do not guarantee correctness for other questions.
Exact sentence copying is not consistently followed.
