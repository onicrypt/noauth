#!/usr/bin/env ruby

require "noauth/version"
require "noauth/attacks"
require "noauth/scans"

module NOauth
  include Attack
  include Scan
end
