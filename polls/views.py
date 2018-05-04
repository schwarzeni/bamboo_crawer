import math
from django.http import HttpResponse, Http404
from django.template import loader

from .models import Bamboo
from .utils import generate_pagination_info

'''
http://127.0.0.1:8000/polls/?current_idx=3&start_id=4&length=10
'''


def index(request):
    one_tab_length = 10
    max_idxs_length = 11

    current_idx = int(request.GET.get('current_idx', 1))
    start_id = int(request.GET.get('start_id', 1))
    length = int(request.GET.get('one_tab_length', one_tab_length))
    total_idx = math.ceil(len(Bamboo.objects.all()) / one_tab_length)

    bamboo_article_raw_result = Bamboo.objects.order_by('id')

    bamboos_list = bamboo_article_raw_result[start_id-1:(start_id + one_tab_length)]

    template = loader.get_template('polls/index.html')

    context = {
        'bamboos_list': bamboos_list,
        'pagination_info': generate_pagination_info(
            one_tab_length=one_tab_length,
            start_id=start_id,
            current_idx=current_idx,
            total_idx=total_idx,
            max_idxs_length=max_idxs_length,
        ),
        'total_count': len(bamboo_article_raw_result)
    }
    return HttpResponse(template.render(context, request))


def article_detail(request, article_id):
    try:
        bamboo_article_detail = Bamboo.objects.get(id=article_id)
    except Bamboo.DoesNotExist:
        raise Http404("Article does not exist")
    template = loader.get_template('polls/article_detail.html')
    context = {'bamboo_article_detail': bamboo_article_detail}
    return HttpResponse(template.render(context, request))


def article_search(request):
    if request.GET:
        post_data = request.GET.get("search_item", "")
        one_tab_length = 10
        max_idxs_length = 11

        current_idx = int(request.GET.get('current_idx', 1))
        start_id = int(request.GET.get('start_id', 1))

        key_array = post_data.split()
        print(key_array)
        # TODO: 尝试查询是否可以优化
        bamboo_article_query_raw_result = Bamboo.objects.all()

        for key in key_array:
            bamboo_article_query_raw_result = bamboo_article_query_raw_result.filter(title__icontains=key)

        total_idx = math.ceil(len(bamboo_article_query_raw_result) / one_tab_length)

        template = loader.get_template('polls/search_result.html')

        pagination_info = generate_pagination_info(
            one_tab_length=one_tab_length,
            start_id=start_id,
            current_idx=current_idx,
            total_idx=total_idx,
            max_idxs_length=max_idxs_length,
        )

        for idx, val in enumerate(pagination_info.paginations):
            pagination_info.paginations[idx].query_str += ("&search_item="+post_data)
            print(pagination_info.paginations[idx].query_str)

        context = {
            'raw_quary': post_data,
            'key_word_array': key_array,
            'bamboos_list': bamboo_article_query_raw_result[start_id-1:(start_id + one_tab_length)],
            'pagination_info': pagination_info,
            'total_count':len(bamboo_article_query_raw_result),
            'current_idx': current_idx,
            'total_idx': total_idx
        }
        return HttpResponse(template.render(context, request))
