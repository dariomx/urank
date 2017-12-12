from collections import defaultdict


class UsageRanking:
    def __init__(self):
        self.vid_cnt = defaultdict(lambda: 0)
        self.vid_rank = dict()
        self.rank_vid = dict()
        self.cnt_min_rank = defaultdict(lambda: 0)

    def videoViewed(self, vid):
        if vid in self.vid_cnt:
            old_cnt = self.vid_cnt[vid]
            new_cnt = old_cnt + 1
            old_rank = self.vid_rank[vid]
            new_rank = self.cnt_min_rank[old_cnt]
            swap_vid = self.rank_vid[new_rank]
            self.vid_cnt[vid] = new_cnt
            self.vid_rank[vid] = new_rank
            self.rank_vid[new_rank] = vid
            self.vid_rank[swap_vid] = old_rank
            self.rank_vid[old_rank] = swap_vid
            if old_rank == new_rank:
                self.cnt_min_rank[old_cnt] = 0
            else:
                self.cnt_min_rank[old_cnt] += 1
            if self.cnt_min_rank[new_cnt] == 0:
                self.cnt_min_rank[new_cnt] = new_rank
        else:
            self.vid_cnt[vid] = 1
            rank = len(self.vid_cnt)
            self.vid_rank[vid] = rank
            self.rank_vid[rank] = vid
            if self.cnt_min_rank[1] == 0:
                self.cnt_min_rank[1] = rank

    def getRanking(self, vid):
        return self.vid_rank[vid]

    def getTopVideos(self):
        for i in xrange(1, 11):
            if i in self.rank_vid:
                yield self.rank_vid[i]
            else:
                break
