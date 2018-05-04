class Pagination():
    def __init__(self, current_idx=0, start_id=0, is_hidden=False, one_tab_length=10):
        self.current_idx = current_idx
        self.start_id = start_id
        self.query_str = "?current_idx=" + str(self.current_idx) + "&start_id=" + str(
            self.start_id) + "&one_tab_length=" + str(one_tab_length)
        self.is_hidden = is_hidden


class PaginationInfo():
    def __init__(self, paginations=None, current_idx=1, one_tab_length=10, prev_pagination=None, next_pagination=None):
        if paginations is None:
            self.paginations = []
        else:
            self.paginations = paginations

        self.prev_pagination = prev_pagination
        self.next_pagination = next_pagination
        self.current_idx = current_idx
        self.one_tab_length = one_tab_length


# 分页设置
def generate_pagination_info(current_idx, total_idx, max_idxs_length, one_tab_length, start_id):
    paginations = []
    # 上下页链接生成
    if current_idx == 1:
        prev_pagination = Pagination(current_idx=1, start_id=1, is_hidden=False, one_tab_length=one_tab_length)
    else:
        prev_pagination = Pagination(current_idx=current_idx - 1, start_id=one_tab_length * (current_idx - 2) + 1,
                                     is_hidden=False, one_tab_length=one_tab_length)

    if current_idx == total_idx:
        next_pagination = Pagination(current_idx=current_idx, start_id=one_tab_length * (current_idx - 1) + 1,
                                     is_hidden=False, one_tab_length=one_tab_length)
    else:
        next_pagination = Pagination(current_idx=current_idx + 1, start_id=one_tab_length * current_idx + 1,
                                     is_hidden=False, one_tab_length=one_tab_length)

    # 其余部分链接生成
    if total_idx > max_idxs_length:
        if current_idx != 1:
            paginations.append(Pagination(current_idx=1, start_id=1, is_hidden=False, one_tab_length=one_tab_length))
        if current_idx - 2 >= 2:
            paginations.append(Pagination(is_hidden=True, one_tab_length=one_tab_length))
            for idx in range(current_idx - 2, current_idx):
                paginations.append(Pagination(current_idx=idx, start_id=one_tab_length * (idx - 1) + 1, is_hidden=False,
                                              one_tab_length=one_tab_length))
        else:
            for idx in range(2, current_idx):
                paginations.append(Pagination(current_idx=idx, start_id=one_tab_length * (idx - 1) + 1, is_hidden=False,
                                              one_tab_length=one_tab_length))

        paginations.append(
            Pagination(current_idx=current_idx, start_id=start_id, is_hidden=False, one_tab_length=one_tab_length))

        if total_idx - 2 - current_idx - 1 >= 2:
            for idx in range(current_idx + 1, current_idx + 3):
                paginations.append(Pagination(current_idx=idx, start_id=one_tab_length * (idx - 1) + 1, is_hidden=False,
                                              one_tab_length=one_tab_length))
            paginations.append(Pagination(is_hidden=True))
        else:
            for idx in range(current_idx + 1, total_idx):
                paginations.append(Pagination(current_idx=idx, start_id=one_tab_length * (idx - 1) + 1, is_hidden=False,
                                              one_tab_length=one_tab_length))

        if current_idx != total_idx:
            paginations.append(
                Pagination(current_idx=total_idx, start_id=((total_idx - 1) * one_tab_length + 1), is_hidden=False,
                           one_tab_length=one_tab_length))
    else:
        for idx in range(1, total_idx+1):
            paginations.append(Pagination(current_idx=idx, start_id=one_tab_length * (idx - 1) + 1, is_hidden=False,
                                          one_tab_length=one_tab_length))
    pagination_info = PaginationInfo(
        paginations=paginations,
        current_idx=current_idx,
        one_tab_length=one_tab_length,
        prev_pagination=prev_pagination,
        next_pagination=next_pagination)

    return pagination_info

