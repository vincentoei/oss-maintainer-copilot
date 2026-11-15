# Reviewed weak labels for LoRA training

The LoRA training set will start from historical pytest issues with existing type labels, exclude all held-out evaluation cases, and manually spot-check the resulting examples. We chose this over hand-labeling every training issue because the project needs enough examples for a meaningful fine-tuning exercise within a limited time budget. Repository labels are noisy and may have been applied after issue creation, so they are training targets only; human-reviewed expected triage outcomes remain the evaluation reference.
