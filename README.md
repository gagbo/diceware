# Diceware implementation

## References

For the algorithm, and the words list I am targeting this [paper](http://weber.fi.eu.org/index.shtml.en#projects)

## Why Diceware ?

Diceware method for generating passwords is really nice and fun (I like
throwing dice), and I would like to use it to generate passwords on the fly for
the occasions where I don't have the time to actually do the full method (quick
sign up on a site I'll probably visit only once).

## Reinventing the wheel

Diceware is simple enough so I can implement it in my own way, so here I am.

There are probably a lot of diceware implementations in the wild ( I'll update
the README to add a list when I look for ways to implement the actual words
list in my program).

I advise you to run the dice or
trust these other guys, since crypto is not my forte (I know I have to use
`os.urandom()` and that's pretty much it, this command line tool does not
protect you from snooping eyes or other infections/memory watchers I do not
know of)

## Usage

The project is not finished yet, but at most times running
```
./diceware.py
```
will display stuff (mostly examples and test cases).

That being said, I really want to run the simplest,
smallest, easiest implementation of the algorithm ; Here are a few scenarios :

 - I want to create passphrases in any single language from command line
   (mainly targetting english and french for now)

 - I want to create passphrases using french (or any language) list but without
   accent. I am fine with small mistakes if it means the password is quicker to
   type on qwerty keyboards

 - I want my girlfriend to want to use that (which will bring portability
   issues later probably for anything non-CLI - Windows, iOS, Firefox,
   Browser integration...)

 - I want to be able to control the count of words for the list (When I have to
   give a dummy account for a one-time login a 3 word list would be fine)

 - I want to be able to add salt or not. Salting the passphrase makes it
   *a lot* better but it adds constraints on the memorability of
   the passphrase. The better solution from the implementation's point of view
   is to give the choice to the user.
