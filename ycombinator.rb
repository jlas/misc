#!/usr/bin/env ruby

## Simple application of Y Combinator to do factorial function
## From Jim Weirich 2012 RubyConf talk here: http://youtu.be/FITJMJjASUs

## Broken up as several expressions

fact_improver = ->(partial) {
  ->(n) { n.zero? ? 1 : n * partial.(n-1) }
}

# Applicative Y Combinator
y = ->(f) {
  ->(x) { f.(->(v) { x.(x).(v) }) }
    .(->(x) { f.(->(v) { x.(x).(v) }) })
}

fact = y.(fact_improver)
puts fact.(5)


## As a pure lambda expression
puts ->(improver) {
  ->(gen) {
    gen.(gen)
  }.(
     ->(gen) { improver.(->(v) { gen.(gen).(v) })
     }
     )
}.(
   ->(partial) {
     ->(n) { n.zero? ? 1 : n * partial.(n-1) }
   }
   ).(5)
