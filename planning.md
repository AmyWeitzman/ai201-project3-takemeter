# TakeMeter — Project Planning

## Community

My chosen community is [r/TopChef](https://www.reddit.com/r/TopChef/). It's a subreddit for a  cooking competition reality show where fans discuss episodes, contestants, judging decisions, etc. 

My chosen labels are analysis, opinion, and discussion. These labels are relevant to this community's posts because fans:

1) like to analyze competition stats and compare across seasons, locations, etc
2) have strong opinions on contestants' cooking skills, the competition winners, show production, and dish quality
3) want to engage with others in a shared love of cooking.

---

## Labels

### 1. `analysis`

**Definition:** The post makes a specific claim and backs it up with concrete evidence (ex: episode details, statistics, cross-season comparisons, or domain expertise) such that the reader can point to the supporting material in the text. Self-reported counts ("I tallied it across 4 seasons") qualify as evidence if the methodology is described, since the reader could in theory replicate it. Posts that present data without stating a conclusion are `discussion`, not `analysis`.

**Examples:**

1. *"Canada? More like soundstageada"* — The author literally counts how many of the season's challenges took place outdoors vs. on a soundstage (2 outdoor out of 10 episodes), then argues the season fails to show Canada. The evidence is stated clearly.
2. *"Canada Fantasy Points so far + the S22 leader vs. the Top Chef Greats (Ep 10)"* — Tracks fantasy point totals across contestants and compares one contestant's numbers to past dominant chefs with specific figures.

---

### 2. `opinion`

**Definition:** The post expresses a clear viewpoint or take but asserts rather than argues, the claim is present but little to no concrete evidence is offered to support it.

**Examples:**

1. *"I prefer Kirsten to Padma"* — States a preference directly with minimal elaboration ("she just gives it such a warm vibe and is way more sympathetic to the contestants"). A clear viewpoint, zero supporting evidence.
2. *"This season should be renamed Top Chef: Toronto"* — Asserts the season fails to represent all of Canada, with a general observation but no episode count or specific comparison to back it up. Confident, unsupported claim.

---

### 3. `discussion`

**Definition:** The post is not primarily making a claim, it is inviting community participation through a question, hypothetical prompt, or personal experience shared with the group. Posts that build a full argument and then ask "does anyone agree?" are `opinion` — the question must be the point, not a wrapper around a take.

**Examples:**

1. *"Restaurant Wars Dream Team"* — Asks readers to pick any 4 chefs from any season for their ideal Restaurant Wars team. Pure hypothetical prompt; the author shares their own picks as a conversation starter, not a take to be defended.
2. *"I ate at Massimo's Restaurant"* — A personal dining experience at a contestant's Montreal restaurant. The author is sharing, not arguing; there is no claim that needs to be evaluated as true or false.

---

## Hard Edge Cases

1. *"Top Chef Season 1 – San Francisco"* — A long, structured episode-by-episode review with clearly labeled pros/cons sections and specific references to challenges and contestants. It reads like analysis, but the "evidence" is mostly personal recollection rather than verifiable data. Labeled `analysis` because the structure and specificity are closer to that camp than to an assertion, but a reasonable person could call it a detailed `opinion`.

2. *"The constant, blatant sponsorships are diluting the value of the show"* — Lists specific sponsors by name (BMW, Chipotle, Saratoga Springs, Whole Foods, Wells Fargo) and mentions the author works in marketing. The specificity and domain expertise push it toward `analysis`,  but someone could argue the core claim ("diluting the value") is still a subjective assertion without measurable evidence.

3. *"Seafood pizza?"* — Opens as a genuine question ("Is seafood pizza really uncommon in North America?") but then provides cultural context from the author's own background suggesting it is common elsewhere. It hovers between a discussion prompt and a soft opinion. Labeled `discussion` because the post is oriented toward asking the community, not asserting a position, but the cultural framing makes it the closest thing to an `opinion` in the discussion pile.

---

## Data Collection Plan

