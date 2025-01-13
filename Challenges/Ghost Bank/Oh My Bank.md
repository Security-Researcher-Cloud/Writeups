[Ghostbank](https://ghostbank.net/?code=xfp-933)

## After Registration
![](assets/GhostBank%20-%20Login%20With%20Email.png)

## Initial Setup
![](assets/GhostBank%20Entry.png)

## E-Mail
![](assets/GhostBank%20-%20Token%20Email.png)

## Using it Normally
![](assets/GhostBank%20-%20Initial%20Account%20After%20Moving%20Around%20Some%20Funds.png)
- In the above we can see that you can transfer from your checking to your savings in amounts that are smaller than a given value

## Loading up Burp
- If we attach this to Burp Suite we can see when it logs into the system with the token, that we see a few calls to api.ghostbank.net and ghostbank.net
![](assets/BurpSuite%20-%20Initial%20Page%20load.png)

## How do transfers work?
- The first thing to examine, since it is the most obvious function on the page -- is how do we transfer funds from one account to the other. 
![](assets/GhostBank%20-%20Making%20a%20transfer.png)
- If we look at that through our burp proxy we can see that the tranfer appears to hit `api/v3/transfer`
![](assets/GhostBank%20-%20Burp%20Transfer%20(Initial).png)
- Send this request to the intruder so that we can setup an attack to see if we can change any of the parameters, specifically focusing on the `account_from` and amount. For the purpose of checking it it works, we will do just the account from with intervals of 100.
- For this test, I will just hit all the numbers between 0 and the one that my account is `759`
![](assets/GhostBank%20-%20Burp%20Setup%20Attack.png)![](assets/GhostBank%20-%20Burp%20Attack%20Output.png)
- Once completed, then we get our notification saying we beat the game
![](assets/GhostBank%20-%20Solution.png)