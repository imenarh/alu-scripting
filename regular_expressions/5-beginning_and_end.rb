#!/usr/bin/env ruby

input = ARGV[0]

puts input.scan(/\Ah.n\z/).join
