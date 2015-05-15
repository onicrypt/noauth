# # coding: utf-8
lib = File.expand_path('../lib', __FILE__)
$LOAD_PATH.unshift(lib) unless $LOAD_PATH.include?(lib)
require 'noauth/version'

Gem::Specification.new do |spec|
  spec.name           = "noauth"
  spec.version        = NOauth::VERSION
  spec.authors        = ["Nicholas Ramsey"]
  spec.email          = ["onicrypt@gmail.com"]
  spec.summary        = %q{"NOauth is a toolkit for extensible testing of OAuth"}
  spec.description    = %q{"NOauth includes an intercepting proxy, attack and scanning scripts, and the capability to extend based on the operator's needs"}
  spec.homepage       = ""
  spec.license        = "GPL V2.0"

  spec.files          = `git ls-files`.split("\n")
  spec.executables    = spec.files.grep(%r{bin/}) {|f| File.basename(f)}
  spec.test_files     = spec.files.grep(%r{^(test|spec|features)/})
  spec.require_paths  = ["lib"]

  spec.add_development_dependency "bundler", "1.9.8"
  spec.add_development_dependency "rake", "10.4.2"
  spec.add_development_dependency "pry", "~> 0.10", ">= 0.10.1"
  spec.add_development_dependency "curb", "0.8.8"
  spec.add_development_dependency "em-proxy", "0.1.8"
end
