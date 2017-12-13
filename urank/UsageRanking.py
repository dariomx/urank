from collections import defaultdict


class UsageRanking:
    def __init__(self):
        self.item_cnt = defaultdict(lambda: 0)
        self.item_rank = dict()
        self.rank_item = dict()
        self.cnt_cnt = defaultdict(lambda: 0)
        self.cnt_min_rank = defaultdict(lambda: 0)

    def use_item(self, id):
        if id in self.item_cnt:
            old_cnt = self.item_cnt[id]
            new_cnt = old_cnt + 1
            old_rank = self.item_rank[id]
            new_rank = self.cnt_min_rank[old_cnt]
            swap_id = self.rank_item[new_rank]
            self.item_cnt[id] = new_cnt
            self.item_rank[id] = new_rank
            self.rank_item[new_rank] = id
            self.item_rank[swap_id] = old_rank
            self.rank_item[old_rank] = swap_id
            self.cnt_cnt[old_cnt] -= 1
            self.cnt_cnt[new_cnt] += 1
            self.cnt_min_rank[old_cnt] += 1
            if self.cnt_cnt[new_cnt] == 1:
                self.cnt_min_rank[new_cnt] = new_rank
        else:
            self.item_cnt[id] = 1
            rank = len(self.item_cnt)
            self.item_rank[id] = rank
            self.rank_item[rank] = id
            self.cnt_cnt[1] += 1
            if self.cnt_cnt[1] == 1:
                self.cnt_min_rank[1] = rank

    def ranking(self, id):
        return self.item_rank[id]

    def get_item(self, rank):
        return self.rank_item[rank]

    def top_items(self, k):
        for i in xrange(1, k+1):
            if i in self.rank_item:
                yield self.rank_item[i]
            else:
                break

    def num_items(self):
        return len(self.item_cnt)

    def __str__(self):
        return str(self.item_cnt) + '\n' + \
               str(self.item_rank) + '\n' + \
               str(self.rank_item) + '\n' + \
               str(self.cnt_min_rank) + '\n'
