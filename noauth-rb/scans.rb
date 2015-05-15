#!/usr/bin/env ruby

def check_state(data)
  # Checks if request contains state parameter
  true if(data.match(/state=\w+/))
end

def csrf_vulnerable(flag)
  if flag
    p "App is vulnerable to Cross-Site Request Forgery (CSRF) & lacks the state parameter" 
  else
    p "App is protected from Cross-Site Request Forgery (CSRF) by the state parameter."
  end
end

def leaks_auth_code(page)
  return false unless page.match(/code=\w+/)
  true
end
