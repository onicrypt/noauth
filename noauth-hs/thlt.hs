third :: String -> String
third "" = "Empty string, how fuggin lame"
third ltrs@(x:y:_) = [ltrs !! 2] ++ " is the 3rd letter of " ++ ltrs 

fug :: (RealFloat a) => a -> a -> String
fug weight height
	| weight / height ^ 2 <= 18.5 	= "Shiiiiit you skinny"
	| weight / height ^ 2 <= 25.0 	= "Perfect, fuggin showoff"
	| weight / height ^ 2 <= 30.0 	= "Grand stand chunky monkey"
	| otherwise 			= "Not even light can escape your pull"

fug' :: (RealFloat a) => a -> a -> String
fug' weight height
	| bmi <= skinny	= "Shiiiiit you skinny"
	| bmi <= normal	= "Perfect, fuggin showoff"
	| bmi <= fat 	= "Grand stand chunky monkey"
	| otherwise	= "Not even light can escape your pull"
	where 	bmi = weight / height ^ 2
		skinny = 18.5
		normal= 25.0
		fat = 30.0
