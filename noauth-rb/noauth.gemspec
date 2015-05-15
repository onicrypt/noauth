# # coding: utf-8
lib = File.expand_path('../lib', __FILE__)
$LOAD_PATH.unshift(lib) unless $LOAD_PATH.include?(lib)
require 'noauth/version'

Gem::Specification.new do |spec|
  spec.name           = "NOauth"
  spec.version        = NOauth::VERSION
  spec.authors        = ["Nicholas Ramsey"]
  spec.email          = ["onicrypt@gmail.com"]
  spec.summary        = %q{""}
  spec.description    = %q{""}
  spec.homepage       = ""
  spec.license        = "GPL V2.0"

  spec.files          = `git ls-files .. | grep -a "noauth-rb/"`.split("\n")
  spec.executables    = spec.files.grep(%r{bin/}) {|f| File.basename(f)}
  spec.test_files     = spec.files.grep(%r{^(test|spec|features)/})
  spec.require_paths  = ["lib"]

  spec.add_development_dependency "bundler"
  spec.add_development_dependency "rake"
  spec.add_development_dependency "curb"
  spec.add_development_dependency "em-proxy"
  spec.add_development_dependency "pry"
end