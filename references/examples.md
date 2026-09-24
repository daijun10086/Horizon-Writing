# Before and after

Each example shows a typical piece of AI writing, what is wrong with it, and a rewrite. The rewrites invent concrete details (numbers, names, dates) to show where such details belong. When you rewrite real text, use the real details, and if you do not know them, ask or say plainly that they are missing. Never make them up.

## 1. A status update

**Before**

> Root-caused the regression — the gate on the fast path was load-bearing. Shipped a fix; perf is back within budget. Honest take: we got lucky here.

**What is wrong.** The reader does not know which regression, which gate, which fast path, or what "within budget" means. "Load-bearing," "shipped," "budget," and "honest" are metaphors and self-vouching that stand in for information. The fragments leave out the reasoning.

**After**

> I found why the nightly benchmark became 18% slower after Tuesday's merge. The merge added a permission check to the function that handles cache hits. That function runs on every request, so the check added about 40 ns to each one. I moved the check to where cache entries are created, which happens once per entry instead of once per request. The fix is merged, and the benchmark is back within 1% of its previous speed.

## 2. A commit message

**Before**

> Fix race + harden gating logic. Pure refactor otherwise.

**What is wrong.** "Race" is fine as a technical term, but the message does not say which data races or what the effect was. "Harden gating logic" is a metaphor with no content. "Pure refactor" asks the reader to trust that nothing else changed.

**After**

> Take the queue lock before reading `pending_count`
>
> Two worker threads could read `pending_count` at the same time and both decide the queue was empty, so one job would wait until the next timer tick (up to 5 s). The reader now holds the queue lock. The rest of the diff renames `chk_ready` to `is_ready` and does not change behavior.

## 3. A paragraph in a paper

**Before**

> Our approach is foundational: it offers a principled, robust, and scalable framework that fundamentally rethinks memory disaggregation. It's not just faster — it's a new paradigm.

**What is wrong.** Every adjective is a claim with no evidence behind it. The reader still does not know what the approach does. "Not just faster, it's a new paradigm" contrasts with a claim nobody made.

**After**

> Our system lets a server use memory on another machine as if it were local. Instead of fetching whole 4 KB pages over the network, it fetches individual 64-byte cache lines, so a program that touches one field of a large object moves 64 times less data. On the six workloads in Section 5, this cuts the slowdown from remote memory from 3.1x to 1.4x.

## 4. An answer to "why is my training loss NaN?"

**Before**

> Great question! Several factors could be at play:
> - **Learning rate:** too high
> - **Data:** possible NaNs
> - **Numerics:** fp16 overflow
>
> Let me know if you'd like me to dive deeper!

**What is wrong.** The opening praise and the closing offer are framing that adds nothing. The bullets are fragments with no explanation of how to tell which cause applies, which is the thing the reader needs.

**After**

> The loss usually becomes NaN for one of three reasons, and you can tell them apart by when it happens. If it happens in the first few steps, check the data: a single NaN or infinite value in the inputs or labels spreads through the whole batch, and `torch.isnan(batch).any()` will find it. If the loss grows for a while and then jumps to NaN, the learning rate is probably too high; try dividing it by 10. If you train in fp16 and the loss is NaN from time to time rather than all at once, values are overflowing the fp16 range, and turning on loss scaling (for example `torch.cuda.amp.GradScaler`) usually fixes it.

## 5. A code review comment

**Before**

> This is a hazard. Needs a forensic look at the provenance of `cfg` before we can certify it.

**What is wrong.** The comment does not say what could go wrong or what the author should do. "Hazard," "forensic," "provenance," and "certify" make a small request sound like an investigation.

**After**

> `cfg` comes straight from the request body here, so a client could set `max_workers` to any value, including a very large one that would exhaust memory. Could you clamp it to the range in `limits.py` (1 to 64) before using it?

## 6. An email to an advisor

**Before**

> Quick update: the ablation settled it. Hypothesis confirmed, the prefetcher wins. Will sharpen the draft and circle back.

**What is wrong.** The advisor may have several students and several projects. They need to know which ablation, what it compared, and what the numbers were. "Settled," "hypothesis confirmed," "wins," and "sharpen" replace the result with a verdict.

**After**

> Hi Professor Lee,
>
> I finished the ablation for the prefetching paper. I turned off each of the three parts of the prefetcher in turn and reran the SPEC CPU2017 memory-bound benchmarks. Removing the stride detector cost the most (a 9% average slowdown), while removing the other two parts cost less than 2% each. This supports our claim in Section 3 that most of the benefit comes from stride detection. I will update Section 5 with these numbers and send you the revised draft by Friday.
>
> Best,
> Mei

## 7. Undefined abbreviations and internal names

**Before**

> The RSB fix in `ktrace2` should unblock the PRR work; FWIW the IPC delta is within noise.

**What is wrong.** Unless every reader works on this exact project, RSB, PRR, `ktrace2`, and IPC need explaining, and "FWIW" is chat shorthand. "Within noise" needs the size of the noise.

**After**

> We fixed a bug in how our kernel tracing tool (`ktrace2`) records the return stack buffer (RSB), the small hardware structure that predicts where function returns go. With correct RSB traces we can continue the return-prediction study. The fix changes instructions per cycle (IPC) by 0.3%, which is less than the 0.5% run-to-run variation we see without any change.

## 8. Hedging and stacked qualifiers

**Before**

> This may potentially help to some extent in certain scenarios, though results could vary.

**What is wrong.** Four hedges and no content. The reader cannot tell when it helps or by how much.

**After**

> This helps when most requests hit the cache: at a 90% hit rate it cut median latency by 30% in our tests. At hit rates below 50% we saw no change.

## 9. Explaining a table in a results section

**Before**

> Table 3 summarizes the results. As shown, our approach achieves the best trade-off, highlighting its effectiveness.

**What is wrong.** The text only points at the table. It does not say what the rows and columns are, which entry matters, why, or what follows from it. "Best trade-off" is a verdict without the numbers behind it. See `explaining-figures.md` for the three-level method (describe, explain why, say what it implies).

**After**

> Table 3 lists, for each of the four cache designs (rows), the average miss rate and the chip area it needs (columns), measured on the 12 SPEC CPU2017 benchmarks. Our design has the second-lowest miss rate, 4.1%, only 0.2 points above the largest design, while using 38% less area. It gets close to the largest design because most of the misses the larger cache avoids come from a few streaming benchmarks, and our design already skips caching their data. So when chip area is limited, adding capacity beyond our design would reduce misses very little for the area it costs.