Examples will be collected from [r/TopChef](https://www.reddit.com/r/TopChef/) using the Pullpush.io public Reddit archive, filtering for text-only posts (no link-only posts) to ensure every example has a body with substantive content for effectively classifying it. 

I would like to collect a roughly even amount of each label type if possible, but if it's skewed, have no more than 50% be of one label type and have at least 25% of each.

If a label is underrepresented, I will try to collect additional posts that would be classified with that label.

---

## Evaluation Metrics

**Primary metric: macro F1-score.** Accuracy alone is misleading here because the classes might be imbalanced. For instance, if one label covers 80% of posts, then the classifier would have 80% accuracy if it just predicted the same label each time, which sound good but really isn't performing classification properly. Macro F1 averages F1 across all three classes equally, so poor performance on the underrepresented classes will drag the score down and be visible, rather than hidden.

**Secondary metric: per-class F1.** Macro F1 gives one number, but per-class F1 shows where the model is failing. For instance, if `analysis` F1 is 0.40 while `opinion` and `discussion` are both above 0.80, that's a signal to collect more `analysis` examples or revisit the label boundary.

**Confusion matrix.** Useful for catching systematic errors, especially the most likely confusion: `opinion` being misclassified as `analysis` (or vice versa), since those two share the property of making a claim. If the model confuses `analysis` with `discussion`, that would suggest the definition of `analysis` isn't being captured at all and the label boundary needs rethinking.

---

## Definition of Success

A macro F1-score above 0.75 across all three classes would indicate the classifier is genuinely learning the distinctions and not just defaulting to the majority class.

For deployment in a real community tool, the per-class F1 should be above 0.70 for every label individually so that the tool doesn't systematically mislabel underrepresented post types. Below that threshold, the classifier is too unreliable and usres won't trust it. A model that hits 0.85+ macro F1 with balanced per-class scores would be strong enough to use in a real subreddit context without significant manual review.

---

## AI Tool Plan

### 1. Label Stress-Testing

I'll provide Claude with the 3 label definitions and an edge case descsription and ask it to generate posts that sit at the boundary between two labels.

Eight posts were generated across 3 boundaries:

**opinion-analysis boundary:**

- *"I tallied it — French-technique dishes placed in the top 3 roughly twice as often as Asian cuisines across the last four seasons."* - Has numbers, but they're self-reported and unverifiable. The original `analysis` definition ("the reader can point to supporting material in the text") didn't distinguish between external verifiable data and personal observation counts. Thus, this is unclassifiable under the original definition.
- *"Watching eliminations back-to-back, Tom interrupted contestants 6 times in the first four episodes of S19 vs twice in the last four."* - Same issue: a specific count from personal re-watch, not from an external source.

**discussion-opinion boundary:**

- *"I found the Canada season repetitive by episode 8 — the challenges felt redundant and I didn't learn about Canadian food. Is this just me? Genuine question."* - The entire body is a negative argument; the question softens it a bit. The original `discussion` definition ("not primarily making a claim") handled this correctly in spirit, but wasn't explicit enough to make the call obvious.
- *"What would you have done on the poutine challenge? I'd have gone traditional because that's what the judges always come back to on regional dishes."* - Question framing wrapping a clear opinion.

**analysis-discussion boundary:**

- *"Of the 11 James Beard nominees who appeared on Top Chef, 4 made the finale and 2 won — higher than the ~8% win rate among all contestants. Curious if others have tracked this."* - Has data and an implicit claim, but the author doesn't state a conclusion. Presents numbers and invites others to interpret them.

**What the stress-test revealed — three gaps in the original definitions:**

1. **Self-reported counts**: The `analysis` definition didn't specify whether personal tallies count as evidence. 

    **Fix:** self-reported counts qualify if the methodology is described (the reader could replicate it). Added to the `analysis` definition.

2. **Question-wrapped opinions**: The `discussion` definition's "not primarily making a claim" qualifier was wasn't explicit enough. 

    **Fix:** added a rule that posts which build a full argument and then ask "does anyone agree?" are `opinion` - the question must be the point, not a wrapper. Added to the `discussion` definition.

3. **Data without a stated conclusion**: A post that presents numbers but doesn't assert what they mean is `discussion`, not `analysis`.

    **Fix:** added this clarification to the `analysis` definition.

---

### 2. Annotation Assistance

I will use Claude to label the first 20 posts in the dataset.Then I will manually review those labels. Depending on whether that sample had a balanced distrubtion of labels, I may do another round of this using the next 20 posts.

---

### 3. Failure Analysis Plan

After training, the full list of wrong predictions (predicted label, true label, and post text) will be exported and given to Claude with this prompt: *"Here are posts my classifier got wrong. Identify any patterns in what's being confused - look for systematic errors by label pair, post length, writing style, or subject matter."*

What to look for:

- **opinion vs. analysis confusions**: Does the model conflate specificity (naming episodes, contestants) with evidence-backed argument? A post can be very specific and still be an unsupported assertion.
- **discussion vs. opinion confusions**: Does the model mistake question-framed opinions for genuine discussion prompts? Posts ending in "?" are not automatically `discussion`.
- **length bias**: Does the model label long posts as `analysis` regardless of whether they actually contain evidence?

After Claude identifies patterns, I'll verify each one manually by pulling a few examples of that pattern from the wrong-predictions list and checking whether the pattern holds. Patterns that appear in fewer than 3 examples will be discarded as noise.
