# Explaining a figure

This file summarizes Yuhao Zhu's post "How to Explain a Scientific Figure" (https://yuhaozhu.com/blog/explain-figure.html) in our own words and adds a worked example. Read the original for his full discussion; it walks through Figure 15 of Benjamin Lee's 2010 paper in *ACM Transactions on Architecture and Code Optimization* (TACO) as its example.

## The idea

A good figure can say more than a hundred words, but a figure placed in a paper without an explanation confuses readers and wastes space. The post is not about how to design a figure (for that, it recommends Edward Tufte's articles and books). It is about how to explain a figure in the text, assuming the figure itself is well made.

The goal is to lead the reader to the information you want them to take from the figure, instead of leaving them to work it out alone. Zhu describes the explanation as a hierarchy with three levels, done in order.

## Level 1: Describe what the figure shows

Start by saying what the figure is about. Say what the x-axis and y-axis are, what each marker, line, or bar stands for, and which observation or trend you want the reader to focus on. The description should be a short text version of the figure that carries the same meaning and quickly gives the reader the context.

In the post's example, the first sentence of the paper's explanation says what is plotted (delay against power for nine architectures, each running its own benchmark). The next sentences point out the one pattern the authors care about: the architectures fall into clusters in different regions of the plot, and each cluster has a different pipeline depth and width.

## Level 2: Explain why

After describing the observation, explain why it happens. In the example, shallow and narrow pipelines sit in the corner with long delay and low power because they have little computing capability, which makes them slow and also keeps their power low.

The paper in the example skips this step, because readers in that field can connect pipeline depth and width to delay and power on their own. Skip it only when the reason is obvious to your readers. When it is not obvious, the explanation is necessary.

## Level 3: Say what it implies

Finally, when you can, say what the data teaches beyond the figure itself. This step is optional, and writers sometimes leave it out to keep the text flowing, but good writers include it whenever they have an insight to offer. In the example, the paper observes that the architectures cluster by their microarchitecture. It then draws an implication for hardware accelerators: when there are not enough resources to build one accelerator per program, a single "compromise" accelerator can serve a group of similar programs.

## Summary

Explaining a figure means guiding the reader: describe what the figure shows, explain why the data looks that way, and point out what it implies, which can suggest a direction for future work.

## A worked example

The following example is not from the post. It shows the three levels applied to a typical results figure in a computer architecture paper.

**Before**

> Figure 7 shows the results. Our prefetcher performs well across the board, with some variation.

This tells the reader nothing that the figure does not, and "some variation" leaves them to find and interpret the variation alone.

**After**

> Figure 7 shows the speedup of our prefetcher over a system with no prefetching (y-axis) for each of the 12 SPEC CPU2017 benchmarks (x-axis). The rightmost bar is the geometric mean. The prefetcher speeds up every benchmark, by 1.31x on average, but the gains split into two groups: the five benchmarks on the left gain more than 1.5x, while the other seven gain less than 1.1x. *(Describe.)*
>
> The split follows how each benchmark accesses memory. The five benchmarks that gain the most walk through large arrays in a regular order, so the prefetcher can predict their next accesses. The other seven mostly follow pointers, and their next address is not known until the current load finishes. *(Explain why.)*
>
> This suggests that the remaining opportunity lies in pointer-heavy programs, which a stride-based design cannot help. We return to this in Section 7. *(Implication.)*

## Checklist for every figure and table

- Does the text refer to the figure by number and explain it, instead of only pointing to it ("see Figure 7")?
- Does the text say what the axes, units, and each marker, line, or bar stand for, and what the baseline is?
- Does it name the one observation the reader should take from the figure?
- Does it explain why the data looks that way, unless the reason is obvious to the intended readers?
- Does it say what the result implies, when there is something useful to say?

The same three levels work for tables: say what the rows and columns are, point out the entry or pattern that matters, explain it, and say what it implies.
