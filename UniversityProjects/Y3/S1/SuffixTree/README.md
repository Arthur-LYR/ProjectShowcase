# Suffix Tree

Implementation of a special type of Suffix Tree called a Generalised Suffix Tree (GST) which stores multiple strings instead of just one. The implementation uses a modified Ukkonen's algorithm to construct the tree and is able to perform pattern matching for all strings within the GST.

## Demo

Execute this command:

```
python gst.py sample.asc
```

The program will compute all occurrences of the three pats in the two texts. The results are in an output file where each row is three integers [p] [t] [i] which means that pattern [p] appears in text [t] at index [i].