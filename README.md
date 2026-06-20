# Take Meter

TakeMeter: a fine-tuned text classifier that evaluates discourse quality in an online community of your choosing.

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

## Data Collection

### Data Collection Source

Examples were collected from [r/TopChef](https://www.reddit.com/r/TopChef/) using the Pullpush.io public Reddit archive, filtering for text-only posts (no link-only posts) to ensure every example has a body with substantive content for effectively classifying it. I asked Claude to write the code to fetch the posts and run it (including subsequent times when I collected more data).

### Labeling Process

I gave Claude the label definitions and the dataset (csv file) and asked it to write initial labels for the first 20 posts so I could then review whether it understood the distinction between the labels well. I reviewed it's classification results and it got them all correct except 2, which were borderline anyway. I adjusted those labels manually. But, since my dataset is a little unbalanced, there were only 2 analysis posts in Claude's initial labeling dataset so I wanted to be sure it really understand that label since it could easily be confused for opinion, so I asked it to label an additional 20 posts, which it got all correct except for 1 which again was borderline and I changed manually. Finally, I asked it to label all 200+ posts and included explanations of the labels I changed manually so it would know how to evaluate borderline ones like those. I reviewed it's final results and there were only 2 I adjusted further.

### Label Distribution

My dataset was a little unbalanced as far as labels because the frequency of certain post types varies in this forum. As I evaluated the model's performance, I increased the number of posts in the dataset to help address certain issues. Below is the initial label distribution; the adjustments I made later are described in the [Evaluation Report](#evaluation-report) section within each **Iteration** section.

| Label | # of Posts | Percentage |
| ----- | ---------- | ---------- |
| analysis | 26 | 13% |
| opinion | 76 | 38% |
| discussion | 98 | 49% |
| **Total** | **200** | **100%** |

### Label Edge-Cases

1. *"Top Chef Season 1 – San Francisco"* — A long, structured episode-by-episode review with clearly labeled pros/cons sections and specific references to challenges and contestants. It reads like analysis, but the "evidence" is mostly personal recollection rather than verifiable data. Labeled `analysis` because the structure and specificity are closer to that camp than to an assertion, but a reasonable person could call it a detailed `opinion`.

2. *"The constant, blatant sponsorships are diluting the value of the show"* — Lists specific sponsors by name (BMW, Chipotle, Saratoga Springs, Whole Foods, Wells Fargo) and mentions the author works in marketing. The specificity and domain expertise push it toward `analysis`, but someone could argue the core claim ("diluting the value") is still a subjective assertion without measurable evidence.

3. *"Seafood pizza?"* — Opens as a genuine question ("Is seafood pizza really uncommon in North America?") but then provides cultural context from the author's own background suggesting it is common elsewhere. It hovers between a discussion prompt and a soft opinion. Labeled `discussion` because the post is oriented toward asking the community, not asserting a position, but the cultural framing makes it the closest thing to an `opinion` in the discussion pile.

---

## Baseline

**Model**: `llama-3.3-70b-versatile` (Groq)

### System Prompt

```
You are classifying posts from the TopChef community in Reddit (r/TopChef).
Assign each post to exactly one of the following categories.

analysis: The post makes a specific claim and backs it up with concrete evidence (ex: episode details, statistics, cross-season comparisons, or domain expertise) such that the reader can point to the supporting material in the text. Self-reported counts ("I tallied it across 4 seasons") qualify as evidence if the methodology is described, since the reader could in theory replicate it. Posts that present data without stating a conclusion are `discussion`, not `analysis`.
Example: "Canada? More like soundstageada — The author literally counts how many of the season's challenges took place outdoors vs. on a soundstage (2 outdoor out of 10 episodes), then argues the season fails to show Canada. The evidence is stated clearly."

opinion: The post expresses a clear viewpoint or take but asserts rather than argues, the claim is present but little to no concrete evidence is offered to support it.
Example: "I prefer Kirsten to Padma — States a preference directly with minimal elaboration ("she just gives it such a warm vibe and is way more sympathetic to the contestants"). A clear viewpoint, zero supporting evidence."

discussion: The post is not primarily making a claim, it is inviting community participation through a question, hypothetical prompt, or personal experience shared with the group. Posts that build a full argument and then ask "does anyone agree?" are `opinion` — the question must be the point, not a wrapper around a take.
Example: "Restaurant Wars Dream Team — Asks readers to pick any 4 chefs from any season for their ideal Restaurant Wars team. Pure hypothetical prompt; the author shares their own picks as a conversation starter, not a take to be defended."

Respond with ONLY the label name.
Do not explain your reasoning.

Valid labels:
analysis
opinion
discussion
```

**Results**

🎯 **Baseline accuracy**: 0.600 (evaluated on 30/30 parseable responses)

**Per-class metrics** (baseline):

| class | precision | recall | f1-score | support |
| --- | --- | --- | --- | --- |
| analysis | 0.00 | 0.00 | 0.00 | 4 |
| opinion | 0.64 | 0.58 | 0.61 | 12 |
| discussion | 0.61 | 0.79 | 0.69 | 14 |
| accuracy | | | 0.60 | 30 |
| macro avg | 0.42 | 0.46 | 0.43 | 30 |
| weighted avg | 0.54 | 0.60 | 0.56 | 30 |

---

## Fine-Tuning

**Base Model**: `distilbert-base-uncased` on Google Colab (T4 GPU)

**Training Set Up**

The dataset was split 70%/15%/15% into training, validation, and testing sets, including stratification so each split has roughly the same label distribution. Each split was tokenized. Training was run on Google Colab using a T4 GPU.

**Hyperparameter Decisions**

- **number of epochs**: used initial value of `3` because that's a good default for small datasets; if the number is too high, you risk overfitting
- **learning rate**: used initial value of `2e-5` because that's the standard starting point for fine-tuning BERT-family models
- **batch size**: used initial value of `16` because that is a good balance of speed and accuracy, and it fits the T4 GPU comfortably

---

## Evaluation Report

The fine-tuned model wasn't performing well so I iterated on my approach multiple times, adjusting the dataset and hyperparameters based on the results to try to improve performance. Below is a walkthrough of each iteration, including the adjustments I made to dataset and model that round, the performance metrics and confusion matrix, and an analysis of wrong label classifications, which helped guide adjustments made in future iterations.

---

### Iteration 1

This was my initial run on my original dataset and system prompt.

**Dataset**

| Label | # of Posts | Percentage |
| ----- | ---------- | ---------- |
| analysis | 26 | 13% |
| opinion | 76 | 38% |
| discussion | 98 | 49% |
| **Total** | **200** | **100%** |

**Note**: `analysis` is underrepresented relative to the other two labels, which reflects the fact that evidence-backed posts are rarer in this community.

#### System Prompt (Iteration 1)

```
You are classifying posts from the TopChef community in Reddit (r/TopChef).
Assign each post to exactly one of the following categories.

analysis: The post makes a specific claim and backs it up with concrete evidence (ex: episode details, statistics, cross-season comparisons, or domain expertise) such that the reader can point to the supporting material in the text. Self-reported counts ("I tallied it across 4 seasons") qualify as evidence if the methodology is described, since the reader could in theory replicate it. Posts that present data without stating a conclusion are `discussion`, not `analysis`.
Example: "Canada? More like soundstageada — The author literally counts how many of the season's challenges took place outdoors vs. on a soundstage (2 outdoor out of 10 episodes), then argues the season fails to show Canada. The evidence is stated clearly."

opinion: The post expresses a clear viewpoint or take but asserts rather than argues, the claim is present but little to no concrete evidence is offered to support it.
Example: "I prefer Kirsten to Padma — States a preference directly with minimal elaboration ("she just gives it such a warm vibe and is way more sympathetic to the contestants"). A clear viewpoint, zero supporting evidence."

discussion: The post is not primarily making a claim, it is inviting community participation through a question, hypothetical prompt, or personal experience shared with the group. Posts that build a full argument and then ask "does anyone agree?" are `opinion` — the question must be the point, not a wrapper around a take.
Example: "Restaurant Wars Dream Team — Asks readers to pick any 4 chefs from any season for their ideal Restaurant Wars team. Pure hypothetical prompt; the author shares their own picks as a conversation starter, not a take to be defended."

Respond with ONLY the label name.
Do not explain your reasoning.

Valid labels:
analysis
opinion
discussion
```

**Metrics**

🎯 **Baseline accuracy**: 0.600 (evaluated on 30/30 parseable responses)

**Per-class metrics** (baseline):

| | precision | recall | f1-score | support |
|---|---|---|---|---|
| analysis | 0.00 | 0.00 | 0.00 | 4 |
| opinion | 0.64 | 0.58 | 0.61 | 12 |
| discussion | 0.61 | 0.79 | 0.69 | 14 |
| accuracy | | | 0.60 | 30 |
| macro avg | 0.42 | 0.46 | 0.43 | 30 |
| weighted avg | 0.54 | 0.60 | 0.56 | 30 |

<br>

🎯 **Fine-tuned model accuracy**: 0.467

**Per-class metrics** (fine-tuned model):

| | precision | recall | f1-score | support |
|---|---|---|---|---|
| analysis | 0.00 | 0.00 | 0.00 | 4 |
| opinion | 0.00 | 0.00 | 0.00 | 12 |
| discussion | 0.47 | 1.00 | 0.64 | 14 |
| accuracy | | | 0.47 | 30 |
| macro avg | 0.16 | 0.33 | 0.21 | 30 |
| weighted avg | 0.22 | 0.47 | 0.30 | 30 |

<br>

**Results Comparison**

| Model | Accuracy |
|---|---:|
| Zero-shot baseline (Groq) | 0.600 |
| Fine-tuned DistilBERT | 0.467 |

Fine-tuning regression: -0.133

<br>

**Confusion Matrix**

| | Pred: analysis | Pred: opinion | Pred: discussion |
|---|---|---|---|
| **True: analysis** | 0 | 0 | 4 |
| **True: opinion** | 0 | 0 | 12 |
| **True: discussion** | 0 | 0 | 14 |

<br>

**3 Wrong Predictions**

The fine-tuned model predicted `discussion` for all 30 test posts, indicating it was just predicting the  majority class as that led to maximal accuracy. All 4 analysis posts and all 12 opinion posts were classified as `discussion`. Below are three representative examples of the types of errors this produced and why the model was confused.

1. **"Differences in International Versions of Top Chef"** (true: `analysis`, predicted: `discussion`)

   > *"What are some differences you've noticed between the U.S. version of Top Chef and international ones? I just finished watching the most recent (aired 2023) season of Top Chef Thailand..."*

   The title reads exactly like a community discussion prompt — "What are some differences you've noticed?" The post then provides specific observations comparing the U.S. and Thai versions, but the question framing dominates the first impression. With `discussion` making up 49% of training data, the model never learned to look past an opening question for the evidence that follows it.

2. **"Air time algorithm"** (true: `opinion`, predicted: `discussion`)

   > *"Has anyone else noticed that whoever gets the most airtime on the episode is usually the one that gets eliminated?"*

   "Has anyone else noticed" is one of the strongest discussion-framing phrases on Reddit - it's an explicit invitation for community confirmation. The post is actually making a specific editorial claim about the show's production patterns, but the model saw the question opener and stopped there. This is the question-wrapped opinion edge case: the post is asserting a take, but wraps it in community-engagement language.

3. **"My Pet Peeve Watching Top Chef"** (true: `opinion`, predicted: `discussion`)

   > *"I get so frustrated when after somebody is eliminated other people will then say now we're getting down to the best chefs."*

   This is a direct personal take with no question and no explicit invitation, but the "watching" framing and emotional reaction ("I get so frustrated") read like a casual community reaction share rather than an assertive claim. Since there is 49% `discussion` in the training set, the model defaulted to that label for any post that didn't exhibit unusually strong evidence signals.

**Root cause**: Not a labeling or definition problem. The model minimized training loss by predicting `discussion` every time, with only 4 analysis training examples after the train/test split, it had no signal to learn that class. Confidence scores across all predictions were low (~30–40%), showing the model wasn't confident in any direction, it was just collapsing to the majority class.

**Sample Classifications**

1. *"Restaurant Wars Dream Team — Asks readers to pick any 4 chefs from any season for their ideal Restaurant Wars team."*
   - **True Label**: discussion
   - **Predicted Label**: discussion ✓
   - **Confidence**: 0.46
   - **Explanation**: A pure community hypothetical with no claim - the model correctly classifies it, and the relatively higher confidence (vs. wrong predictions) shows the model is most certain on classic discussion patterns.

2. *"Canada? More like soundstageada — The author counts how many of the season's challenges took place outdoors vs. on a soundstage (2 outdoor out of 10 episodes), then argues the season fails to show Canada."*
   - **True Label**: analysis
   - **Predicted Label**: discussion ✗
   - **Confidence**: 0.36
   - **Explanation**: Despite containing a specific episode count and a clear conclusion, the model treats this as a discussion post - even a very clear analysis example isn't enough to overcome the majority-class prediction issue.

3. *"Air time algorithm — Has anyone else noticed that whoever gets the most airtime on the episode is usually the one that gets eliminated?"*
   - **True Label**: opinion
   - **Predicted Label**: discussion ✗
   - **Confidence**: 0.33
   - **Explanation**: "Has anyone else noticed" is a common discussion opener; the model stops there and never processes the claim being made about production patterns.

4. *"My Pet Peeve Watching Top Chef — I get so frustrated when after somebody is eliminated other people will then say now we're getting down to the best chefs."*
   - **True Label**: opinion
   - **Predicted Label**: discussion ✗
   - **Confidence**: 0.38
   - **Explanation**: A direct personal take with no question and no invitation, but the "watching" + "I get so frustrated" framing pattern-matches to a reaction being shared with the community rather than an opinion being asserted.

5. *"Differences in International Versions of Top Chef — What are some differences you've noticed between the U.S. version of Top Chef and international ones?"*
   - **True Label**: analysis
   - **Predicted Label**: discussion ✗
   - **Confidence**: 0.35
   - **Explanation**: The question-title format is treated as a community discussion invitation; the specific observations about the Thai version in the body are never reached.

---

### Iteration 2

**Changes**

- Added 14 more `analysis` posts - mostly long episode-by-episode season recaps plus a few structured arguments, which are the clearest possible analysis examples since they have explicit evidence for every claim
- Added a second `analysis` example to the system prompt that more clearly shows what analysis looks like: a specific quote with an episode number, and a structural argument listing specific episode restrictions as evidence

**Dataset**

| Label | # of Posts | Percentage |
| ----- | ---------- | ---------- |
| analysis | 40 | 19% |
| opinion | 76 | 36% |
| discussion | 98 | 46% |
| **Total** | **214** | **100%** |

#### System Prompt (Iteration 2)

```
You are classifying posts from the TopChef community in Reddit (r/TopChef).
Assign each post to exactly one of the following categories.

analysis: The post makes a specific claim and backs it up with concrete evidence (ex: episode details, statistics, cross-season comparisons, or domain expertise) such that the reader can point to the supporting material in the text. Self-reported counts ("I tallied it across 4 seasons") qualify as evidence if the methodology is described, since the reader could in theory replicate it. Posts that present data without stating a conclusion are `discussion`, not `analysis`.
Example: "Did Season 9 have the worst group of chefs skills-wise? — 7 episodes in and the cooking is uninspired. Tom said it himself at the end of Episode 7: 'We chose 16 chefs and quite frankly I'm starting to think maybe I chose the wrong chefs.' The challenges aren't helping either — canned items from survivor kits don't showcase individual skill."
Example: "Most Overcomplicated Challenges — the Seattle quickfire had three simultaneous random rules: make a holiday dish from your family, use Truvia, and share one knife between everyone. Top Chef Masters S1 changed the venue mid-challenge without explanation, creating food safety issues. What other episodes felt set up to fail?"

opinion: The post expresses a clear viewpoint or take but asserts rather than argues, the claim is present but little to no concrete evidence is offered to support it.
Example: "I prefer Kirsten to Padma — States a preference directly with minimal elaboration ("she just gives it such a warm vibe and is way more sympathetic to the contestants"). A clear viewpoint, zero supporting evidence."

discussion: The post is not primarily making a claim, it is inviting community participation through a question, hypothetical prompt, or personal experience shared with the group. Posts that build a full argument and then ask "does anyone agree?" are `opinion` — the question must be the point, not a wrapper around a take.
Example: "Restaurant Wars Dream Team — Asks readers to pick any 4 chefs from any season for their ideal Restaurant Wars team. Pure hypothetical prompt; the author shares their own picks as a conversation starter, not a take to be defended."

Respond with ONLY the label name.
Do not explain your reasoning.

Valid labels:
analysis
opinion
discussion
```

**Metrics**

🎯 **Baseline accuracy**: 0.636 (evaluated on 33/33 parseable responses)

**Per-class metrics** (baseline):

| | precision | recall | f1-score | support |
|---|---|---|---|---|
| analysis | 1.00 | 0.33 | 0.50 | 6 |
| opinion | 0.60 | 0.50 | 0.55 | 12 |
| discussion | 0.62 | 0.87 | 0.72 | 15 |
| accuracy | | | 0.64 | 33 |
| macro avg | 0.74 | 0.57 | 0.59 | 33 |
| weighted avg | 0.68 | 0.64 | 0.62 | 33 |

*Baseline went up slightly - adding the second analysis example to the system prompt improved LLM precision on analysis posts (1.00), though recall is still low.*

<br>

🎯 **Fine-tuned model accuracy**: 0.424

**Per-class metrics** (fine-tuned model):

| | precision | recall | f1-score | support |
|---|---|---|---|---|
| analysis | 0.00 | 0.00 | 0.00 | 6 |
| opinion | 0.00 | 0.00 | 0.00 | 12 |
| discussion | 0.44 | 0.93 | 0.60 | 15 |
| accuracy | | | 0.42 | 33 |
| macro avg | 0.15 | 0.31 | 0.20 | 33 |
| weighted avg | 0.20 | 0.42 | 0.27 | 33 |

*Fine-tuned accuracy went down slightly - the model still collapsed to nearly all-discussion predictions.*

<br>

**Results Comparison**

| Model | Accuracy |
|---|---:|
| Zero-shot baseline (Groq) | 0.636 |
| Fine-tuned DistilBERT | 0.424 |

Fine-tuning regression: -0.212

<br>

**Confusion Matrix**

| | Pred: analysis | Pred: opinion | Pred: discussion |
|---|---|---|---|
| **True: analysis** | 0 | 0 | 6 |
| **True: opinion** | 0 | 0 | 12 |
| **True: discussion** | 0 | 1 | 14 |

**3 Wrong Predictions**

The pattern of predicting the majority class from Iteration 1 continued - 32 of 33 posts were predicted as `discussion`, with one exception: a single `discussion` post was predicted as `opinion`.

1. **"Canada Fantasy Points so far + the S22 leader vs. the Top Chef Greats"** (true: `analysis`, predicted: `discussion`)

   > *"Being in the bottom twice this week only slightly reduced Tristen's lead over the other contestants. Massimo passed Katiana for second place and Shuai jumped from 7th place to 3rd."*

   This post contains specific fantasy point totals and cross-contestant standings which are clear analysis signals. But the "so far" framing positions it as a in-progress community update rather than a finished argument, and the tone is more like sharing a scoreboard than presenting a case. The model has no way to distinguish between numbers used as evidence and numbers used as context, and defaulted to `discussion`.

2. **"This season makes me think Canada is void of interesting food"** (true: `opinion`, predicted: `discussion`)

   > *"So every season I watch thus far wherever they go they end up really focusing on the food that's from there... I was excited to see what Canada would bring but it seems like the whole season is just, cooking."*

   The generalizing "So every season I watch" opening and the trailing "it seems like" make this read like a reflective observation being shared with the community, not a confident take being asserted. Adding 14 more analysis examples had no effect on the opinion/discussion boundary.

3. **A `discussion` post predicted as `opinion`** (the single exception in the confusion matrix)

   The one post that wasn't predicted as `discussion` was actually a `discussion` post incorrectly predicted as `opinion`. This is the first sign of the model starting identify the label space at all - one post was assertive enough in its opening that it tipped the prediction. The fact that the error goes the wrong direction (a correct `discussion` post mislabeled as `opinion`) rather than catching any of the 18 wrong-labeled posts is an indicator that the model still isn't learning real distinctions, though.

**Root cause**: 14 additional analysis examples still wasn't enough for the model to learn the classes. The improved system prompt helped the zero-shot baseline but doesn't affect the fine-tuned model, which doesn't use the prompt at inference time.

**Sample Classifications**

1. *"I ate at Massimo's Restaurant — My husband and I had dinner at the chef's table... We watched what appeared to be Gregory teach an employee to make his Spring Green Salad."*
   - **True Label**: discussion
   - **Predicted Label**: discussion ✓
   - **Confidence**: 0.48
   - **Explanation**: A personal dining experience narrative with no claim being made - the model correctly catches this, which is the one class it has learned.

2. *"This season 22 competitor is blowing Buddha out of the water in Top Chef fantasy — I run a fantasy league for friends. I've never seen someone run away with points like Tristen has this season. He is twice as good as Buddha was in both of his seasons halfway through."*
   - **True Label**: analysis
   - **Predicted Label**: discussion ✗
   - **Confidence**: 0.34
   - **Explanation**: Contains specific comparative stats (twice as good as Buddha, halfway through the season) but the "I run a fantasy league for friends" framing reads as a community update share, not an analytical argument.

3. *"This season makes me think Canada is void of interesting food — So every season I watch thus far wherever they go they end up really focusing on the food that's from there... it seems like the whole season is just, cooking."*
   - **True Label**: opinion
   - **Predicted Label**: discussion ✗
   - **Confidence**: 0.32
   - **Explanation**: The generalizing opener ("So every season I watch") and trailing hedge ("it seems like") both read as community reflection rather than a take being asserted; the model has still not learned the opinion class.

4. *"I prefer Kirsten to Padma — I know this is crazy but she just gives it such a warm vibe and is way more sympathetic to the contestants she's been there."*
   - **True Label**: opinion
   - **Predicted Label**: discussion ✗
   - **Confidence**: 0.40
   - **Explanation**: The clearest possible opinion - "I prefer X to Y" with zero supporting evidence - and still classified as discussion; this shows the opinion class has not been learned at all.

5. *"Seafood pizza? — Is seafood pizza really uncommon in North America? Because where I'm from this was actually a pretty popular combination."*
   - **True Label**: discussion
   - **Predicted Label**: opinion ✗
   - **Confidence**: 0.37
   - **Explanation**: The single exception in this iteration — one of the edge cases from the label definitions, where the author provides cultural context that tips the model toward opinion prediction; the only sign the model is starting to see beyond pure discussion.

---

### Iteration 3

**Changes**

- Added 35 more posts (8 `analysis`, 27 `opinion`) - genuine `analysis` posts are rare in this community, so the 8 new analysis posts are the highest-quality candidates found across a large fetch of the Reddit archive
- Changed `metric_for_best_model` from `accuracy` to `f1` since `discussion` is ~39% of data, predicting it every time still gets ~40% accuracy, so the model was being rewarded for predicting the majority class; macro F1 penalizes this and forces the checkpoint selector to care about all three classes
  - Updated `compute_metrics` to return macro F1 in addition to accuracy so the metric would be available
- Increased `num_train_epochs` from `3` to `8` to give the model more time to learn from the imbalanced dataset
- Decreased `per_device_train_batch_size` from `16` to `8` so there are more frequent weight updates per epoch, which leads to more granular learning on the minority classes

<br>

**Dataset**

| Label | # of Posts | Percentage |
| ----- | ---------- | ---------- |
| analysis | 48 | 19.3% |
| opinion | 103 | 41.4% |
| discussion | 98 | 39.4% |
| **Total** | **249** | **100%** |

<br>

**Metrics**

🎯 **Baseline accuracy**: 0.684 (evaluated on 38/38 parseable responses)

**Per-class metrics** (baseline):

| | precision | recall | f1-score | support |
|---|---|---|---|---|
| analysis | 0.67 | 0.29 | 0.40 | 7 |
| opinion | 0.75 | 0.75 | 0.75 | 16 |
| discussion | 0.63 | 0.80 | 0.71 | 15 |
| accuracy | | | 0.68 | 38 |
| macro avg | 0.68 | 0.61 | 0.62 | 38 |
| weighted avg | 0.69 | 0.68 | 0.67 | 38 |

<br>

🎯 **Fine-tuned model accuracy**: 0.658

**Per-class metrics** (fine-tuned model):

| | precision | recall | f1-score | support |
|---|---|---|---|---|
| analysis | 0.67 | 0.29 | 0.40 | 7 |
| opinion | 0.65 | 0.69 | 0.67 | 16 |
| discussion | 0.67 | 0.80 | 0.73 | 15 |
| accuracy | | | 0.66 | 38 |
| macro avg | 0.66 | 0.59 | 0.60 | 38 |
| weighted avg | 0.66 | 0.66 | 0.64 | 38 |

<br>

**Results Comparison**

| Model | Accuracy |
|---|---:|
| Zero-shot baseline (Groq) | 0.684 |
| Fine-tuned DistilBERT | 0.658 |

Fine-tuning regression: -0.026

<br>

**Confusion Matrix**

| | Pred: analysis | Pred: opinion | Pred: discussion |
|---|---|---|---|
| **True: analysis** | 2 | 3 | 2 |
| **True: opinion** | 1 | 11 | 4 |
| **True: discussion** | 0 | 3 | 12 |

**3 Wrong Predictions**

The model is finally making decent predictions across all three classes. The confusion matrix reveals three distinct error patterns.

1. **`analysis` predicted as `opinion`** (3 cases - the most common analysis error)

   Representative post: **"The constant, blatant sponsorships are diluting the value of the show"** (true: `analysis`, predicted: `opinion`)

   > *"This past episode felt like a commercial from A-Z. I work in marketing, I totally understand that Bravo needs the partnership dollars... BMW, Chipotle, Saratoga Springs, Whole Foods, Wells Fargo."*

   This post lists specific sponsors as evidence and cites domain expertise ("I work in marketing"), which is what makes it `analysis`. But the central claim,  "diluting the value of the show", is inherently subjective, and the editorial tone throughout ("getting to be overkill") sounds like an assertive opinion. The model correctly learned that confident assertions signal `opinion`; it hasn't yet learned to weigh the presence of enumerated evidence against the assertive tone. The hard boundary here is an analysis post and a strong opinion can both be specific and confident; the distinguishing feature is whether the specifics are being used *as evidence for a conclusion* or *cited as context for an assertion*, a distinction that doesn't map to any surface-level token pattern.

2. **`opinion` predicted as `discussion`** (4 cases - the most common opinion error)

   Representative post: **"Top Chef Observations"** (true: `opinion`, predicted: `discussion`)

   > *"Hey all! What observations about Top Chef over the season have you noticed? I have found that Padma was more critical and made the chefs more competitive with one another, where Kristin is more joyful..."*

   The opening, "Hey all! What observations have you noticed?", is a common discussion opener. The body then expresses a specific view (Padma more critical vs. Kristin more joyful), but the model sees the community-invitation structure first and predicts `discussion`. This is exactly the question-wrapped opinion edge case from the label stress-testing. The model learned a simpler version of the definition rule: invitation language = `discussion`, regardless of what follows.

3. **`discussion` predicted as `opinion`** (3 cases)

   Representative post: **"Blind judging"** (true: `discussion`, predicted: `opinion`)

   > *"Does anyone know why they don't do blind judging very often? Like I get not wanting to every time because it adds more drama. But I feel like the show would be better if at least 50% of the elimination..."*

   This post opens with a genuine question ("Does anyone know why...") but immediately pivots to a personal view ("I feel like the show would be better if..."). The opinion sentiment in the body overrides the question framing in the title. The model now correctly reads strong personal sentiment as an `opinion` signal, but it's applying that signal even when the post's primary purpose is prompting community input. Discussion posts often open with a personal hook to draw readers in and the model hasn't learned to distinguish that hook from the post's actual intent.

**Sample Classifications**

1. *"When criticism goes back in their face — I've noticed this has happened multiple times, when a chef on the bottom will criticize another dish that they thought was bad (but wasn't on the bottom) and then the judges will throw their criticism back in their face. CJ did it in season 10 when he criticized a dish... and Tom said that that dish was better than his."*
   - **True Label**: analysis
   - **Predicted Label**: opinion ✗
   - **Confidence**: 0.76
   - **Explanation**: The model is quite confident: the post makes a clear claim ("this has happened multiple times") backed by specific cross-season examples, but the assertive, opinionated tone throughout is read as opinion. The model hasn't learned to distinguish evidence-backed assertiveness from unsupported assertiveness.

2. *"How Canada/Toronto could have been — So they've done 10 episodes in the Toronto studio, with brief glimpses at different parts of the country, and are only just now going to Calgary. So figuring 1/10 was Restaurant Wars..."*
   - **True Label**: opinion
   - **Predicted Label**: analysis ✗
   - **Confidence**: 0.69
   - **Explanation**: The episode count ("10 episodes in the Toronto studio, 1/10 for Restaurant Wars") reads as structured data to the model - it has learned that numbers and episode references signal analysis. But this post is using those numbers to assert a take, not build an argument, making this a perfect example of the analysis/opinion boundary the model hasn't fully learned.

3. *"Help me describe Top Chef and LCK to my boyfriend — He wants to watch top chef because it introduces us to a lot of chefs we see on the food network but he doesn't really understand it, I think because..."*
   - **True Label**: discussion
   - **Predicted Label**: opinion ✗
   - **Confidence**: 0.82
   - **Explanation**: Very confident wrong prediction - the author is explaining the show for someone new, which involves describing what the show is and how it works. These explanatory statements read like opinions ("I think because..."), and the model has no way to distinguish between explaining a position and explaining a show.

4. *"Anya and her pine cones — Anya, hold your head high, you introduced Daniel Boulud to an ingredient he had never had before and that is saying something. I wish we were going to see more of your cooking."*
   - **True Label**: opinion
   - **Predicted Label**: discussion ✗
   - **Confidence**: 0.90
   - **Explanation**: The highest-confidence wrong prediction in the set — the model is 90% sure this is discussion. The post is addressed directly to a chef ("Anya, hold your head high") in a supportive, sharing tone, which reads exactly like a community appreciation post rather than a take being defended.

5. *"Television shows do not need teaser previews to keep you watching — Let's talk about shows that feel compelled to show you snippets of the third act of the show during the commercial outro between the..."*
   - **True Label**: analysis
   - **Predicted Label**: discussion ✗
   - **Confidence**: 0.74
   - **Explanation**: "Let's talk about" is one of the most common discussion-framing phrases on Reddit; the model sees it and predicts discussion confidently, even though the post goes on to make a specific argument about TV production choices with examples.

---

## Reflection

There were many posts that captured aspects of multiple labels so the model got confused and predicted the wrong one. Rather than interpretting the intent of the post as a whole, which is what I did to label them, the model seemed to try to match part of a label definition and then chose that one even if the post exhibited parts of multiple label definitions or the entire post as a whole better matched another label. This indicates my definitions probably weren't distinct enough so the model couldn't clearly detect which post was which type. There were also far fewer `analysis` examples for the model to learn from in the first place.

However, adding more data, adding more representative data to balance out the dataset, and tuning the hyparameters seemed to lead to significnt performance improvements as I iterated.

To further address these issues, I could:
1. Adjust my label definitions to be more clearly distinguishable
2. Provide examples/guidance on how to handle common edge cases
3. Include more data and a more balanced dataset
---

## Spec Reflection

**One way the spec helped**: The label stress-testing exercise in planning.md caught the "question-wrapped opinion" edge case before any training happened, which led to adding the explicit rule "the question must be the point, not a wrapper around a take" to the `discussion` definition. In Iteration 3, `opinion`/`discussion` confusions in both directions became the second-most-common error type in the confusion matrix. Identifying it in planning didn't prevent the model from struggling with it, but it meant the definition was as tight as it could be, and the failure could be diagnosed precisely rather than attributed to a vague labeling inconsistency.

**One way implementation diverged from the spec**: The Data Collection Plan set a target of "no more than 50% of one label type and at least 25% of each." In practice, genuine `analysis` posts are uncommon in r/TopChef - after three rounds of data collection across hundreds of archived posts, `analysis` topped out at 19% of the dataset. The goal couldn't be met without lowering the bar for what counts as analysis, which would have undermined the label's coherence. The implementation adapted by pursuing hyperparameter changes (macro F1 as the checkpoint metric, more epochs, smaller batch size) instead of forcing balance through looser labeling.

---

## AI Usage

1. **Writing code to fetch posts from Reddit**: I asked Claude to write a script to pull Reddit posts for this community from the Pullpush.io archive. Initially it included posts that were just links to external articles, so I told it to filter those out and only include text posts with a body since the classifier model wouldn't go out and read linked websites. A post with just a title and no body would have too little content to classify reliably.

2. **Writing initial labels for review**: I asked Claude to label the first 20 posts using my label definitions so I could review whether it understood the distinctions. I then asked it to label an additional 20 because `analysis` was underrepresented in the first sample. After reviewing those results manually and adjusting the borderline cases, I asked Claude to label all 200+ posts with guidance on how to handle the boundary cases I'd already resolved. I reviewed the final batch and adjusted 2 more.

3. **Talking through strategies to improve performance**: When the fine-tuned model performed worse than the baseline, I worked through possible causes with Claude, including hyperparameter tuning, additional data collection, and identifying better analysis examples in the dataset. Claude initially suggested trying different model architectures and libraries, and I redirected it - I wanted to first exhaust adjustments to the existing training code and dataset before doing a major code rewrite.
