The problem this utility solves, is that of ranking of items per usage. That is, 
we have some items which are identified by id; and we offer a method to letting
us know when the item associated with such id has been used. The item and the 
usage could have many meanings, for example a product being sold on a e-comm
page; or a moving being watched on an streaming service. The only thing we care
about, are the ids of those items and the number of times they are used.

At any given point in time, we offer the following O(1) services:

1. Given an item id, return its ranking. Rankings start at 1.
2. Given a ranking, return item id occupying such ranking.

and this additional O(k) time service:

3. Return the current top-k products (descending order per ranking).

As you might expect, these nice time complexities come at the cost of using
extra memory; O(n) more memory to be precise.

The assumption is that the total number of items to be tracked, is something we
can keep in a single computer memory. We also assume that user of this utility,
does not care about how ties are broken; that is, within a particular usage
counter, we do not care about the permutation used to sort all the items which
have been used such number of times.

If you just want to use this utility, go ahead now. The rest of this readme is
about the internals, in case you are curious.

Cheers.


Internals:

The main idea behind this utility, is inspired by the main idea behind the 
solution to this popular interview question:

https://leetcode.com/problems/insert-delete-getrandom-o1/description/

The main idea in problem above, is that we want to have some maps which can
tells us in O(1), the position of a given id. But we fear deletions, because
they may involve shifting a local array; which in turn can translate into 
updating the whole internal array (O(n) time complexity). 

The trick is that, when faced with a deletion; we pay attention to a particular 
"fixed" position within the logical array and use it to swap with element being 
deleted. With that simple but powerful idea, the element to be deleted will be 
always at the end of the logical array; and therefore, its removal can be done 
in O(1) time.

Leveraging the idea, let us explain now the solution.

Is clear that we need to keep track of a counter per item, telling us how many
times it has been used. This map will be indexed by item id. Also, since we want
to achieve O(1) ranking queries, we will precompute the ranking for all items.
Answering the top-k query can be implemented with the inverse map, from rankings
into item ids; though this extra structure is useful for other stuff as well
(we will see in a bit).

Alright, let us see the main idea with an example. Let us suppose that we have
the following counters, each one with an associated item id and all sorted
according to the ranking.

usage counters: 3 2 2 2 1 <br />
assoc item ids: a b c d e <br />
rankings      : 1 2 3 4 5 <br />

In the example above, the product a has been used 3 times, hence it has the 
prestigious ranking of 1. Then we have b,c and d items with counter of 2;
per our assumptions we break the tie arbitrarily, by assigning rankings as b=2,
c=3 and d=4. Finally, with a counter of 1 we just have item e, which occupies
the last place as expected.

What would happen if item c is used one more time, that is, if the user of this
structure calls method usageRanking.use_item(c)?

We do not want to alter a lot of the slots in the rankings mapping, hence we pay
attention to an special place: the least ranking associated with a given counter.
In this case, the (old) counter is 2 and its least ranking is 2 that belongs to
item b. We said that we do not care about internal ordering within same counter,
hence we just swap ranking with that special position. That is, we swap rankings
between c and b, leading to:

usage counters: 3 3 2 2 1 <br />
assoc item ids: a c b d e <br />
rankings      : 1 2 3 4 5 <br />

The counters got updated in a funny way: the left most previous counter got
"upgraded", such that it belongs now to next group. In this case, left-most
counter 2 became a 3. The rankings structure got almost unchanged, just a couple
of slots were altered: the ranking 2 now belongs to item c, while item b got 
downgraded to ranking 3.

In general, the trick above allows one to updating just a couple of rankings;
the one associated with item being used, and the least ranking of old counter.
It is that guy, the least ranking of old counter, the one who lies in the
boundary between sections of items sharing new and old counters. For the rest
of the items with new counter, is irrelevant that and old counter pal got 
upgraded; the amount of items behind is still the same, so they keep their 
current rankings. Something similar happens to the rest of the items indeed,
as the rankings are computed based on total amount of different items; and
that amount has not really changed.

Therefore, the main trick is to maintain that additional structure which tracks
what is the least ranking associated to each usage counter. Using the inverse
mapping of ranking -> item id, we can know what is the associated item to do
the swap against. The main logic to maintaining this extra map is as follows.
The least rankings of two counters are to be affected: the one associated with
old counter of item, and the one associated with same counter after being
incremented by one.

old counter: next least ranking is old ranking + 1
new counter: if adding first item, least ranking is simply that item's ranking
  
The main trick above is that the next least ranking does not need to be computed
with any search, we can assume is the next biggest ranking (old ranking + 1).
This idea comes from the visual example provided: if we upgrade the left-most
counter from 2 to 3, then next left-most counter 2 can become the new special
guy for that slot (next item with counter = 2). Even when the item associated
with old ranking + 1, does not really belong to associated counter; it is safe
to make the update. This is because when using that empty counter for real, we
will update first with second rule above and initialize the least ranking with
a proper value. In other words, it does not matter that we temporarily carry
an incorrect ranking there; it will get fixed prior we actually use it.

In order to know whether we are adding an item to an empty group (first item
using that counter), we keep an additional structure to count how many items
have been used same number of times (index is of course the usage counter). This
is the auxiliary structure that allows to implement the rule for new counters,
described a couple of paragraphs above.

There are some extra considerations, but the ones above are the most important.
Exception is perhaps what occurs with new items, being used for the first time. 
We do not need any extra search for getting its ranking either: we can simply 
think that they are placed at the right-most end of our logical array of counters
presented in the example. They will born always with a counter of one, and we can 
assign the last ranking per convention. 

I made this utility based on an interview question I got, some time ago. I could
not solve it within expected time constraints; but after thinking some extra
hours came up with this solution. I consider it has decent performance, though
it requires more extensive testing. Feel free to drop me a line if you find
any issues, or if you want to contribute with more test cases.

Kind regards.



