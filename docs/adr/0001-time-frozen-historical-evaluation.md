# Time-frozen historical evaluation

Historical evaluation cases use only repository evidence available when each issue was opened; the live demo uses the latest available repository material. We chose separate evidence views because later fixes, labels, and maintainer replies could reveal the expected answer in historical tests, while a live maintainer needs current information. This requires preserving or reconstructing an evidence cutoff for each case, but keeps comparisons between model and retrieval versions meaningful.

Model-training examples precede held-out evaluation cases in time, and issues from the same family stay in the same training or evaluation partition. Earlier issues may still appear as retrieval evidence for a later case when they were available before its cutoff.

Evaluation uses issue titles and bodies that were not edited after opening, or manually verified originals. Cases without a reliable opening version are excluded. Each case records an issue-opening cutoff and a repository commit SHA from before that cutoff; later comments, labels, closures, and duplicate decisions remain available for annotation but never enter the model input.
