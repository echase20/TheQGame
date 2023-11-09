The commit we tagged for your submission is 0b34cb6f6102716ebc64d8cb5064e4b5a297a582.
**If you use GitHub permalinks, they must refer to this commit or your self-eval will be rejected.**
Navigate to the URL below to create permalinks and check that the commit hash in the final permalink URL is correct:

https://github.khoury.northeastern.edu/CS4500-F23/salty-camels/tree/0b34cb6f6102716ebc64d8cb5064e4b5a297a582

## Self-Evaluation Form for Milestone 7

Indicate below each bullet which file/unit takes care of each task:

The require revision calls for turning Q bonus points and
finished-the-game bonus points into named constants

1. Which unit tests check the Q-bonus functionality? Is it abstracted
   over the named constant? 
https://github.khoury.northeastern.edu/CS4500-F23/salty-camels/blob/0b34cb6f6102716ebc64d8cb5064e4b5a297a582/Q/Tests/test_points.py#L47-L53
<p>It is not abstracted over a named constant although we can easily add this after the recent cleanup using the rulebook class. Each Gamestate takes in a rulebook
https://github.khoury.northeastern.edu/CS4500-F23/salty-camels/blob/0b34cb6f6102716ebc64d8cb5064e4b5a297a582/Q/Common/game_state.py#L24-L31
</p>

2. Which unit tests check the finished-the-game functionality? Is it
   abstracted over the named constant?
https://github.khoury.northeastern.edu/CS4500-F23/salty-camels/blob/0b34cb6f6102716ebc64d8cb5064e4b5a297a582/Q/Tests/test_referee.py#L75-L90
<p>This unit test does not directly call the end game method but we think this suffices. It returns a pair result that we compare to our expected pair result.</p>

<p>It is not abstracted over a named constant although we can easily add this after the recent cleanup. We did not realize this was a required functionality.</p>

3. Do you also have integration tests that show how setting the bonus
   constants to different constants yields different results for the
   same starting point? (This is optional but helps with milestone 8
   and fits to the request.) 
   <p>We do not. Though we made this simpler to implement with our recent changes in this milestone.</p>


The ideal feedback for each of these three points is a GitHub
perma-link to the range of lines in a specific file or a collection of
files.

A lesser alternative is to specify paths to files and, if files are
longer than a laptop screen, positions within files are appropriate
responses.

You may wish to add a sentence that explains how you think the
specified code snippets answer the request.

If you did *not* realize these pieces of functionality, say so.

