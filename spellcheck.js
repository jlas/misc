#!/usr/bin/env node

fs = require('fs');

var WORDSFILE = "/usr/share/dict/words";
var NUMSUGGS = 10;
var NUMRANDITRS = 1000;

/**
 * Return edit distance from word1 to word2. That is, calculate the number
 * of edits (letter delete, insert, or substitution) it takes to transform
 * word1 to word2.
 *
 * Based on http://www.cs.berkeley.edu/~vazirani/algorithms/chap6.pdf
 */
function editdist(word1, word2) {

    // if two words differ at a certain index, return 1
    function diff(idx1, idx2) {
        if (word1[idx1] === word2[idx2]) {
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

words = fs.readFileSync(WORDSFILE).toString();
wordsarr = words.split("\n");

// Returns a random integer between min and max
// Using Math.round() will give you a non-uniform distribution!
function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1) + min);
}

/**
 * Get suggestions for a possibly misspelled word. Candidate suggestions are
 * selected randomly and sorted by edit distance. The lowest edit distance
 * suggestions are returned.
 *
 * This is a pretty crappy way to get suggestions.
 */
function suggestions(word) {

    var suggs = [];

    for (var i = 0; i < NUMRANDITRS; i++) {
        var randidx = getRandomInt(0, wordsarr.length - 1);
        var randword = wordsarr[randidx];
        suggs.push({word: randword,
                    dist: editdist(word, randword)});
        suggs.sort(function (a, b) {
            if (a.dist > b.dist) {
                return 1;
            } else if (a.dist < b.dist) {
                return -1;
            }
            return 0;
        });
    }

    return suggs.slice(0, NUMSUGGS);
}

if (process.argv.length < 3) {
    console.log("Please provide a word to spellcheck.");
    process.exit(1);
}

var word = process.argv[process.argv.length-1];
console.log("Suggestions for: " + word);
console.log(suggestions(word));