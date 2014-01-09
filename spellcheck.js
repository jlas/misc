#!/usr/bin/env node

fs = require('fs');

var WORDSFILE = "/usr/share/dict/words";
var NUMSUGGS = 10;
var MAXITERS = 2000;
var LENDIFF = 2;


// Returns a random integer between min and max
// Using Math.round() will give you a non-uniform distribution!
function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1) + min);
}

/**
 * Return edit distance from word1 to word2. That is, calculate the number
 * of edits (letter delete, insert, or substitution) it takes to transform
 * word1 to word2.
 *
 * Based on http://www.cs.berkeley.edu/~vazirani/algorithms/chap6.pdf
 *
 * @param word1 (string)
 * @param word2 (string)
 */
function editdist(word1, word2) {

    // if two words differ at a certain index, return 1
    function diff(idx1, idx2) {
        if (word1[idx1-1] === word2[idx2-1]) {
            return 0;
        }
        return 1;
    }

    distarr = [];
    len1 = word1.length;
    len2 = word2.length;

    for (var i = 0; i <= len1; i++) {
        distarr[i] = [];  // initialize empty array
        distarr[i][0] = i;
    }

    for (var j = 1; j <= len2; j++) {
        distarr[0][j] = j;
    }

    for (var i = 1; i <= len1; i++) {
        for (var j = 1; j <= len2; j++) {
            distarr[i][j] = Math.min(distarr[i-1][j] + 1,
                                     distarr[i][j-1] + 1,
                                     distarr[i-1][j-1] + diff(i, j));
        }
    }

    return distarr[len1][len2];
}

// Tests
//console.log(editdist("exponential", "polynomial"));  // => 6
//console.log(editdist("sunny", "snowy"));  // => 3

/**
 * Get suggestions for a possibly misspelled word, using candidates from the
 * given word pool.
 *
 * If word pool is larger than iteration limit, then pick candidates randomly.
 *
 * @param word (string) word to find suggestions for
 * @param wordpool (array) set of words to choose suggestions from
 */
function suggestions(word, wordpool) {
    var suggs = [];
    var iters = wordpool.length;
    var getidx = function (i) { return i; };

    // setup random selection
    if (wordpool.length > MAXITERS) {
        iters = MAXITERS;
        getidx = function () {
            return getRandomInt(0, wordpool.length - 1);
        };
    }

    for (var i = 0; i < iters; i++) {
        var idx = getidx(i);
        var randword = wordpool[idx];
        suggs.push({word: randword,
                    dist: editdist(word, randword)});
    }

    return suggs;
}

// command line arg check
if (process.argv.length < 3) {
    console.log("Please provide a word to spellcheck.");
    process.exit(1);
}

var word = process.argv[process.argv.length-1];
var proxlen = [];
var firstletter = [];
var lastletter = [];

// load english words from system words file
words = fs.readFileSync(WORDSFILE).toString();
wordsarr = words.split("\n");

/**
 * Filter dictionary into list of words (within +/- word length) with same first
 * letter, same last letter, and others.
 */
wordsarr.forEach(function(dictword) {
    if (Math.abs(word.length - dictword.length) < LENDIFF) {
        if (word[0] === dictword[0]) {
            firstletter.push(dictword);
        } else if (word[word.length - 1] === dictword[dictword.length - 1]) {
            lastletter.push(dictword);
        } else {
            proxlen.push(dictword);
        }
    }
});

// compare function for sorting suggestions
function compareSuggs(a, b) {
    if (a.dist > b.dist) {
        return 1;
    } else if (a.dist < b.dist) {
        return -1;
    }
    return 0;
}

console.log("Suggestions for: " + word);
console.log(suggestions(word, firstletter)
            .concat(suggestions(word, proxlen))
            .concat(suggestions(word, lastletter))
            .sort(compareSuggs)
            .slice(0, NUMSUGGS));
