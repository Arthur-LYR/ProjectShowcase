# LZ77

Implementation of LZ77 encoding. 

## Encoding

A test txt file is provided that may be used. To encode, simply execute the command:

```
python myzip.py <FILENAME> <WINDOW> <LOOKAHEAD>
```

Example:

```
python myzip.py test.txt 10 10
```

## Decoding

The encoder should produce a bin file which may be decoded using the following command:

```
python myunzip.py <FILENAME>
```

Example:

```
python myunzip.py test.txt.bin
```