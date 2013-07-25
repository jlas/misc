#!/usr/bin/env python

import subprocess

CHUNK_SIZE = 500
ENCODE_CHAR = '|'

def encode(source_rows):
    # space out the fragments becuase the translator
    # works better with punctuation this way
    encoded = ('  ' + ENCODE_CHAR + '  ').join(source_rows)
    cnt = 0
    translated = ""
    while encoded:
        lastidx = idx = 0
        while idx < CHUNK_SIZE:
            lastidx = idx
            idx = encoded.find(ENCODE_CHAR, lastidx+1)
            if idx == -1:
                lastidx = len(encoded)
                break

        chunk = encoded[:lastidx]
        translated += subprocess.check_output(['en2pt', chunk]).strip()
        encoded = encoded[lastidx:]
        cnt += 1

    print 'made %s translations' % cnt
    return map(lambda s: s.strip(), translated.split(ENCODE_CHAR))
