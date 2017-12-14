from unittest import TestCase

from urank.UsageRanking import UsageRanking

"""
To make testing easier; we are using a compact representation of the 
UsageRanking state: an sorted array of usage counters, representing
the items sorted by ranking. 

Note: this compact representation (see README.md), was actually used
to conceive the algorithm. The implementation does not really materialize
this sorted array of counters, due practical reasons (not useful for answering
the queries we care about); but it seems interesting to me, that for testing
purposes the same representation comes handy and has practical usage.
"""

class TestUsageRanking(TestCase):
    def build_urank(self, sorted_cnt):
        urank = UsageRanking()
        for id in range(len(sorted_cnt)):
            rank = id+1
            cnt = sorted_cnt[id]
            urank.item_cnt[id] = cnt
            urank.item_rank[id] = rank
            urank.rank_item[rank] = id
            urank.cnt_cnt[cnt] += 1
            if urank.cnt_min_rank[cnt] == 0:
                urank.cnt_min_rank[cnt] = rank
        return urank

    def to_sorted_cnt(self, urank):
        get_cnt = lambda r: urank.item_cnt[urank.rank_item[r]]
        return list(map(get_cnt, range(1, urank.num_items()+1)))

    def _test_use_item(self, in_sorted_cnt, id, out_sorted_cnt):
        urank = self.build_urank(in_sorted_cnt)
        urank.use_item(id)
        self.assertEquals(self.to_sorted_cnt(urank), out_sorted_cnt)

    def data_provider(self):
        return [
            (
                [],
                0,
                [1]
            ),
            (
                [1,1,1],
                0,
                [2,1,1]
            ),
            (
                [1, 1, 1],
                1,
                [2, 1, 1]
            ),
            (
                [1, 1, 1],
                2,
                [2, 1, 1]
            ),
            (
                [3, 2, 1],
                0,
                [4, 2, 1]
            ),
            (
                [3, 2, 1],
                1,
                [3, 3, 1]
            ),
            (
                [3, 2, 1],
                2,
                [3, 2, 2]
            ),
            (
                [3, 2, 2, 1, 1, 1],
                0,
                [4, 2, 2, 1, 1, 1]
            ),
            (
                [3, 2, 2, 1, 1, 1],
                1,
                [3, 3, 2, 1, 1, 1]
            ),
            (
                [3, 2, 2, 1, 1, 1],
                2,
                [3, 3, 2, 1, 1, 1]
            ),
            (
                [3, 2, 2, 1, 1, 1],
                3,
                [3, 2, 2, 2, 1, 1]
            ),
            (
                [3, 2, 2, 1, 1, 1],
                4,
                [3, 2, 2, 2, 1, 1]
            ),
            (
                [3, 2, 2, 1, 1, 1],
                5,
                [3, 2, 2, 2, 1, 1]
            ),
            (
                [3, 1, 1, 1],
                0,
                [4, 1, 1, 1]
            ),
            (
                [3, 1, 1, 1],
                1,
                [3, 2, 1, 1]
            ),
            (
                [3, 1, 1, 1],
                2,
                [3, 2, 1, 1]
            ),
            (
                [3, 1, 1, 1],
                3,
                [3, 2, 1, 1]
            ),
            (
                [3, 2, 1],
                100,
                [3, 2, 1, 1]
            ),
            (
                [3, 3, 3, 2, 2, 1],
                0,
                [4, 3, 3, 2, 2, 1]
            ),
            (
                [3, 3, 3, 2, 2, 1],
                1,
                [4, 3, 3, 2, 2, 1]
            ),
            (
                [3, 3, 3, 2, 2, 1],
                2,
                [4, 3, 3, 2, 2, 1]
            ),
            (
                [3, 3, 3, 2, 2, 1],
                3,
                [3, 3, 3, 3, 2, 1]
            ),
            (
                [3, 3, 3, 2, 2, 1],
                4,
                [3, 3, 3, 3, 2, 1]
            ),
            (
                [3, 3, 3, 2, 2, 1],
                5,
                [3, 3, 3, 2, 2, 2]
            ),
            (
                [3, 1],
                0,
                [4, 1]
            ),
            (
                [3, 1],
                1,
                [3, 2]
            ),
            (
                [3, 3, 1],
                0,
                [4, 3, 1]
            ),
            (
                [3, 3, 1],
                1,
                [4, 3, 1]
            ),
            (
                [3, 3, 1],
                2,
                [3, 3, 2]
            )
        ]

    def test_use_item(self):
        for in_sorted_cnt, id, out_sorted_cnt in self.data_provider():
            self._test_use_item(in_sorted_cnt, id, out_sorted_cnt)

