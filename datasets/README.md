# Datasets

## UCI SMS Spam Collection

The training dataset is automatically downloaded when you run the training script:

```bash
python -m app.ml.train
```

### Dataset Information

- **Name**: SMS Spam Collection
- **Size**: 5,574 messages
- **Classes**: spam (747), ham (4,827)
- **Format**: TSV (tab-separated values)
- **License**: CC0 1.0 Universal (Public Domain)
- **Source**: [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/sms+spam+collection)

### Format

Each line contains a label and message separated by a tab:

```
ham	Go until jurong point, crazy.. Available only in bugis...
spam	Free entry in 2 a wkly comp to win FA Cup final tkts...
```

### Manual Download

If automatic download fails, download the dataset manually:

1. Visit https://archive.ics.uci.edu/ml/datasets/sms+spam+collection
2. Download the ZIP file
3. Extract `SMSSpamCollection` to this directory

## Data Privacy

This dataset contains real SMS messages that were donated for research purposes.
No personally identifying information is included. The dataset is publicly available
under CC0 license.
